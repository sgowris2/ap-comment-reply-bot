import streamlit as st

def sidebar_config_editor(config):
    st.sidebar.header("⚙️ Settings")

    # Language
    lang = st.sidebar.selectbox("Language", ["English", "Hindi"])

    # Context (important → keep outside advanced)
    config["context"] = st.sidebar.text_area(
        "Post Context (Optional)",
        config["context"],
        height=120
    )

    with st.sidebar.expander("Prompt Settings", expanded=False):
        config["system_prompt"] = st.text_area(
            "System Prompt",
            config["system_prompt"],
            height=200
        )

        config["instructions"] = st.text_area(
            "Instructions",
            config["instructions"],
            height=200
        )

        config["ap_framework"] = st.text_area(
            "AP Framework",
            config.get("ap_framework", ""),
            height=200
        )

    model = st.sidebar.selectbox(
        "Model",
        ["claude-haiku-4-5", "claude-sonnet-4-6"]
    )

    with st.sidebar.expander("Generation Settings", expanded=False):
        temperature = st.slider("Creativity", 0.0, 1.0, 0.5)
        n = st.slider("Replies", 1, 5, 1)

    return config, model, temperature, n, lang


def display_results(results):
    for i, r in enumerate(results):
        with st.container():
            st.markdown(f"### Reply {i+1}")
            st.write(r["text"])

            usage = r["usage"]
            st.caption(
                f"Tokens → Input: {usage.input_tokens} | Output: {usage.output_tokens}"
            )
            st.divider()