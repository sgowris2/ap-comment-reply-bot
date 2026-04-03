from dataclasses import dataclass, field
from typing import Optional

@dataclass
class PromptConfig:
    task: str
    instructions: str
    examples: list
    context: str
    ap_framework: str
    ap_framework_2: str

@dataclass
class GenerationRequest:
    prompt: str
    temperature: float
    model: str
    system: Optional[list] = None
    tools: list = field(default_factory=list)
    tool_choice: dict = field(default_factory=dict)