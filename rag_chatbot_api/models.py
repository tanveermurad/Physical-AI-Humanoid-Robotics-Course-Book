from pydantic import BaseModel
from typing import List, Optional, Dict

class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[ChatMessage]] = None
    selected_text: Optional[str] = None  # Text selected from course content
    user_profile: Optional[Dict] = None  # User background for personalization
    user_id: Optional[str] = None  # User ID from Better Auth

class ChatResponse(BaseModel):
    response: str
    source_documents: List[str] = []
    chat_history: List[ChatMessage]

class IngestRequest(BaseModel):
    file_paths: List[str]

class IngestResponse(BaseModel):
    status: str
    details: str
