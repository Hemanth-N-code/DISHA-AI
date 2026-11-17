# backend/app/schemas/chat.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatMessage(BaseModel):
    role: Optional[str] = "user"  # user | assistant | system
    content: Optional[str] = ""
    sender: Optional[str] = None
    text: Optional[str] = None

    class Config:
        extra = "ignore"

class ChatRequest(BaseModel):
    message: str
    career_context_id: Optional[str] = None
    conversation_history: Optional[List[Dict[str, Any]]] = []

class ChatResponse(BaseModel):
    reply: str
    suggested_actions: List[str] = []
    grounded_career_sources: List[str] = []
    what_if_trigger: Optional[Dict[str, Any]] = None
