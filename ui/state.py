import streamlit as st
from config.english import DEFAULT_CONFIG as EN
from config.hindi import DEFAULT_CONFIG as HI

def init_state():
    if "language" not in st.session_state:
        st.session_state.language = "English"
        st.session_state.config = EN.copy()

def switch_language(lang):
    if lang == "English":
        st.session_state.config = EN.copy()
    else:
        st.session_state.config = HI.copy()

    st.session_state.language = lang