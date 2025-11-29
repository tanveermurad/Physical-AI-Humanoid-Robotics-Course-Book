import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import uuid

from models import ChatRequest, ChatResponse, IngestRequest, IngestResponse, ChatMessage
from rag_core import get_conversational_rag_chain, embed_and_store_documents, format_chat_history_for_langchain
from qdrant_client_config import get_qdrant_client
from database import init_db, get_db, ChatHistory
from openai_agent import chat_with_agent, format_chat_history_for_agent

load_dotenv()

app = FastAPI(
    title="RAG Chatbot API",
    description="API for a RAG chatbot powered by Qdrant, OpenAI/Gemini, and FastAPI.",
    version="0.1.0",
)

# --- CORS Configuration ---
# Allow all origins for development. In production, restrict this.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust this to your frontend's origin in production, e.g., ["http://localhost:3000", "https://your-docusaurus-site.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Event Handlers ---
@app.on_event("startup")
async def on_startup():
    print("Initializing database...")
    await init_db()
    print("Database initialized.")

# --- Dependencies ---
def get_qdrant_client_dependency() -> QdrantClient:
    return get_qdrant_client()

# --- Endpoints ---

@app.post("/embed", response_model=IngestResponse)
async def embed_documents(
    request: IngestRequest,
    qdrant_client: QdrantClient = Depends(get_qdrant_client_dependency)
):
    """
    Ingests a list of markdown files, chunks them, embeds them, and stores them in Qdrant.
    This endpoint will recreate the Qdrant collection on each call.
    """
    if not request.file_paths:
        raise HTTPException(status_code=400, detail="No file paths provided for ingestion.")
    
    try:
        await embed_and_store_documents(request.file_paths)
        return IngestResponse(status="success", details=f"Successfully ingested {len(request.file_paths)} files.")
    except Exception as e:
        print(f"Error during embedding: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to embed documents: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Answers a question using OpenAI Agents with Qdrant retrieval,
    incorporating chat history and user personalization.
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        # Generate session_id (use user_id if available, otherwise UUID)
        session_id = request.user_id or str(uuid.uuid4())

        # Format chat history for OpenAI agent
        formatted_chat_history = format_chat_history_for_agent(request.chat_history or [])

        # Call OpenAI agent with personalization and selected text
        result = await chat_with_agent(
            message=request.message,
            selected_text=request.selected_text,
            user_profile=request.user_profile,
            chat_history=formatted_chat_history
        )

        assistant_response = result["response"]
        source_documents = result["sources"]
        tool_calls = result["tool_calls"]

        # Store chat history in the database (Neon Postgres)
        new_chat_entry = ChatHistory(
            session_id=session_id,
            user_id=request.user_id,
            user_message=request.message,
            assistant_message=assistant_response,
            selected_text=request.selected_text,
            metadata={
                "sources": source_documents,
                "tool_calls": tool_calls,
                "user_profile": request.user_profile
            }
        )
        db.add(new_chat_entry)
        await db.commit()
        await db.refresh(new_chat_entry)

        # Update chat history for the response
        updated_chat_history = request.chat_history or []
        updated_chat_history.append(ChatMessage(role="user", content=request.message))
        updated_chat_history.append(ChatMessage(role="assistant", content=assistant_response))

        return ChatResponse(
            response=assistant_response,
            source_documents=source_documents,
            chat_history=updated_chat_history
        )
    except Exception as e:
        print(f"Error during chat: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred while processing your request: {str(e)}")

# --- Run the application (for development) ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)