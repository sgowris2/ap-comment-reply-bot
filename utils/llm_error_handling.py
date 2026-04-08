from enum import Enum
import anthropic

class LLMErrorType(Enum):
    AUTH = "auth"                # wrong API key
    NO_CREDITS = "no_credits"    # quota exhausted
    RATE_LIMIT = "rate_limit"    # too many requests
    UNAVAILABLE = "unavailable"  # provider down / overloaded
    UNKNOWN = "unknown"          # everything else


def handle_llm_error(error_type, attempt):

    if error_type == LLMErrorType.AUTH:
        raise Exception("❌ Invalid API key. Fix credentials.")

    elif error_type == LLMErrorType.NO_CREDITS:
        raise Exception("💳 No credits left. Check billing.")

    elif error_type == LLMErrorType.RATE_LIMIT:
        raise Exception("⏳ Rate limit hit. Slow down.")

    elif error_type == LLMErrorType.UNAVAILABLE:
        raise Exception("⚠️ Service unavailable. Try again later.")

    elif error_type == LLMErrorType.UNKNOWN:
        raise Exception("❓ An unknown error occurred. Check logs for details.")