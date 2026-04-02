from domain.prompt_builder import build_prompt
from domain.models import GenerationRequest

def generate_replies(config, user_input, n, model, temperature, client):
    results = []

    for _ in range(n):
        prompt = build_prompt(config, user_input)

        request = GenerationRequest(
            prompt=prompt,
            temperature=temperature,
            model=model
        )

        response = client.generate(request)

        results.append({
            "text": response["text"],
            "usage": response["usage"]
        })

    return results