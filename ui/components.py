import streamlit as st

def sidebar_config_editor():
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
        "Post Context (Optional)",
        st.session_state.config["context"],
        height=120
    )

    with st.sidebar.expander("Prompt Settings", expanded=False):
        st.session_state.config["task"] = st.text_area(
            "Task",
            st.session_state.config["task"],
            height=200
        )
        st.session_state.config["instructions"] = st.text_area(
            "Instructions",
            st.session_state.config["instructions"],
            height=200
        )
        st.session_state.config["ap_framework"] = st.text_area(
            "AP Framework",
            st.session_state.config.get("ap_framework", ""),
            height=200
        )

    model_options = {
        "⚡ Fast (Haiku 4.5)": "claude-haiku-4-5",
        "🧠 Smart (Sonnet 4.6)": "claude-sonnet-4-6",
    }
    labels = list(model_options.keys())
    values = list(model_options.values())
    st.session_state.model = st.sidebar.selectbox(
        "Model",
        labels,
        index=values.index(st.session_state.model)
    )
    st.session_state.model = model_options[st.session_state.model]

    with st.sidebar.expander("Generation Settings", expanded=False):
        st.session_state.temperature = st.slider(
            "Creativity", 0.0, 1.0, st.session_state.temperature
        )
        st.session_state.n = st.slider(
            "Replies", 1, 5, st.session_state.n
        )

    return lang


def display_results(replies, usage, cost):
    for i, r in enumerate(replies):
        with st.container():
            st.markdown(f"### Reply {i+1}")
            st.write(r["text"])
            st.divider()

    st.caption(
        f"Tokens → Input: {usage.input_tokens} | Output: {usage.output_tokens} | 💰 Cost: Rs. {cost*100.0:.2f}"
    )