"""Ollama REST API client for local LLM inference."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import requests

from utils.error_handler import OllamaConnectionError, OllamaError, OllamaModelError

logger = logging.getLogger(__name__)


class OllamaClient:
    """Minimal client for the Ollama HTTP API."""

    def __init__(
        self,
        base_url: str,
        model: str = "",
        connect_timeout: int = 10,
        read_timeout: int = 300,
    ) -> None:
        self._base_url = (base_url or "").rstrip("/")
        self._model = (model or "").strip()
        self._timeout = (connect_timeout, read_timeout)
        self._session = requests.Session()

    def _url(self, path: str) -> str:
        return f"{self._base_url}{path}"

    def _handle_request_exception(self, exc: Exception) -> None:
        if isinstance(exc, requests.exceptions.Timeout):
            raise OllamaConnectionError(
                f"The Ollama request to {self._base_url} timed out."
            ) from exc
        if isinstance(exc, requests.exceptions.ConnectionError):
            raise OllamaConnectionError(
                f"Could not connect to Ollama at {self._base_url}. "
                "Confirm the service is running."
            ) from exc
        raise OllamaConnectionError("The Ollama request failed.") from exc

    @staticmethod
    def _error_detail(response: requests.Response) -> str:
        try:
            body = response.json()
            if isinstance(body, dict):
                return str(body.get("error") or "").strip()
        except ValueError:
            pass
        return ""

    def list_models(self) -> List[str]:
        """Return the names of models available on the Ollama server."""
        try:
            response = self._session.get(self._url("/api/tags"), timeout=self._timeout)
        except requests.exceptions.RequestException as exc:
            self._handle_request_exception(exc)

        if response.status_code >= 400:
            raise OllamaError(f"Ollama returned HTTP {response.status_code} when listing models.")

        try:
            body = response.json()
        except ValueError as exc:
            raise OllamaError("Ollama returned an unexpected response when listing models.") from exc

        models = body.get("models") if isinstance(body, dict) else None
        names: List[str] = []
        for entry in models or []:
            name = entry.get("name") or entry.get("model")
            if name:
                names.append(name)
        return names

    def resolve_model(self) -> str:
        """Determine which model to use, validating it against the server."""
        available = self.list_models()
        if not available:
            raise OllamaModelError(
                "No models are available in Ollama. Pull a model first, "
                "for example: ollama pull llama3"
            )
        if not self._model:
            return available[0]
        if self._model in available:
            return self._model
        # Ollama reports models with an implicit ":latest" tag; accept either form.
        if f"{self._model}:latest" in available:
            return f"{self._model}:latest"
        raise OllamaModelError(
            f"Model '{self._model}' is not available. Installed models: "
            f"{', '.join(available)}"
        )

    def chat(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> str:
        """Send a chat-completion request and return the assistant's text."""
        resolved_model = model or self.resolve_model()
        payload: Dict[str, Any] = {
            "model": resolved_model,
            "messages": messages,
            "stream": False,
        }

        try:
            response = self._session.post(
                self._url("/api/chat"), json=payload, timeout=self._timeout
            )
        except requests.exceptions.RequestException as exc:
            self._handle_request_exception(exc)

        if response.status_code == 404:
            detail = self._error_detail(response)
            raise OllamaModelError(detail or f"Model '{resolved_model}' was not found.")
        if response.status_code >= 400:
            detail = self._error_detail(response)
            raise OllamaError(detail or f"Ollama returned HTTP {response.status_code}.")

        try:
            body = response.json()
        except ValueError as exc:
            raise OllamaError("Ollama returned an unexpected (non-JSON) response.") from exc

        message = body.get("message") if isinstance(body, dict) else None
        content = (message or {}).get("content", "") if isinstance(message, dict) else ""
        if not isinstance(content, str) or not content.strip():
            raise OllamaError("Ollama returned an empty response.")
        return content.strip()

    def test_connection(self) -> str:
        """Verify connectivity and report the resolved model."""
        available = self.list_models()
        if not available:
            raise OllamaModelError(
                "Connected to Ollama, but no models are installed. "
                "Pull a model first, for example: ollama pull llama3"
            )
        resolved = self.resolve_model()
        return f"Connected to Ollama. Using model '{resolved}'."
