import operator
from typing import Annotated, TypedDict, Union, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from app.core.logger import get_logger

logger = get_logger(__name__)

# Define the state of the graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_step: str

# Define nodes/agents
async def router_node(state: AgentState):
    """
    Decides whether to route to general chat or RAG based on the last message.
    """
    last_message = state["messages"][-1].content.lower()
    logger.info(f"Router received message: {last_message}")
    
    # Simple keyword-based routing for demonstration
    if any(keyword in last_message for keyword in ["analysis", "data", "report", "context", "search"]):
        logger.info("Routing to RAG node")
        return {"next_step": "rag"}
    else:
        logger.info("Routing to General Chat node")
        return {"next_step": "general"}

async def general_chat_node(state: AgentState):
    """
    Handles general conversation.
    """
    logger.info("General Chat Node Executing")
    last_user_msg = state["messages"][-1].content
    response = AIMessage(content=f"General Chat Agent: I received your message '{last_user_msg}'. How can I help you today?")
    return {"messages": [response]}

async def rag_node(state: AgentState):
    """
    Handles knowledge retrieval queries.
    """
    logger.info("RAG Node Executing")
    last_user_msg = state["messages"][-1].content
    response = AIMessage(content=f"RAG Agent: I am searching the knowledge base for '{last_user_msg}'... [Market data would appear here]")
    return {"messages": [response]}

# Define the routing logic
def route_step(state: AgentState):
    if state["next_step"] == "rag":
        return "rag_node"
    return "general_chat_node"

# Build the graph
def build_agent_graph():
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("general_chat_node", general_chat_node)
    workflow.add_node("rag_node", rag_node)

    # Set entry point
    workflow.set_entry_point("router")

    # Add conditional edges
    workflow.add_conditional_edges(
        "router",
        route_step,
        {
            "general_chat_node": "general_chat_node",
            "rag_node": "rag_node"
        }
    )

    # Add edges to END
    workflow.add_edge("general_chat_node", END)
    workflow.add_edge("rag_node", END)

    return workflow.compile()

agent_app = build_agent_graph()
