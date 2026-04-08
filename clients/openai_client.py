import os
from openai import OpenAI

from utils.llm_error_handling import LLMErrorType, handle_llm_error


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.default_model = os.getenv("APP_DEFAULT_MODEL", "gpt-4o-mini")

    def generate(self, request):
        kwargs = dict(
            model=request.model or self.default_model,
            messages=[
                {"role": "system", "content": request.system}
            ] if request.system else []
        )

        # append user message
        kwargs["messages"].append({
            "role": "user",
            "content": request.prompt
        })

        if request.temperature is not None:
            kwargs["temperature"] = request.temperature

        if request.tools:
            kwargs["tools"] = request.tools
            kwargs["tool_choice"] = request.tool_choice

        try:
            response = self.client.chat.completions.create(**kwargs)

            message = response.choices[0].message

            return {
                "input": message.tool_calls if hasattr(message, "tool_calls") else None,
                "text": message.content,
                "usage": response.usage
            }

        except Exception as e:
            error_type = self.classify_openai_error(e)
            handle_llm_error(error_type, attempt=0)

    @staticmethod
    def classify_openai_error(e: Exception) -> LLMErrorType:
        msg = str(e).lower()

        # OpenAI SDK exceptions (v1+)
        from openai import (
            AuthenticationError,
            RateLimitError,
            APIConnectionError,
            APITimeoutError,
            InternalServerError,
            BadRequestError,
            PermissionDeniedError
        )

        # --- AUTH ---
        if isinstance(e, (AuthenticationError, PermissionDeniedError)):
            return LLMErrorType.AUTH

        # --- RATE LIMIT ---
        if isinstance(e, RateLimitError):
            return LLMErrorType.RATE_LIMIT

        # --- NO CREDITS / QUOTA ---
        if "quota" in msg or "billing" in msg or "insufficient" in msg:
            return LLMErrorType.NO_CREDITS

        # --- UNAVAILABLE ---
        if isinstance(e, (
            APIConnectionError,
            APITimeoutError,
            InternalServerError
        )):
            return LLMErrorType.UNAVAILABLE

        if "overloaded" in msg or "server error" in msg:
            return LLMErrorType.UNAVAILABLE

        # --- INVALID REQUEST (optional refinement) ---
        if isinstance(e, BadRequestError):
            return LLMErrorType.UNKNOWN  # or create INVALID if you want

        # --- FALLBACK ---
        return LLMErrorType.UNKNOWN