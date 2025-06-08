from pydantic import BaseModel
from typing import Optional, List


class LLMConfig(BaseModel):
    provider: str = "openai"
    model: str = "gpt-4o"
    temperature: float = 0.0
    reasoning_effort: Optional[str] = None


class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str


class AgentRequest(BaseModel):
    messages: List[ChatMessage]
    llm_config: Optional[LLMConfig] = None
