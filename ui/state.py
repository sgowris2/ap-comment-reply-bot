import streamlit as st
from prompts.v4 import DEFAULT_CONFIG as EN

def init_state(env=None):

    st.session_state.environment = env

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "role" not in st.session_state:
        st.session_state.role = None

    if "language" not in st.session_state:
        st.session_state.language = "English"
        st.session_state.config = EN.copy()

    if "model" not in st.session_state:
        st.session_state.model = "claude-sonnet-4-6"
        st.session_state.post_process_replies = False
        st.session_state.post_processing_model = "claude-haiku-4-5"
        st.session_state.temperature = 1.0
        st.session_state.n = 3
        st.session_state.last_replies = None
        st.session_state.last_usage = None
        st.session_state.last_input = ""