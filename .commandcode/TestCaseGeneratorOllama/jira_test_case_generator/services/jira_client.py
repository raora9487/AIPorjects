"""Jira REST API client.

A thin, reusable wrapper around the Jira Cloud REST API v3 that retrieves
an issue and normalizes it into a :class:`JiraStory`. The API token is held
only in memory and is never written to logs or exception messages.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import requests
from requests.auth import HTTPBasicAuth

from models.data_models import JiraStory
from utils.error_handler import (
    JiraAuthError,
    JiraConnectionError,
    JiraError,
    JiraNotFoundError,
)

logger = logging.getLogger(__name__)

_STANDARD_FIELDS: List[str] = [
    "summary",
    "description",
    "issuetype",
    "priority",
    "status",
    "labels",
    "components",
    "reporter",
    "assignee",
]


def adf_to_text(node: Any) -> str:
    """Convert an Atlassian Document Format node into readable plain text."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "".join(adf_to_text(item) for item in node)
    if not isinstance(node, dict):
        return str(node)

    node_type = node.get("type", "")
    content = node.get("content", [])

    if node_type == "text":
        return node.get("text", "")
    if node_type == "hardBreak":
        return "\n"
    if node_type == "mention":
        return f"@{node.get('attrs', {}).get('text', '')}"
    if node_type == "emoji":
        return node.get("attrs", {}).get("text", "")
    if node_type == "inlineCard":
        return node.get("attrs", {}).get("url", "")
    if node_type == "bulletList":
        return "".join(f"- {adf_to_text(item).strip()}\n" for item in content)
    if node_type == "orderedList":
        return "".join(
            f"{index}. {adf_to_text(item).strip()}\n"
            for index, item in enumerate(content, start=1)
        )
    if node_type in ("paragraph", "heading", "blockquote"):
        return f"{adf_to_text(content)}\n"
    if node_type == "codeBlock":
        return f"{adf_to_text(content)}\n"
    if node_type == "rule":
        return "---\n"
    if node_type in ("table", "tableRow", "tableCell", "tableHeader"):
        return adf_to_text(content)
    return adf_to_text(content)


def _text_value(value: Any) -> str:
    """Normalize a Jira field value (ADF, string, or object) to text."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return adf_to_text(value).strip()
    return str(value).strip()


class JiraClient:
    """Client for reading Jira issues."""

    def __init__(
        self,
        base_url: str,
        email: str,
        token: str,
        timeout: int = 20,
    ) -> None:
        self._base_url = (base_url or "").rstrip("/")
        self._email = email or ""
        self._token = token or ""
        self._timeout = timeout
        self._auth = HTTPBasicAuth(self._email, self._token)
        self._session = requests.Session()
        self._session.headers.update({"Accept": "application/json"})
        self._acceptance_field_id: Optional[str] = None
        self._acceptance_field_resolved = False

    @property
    def secrets(self) -> List[str]:
        """Values that must never leak into logs or exception messages."""
        return [self._token]

    def _url(self, path: str) -> str:
        return f"{self._base_url}{path}"

    def _request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            response = self._session.get(
                self._url(path),
                params=params,
                auth=self._auth,
                timeout=self._timeout,
            )
        except requests.exceptions.Timeout as exc:
            raise JiraConnectionError(
                f"Jira request to {self._base_url} timed out."
            ) from exc
        except requests.exceptions.SSLError as exc:
            raise JiraConnectionError("Jira SSL verification failed.") from exc
        except requests.exceptions.ConnectionError as exc:
            raise JiraConnectionError(
                f"Could not connect to Jira at {self._base_url}."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise JiraConnectionError("Jira request failed before a response was received.") from exc

        if response.status_code == 401:
            raise JiraAuthError("Jira rejected the supplied email or API token.")
        if response.status_code == 403:
            raise JiraAuthError("The Jira account lacks permission for this resource.")
        if response.status_code == 404:
            raise JiraNotFoundError("Jira resource not found.")
        if response.status_code >= 500:
            raise JiraError(
                f"Jira server error (HTTP {response.status_code}). Try again later."
            )
        if response.status_code >= 400:
            raise JiraError(f"Jira request failed (HTTP {response.status_code}).")

        try:
            return response.json()
        except ValueError as exc:
            raise JiraError("Jira returned an unexpected (non-JSON) response.") from exc

    def _find_acceptance_field(self) -> Optional[str]:
        """Discover a custom field whose name references acceptance criteria."""
        if self._acceptance_field_resolved:
            return self._acceptance_field_id
        self._acceptance_field_resolved = True

        try:
            fields = self._request("/rest/api/3/field")
        except JiraError:
            return None

        for field in fields if isinstance(fields, list) else []:
            name = str(field.get("name", "")).lower()
            if "acceptance" in name and "criteria" in name:
                self._acceptance_field_id = field.get("id")
                break
        return self._acceptance_field_id

    @staticmethod
    def _extract_acceptance_from_description(description: str) -> str:
        """Fall back to the convention of an 'Acceptance Criteria' section."""
        if not description:
            return ""
        lines = description.splitlines()
        collected: List[str] = []
        capturing = False
        for line in lines:
            lowered = line.strip().lower()
            if not capturing and "acceptance criteria" in lowered:
                capturing = True
                remainder = line.split(":", 1)
                if len(remainder) == 2 and remainder[1].strip():
                    collected.append(remainder[1].strip())
                continue
            if capturing:
                if lowered.startswith(("definition of done", "notes", "out of scope")):
                    break
                collected.append(line)
        return "\n".join(collected).strip()

    def get_issue(self, issue_key: str) -> JiraStory:
        """Fetch a Jira issue and normalize it into a :class:`JiraStory`."""
        fields = list(_STANDARD_FIELDS)
        acceptance_field = self._find_acceptance_field()
        if acceptance_field:
            fields.append(acceptance_field)

        payload = self._request(
            f"/rest/api/3/issue/{issue_key}",
            params={"fields": ",".join(fields)},
        )

        raw_fields = payload.get("fields") or {}
        description = _text_value(raw_fields.get("description"))

        acceptance = ""
        if acceptance_field:
            acceptance = _text_value(raw_fields.get(acceptance_field))
        if not acceptance:
            acceptance = self._extract_acceptance_from_description(description)

        issue_type = (raw_fields.get("issuetype") or {}).get("name", "")
        priority = (raw_fields.get("priority") or {}).get("name", "")
        status = (raw_fields.get("status") or {}).get("name", "")
        reporter = (raw_fields.get("reporter") or {}).get("displayName", "")
        assignee = (raw_fields.get("assignee") or {}).get("displayName", "")
        components = [
            component.get("name", "")
            for component in (raw_fields.get("components") or [])
            if component.get("name")
        ]

        return JiraStory(
            key=payload.get("key", issue_key),
            summary=raw_fields.get("summary", "") or "",
            description=description,
            acceptance_criteria=acceptance,
            issue_type=issue_type,
            priority=priority,
            status=status,
            labels=list(raw_fields.get("labels") or []),
            components=components,
            reporter=reporter,
            assignee=assignee,
            url=f"{self._base_url}/browse/{payload.get('key', issue_key)}",
        )

    def test_connection(self) -> str:
        """Verify credentials by reading the authenticated user."""
        user = self._request("/rest/api/3/myself")
        display_name = user.get("displayName") or user.get("emailAddress") or "user"
        return f"Connected to Jira as {display_name}."
