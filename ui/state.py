import streamlit as st
from prompts.v1 import DEFAULT_CONFIG as EN

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
        st.session_state.temperature = 0.6
        st.session_state.n = 1
        st.session_state.last_replies = None
        st.session_state.last_usage = None
        st.session_state.last_input = ""

    if "ap_framework_mode" not in st.session_state.config:
        st.session_state.ap_framework_mode = "balanced"