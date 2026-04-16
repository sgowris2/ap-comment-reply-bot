import anthropic
import os
from anthropic.types.usage import Usage

from utils.llm_error_handling import LLMErrorType, handle_llm_error


class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("API_KEYS_ANTHROPIC")
        )
        self.default_model = os.getenv("APP_DEFAULT_MODEL", "claude-sonnet-4-6")
        self.post_processing_model = os.getenv("APP_POST_PROCESSING_MODEL", "claude-haiku-4-5")

    def generate(self, request):
        kwargs = dict(
            model=request.model,
            max_tokens=1000,
            temperature=request.temperature,
            messages=[{"role": "user", "content": self.normalize_blocks(request.prompt)}]
        )

        if request.system:
            kwargs["system"] = self.normalize_blocks(request.system)

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
            error_type, exception = self.classify_anthropic_error(e)
            handle_llm_error(error_type, exception, attempt=0)

    @staticmethod
    def normalize_blocks(blocks):
        normalized = []
        for b in blocks:
            nb = {
                "type": b.get("type", "text"),
                "text": str(b.get("text", ""))
            }
            if "cache_control" in b:
                nb["cache_control"] = b["cache_control"]
            normalized.append(nb)
        return normalized

    @staticmethod
    def add_usage(usage1: Usage, usage2: Usage) -> Usage:
        """Combine two Usage objects by summing their token counts."""
        return Usage(
            cache_creation=usage1.cache_creation or usage2.cache_creation,
            cache_creation_input_tokens=(usage1.cache_creation_input_tokens or 0) + (
                        usage2.cache_creation_input_tokens or 0),
            cache_read_input_tokens=(usage1.cache_read_input_tokens or 0) + (usage2.cache_read_input_tokens or 0),
            inference_geo=usage1.inference_geo or usage2.inference_geo,
            input_tokens=usage1.input_tokens + usage2.input_tokens,
            output_tokens=usage1.output_tokens + usage2.output_tokens,
            server_tool_use=usage1.server_tool_use or usage2.server_tool_use,
            service_tier=usage1.service_tier or usage2.service_tier,
        )


    @staticmethod
    def classify_anthropic_error(e: Exception) -> tuple[LLMErrorType, Exception]:
        msg = str(e).lower()

        # --- AUTH ---
        if isinstance(e, anthropic.AuthenticationError):
            return LLMErrorType.AUTH, e

        # --- RATE LIMIT ---
        if isinstance(e, anthropic.RateLimitError):
            return LLMErrorType.RATE_LIMIT, e

        # --- NO CREDITS / QUOTA ---
        if "credit" in msg or "quota" in msg or "billing" in msg:
            return LLMErrorType.NO_CREDITS, e

        # --- UNAVAILABLE (most important bucket) ---
        if isinstance(e, (
                anthropic.APIConnectionError,
                anthropic.APITimeoutError,
                anthropic.InternalServerError
        )):
            return LLMErrorType.UNAVAILABLE, e

        if "overloaded" in msg:
            return LLMErrorType.UNAVAILABLE, e

        # --- FALLBACK ---
        return LLMErrorType.UNKNOWN, e