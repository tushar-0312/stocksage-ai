from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

from core import ModelLoader
from tools import all_tools
from agent.prompts import TRADING_SYSTEM_PROMPT


class AgentState(TypedDict):
    """State schema for the trading agent."""
    messages: Annotated[list, add_messages]


class TradingAgent:
    """LangGraph-based trading assistant agent."""
    
    def __init__(self):
        self.model_loader = ModelLoader()
        self.llm = self.model_loader.load_llm()
        self.tools = all_tools
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.graph = None
    
    def _chatbot_node(self, state: AgentState) -> dict:
        """Process user message and generate response."""
        messages = state["messages"]
        
        # Add system prompt if this is the first message
        if len(messages) == 1:
            messages = [SystemMessage(content=TRADING_SYSTEM_PROMPT)] + messages
        
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def build(self) -> None:
        """Build the LangGraph workflow."""
        graph_builder = StateGraph(AgentState)
        
        # Add nodes
        graph_builder.add_node("chatbot", self._chatbot_node)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        
        # Add edges
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        
        self.graph = graph_builder.compile()
    
    def get_graph(self):
        """Get the compiled graph."""
        if self.graph is None:
            raise ValueError("Graph not built. Call build() first.")
        return self.graph


# Backwards compatibility alias
GraphBuilder = TradingAgent
