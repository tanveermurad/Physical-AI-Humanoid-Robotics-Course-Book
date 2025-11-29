import os
import asyncio
from pathlib import Path
from rag_core import embed_and_store_documents
from qdrant_client_config import get_qdrant_client
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Define the directory where your markdown files are located
    # Adjust this path as necessary for your Docusaurus docs
    DOCS_DIR = Path(__file__).parent.parent / "my-book" / "docs"
    
    if not DOCS_DIR.exists():
        print(f"Error: Documentation directory not found at {DOCS_DIR}")
        print("Please ensure 'my-book/docs' exists relative to the rag_chatbot_api directory.")
        return

    # Find all markdown files in the specified directory
    markdown_files = list(DOCS_DIR.glob("**/*.md"))
    markdown_file_paths = [str(f.resolve()) for f in markdown_files]

    if not markdown_file_paths:
        print(f"No markdown files found in {DOCS_DIR}. Please check the path and file extensions.")
        return
    
    print(f"Found {len(markdown_file_paths)} markdown files to ingest.")
    print("\n".join(markdown_file_paths))

    try:
        await embed_and_store_documents(markdown_file_paths)
        print("\nIngestion complete!")
    except Exception as e:
        print(f"\nAn error occurred during ingestion: {e}")

if __name__ == "__main__":
    # Ensure Qdrant is accessible before attempting ingestion
    try:
        client = get_qdrant_client()
        client.get_collections() # Try to connect to Qdrant
        print("Successfully connected to Qdrant.")
    except Exception as e:
        print(f"Failed to connect to Qdrant. Please check QDRANT_URL and QDRANT_API_KEY in your .env file: {e}")
        exit(1)

    asyncio.run(main())