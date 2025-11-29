import asyncio
from pathlib import Path
from rag_core import embed_and_store_documents

async def main():
    print("Starting data ingestion...")
    
    # Adjust this path to where your markdown documents are located relative to this script
    # This assumes ingest_data.py is in rag_chatbot_api/ and docs are in my-book/docs/
    docs_path = Path(__file__).parent.parent / "my-book" / "docs"
    
    if not docs_path.is_dir():
        print(f"Error: Document path not found: {docs_path}")
        print("Please ensure 'my-book/docs' exists and contains markdown files.")
        return

    markdown_files = list(docs_path.glob("**/*.md"))
    markdown_file_paths = [str(f) for f in markdown_files]

    if not markdown_file_paths:
        print(f"No markdown files found in {docs_path}. Please add some .md files to ingest.")
        return

    print(f"Found {len(markdown_file_paths)} markdown files to ingest.")
    for f in markdown_file_paths:
        print(f"- {f}")

    try:
        await embed_and_store_documents(markdown_file_paths)
        print("Data ingestion completed successfully.")
    except Exception as e:
        print(f"Data ingestion failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
