import anthropic
import os

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        self.default_model = os.getenv(
            "DEFAULT_MODEL",
            "claude-3-sonnet-20240229"
        )

    def generate(self, request):
        response = self.client.messages.create(
            model=request.model,
            max_tokens=500,
            temperature=request.temperature,
            messages=[
                {"role": "user", "content": request.prompt}
            ]
        )

        return {
            "text": response.content[0].text,
            "usage": response.usage
        }