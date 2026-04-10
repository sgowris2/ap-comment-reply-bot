import threading

import streamlit as st

from clients.supabase_client import supabase


def log_generation_event(data: dict):
    """
    Synchronous logging function.
    Expects a fully constructed payload (no Streamlit state access here).
    """
    try:
        supabase.table("generated_replies").insert(data).execute()
    except Exception as e:
        print("⚠️ Logging failed:", e)


def log_generation_event_async(data: dict):
    """
    Fire-and-forget async logger using a background thread.
    """
    thread = threading.Thread(
        target=_safe_log_wrapper,
        args=(data,),
        daemon=True  # ensures thread won't block app shutdown
    )
    thread.start()


def _safe_log_wrapper(data: dict):
    """
    Internal wrapper to prevent thread crashes from affecting the app.
    """
    try:
        log_generation_event(data)
    except Exception as e:
        print("⚠️ Async logging failed:", e)


def construct_log_payload(cost, replies, usage, user_input):
    payload = {
        "user_id": st.session_state.get("user_id", "anonymous"),
        "role": st.session_state.get("role"),

        "transcript": st.session_state.config.get("context"),

        "model": st.session_state.model,
        "temperature": st.session_state.temperature,
        "n_replies": st.session_state.n,

        "comment": user_input,

        "generated_reply_options": [r["text"] for r in replies],
        "generated_reply": replies[0]["text"] if replies else None,

        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "estimated_cost": cost,
        "environment": st.session_state.get("environment"),
    }
    return payload
