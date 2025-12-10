from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    role: str # user, assistant, system
    content: str
    
class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: str
    timestamp: datetime

class ConversationCreate(BaseModel):
    title: Optional[str] = "New Chat"

class Conversation(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []
