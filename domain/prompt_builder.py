def format_examples(examples):
    return "\n".join(
        [f"Input: {e['input']}\nOutput: {e['output']}" for e in examples]
    )

def build_prompt(config, user_input):
    return f"""
{config.system_prompt}

AP Framework:
{config.ap_framework}

Instructions:
{config.instructions}

Context:
{config.context}

Examples:
{format_examples(config.examples)}

User Comment:
{user_input}

Reply:
""".strip()