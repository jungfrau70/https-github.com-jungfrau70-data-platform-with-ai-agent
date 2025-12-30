import uuid
from datetime import datetime
from typing import List
from app.db.neo4j import neo4j_driver
from app.models.chat import MessageCreate, Message, Conversation
from app.core.logger import get_logger

logger = get_logger(__name__)

class ChatService:
    async def create_conversation(self, user_email: str, title: str) -> Conversation:
        logger.info(f"Creating conversation for {user_email} with title: {title}")
        conversation_id = str(uuid.uuid4())
        now = datetime.now()
        
        query = """
        MATCH (u:User {email: $email})
        CREATE (c:Conversation {id: $id, title: $title, created_at: $now, updated_at: $now})
        CREATE (u)-[:HAS_CHAT]->(c)
        RETURN c
        """
        
        async with neo4j_driver.driver.session() as session:
            result = await session.run(query, email=user_email, id=conversation_id, title=title, now=now)
            record = await result.single()
            node = record["c"]
            return Conversation(
                id=node["id"],
                title=node["title"],
                created_at=node["created_at"].to_native(),
                updated_at=node["updated_at"].to_native(),
                messages=[]
            )

    async def add_message(self, conversation_id: str, message: MessageCreate) -> Message:
        message_id = str(uuid.uuid4())
        now = datetime.now()
        
        query = """
        MATCH (c:Conversation {id: $cid})
        CREATE (m:Message {id: $mid, role: $role, content: $content, timestamp: $now})
        CREATE (c)-[:HAS_MESSAGE]->(m)
        RETURN m
        """
        
        async with neo4j_driver.driver.session() as session:
            result = await session.run(query, cid=conversation_id, mid=message_id, role=message.role, content=message.content, now=now)
            record = await result.single()
            node = record["m"]
            return Message(
                id=node["id"],
                role=node["role"],
                content=node["content"],
                timestamp=node["timestamp"].to_native()
            )

    async def get_conversations(self, user_email: str) -> List[Conversation]:
        query = """
        MATCH (u:User {email: $email})-[:HAS_CHAT]->(c:Conversation)
        RETURN c
        ORDER BY c.updated_at DESC
        """
        async with neo4j_driver.driver.session() as session:
            result = await session.run(query, email=user_email)
            conversations = []
            async for record in result:
                node = record["c"]
                conversations.append(Conversation(
                    id=node["id"],
                    title=node["title"],
                    created_at=node["created_at"].to_native(),
                    updated_at=node["updated_at"].to_native(),
                    messages=[] # Messages can be fetched lazily or separately
                ))
            return conversations

    async def get_messages(self, conversation_id: str) -> List[Message]:
        query = """
        MATCH (c:Conversation {id: $cid})-[:HAS_MESSAGE]->(m:Message)
        RETURN m
        ORDER BY m.timestamp ASC
        """
        async with neo4j_driver.driver.session() as session:
            result = await session.run(query, cid=conversation_id)
            messages = []
            async for record in result:
                node = record["m"]
                messages.append(Message(
                    id=node["id"],
                    role=node["role"],
                    content=node["content"],
                    timestamp=node["timestamp"].to_native()
                ))
            return messages

    # Placeholder for RAG/LLM logic
    async def get_ai_response(self, conversation_id: str, user_message: str) -> str:
        from app.core.agent_graph import agent_app
        from langchain_core.messages import HumanMessage
        
        # Invoke the graph with the user message
        logger.info(f"Invoking Agent Graph for conversation {conversation_id}")
        try:
            result = await agent_app.ainvoke({
                "messages": [HumanMessage(content=user_message)]
            })
            
            # Extract the final response
            last_message = result["messages"][-1]
            logger.info(f"Agent Graph returned response: {last_message.content[:50]}...")
            return last_message.content
        except Exception as e:
            logger.error(f"Error invoking Agent Graph: {e}", exc_info=True)
            return "Sorry, I encountered an error processing your request."

chat_service = ChatService()
