from dataclasses import dataclass

@dataclass
class PromptConfig:
    system_prompt: str
    instructions: str
    examples: list
    context: str
    ap_framework: str

@dataclass
class GenerationRequest:
    prompt: str
    temperature: float
    model: str