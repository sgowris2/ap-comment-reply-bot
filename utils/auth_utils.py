import os

import bcrypt
import streamlit as st

PEPPER = os.getenv("PASSWORD_PEPPER", "")


def get_credentials():
    creds = {}

    # --- admin ---
    creds[os.getenv("AUTH_ADMIN_USERNAME")] = {
        "username": os.getenv("AUTH_ADMIN_USERNAME"),
        "password_hash": os.getenv("AUTH_ADMIN_PASSWORD_HASH"),
        "role": "admin"
    }
    users = st.secrets["auth"]["users"]

    for user in users:
        creds[user["username"]] = {
            "username": user["username"],
            "password_hash": user["password_hash"],
            "role": user.get("role", "user")
        }

    return creds


def verify_password(password, stored_hash):
    pepper = st.secrets["auth"].get("password_pepper", PEPPER)
    return bcrypt.checkpw(
        (password + pepper).encode(),
        stored_hash.strip().encode()
    )


def authenticate(username, password):
    credentials = get_credentials()

    print(credentials)
    print(username)
    user = credentials.get(username)
    print(user)
    if not user:
        return None

    if verify_password(password, user["password_hash"]):
        print("Password verified for user:", username)
        return user["role"]

    print("Password verification failed for user:", username)
    return None
