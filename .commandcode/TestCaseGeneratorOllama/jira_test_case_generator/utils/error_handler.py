"""Application exception hierarchy and safe error reporting helpers.

Every exception defined here carries a message that is safe to show to the
end user: no credentials are ever embedded in exception text.
"""

from __future__ import annotations

import logging
from typing import Iterable, Optional

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base class for all expected application errors."""


class ConfigurationError(AppError):
    """Raised when required configuration is missing or invalid."""


class ValidationError(AppError):
    """Raised when user-supplied input fails validation."""


class JiraError(AppError):
    """Generic Jira integration failure."""


class JiraAuthError(JiraError):
    """Jira rejected the supplied credentials or permissions."""


class JiraNotFoundError(JiraError):
    """The requested Jira issue does not exist or is not visible."""


class JiraConnectionError(JiraError):
    """Jira could not be reached (network, DNS, timeout)."""


class OllamaError(AppError):
    """Generic Ollama integration failure."""


class OllamaConnectionError(OllamaError):
    """Ollama could not be reached (network, DNS, timeout)."""


class OllamaModelError(OllamaError):
    """The requested Ollama model is unavailable."""


def mask_secret(value: Optional[str]) -> str:
    """Return a masked representation of a secret, safe for logs and UI."""
    if not value:
        return "(not set)"
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}{'*' * 10}{value[-2:]}"


def scrub(text: str, secrets: Iterable[str]) -> str:
    """Remove any occurrence of the given secrets from ``text``."""
    cleaned = text or ""
    for secret in secrets:
        if secret:
            cleaned = cleaned.replace(secret, "***")
    return cleaned


def log_error(exc: Exception, secrets: Iterable[str] = ()) -> None:
    """Log an exception with credentials scrubbed from the message."""
    logger.error("%s: %s", type(exc).__name__, scrub(str(exc), secrets))


def user_message(exc: Exception) -> str:
    """Map an exception to a concise, user-friendly message."""
    if isinstance(exc, JiraAuthError):
        return (
            "Jira authentication failed. Check the Jira email and API token in "
            "Settings, then try again."
        )
    if isinstance(exc, JiraNotFoundError):
        return "The Jira issue was not found. Verify the issue key (for example PROJ-1234)."
    if isinstance(exc, JiraConnectionError):
        return "Could not reach Jira. Check the Jira URL and your network connection."
    if isinstance(exc, JiraError):
        return f"Jira request failed: {exc}"
    if isinstance(exc, OllamaConnectionError):
        return "Could not reach Ollama. Confirm Ollama is running and the URL is correct."
    if isinstance(exc, OllamaModelError):
        return f"Ollama model unavailable: {exc}"
    if isinstance(exc, OllamaError):
        return f"Ollama request failed: {exc}"
    if isinstance(exc, (ValidationError, ConfigurationError)):
        return str(exc)
    if isinstance(exc, AppError):
        return str(exc)
    return "An unexpected error occurred. Please review the logs for details."
