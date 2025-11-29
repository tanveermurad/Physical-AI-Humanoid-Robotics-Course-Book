import os
from typing import List, Tuple
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Distance, VectorParams
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from qdrant_client_config import get_qdrant_client, recreate_qdrant_collection, QDRANT_COLLECTION_NAME
from models import ChatMessage
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "openai") # or "gemini"
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "openai") # or "gemini"

if EMBEDDING_MODEL_NAME == "openai" and not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be set for OpenAI embeddings.")
if EMBEDDING_MODEL_NAME == "gemini" and not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY must be set for Gemini embeddings.")
if LLM_MODEL_NAME == "openai" and not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be set for OpenAI LLM.")
if LLM_MODEL_NAME == "gemini" and not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY must be set for Gemini LLM.")

# --- Initialize Embeddings and LLMs ---
def get_embeddings_model():
    if EMBEDDING_MODEL_NAME == "openai":
        return OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
    elif EMBEDDING_MODEL_NAME == "gemini":
        return GoogleGenerativeAIEmbeddings(google_api_key=GOOGLE_API_KEY, model="models/embedding-001")
    else:
        raise ValueError(f"Unsupported embedding model: {EMBEDDING_MODEL_NAME}")

def get_llm_model():
    if LLM_MODEL_NAME == "openai":
        return ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.3)
    elif LLM_MODEL_NAME == "gemini":
        return ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-pro", temperature=0.3)
    else:
        raise ValueError(f"Unsupported LLM model: {LLM_MODEL_NAME}")

embeddings = get_embeddings_model()
llm = get_llm_model()

# Determine vector size based on the embedding model chosen
if EMBEDDING_MODEL_NAME == "openai":
    VECTOR_SIZE = 1536  # OpenAI text-embedding-ada-002 output dimension
elif EMBEDDING_MODEL_NAME == "gemini":
    VECTOR_SIZE = 768   # Gemini embedding-001 output dimension
else:
    raise ValueError(f"Unknown vector size for embedding model: {EMBEDDING_MODEL_NAME}")


# --- Document Processing ---
def load_and_split_markdown(file_path: str) -> List[Document]:
    """
    Loads a markdown file and splits it into chunks.
    """
    loader = UnstructuredMarkdownLoader(file_path)
    documents = loader.load()

    # Using RecursiveCharacterTextSplitter for more general chunking,
    # but MarkdownTextSplitter can be considered for stricter markdown structure.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    # Alternatively for markdown specific splitting:
    # text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)

    chunks = text_splitter.split_documents(documents)
    return chunks

async def embed_and_store_documents(file_paths: List[str]):
    """
    Loads, splits, embeds documents, and stores them in Qdrant.
    """
    client = get_qdrant_client()
    recreate_qdrant_collection(client, VECTOR_SIZE) # Recreate for fresh ingestion

    all_chunks: List[Document] = []
    for file_path in file_paths:
        print(f"Processing {file_path}...")
        chunks = load_and_split_markdown(file_path)
        all_chunks.extend(chunks)

    if not all_chunks:
        print("No chunks to embed and store.")
        return

    # Generate embeddings
    print(f"Generating {len(all_chunks)} embeddings...")
    texts = [chunk.page_content for chunk in all_chunks]
    metadatas = [chunk.metadata for chunk in all_chunks]
    
    # Langchain's embeddings.embed_documents handles batching
    vectors = embeddings.embed_documents(texts)
    
    points = []
    for i, vector in enumerate(vectors):
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={"content": texts[i], **metadatas[i]},
            )
        )
    
    print(f"Uploading {len(points)} points to Qdrant...")
    client.upsert(
        collection_name=QDRANT_COLLECTION_NAME,
        wait=True,
        points=points,
    )
    print("Documents embedded and stored in Qdrant.")

# --- RAG Chain ---
def get_conversational_rag_chain(qdrant_client: QdrantClient):
    """
    Creates and returns a conversational RAG chain.
    """
    # Create a retriever
    # We need to adapt the Qdrant client to work as a Langchain retriever
    # Qdrant client directly does not have .as_retriever(), so we create a custom one or use existing integration
    from langchain_qdrant import QdrantVectorStore
    
    vectorstore = QdrantVectorStore(
        client=qdrant_client,
        collection_name=QDRANT_COLLECTION_NAME,
        embeddings=embeddings,
        content_payload_key="content" # This is important to tell QdrantVectorStore where the text content is
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5}) # Retrieve top 5 relevant documents

    # Contextualize question prompt
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood without "
        "the chat history. Do NOT answer the question, just reformulate "
        "it if necessary and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # Answer question prompt
    qa_system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don\'t know the answer, just say that you don\'t know. "
        "Keep the answer concise and relevant to the book content. "
        "Do not make up information. "
        "Ensure your answer is directly supported by the provided context. "
        "If the question is outside the scope of the provided context, "
        "politely state that you can only answer questions based on the book content. \n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    document_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    # This chain will retrieve relevant documents and then pass them to the LLM
    rag_chain = create_retrieval_chain(history_aware_retriever, document_chain)

    return rag_chain

def format_chat_history_for_langchain(chat_history: List[ChatMessage]) -> List[Tuple[str, str]]:
    """
    Converts the Pydantic ChatMessage list to Langchain's expected format.
    """
    formatted_history = []
    for message in chat_history:
        if message.role == "user":
            formatted_history.append(HumanMessage(content=message.content))
        elif message.role == "assistant":
            formatted_history.append(AIMessage(content=message.content))
    return formatted_history

if __name__ == "__main__":
    # Example usage for ingestion (run this script directly to test ingestion)
    # Assumes you have some markdown files in 'my-book/docs'
    # and QDRANT_URL, QDRANT_API_KEY, OPENAI_API_KEY/GOOGLE_API_KEY set in .env
    
    # You would typically call this from ingest_data.py
    # from pathlib import Path
    # markdown_files = list(Path("../../my-book/docs").glob("**/*.md"))
    # markdown_file_paths = [str(f) for f in markdown_files]
    # import asyncio
    # asyncio.run(embed_and_store_documents(markdown_file_paths))

    print("rag_core.py loaded. For ingestion, run ingest_data.py after setting up your .env file.")
    print("For chat, use the FastAPI application in main.py.")
