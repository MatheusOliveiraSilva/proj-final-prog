from agent.nodes import AgentNodes
from agent.states import AgentState
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from agent.agent_toolbox.toolbox import TOOLS

class Agent:
    def __init__(self):
        self.nodes = AgentNodes()
        self.graph: CompiledStateGraph = self.build_graph(self.nodes)
    
    def build_graph(self, nodes: AgentNodes) -> CompiledStateGraph:
        graph = StateGraph(AgentState)

        graph.add_node("agent", nodes.agent_node)
        graph.add_node("tools", ToolNode(TOOLS))

        graph.add_edge(START, "agent")  # 1.Início do grafo, vai para o agente
        graph.add_conditional_edges("agent", tools_condition)  # 2. Usa uma ferramenta ou responde o usuário
        graph.add_edge("tools", "agent")  # 3. Volta para o agente (passo 2)
        
        return graph.compile()
    
    def run_agent(self, agent_input: AgentState) -> AgentState:
        return self.graph.invoke(agent_input)
    
    def run_agent_streaming(self, agent_input: AgentState):
        for data in self.graph.stream(
            agent_input,
            stream_mode="messages"
        ):
    
            yield f"data: {data}\n\n"

