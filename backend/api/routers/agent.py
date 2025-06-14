from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from agent.states import AgentState
from api.schemas.agent_schemas import AgentRequest

from agent.graph import Agent

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)

agent = Agent()

def parse_chat_history(chat_history: List[tuple[str, str]]) -> List[BaseMessage]:
    """
    This function is used to parse the chat history.

    Example:
    input:
    [("user", "Hello, how are you?"), ("assistant", "I'm good, thank you! How can I help you today?")]
    will be parsed as:
    [HumanMessage(content="Hello, how are you?"), AIMessage(content="I'm good, thank you! How can I help you today?")]
    """

    parsed_chat_history = []
    for message in chat_history:
        if message.role == "user":
            parsed_chat_history.append(HumanMessage(content=message.content))
        elif message.role == "assistant":
            parsed_chat_history.append(AIMessage(content=message.content))
    return parsed_chat_history

@router.post("/chat")
def stream_agent_chat(agent_request: AgentRequest):
    """
    Receives a user message and LLM config, streams the agent's response using SSE.
    """
    try:
        global agent
        
        # 1. Parse tuple list into list of langchain BaseMessage's.
        chat_history = parse_chat_history(agent_request.messages)

        # 2. Create agent input.
        agent_input: AgentState = {
            "messages": chat_history,
            "llm_config": agent_request.llm_config.model_dump(),
            "thread_id": agent_request.thread_id
        }

        # 3. Stream response.
        return StreamingResponse(agent.run_agent_streaming(agent_input), media_type="text/event-stream")

    # 4. Handle exceptions.
    except Exception as e:
        print(f"Error in stream_agent_chat: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
