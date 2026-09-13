"""Main screen: a lightweight ChatGPT-style interface for test-case generation."""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

import streamlit as st

from models.data_models import AppSettings, JiraStory
from services.jira_client import JiraClient
from services.ollama_client import OllamaClient
from services.prompt_builder import build_messages
from utils.error_handler import AppError, log_error, user_message
from utils.validators import validate_jira_id

logger = logging.getLogger(__name__)


def _init_state() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("jira_id_input", "")
    st.session_state.setdefault("jira_story", None)
    st.session_state.setdefault("force_refresh", False)


def _append_error(message: str) -> None:
    st.session_state.messages.append(
        {"role": "assistant", "content": message, "is_error": True}
    )


def _clear_conversation() -> None:
    st.session_state.messages = []
    st.session_state.jira_story = None
    st.session_state.force_refresh = False


def _render_story_details(story: JiraStory) -> None:
    st.markdown(f"**{story.key}** — {story.summary or '(no summary)'}")
    if story.url:
        st.markdown(f"[Open in Jira]({story.url})")
    meta = " | ".join(
        part
        for part in (
            f"Type: {story.issue_type}" if story.issue_type else "",
            f"Priority: {story.priority}" if story.priority else "",
            f"Status: {story.status}" if story.status else "",
        )
        if part
    )
    if meta:
        st.caption(meta)
    if story.description:
        st.markdown("**Description**")
        st.markdown(story.description)
    if story.acceptance_criteria:
        st.markdown("**Acceptance Criteria**")
        st.markdown(story.acceptance_criteria)


def _render_sidebar(settings: AppSettings) -> None:
    with st.sidebar:
        st.subheader("Jira Story")
        st.text_input(
            "Jira User Story ID",
            key="jira_id_input",
            placeholder="PROJ-1234",
        )
        if st.button("Reload Story"):
            st.session_state.jira_story = None
            st.session_state.force_refresh = True
            st.rerun()
        if st.button("Clear Conversation"):
            _clear_conversation()
            st.rerun()

        story: Optional[JiraStory] = st.session_state.get("jira_story")
        if story is not None:
            with st.expander("Current Jira Story", expanded=False):
                _render_story_details(story)

        st.divider()
        if not settings.is_jira_configured:
            st.warning("Jira is not configured. Open Settings to add credentials.")
        if not settings.is_ollama_configured:
            st.warning("Ollama is not configured. Open Settings to add its URL.")


def _get_story(jira_id: str, settings: AppSettings) -> JiraStory:
    cached: Optional[JiraStory] = st.session_state.get("jira_story")
    if cached and cached.key == jira_id and not st.session_state.get("force_refresh"):
        return cached

    client = JiraClient(settings.jira_base_url, settings.jira_email, settings.jira_token)
    with st.spinner(f"Fetching {jira_id} from Jira..."):
        story = client.get_issue(jira_id)
    st.session_state.jira_story = story
    st.session_state.force_refresh = False
    return story


def _model_history() -> List[Dict[str, str]]:
    """Prior chat turns, excluding the pending prompt and any error notices."""
    return [
        {"role": message["role"], "content": message["content"]}
        for message in st.session_state.messages[:-1]
        if not message.get("is_error")
    ]


def _handle_prompt(prompt: str, settings: AppSettings) -> None:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        jira_id = validate_jira_id(st.session_state.get("jira_id_input", ""))
    except AppError as exc:
        _append_error(user_message(exc))
        st.rerun()
        return

    if not settings.is_jira_configured:
        _append_error(
            "Jira is not configured. Open the Settings page and save your Jira URL, "
            "email, and API key."
        )
        st.rerun()
        return
    if not settings.is_ollama_configured:
        _append_error("Ollama is not configured. Open the Settings page and save the Ollama URL.")
        st.rerun()
        return

    try:
        story = _get_story(jira_id, settings)
    except AppError as exc:
        log_error(exc, [settings.jira_token])
        _append_error(user_message(exc))
        st.rerun()
        return
    except Exception as exc:  # pragma: no cover - defensive
        log_error(exc, [settings.jira_token])
        _append_error("An unexpected error occurred while retrieving the Jira story.")
        st.rerun()
        return

    if not story.has_description:
        st.warning(
            "The Jira story has an empty description. Test cases will rely on the "
            "summary and any available acceptance criteria."
        )

    messages = build_messages(story, prompt, _model_history())
    client = OllamaClient(settings.ollama_url, settings.ollama_model)

    try:
        with st.spinner("Generating test cases with Ollama..."):
            answer = client.chat(messages)
    except AppError as exc:
        log_error(exc)
        _append_error(user_message(exc))
        st.rerun()
        return
    except Exception as exc:  # pragma: no cover - defensive
        log_error(exc)
        _append_error("An unexpected error occurred while generating test cases.")
        st.rerun()
        return

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()


def render(settings: AppSettings) -> None:
    _init_state()
    _render_sidebar(settings)

    st.title("Jira Test Case Generator")
    st.caption(
        "Enter a Jira User Story ID in the sidebar, then describe the test cases "
        "you need. Test cases are generated locally with Ollama."
    )

    for message in st.session_state.messages:
        if message.get("is_error"):
            with st.chat_message("assistant"):
                st.error(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if not st.session_state.messages:
        st.info(
            "Try a request such as: *Design comprehensive functional and negative "
            "test cases for this user story.*"
        )

    prompt = st.chat_input("Describe the test cases you need...")
    if prompt:
        _handle_prompt(prompt, settings)
