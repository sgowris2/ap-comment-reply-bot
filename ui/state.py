import streamlit as st
from config.english import DEFAULT_CONFIG as EN
from config.hindi import DEFAULT_CONFIG as HI

def init_state():
    if "language" not in st.session_state:
        st.session_state.language = "English"
        st.session_state.config = EN.copy()
        st.session_state.model = "claude-haiku-4-5"
        st.session_state.temperature = 0.5
        st.session_state.n = 1
        st.session_state.last_replies = None
        st.session_state.last_usage = None
        st.session_state.last_input = ""

def switch_language(lang):
    st.session_state.config = EN.copy() if lang == "English" else HI.copy()
    st.session_state.language = lang