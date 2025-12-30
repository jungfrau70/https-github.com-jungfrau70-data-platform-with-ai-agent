import pytest
import pytest_asyncio
from app.core.agent_graph import agent_app
from langchain_core.messages import HumanMessage

@pytest.mark.asyncio
async def test_agent_graph_routing_general():
    """Test that general queries go to the general chat node."""
    response = await agent_app.ainvoke({"messages": [HumanMessage(content="Hello there")]})
    last_msg = response["messages"][-1].content
    assert "General Chat Agent" in last_msg

@pytest.mark.asyncio
async def test_agent_graph_routing_rag():
    """Test that data-related queries go to the RAG node."""
    response = await agent_app.ainvoke({"messages": [HumanMessage(content="Show me data analysis")]})
    last_msg = response["messages"][-1].content
    assert "RAG Agent" in last_msg
