from typing import Optional, TypedDict

class LLMConfigType(TypedDict):
    provider: str
    model: str
    temperature: float
    reasoning_effort: Optional[str]  # Para casos de modelos como família o1, o3 e o4.