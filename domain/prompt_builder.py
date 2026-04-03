import json


def format_examples(examples: dict) -> str:
    pairs = examples.get("comment_reply_pairs", [])
    if not pairs:
        return "None"

    lines = []
    note = examples.get("note", "")
    if note:
        lines.append(f"Note: {note}\n")

    transcript = examples.get("transcript_this_example_is_based_on", {})
    if transcript:
        lines.append(f"These examples are based on a video about: {transcript.get('video_topic', '')}")
        lines.append(f"Central metaphor: {transcript.get('central_metaphor', '')}\n")

    for pair in pairs:
        lines.append(f"Comment ({pair.get('comment_language', '')}): {pair['comment']}")
        lines.append(f"Reply ({pair.get('reply_language', '')}): {pair['reply']}")
        if pair.get("notes"):
            lines.append(f"Why: {pair['notes']}")
        lines.append("")

    return "\n".join(lines)


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
            "cache_control": {"type": "ephemeral"}  # cached across all calls
        }
    ]

    # Build user message content blocks
    user_content = []

    if transcript:
        user_content.append({
            "type": "text",
            "text": f"VIDEO TRANSCRIPT:\n{transcript}",
            "cache_control": {"type": "ephemeral"}  # cached per video
        })

    user_content.append({
        "type": "text",
        "text": f"COMMENT:\n{comment}"
        # no cache_control — changes every call
    })

    return system, user_content


def _build_system_text(config, n):
    return f"""
    {config.task}
    
    AP Framework:
    {config.ap_framework}
    
    Instructions:
    {format_instructions(config.instructions)}
    
    Context:
    {config.context or "None"}
    
    Number of reply options to generate: {n}
    """.strip()


# Examples:
#     {format_examples(config.examples) if config.examples else "None"}