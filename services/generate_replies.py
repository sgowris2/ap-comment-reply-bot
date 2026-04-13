import json
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
    "claude-haiku-3":   {"input": 0.25,  "output": 1.25, "cache_write": 0.50,   "cache_read": 0.025},
    "claude-haiku-3-5": {"input": 0.8,   "output": 4,    "cache_write": 1.6,    "cache_read": 0.08},
    "claude-haiku-4-5": {"input": 1,     "output": 5,    "cache_write": 2,   "cache_read": 0.1},
    "claude-sonnet-4-6":{"input": 3,     "output": 15,   "cache_write": 6,   "cache_read": 0.3},
    "claude-opus-4-6": {"input": 5,     "output": 25,   "cache_write": 10,    "cache_read": 0.5},
}

def generate_replies(config, user_input, n, model, temperature, client):
    system, prompt = build_prompt(config, user_input, n)

    request = GenerationRequest(
        prompt=prompt,
        system=system,
        temperature=temperature,
        model=model,
        tools=[REPLY_TOOL],
        tool_choice={"type": "tool", "name": "submit_replies"}
    )

    response = client.generate(request)
    reply_options = response["input"]["reply_options"]  # already a parsed list
    if isinstance(reply_options, str):
        reply_options = json.loads(reply_options)
    usage = response["usage"]
    cost = calculate_cost(model, usage)

    results = [{"text": r} for r in reply_options]
    return results, usage, cost

def post_process_replies(config, replies, model, temperature, client):
    system = config.post_process_instructions
    prompt = list()
    for reply in replies:
        prompt.append({
            "type": "text",
            "text": f"REPLY OPTION:\n{reply['text']}"
        })
    request = GenerationRequest(
        prompt=prompt,
        system=system,
        temperature=temperature,
        model=model,
        tools=[REPLY_TOOL],
        tool_choice={"type": "tool", "name": "submit_replies"}
    )
    print(request)
    response = client.generate(request)
    print(response)
    processed_replies = response["input"]["reply_options"]  # already a parsed list
    if isinstance(processed_replies, str):
        processed_replies = json.loads(processed_replies)
    usage = response["usage"]
    cost = calculate_cost(model, usage)

    results = [{"text": r} for r in processed_replies]
    return results, usage, cost


def calculate_cost(model, usage):
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        return 0.0

    cache_write  = getattr(usage, "cache_creation_input_tokens", 0)
    cache_read   = getattr(usage, "cache_read_input_tokens", 0)
    plain_input  = usage.input_tokens

    return (
        (plain_input  / 1_000_000) * pricing["input"]        +
        (cache_write  / 1_000_000) * pricing["cache_write"]  +
        (cache_read   / 1_000_000) * pricing["cache_read"]   +
        (usage.output_tokens / 1_000_000) * pricing["output"]
    )