def extract_tokens(usage):
    return {
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "total_tokens": usage.input_tokens + usage.output_tokens
    }