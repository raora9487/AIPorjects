"""Input validation helpers for user-supplied configuration and input."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from utils.error_handler import ValidationError

# Jira issue keys are <PROJECT>-<NUMBER>. Project keys vary in length and may
# contain letters, digits and underscores, so we validate the shape rather
# than hard-coding a fixed length.
_JIRA_KEY_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*-\d+$")
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_required(value: str, field_name: str) -> str:
    """Ensure a value is present and return it stripped."""
    cleaned = (value or "").strip()
    if not cleaned:
        raise ValidationError(f"{field_name} is required.")
    return cleaned


def validate_jira_id(value: str) -> str:
    """Validate and normalize a Jira issue key such as ``PROJ-1234``."""
    cleaned = validate_required(value, "Jira User Story ID").upper()
    if not _JIRA_KEY_PATTERN.match(cleaned):
        raise ValidationError(
            "Invalid Jira User Story ID. Expected a format like PROJ-1234."
        )
    return cleaned


def validate_url(value: str, field_name: str = "URL") -> str:
    """Validate an HTTP/HTTPS URL and return it without a trailing slash."""
    cleaned = validate_required(value, field_name)
    parsed = urlparse(cleaned)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValidationError(f"{field_name} must be a valid HTTP or HTTPS URL.")
    return cleaned.rstrip("/")


def validate_email(value: str, field_name: str = "Email") -> str:
    """Validate an email address shape."""
    cleaned = validate_required(value, field_name)
    if not _EMAIL_PATTERN.match(cleaned):
        raise ValidationError(f"{field_name} must be a valid email address.")
    return cleaned
