import anthropic
import os

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.default_model = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-6")

    def generate(self, request):
        kwargs = dict(
            model=request.model,
            max_tokens=1000,
            temperature=request.temperature,
            messages=[{"role": "user", "content": request.prompt}]
        )

        if request.tools:
            kwargs["tools"] = request.tools
            kwargs["tool_choice"] = request.tool_choice

        response = self.client.messages.create(**kwargs)
        block = response.content[0]

        return {
            "input": block.input if hasattr(block, "input") else None,
            "text": block.text if hasattr(block, "text") else None,
            "usage": response.usage
        }