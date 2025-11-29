from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    response: str
    source_documents: List[str] = []
    chat_history: List[ChatMessage]

class IngestRequest(BaseModel):
    file_paths: List[str]

class IngestResponse(BaseModel):
    status: str
    details: str
