import json


def format_instructions(instructions) -> str:
    if isinstance(instructions, str):
        return instructions
    return json.dumps(instructions, ensure_ascii=False, indent=2)


def build_prompt(config, user_input, n=1):
    system_text = _build_system_text(config, n)
    transcript = config.context
    comment = user_input

    system = [
        {
            "type": "text",
            "text": system_text,
            "cache_control": {"type": "ephemeral", "ttl": "1h"}  # cached across all calls
        }
    ]

    # Build user message content blocks
    user_content = list()

    if transcript:
        user_content.append({
            "type": "text",
            "text": f"VIDEO TRANSCRIPT:\n{transcript}",
            "cache_control": {"type": "ephemeral", "ttl": "5m"}
        })

    user_content.append({
        "type": "text",
        "text": f"Number of reply options to generate: {n}",
        "cache_control": {"type": "ephemeral", "ttl": "1h"}
    })

    user_content.append({
        "type": "text",
        "text": f"COMMENT:\n{comment}"
    })

    return system, user_content


def _build_system_text(config, n):
    return f"""
    {config.task}
    
    AP Framework:
    {config.ap_framework}
    
    Instructions:
    {format_instructions(config.instructions)}
    """.strip()
