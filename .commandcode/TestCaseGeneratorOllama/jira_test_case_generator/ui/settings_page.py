"""Settings screen: Jira and Ollama configuration with validation."""

from __future__ import annotations

import logging

import streamlit as st

from config import settings as settings_store
from models.data_models import AppSettings
from services.jira_client import JiraClient
from services.ollama_client import OllamaClient
from utils.error_handler import AppError, log_error, user_message
from utils.validators import validate_email, validate_required, validate_url

logger = logging.getLogger(__name__)

_WIDGET_KEYS = {
    "jira_base_url": "cfg_jira_url",
    "jira_email": "cfg_jira_email",
    "jira_token": "cfg_jira_token",
    "ollama_url": "cfg_ollama_url",
    "ollama_model": "cfg_ollama_model",
}


def _seed_widget_state(current: AppSettings) -> None:
    for attribute, key in _WIDGET_KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = getattr(current, attribute)


def _read_form() -> AppSettings:
    return AppSettings(
        jira_base_url=(st.session_state.get(_WIDGET_KEYS["jira_base_url"]) or "").strip(),
        jira_email=(st.session_state.get(_WIDGET_KEYS["jira_email"]) or "").strip(),
        jira_token=(st.session_state.get(_WIDGET_KEYS["jira_token"]) or "").strip(),
        ollama_url=(st.session_state.get(_WIDGET_KEYS["ollama_url"]) or "").strip(),
        ollama_model=(st.session_state.get(_WIDGET_KEYS["ollama_model"]) or "").strip(),
    )


def _validate(candidate: AppSettings) -> AppSettings:
    candidate.jira_base_url = validate_url(candidate.jira_base_url, "Jira URL")
    validate_email(candidate.jira_email, "Jira Email")
    validate_required(candidate.jira_token, "Jira API Key")
    candidate.ollama_url = validate_url(candidate.ollama_url, "Ollama URL")
    return candidate


def _save() -> None:
    try:
        candidate = _validate(_read_form())
    except AppError as exc:
        st.error(user_message(exc))
        return

    path = settings_store.save_settings(candidate)
    st.session_state.settings = candidate
    st.success(f"Settings saved to {path}.")


def _reset() -> None:
    removed = settings_store.reset_settings_file()
    st.session_state.settings = AppSettings()
    for key in _WIDGET_KEYS.values():
        st.session_state[key] = ""
    st.success(
        "Settings reset. The stored configuration file was removed."
        if removed
        else "Settings cleared."
    )


def _test_jira() -> None:
    try:
        candidate = _validate(_read_form())
        client = JiraClient(candidate.jira_base_url, candidate.jira_email, candidate.jira_token)
        with st.spinner("Contacting Jira..."):
            message = client.test_connection()
        st.success(message)
    except AppError as exc:
        st.error(user_message(exc))
    except Exception as exc:  # pragma: no cover - defensive
        log_error(exc)
        st.error("Unexpected error while contacting Jira.")


def _test_ollama() -> None:
    try:
        candidate = _read_form()
        validate_url(candidate.ollama_url, "Ollama URL")
        client = OllamaClient(candidate.ollama_url, candidate.ollama_model)
        with st.spinner("Contacting Ollama..."):
            message = client.test_connection()
        st.success(message)
    except AppError as exc:
        st.error(user_message(exc))
    except Exception as exc:  # pragma: no cover - defensive
        log_error(exc)
        st.error("Unexpected error while contacting Ollama.")


def render(current: AppSettings) -> None:
    st.header("Settings")
    st.caption(
        "Configuration is stored locally in a .env file. The Jira API key is "
        "masked and never written to logs or displayed in responses."
    )

    _seed_widget_state(current)

    st.subheader("Jira Configuration")
    st.text_input(
        "Jira URL",
        key=_WIDGET_KEYS["jira_base_url"],
        placeholder="https://your-domain.atlassian.net",
    )
    st.text_input(
        "Jira Email",
        key=_WIDGET_KEYS["jira_email"],
        placeholder="you@example.com",
    )
    st.text_input(
        "Jira API Key",
        key=_WIDGET_KEYS["jira_token"],
        type="password",
    )
    if current.jira_token:
        st.caption(f"Currently loaded key: {current.masked_token()}")

    st.subheader("Ollama Configuration")
    st.text_input(
        "Ollama URL",
        key=_WIDGET_KEYS["ollama_url"],
        placeholder="http://localhost:11434",
    )
    st.text_input(
        "Ollama Model (optional)",
        key=_WIDGET_KEYS["ollama_model"],
        placeholder="e.g. llama3",
        help="Leave blank to use the first model available on the Ollama server.",
    )

    st.divider()
    save_col, reset_col, jira_col, ollama_col = st.columns(4)
    with save_col:
        if st.button("Save Settings", type="primary"):
            _save()
    with reset_col:
        if st.button("Reset Settings"):
            _reset()
    with jira_col:
        if st.button("Test Jira Connection"):
            _test_jira()
    with ollama_col:
        if st.button("Test Ollama Connection"):
            _test_ollama()

    env_file = settings_store.current_env_file()
    if env_file:
        st.caption(f"Configuration loaded from: {env_file}")
