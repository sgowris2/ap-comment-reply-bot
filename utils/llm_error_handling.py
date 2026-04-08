from enum import Enum

class LLMErrorType(Enum):
    AUTH = "auth"                # wrong API key
    NO_CREDITS = "no_credits"    # quota exhausted
    RATE_LIMIT = "rate_limit"    # too many requests
    UNAVAILABLE = "unavailable"  # provider down / overloaded
    UNKNOWN = "unknown"          # everything else

class LLMError(Exception):
    def __init__(self, error_type: LLMErrorType, message: str = ""):
        self.error_type = error_type
        self.message = message
        super().__init__(f"{error_type.value}: {message}")


def handle_llm_error(error_type, attempt):

    if error_type == LLMErrorType.AUTH:
        raise LLMError(error_type, "❌ Invalid API key. Fix credentials.")

    elif error_type == LLMErrorType.NO_CREDITS:
        raise LLMError(error_type, "💳 No credits left. Check billing.")

    elif error_type == LLMErrorType.RATE_LIMIT:
        raise LLMError(error_type, "⏳ Rate limit hit. Slow down.")

    elif error_type == LLMErrorType.UNAVAILABLE:
        raise LLMError(error_type, "⚠️ Service unavailable. Try again later.")

    else:
        raise LLMError(error_type, "❓ An unknown error occurred. Check logs for details.")