import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from ui.state import init_state, switch_language
from ui.components import sidebar_config_editor, display_results
from clients.claude_client import ClaudeClient
from api.generate_replies import generate_replies
from domain.models import PromptConfig


def main():
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

    init_state()

    lang = sidebar_config_editor()

    if lang != st.session_state.language:
        switch_language(lang)

    config = PromptConfig(**st.session_state.config)

    st.markdown("### Enter Comment")

    with st.form(key="input_form", clear_on_submit=False):
        user_input = st.text_area(
            "Comment",
            placeholder="Paste Instagram comment here...",
            height=120
        )
        submitted = st.form_submit_button("Generate")

    if submitted and user_input.strip():
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

    if st.session_state.get("last_replies"):
        display_results(st.session_state.last_replies, st.session_state.last_usage, st.session_state.last_cost)


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("Missing ANTHROPIC_API_KEY")

    main()