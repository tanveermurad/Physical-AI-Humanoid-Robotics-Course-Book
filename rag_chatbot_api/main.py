from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
from qdrant_client import QdrantClient, models
from rag_chatbot_api.qdrant_client_config import get_qdrant_client, get_qdrant_collection_name

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini generative model
GENERATIVE_MODEL = genai.GenerativeModel("gemini-pro") # Using gemini-pro for text generation
EMBEDDING_MODEL = "models/embedding-001" # Consistent with ingest_data.py

class ChatRequest(BaseModel):
    message: str
    session_id: str = None
    selected_text: str = None

@app.get("/")
async def read_root():
    return {"message": "RAG Chatbot API is running!"}

# Function to get embeddings using Gemini (duplicated from ingest_data.py for clarity/modularity)
def get_embedding(text: str) -> list[float]:
    response = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="RETRIEVAL_QUERY" # Task type for queries
    )
    return response['embedding']

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_query = request.message
    qdrant_client = get_qdrant_client()
    collection_name = get_qdrant_collection_name()

    # 1. Generate embedding for the user query
    query_embedding = get_embedding(user_query)

    # 2. Query Qdrant for relevant document chunks
    try:
        search_result = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=3 # Retrieve top 3 relevant chunks
        )
    except Exception as e:
        print(f"Error searching Qdrant: {e}")
        return {"response": "An error occurred while retrieving information. Please try again later."}

    context = []
    if search_result:
        for hit in search_result:
            context.append(hit.payload['content'])
    
    context_str = "\n".join(context)

    # 3. Construct a prompt for Gemini
    prompt_parts = [
        f"You are a helpful assistant that answers questions based on the provided book content. "
        f"If the answer is not in the context, clearly state that you don't have enough information. "
        f"Do not make up answers.\n\n"
        f"Context from book:\n{context_str}\n\n"
        f"Question: {user_query}\n\n"
        f"Answer:"
    ]

    # Add selected text as additional context if provided
    if request.selected_text:
        prompt_parts[0] += f"\n\nAdditional context from selected text:\n{request.selected_text}\n"

    # 4. Call the Gemini generative model
    try:
        response = GENERATIVE_MODEL.generate_content(prompt_parts)
        response_message = response.text
    except Exception as e:
        print(f"Error generating content with Gemini: {e}")
        response_message = "An error occurred while generating a response. Please try again later."

    return {"response": response_message}

if __name__ == "__main__":
    import uvicorn
    # A quick check for Google API key
    if not GOOGLE_API_KEY:
        print("Please set your GOOGLE_API_KEY environment variable.")
        print("You can get one from https://makersuite.google.com/k/api")
        exit(1)
        
    uvicorn.run(app, host="0.0.0.0", port=8000)

