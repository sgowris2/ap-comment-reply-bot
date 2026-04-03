from dataclasses import dataclass, field

@dataclass
class PromptConfig:
    task: str
    instructions: str
    examples: list
    context: str
    ap_framework: str

@dataclass
class GenerationRequest:
    prompt: str
    temperature: float
    model: str
    tools: list = field(default_factory=list)
    tool_choice: dict = field(default_factory=dict)