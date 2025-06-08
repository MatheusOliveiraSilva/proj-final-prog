from typing import Optional, TypedDict

class LLMConfig(TypedDict):
    model: str
    temperature: float
    reasoning: bool
    reasoning_effort: Optional[str]  # Para casos de modelos como família o1, o3 e o4.