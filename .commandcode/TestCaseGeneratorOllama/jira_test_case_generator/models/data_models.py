"""Shared data models for the Jira Test Case Generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class JiraStory:
    """A normalized, display-friendly view of a Jira issue."""

    key: str
    summary: str = ""
    description: str = ""
    acceptance_criteria: str = ""
    issue_type: str = ""
    priority: str = ""
    status: str = ""
    labels: List[str] = field(default_factory=list)
    components: List[str] = field(default_factory=list)
    reporter: str = ""
    assignee: str = ""
    url: str = ""

    @property
    def has_description(self) -> bool:
        return bool(self.description and self.description.strip())

    def to_prompt_text(self) -> str:
        """Render the story as structured text that grounds the LLM prompt."""
        lines = [
            f"Jira Issue Key: {self.key}",
            f"Summary: {self.summary or '(not provided)'}",
            f"Issue Type: {self.issue_type or '(not provided)'}",
            f"Priority: {self.priority or '(not provided)'}",
            f"Status: {self.status or '(not provided)'}",
            f"Components: {', '.join(self.components) or '(none)'}",
            f"Labels: {', '.join(self.labels) or '(none)'}",
            f"Reporter: {self.reporter or '(not provided)'}",
            f"Assignee: {self.assignee or '(not provided)'}",
            "",
            "Description:",
            self.description.strip() or "(empty description)",
            "",
            "Acceptance Criteria:",
            self.acceptance_criteria.strip() or "(not provided in the Jira story)",
        ]
        return "\n".join(lines)


@dataclass
class AppSettings:
    """Runtime configuration. Never logged or rendered in full."""

    jira_base_url: str = ""
    jira_email: str = ""
    jira_token: str = ""
    ollama_url: str = ""
    ollama_model: str = ""

    @property
    def is_jira_configured(self) -> bool:
        return bool(self.jira_base_url and self.jira_email and self.jira_token)

    @property
    def is_ollama_configured(self) -> bool:
        return bool(self.ollama_url)

    def masked_token(self) -> str:
        """Return a safe representation of the API token for display."""
        if not self.jira_token:
            return ""
        if len(self.jira_token) <= 4:
            return "*" * len(self.jira_token)
        return f"{self.jira_token[:2]}{'*' * 10}{self.jira_token[-2:]}"
