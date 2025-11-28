from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None
    selected_text: str = None

@app.get("/")
async def read_root():
    return {"message": "RAG Chatbot API is running!"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # This will be replaced with actual RAG logic
    # For now, just echo the message
    response_message = f"You said: {request.message}"
    if request.selected_text:
        response_message += f"\n(Context from selected text: {request.selected_text[:50]}...)"
    return {"response": response_message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

