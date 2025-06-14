from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages
from langchain_core.documents import Document
from common.types import LLMConfigType

class AgentState(TypedDict):
    messages: Annotated[List, add_messages]
    llm_config: LLMConfigType
    thread_id: str
