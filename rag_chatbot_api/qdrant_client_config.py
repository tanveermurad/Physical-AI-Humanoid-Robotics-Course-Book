import os
from qdrant_client import QdrantClient, models

# Retrieve Qdrant Cloud API Key and URL from environment variables
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

if not QDRANT_HOST or not QDRANT_API_KEY:
    print("WARNING: QDRANT_HOST and QDRANT_API_KEY environment variables must be set for Qdrant to function correctly.")
    print("Please obtain your credentials from Qdrant Cloud (Free Tier) and set them.")

qdrant_client = QdrantClient(
    host=QDRANT_HOST,
    api_key=QDRANT_API_KEY,
)

def get_qdrant_client():
    """Returns the initialized Qdrant client."""
    return qdrant_client

def get_qdrant_collection_name():
    """Returns the Qdrant collection name."""
    return QDRANT_COLLECTION_NAME

def create_collection_if_not_exists(client: QdrantClient, collection_name: str, vector_size: int = 1536):
    """
    Creates a Qdrant collection if it does not already exist.
    Assumes a vector size of 1536, typical for OpenAI's `text-embedding-ada-002`.
    """
    try:
        if not client.collection_exists(collection_name=collection_name):
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
            )
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")
    except Exception as e:
        print(f"Error managing collection '{collection_name}': {e}")
