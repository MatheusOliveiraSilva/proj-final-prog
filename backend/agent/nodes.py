from agent.states import AgentState
from common.llm_config import LLMConfig
from agent.agent_prompt import AGENT_SYSTEM_PROMPT

class AgentNodes:
    def __init__(self):
        self.agent_system_prompt = AGENT_SYSTEM_PROMPT

    def agent_node(self, state: AgentState) -> AgentState:

        llm_config = LLMConfig(state["llm_config"])
        llm = llm_config.get_llm()

        return {"messages": [llm.invoke([self.agent_system_prompt] + state["messages"])]}