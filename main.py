import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from ui.state import init_state, switch_language
from ui.components import sidebar_config_editor, display_results, AP_FRAMEWORK_OPTIONS, display_results_streaming
from clients.claude_client import ClaudeClient
from api.generate_replies import generate_replies
from domain.models import PromptConfig


def login_screen():
    st.markdown(
        """
        <h1 style='text-align: center;'>💬 AP Comment Reply Generator</h1>
        <h3 style='text-align: center;'>🔐 Login</h3>
        """,
        unsafe_allow_html=True
    )
    st.write("")
    username = st.text_input("Username").strip()
    password = st.text_input("Password", type="password").strip()
    st.write("")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        login_clicked = st.button("Login", use_container_width=True)
    st.write("")

    if login_clicked:
        role = AUTH_LOOKUP.get((username, password))
        if role:
            st.session_state.authenticated = True
            st.session_state.role = role
            st.session_state.is_admin = role == "admin"
            st.rerun()
        else:
            st.error("Invalid credentials")


def comment_generation_screen():
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 400px !important;
            }
            section[data-testid="stSidebar"] > div {
                width: 400px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("💬 AP Comment Reply Generator")
    lang = sidebar_config_editor()
    if lang != st.session_state.language:
        switch_language(lang)
    selected_mode = st.session_state.config.get("ap_framework_mode", "balanced")
    framework_key = AP_FRAMEWORK_OPTIONS[selected_mode]
    st.session_state.config["ap_framework"] = st.session_state.config.get(framework_key, st.session_state.config.get(
        "ap_framework_full", ""))
    config = PromptConfig(**st.session_state.config)
    st.markdown("### Enter Comment")
    with st.form(key="input_form", clear_on_submit=False):
        user_input = st.text_area(
            "Comment",
            placeholder="Paste Instagram comment here...",
            height=120
        )
        submitted = st.form_submit_button("Generate Replies")
    status_placeholder = st.empty()
    if submitted and user_input.strip():
        with status_placeholder:
            with st.spinner():
                st.session_state.last_input = user_input
                client = ClaudeClient()
                replies, usage, cost = generate_replies(
                    config,
                    user_input,
                    st.session_state.n,
                    st.session_state.model,
                    st.session_state.temperature,
                    client
                )
                st.session_state.last_replies = replies
                st.session_state.last_usage = usage
                st.session_state.last_cost = cost

        display_results_streaming(replies, usage, cost)

    elif st.session_state.get("last_replies"):
        display_results(st.session_state.last_replies, st.session_state.last_usage, st.session_state.last_cost)


def main():

    init_state()
    if not st.session_state.authenticated:
        login_screen()
        return
    comment_generation_screen()


if __name__ == "__main__":

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("Missing ANTHROPIC_API_KEY")

    if not os.getenv("ADMIN_USERNAME") or not os.getenv("ADMIN_PASSWORD"):
        raise ValueError("Missing ADMIN_USERNAME or ADMIN_PASSWORD")

    if not os.getenv("USER_USERNAME") or not os.getenv("USER_PASSWORD"):
        raise ValueError("Missing USER_USERNAME or USER_PASSWORD")

    CREDENTIALS = {
        "admin": {
            "username": os.getenv("ADMIN_USERNAME").strip(),
            "password": os.getenv("ADMIN_PASSWORD").strip(),
        },
        "user": {
            "username": os.getenv("USER_USERNAME").strip(),
            "password": os.getenv("USER_PASSWORD").strip(),
        },
    }
    AUTH_LOOKUP = {
        (creds["username"], creds["password"]): role
        for role, creds in CREDENTIALS.items()
    }

    main()