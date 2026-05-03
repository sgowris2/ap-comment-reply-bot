import json
from itertools import product


class PromptBuilder:

    def __init__(self, config):
        self.config = config
        self.system_prompts = self._initialize_system_prompt_variants()

    def _initialize_system_prompt_variants(self):
        return {
            (mode, gita): [
                {
                    "type": "text",
                    "text": self._build_system_prompt(mode=mode, gita=gita),  # no config arg
                    "cache_control": {"type": "ephemeral", "ttl": "1h"}  # cached across all calls,
                }
            ]
            for mode, gita in product(["regular", "serious"], [True, False])
        }

    def build_prompt(self, user_input, n=1, mode="regular", gita=True):
        system = self.system_prompts[(mode, gita)]  # use pre-built, never rebuild
        transcript = self.config.context.strip()

        user_content = []

        if transcript:
            user_content.append({
                "type": "text",
                "text": f"VIDEO TRANSCRIPT:\n{transcript}",
                "cache_control": {"type": "ephemeral", "ttl": "1h"}  # second-level cache for same-video batches
            })

        user_content.append({
            "type": "text",
            "text": f"Number of reply options to generate: {n}"
        })

        user_content.append({
            "type": "text",
            "text": f"COMMENT:\n{user_input}"
        })

        return system, user_content

    def _build_system_prompt(self, mode="regular", gita=True):  # no config param
        base = f"""
        {self.config.task}

        AP Framework:
        {self.config.ap_framework}

        Instructions:
        {self.format_instructions(self.config.instructions)}
        """.strip()

        mode_suffix = self.config.mode_suffixes[mode]
        gita_suffix = self.config.gita_suffixes["enabled"] if gita else self.config.gita_suffixes["disabled"]

        return base + mode_suffix + gita_suffix

    @staticmethod
    def format_instructions(instructions) -> str:
        if isinstance(instructions, str):
            return instructions
        return json.dumps(instructions, ensure_ascii=False, indent=2)
