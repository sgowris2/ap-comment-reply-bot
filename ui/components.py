import time

import streamlit as st

AP_FRAMEWORK_OPTIONS = {
    "full": "ap_framework_full",
    "balanced": "ap_framework_200",
    "short": "ap_framework_100",
}

def sidebar_config_editor():
    is_admin = st.session_state.is_admin

    st.sidebar.header("⚙️ Settings")

    show_language = False   # If we want to enable langauge switching in the future
    if show_language:
        lang = st.sidebar.selectbox(
            "Language",
            ["English", "Hindi"],
            index=["English", "Hindi"].index(st.session_state.language),
            disabled=True
        )
    else:
        lang = st.session_state.language

    st.session_state.config["context"] = st.sidebar.text_area(
        "Post Transcript (Recommended)",
        st.session_state.config["context"],
        height=400
    )

    apf_labels = list(AP_FRAMEWORK_OPTIONS.keys())
    default_label = st.session_state.config.get("ap_framework_mode", apf_labels[0])
    if default_label not in apf_labels:
        default_label = apf_labels[0]

    if is_admin:
        with st.sidebar.expander("Prompt Settings", expanded=False):
            st.session_state.config["task"] = st.text_area(
                "Task",
                st.session_state.config["task"],
                height=200,
            )
            st.session_state.config["instructions"] = st.text_area(
                "Instructions",
                st.session_state.config["instructions"],
                height=200,
            )
            selected_label = st.selectbox(
                "AP Framework",
                apf_labels,
                index=apf_labels.index(default_label),
                key="ap_framework_mode",
            )
            st.session_state.config["ap_framework_mode"] = selected_label
            if st.session_state.get("last_ap_mode") != selected_label:
                framework_key = AP_FRAMEWORK_OPTIONS[selected_label]
                st.session_state["ap_framework_text"] = st.session_state.config.get(framework_key, "")
                st.session_state["last_ap_mode"] = selected_label

            st.session_state.config["ap_framework"] = st.text_area(
                "AP Framework",
                key="ap_framework_text",
                height=200,
            )

    selected_mode = st.session_state.config.get("ap_framework_mode", "balanced")
    framework_key = AP_FRAMEWORK_OPTIONS[selected_mode]
    st.session_state.config["ap_framework"] = st.session_state.config.get(framework_key, "")


    if is_admin:
        with st.sidebar.expander("Model Settings", expanded=False):
            model_options = {
                "⚡ Fast (Haiku 4.5)": "claude-haiku-4-5",
                "🧠 Smart (Sonnet 4.6)": "claude-sonnet-4-6",
            }
            model_labels = list(model_options.keys())
            model_values = list(model_options.values())
            st.session_state.model = st.selectbox(
                "Model",
                model_labels,
                index=model_values.index(st.session_state.model),
            )
            st.session_state.model = model_options[st.session_state.model]
            st.session_state.temperature = st.slider(
                "Creativity", 0.0, 1.0, st.session_state.temperature,
            )
            st.session_state.n = st.slider(
                "Replies", 1, 5, st.session_state.n,
            )

    return lang


def stream_text(text, placeholder, delay=0.01):
    rendered = ""
    for char in text:
        rendered += char
        placeholder.markdown(rendered + "▌")
        time.sleep(delay)
    placeholder.markdown(rendered)


def display_results_streaming(replies, usage, cost):
    for i, r in enumerate(replies):
        st.markdown(f"### Reply {i+1}")
        placeholder = st.empty()

        stream_text(r["text"], placeholder)

        st.divider()
        time.sleep(0.2)

    _display_cost(cost, usage)

def display_results(replies, usage, cost):
    for i, r in enumerate(replies):
        with st.container():
            st.markdown(f"### Reply {i+1}")
            st.write(r["text"])
            st.divider()

    _display_cost(cost, usage)


def _display_cost(cost, usage):
    if st.session_state.is_admin:
        cache_write = getattr(usage, "cache_creation_input_tokens", 0)
        cache_read = getattr(usage, "cache_read_input_tokens", 0)
        st.caption(
            f"Tokens → Input: {usage.input_tokens} (Cache Read: {cache_read}, Write: {cache_write}) | Output: {usage.output_tokens} | 💰 Cost: Rs. {cost * 100.0:.2f}"
        )
