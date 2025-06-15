from agent.states import AgentState
from common.llm_config import LLMConfig
from agent.agent_prompt import AGENT_SYSTEM_PROMPT
from agent.agent_toolbox.toolbox import TOOLS
from agent.agent_toolbox.tools.doc_search import search_documents
import logging

# Configure logging
logger = logging.getLogger(__name__)

class AgentNodes:
    def __init__(self):
        self.agent_system_prompt = AGENT_SYSTEM_PROMPT

    def agent_node(self, state: AgentState) -> AgentState:

        logger.info(f"Agent node called with llm_config: {state.get('llm_config')}")
        
        llm_config = LLMConfig(state["llm_config"])
        llm = llm_config.get_llm()
        
        if llm is None:
            logger.error("LLM is None! Check configuration.")
            raise ValueError("Failed to initialize LLM from config")

        # Inject thread_id into the search function for this execution
        thread_id = state.get("thread_id")
        logger.info(f"Raw thread_id from state: '{thread_id}'")
        
        # Ensure thread_id has the 'thread_' prefix if it doesn't already
        if thread_id and not thread_id.startswith("thread_"):
            thread_id = f"thread_{thread_id}"
            logger.info(f"Added thread_ prefix. Final thread_id: '{thread_id}'")
        
        if thread_id:
            search_documents._current_thread_id = thread_id
            logger.info(f"Set thread_id for search: '{thread_id}'")
        
        llm_with_tools = llm.bind_tools(TOOLS)

        return {"messages": [llm_with_tools.invoke([self.agent_system_prompt] + state["messages"])]}