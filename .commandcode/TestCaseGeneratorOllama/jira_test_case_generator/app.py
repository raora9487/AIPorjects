"""Entry point for the Jira Test Case Generator Streamlit application.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st

from config.settings import load_settings
from ui.main_page import render as render_main_page
from ui.settings_page import render as render_settings_page

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

PAGES = ("Test Case Generator", "Settings")


def main() -> None:
    st.set_page_config(
        page_title="Jira Test Case Generator",
        page_icon="🧪",
        layout="wide",
    )

    if "settings" not in st.session_state:
        st.session_state.settings = load_settings()

    with st.sidebar:
        st.title("🧪 QA Assistant")
        page = st.radio(
            "Navigation",
            PAGES,
            key="nav_page",
            label_visibility="collapsed",
        )

    settings = st.session_state.settings
    if page == "Settings":
        render_settings_page(settings)
    else:
        render_main_page(settings)


if __name__ == "__main__":
    main()
