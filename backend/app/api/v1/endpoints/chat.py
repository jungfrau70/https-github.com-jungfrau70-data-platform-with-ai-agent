from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app.models.user import User
from app.models.chat import Conversation, ConversationCreate, Message, MessageCreate
from app.services.chat_service import chat_service

router = APIRouter()

@router.post("/conversations", response_model=Conversation)
async def create_conversation(
    *,
    conversation_in: ConversationCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Create a new conversation.
    """
    return await chat_service.create_conversation(current_user.email, conversation_in.title)

@router.get("/conversations", response_model=List[Conversation])
async def get_conversations(
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get all conversations for the current user.
    """
    return await chat_service.get_conversations(current_user.email)

@router.get("/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_messages(
    conversation_id: str,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get messages for a specific conversation.
    """
    # TODO: Verify user ownership
    return await chat_service.get_messages(conversation_id)

@router.post("/conversations/{conversation_id}/messages", response_model=Message)
async def send_message(
    conversation_id: str,
    message_in: MessageCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Send a message to the chatbot and get a response.
    """
    # 1. Save user message
    # TODO: Verify user ownership
    user_msg = await chat_service.add_message(conversation_id, message_in)
    
    # 2. Get AI response (Placeholder)
    ai_content = await chat_service.get_ai_response(conversation_id, message_in.content)
    
    # 3. Save AI message
    ai_msg_in = MessageCreate(role="assistant", content=ai_content)
    await chat_service.add_message(conversation_id, ai_msg_in)
    
    # Return user message (or AI message? - typically we might want stream or last msg)
    # For now, let's return the user message and letting frontend fetch history or receive stream
    # But usually API returns the response. Let's return the AI message for non-streaming.
    # To be perfect, we should wait and return the AI message.
    
    # Re-fetching for the proper ID/Timestamp
    # Actually, add_message returns the stored message object.
    # Let's return the AI message which is the response.
    
    ai_msg_stored = await chat_service.add_message(conversation_id, ai_msg_in)
    return ai_msg_stored
