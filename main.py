import os

import bcrypt
import streamlit as st
from utils.load_secrets import inject_secrets_to_env
inject_secrets_to_env()

from ui.state import init_state, switch_language
from ui.components import sidebar_config_editor, display_results, AP_FRAMEWORK_OPTIONS, display_results_streaming
from clients.claude_client import ClaudeClient
from api.logging_service import log_generation_event_async, construct_log_payload
from api.generate_replies import generate_replies
from domain.models import PromptConfig
from utils.auth_utils import authenticate



def login_screen():
    st.markdown(
        """
        <h1 style='text-align: center;'>💬 AP Comment Reply Generator</h1>
        <h3 style='text-align: center;'>🔐 Login</h3>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("Username").strip()
    password = st.text_input("Password", type="password").strip()

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        login_clicked = st.button("Login", use_container_width=True)

    if login_clicked:
        role = authenticate(username, password)

        if role:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role
            st.session_state.is_admin = role == "admin"
            st.rerun()
        else:
            st.error("Invalid credentials")

# def login_screen():
#     st.markdown(
#         """
#         <h1 style='text-align: center;'>💬 AP Comment Reply Generator</h1>
#         <h3 style='text-align: center;'>🔐 Login</h3>
#         """,
#         unsafe_allow_html=True
#     )
#     st.write("")
#     username = st.text_input("Username").strip()
#     password = st.text_input("Password", type="password").strip()
#     st.write("")
#     col1, col2, col3 = st.columns([2, 1, 2])
#     with col2:
#         login_clicked = st.button("Login", use_container_width=True)
#     st.write("")
#
#     if login_clicked:
#         role = AUTH_LOOKUP.get((username, password))
#         if role:
#             st.session_state.authenticated = True
#             st.session_state.role = role
#             st.session_state.is_admin = role == "admin"
#             st.rerun()
#         else:
#             st.error("Invalid credentials")


def create_new_user_screen():
    if not st.session_state.get("is_admin"):
        st.error("Access denied")
        return

    st.subheader("👤 Create New User")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Create User"):
        if not new_username or not new_password:
            st.warning("Please fill all fields")
            return

        hashed = bcrypt.hashpw(
            (new_password + PEPPER).encode(),
            bcrypt.gensalt()
        ).decode()

        st.success("User created! Copy this into your secrets.toml 👇")

        st.code(f"""
        [[auth.users]]
        username = "{new_username}"
        password_hash = "{hashed}"
        role = "{role}"
        """)


def comment_generation_screen():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
        <style>
            [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
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
        payload = construct_log_payload(cost, replies, usage, user_input)
        log_generation_event_async(payload)

    elif st.session_state.get("last_replies"):
        display_results(st.session_state.last_replies, st.session_state.last_usage, st.session_state.last_cost)


def main(env=None):

    try:
        init_state(env)
        st.set_page_config(
            page_title="AP Comment Reply Generator",
            page_icon="💬",
        )
        if not st.session_state.authenticated:
            login_screen()
            return
        comment_generation_screen()

    except Exception as e:
        st.warning(str(e))


if __name__ == "__main__":

    PEPPER = os.getenv("AUTH_PASSWORD_PEPPER", None)
    if PEPPER is None:
        raise ValueError("Missing AUTH_PASSWORD_PEPPER")
    else:
        PEPPER = PEPPER.strip()

    if not os.getenv("API_KEYS_ANTHROPIC"):
        raise ValueError("Missing API_KEYS_ANTHROPIC")

    if not os.getenv("AUTH_ADMIN_USERNAME") or not os.getenv("AUTH_ADMIN_PASSWORD_HASH"):
        raise ValueError("Missing AUTH_ADMIN_USERNAME or AUTH_ADMIN_PASSWORD_HASH")

    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY")

    ENVIRONMENT = os.getenv("APP_ENV", "development").strip()


    # admin = {
    #     "username": os.getenv("AUTH_ADMIN_USERNAME").strip(),
    #     "password": os.getenv("AUTH_ADMIN_PASSWORD").strip(),
    # }
    # users_raw = os.getenv("AUTH_USERS", "[]")
    # users_list = json.loads(users_raw)
    #
    # CREDENTIALS = dict()
    # CREDENTIALS["admin"] = admin
    # for user in users_list:
    #     username = user["username"].strip()
    #     password = user["password"].strip()
    #     CREDENTIALS[username] = {
    #         "username": username,
    #         "password": password,
    #     }
    # AUTH_LOOKUP = {
    #     (creds["username"], creds["password"]): role
    #     for role, creds in CREDENTIALS.items()
    # }

    main(env=ENVIRONMENT)