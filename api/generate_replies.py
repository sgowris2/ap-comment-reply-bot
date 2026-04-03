from domain.prompt_builder import build_prompt
from domain.models import GenerationRequest

REPLY_TOOL = {
    "name": "submit_replies",
    "description": "Submit the generated comment replies",
    "input_schema": {
        "type": "object",
        "properties": {
            "reply_options": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of reply options"
            }
        },
        "required": ["reply_options"]
    }
}

MODEL_PRICING = {
    "claude-haiku-3": {"input": 0.25, "output": 1.25},
    "claude-haiku-3-5": {"input": 0.8, "output": 4},
    "claude-haiku-4-5": {"input": 1, "output": 5},

    "claude-sonnet-4": {"input": 3, "output": 15},
    "claude-sonnet-4-5": {"input": 3, "output": 15},
    "claude-sonnet-4-6": {"input": 3, "output": 15},
}

def generate_replies(config, user_input, n, model, temperature, client):
    prompt = build_prompt(config, user_input, n)

    request = GenerationRequest(
        prompt=prompt,
        temperature=temperature,
        model=model,
        tools=[REPLY_TOOL],
        tool_choice={"type": "tool", "name": "submit_replies"}
    )

    response = client.generate(request)
    reply_options = response["input"]["reply_options"]  # already a parsed list
    usage = response["usage"]
    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens
    cost = calculate_cost(model, input_tokens, output_tokens)

    results = [{"text": r} for r in reply_options]
    return results, usage, cost


def calculate_cost(model, input_tokens, output_tokens):
    pricing = MODEL_PRICING.get(model)

    if not pricing:
        return 0.0  # fallback safety

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return input_cost + output_cost