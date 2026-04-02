import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from ui.state import init_state, switch_language
from ui.components import sidebar_config_editor, display_results
from clients.claude_client import ClaudeClient
from api.api import generate_replies
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

    # Sidebar config
    config_dict, model, temperature, n, lang = sidebar_config_editor(
        st.session_state.config
    )

    # Language switch
    if lang != st.session_state.language:
        switch_language(lang)

    config = PromptConfig(**config_dict)

    # Main input (center focus)
    st.markdown("### Enter Comment")

    with st.form(key="input_form", clear_on_submit=False):
        user_input = st.text_area(
            "Comment",
            placeholder="Paste Instagram comment here...",
            height=120
        )

        submitted = st.form_submit_button("Generate")

    # Generate on submit (Enter works here)
    if submitted and user_input.strip():
        st.session_state.last_input = user_input

        client = ClaudeClient()

        results = generate_replies(
            config,
            user_input,
            n,
            model,
            temperature,
            client
        )

        display_results(results)


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("Missing ANTHROPIC_API_KEY")

    main()