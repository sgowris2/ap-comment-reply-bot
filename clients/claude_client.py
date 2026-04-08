import anthropic
import os

from utils.llm_error_handling import LLMErrorType, handle_llm_error


class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("API_KEYS_ANTHROPIC")
        )
        self.default_model = os.getenv("APP_DEFAULT_MODEL", "claude-sonnet-4-6")

    def generate(self, request):
        kwargs = dict(
            model=request.model,
            max_tokens=1000,
            temperature=request.temperature,
            messages=[{"role": "user", "content": request.prompt}]
        )

        if request.system:
            kwargs["system"] = request.system

        if request.tools:
            kwargs["tools"] = request.tools
            kwargs["tool_choice"] = request.tool_choice

        try:
            response = self.client.messages.create(**kwargs)
            block = response.content[0]

            return {
                "input": block.input if hasattr(block, "input") else None,
                "text": block.text if hasattr(block, "text") else None,
                "usage": response.usage
            }
        except Exception as e:
            error_type = self.classify_anthropic_error(e)
            handle_llm_error(error_type, attempt=0)


    @staticmethod
    def classify_anthropic_error(e: Exception) -> LLMErrorType:
        msg = str(e).lower()

        # --- AUTH ---
        if isinstance(e, anthropic.AuthenticationError):
            return LLMErrorType.AUTH

        # --- RATE LIMIT ---
        if isinstance(e, anthropic.RateLimitError):
            return LLMErrorType.RATE_LIMIT

        # --- NO CREDITS / QUOTA ---
        if "credit" in msg or "quota" in msg or "billing" in msg:
            return LLMErrorType.NO_CREDITS

        # --- UNAVAILABLE (most important bucket) ---
        if isinstance(e, (
                anthropic.APIConnectionError,
                anthropic.APITimeoutError,
                anthropic.InternalServerError
        )):
            return LLMErrorType.UNAVAILABLE

        if "overloaded" in msg:
            return LLMErrorType.UNAVAILABLE

        # --- FALLBACK ---
        return LLMErrorType.UNKNOWN