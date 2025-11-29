import os
import glob
from dotenv import load_dotenv
import google.generativeai as genai
from qdrant_client import QdrantClient, models
import re

# Load environment variables from .env file
load_dotenv()

# Initialize Google Generative AI client
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

genai.configure(api_key=GOOGLE_API_KEY)
# Using "models/embedding-001" as it is commonly available and has a dimension of 768
EMBEDDING_MODEL = "models/embedding-001"
EMBEDDING_DIMENSION = 768 

# Initialize Qdrant client
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

if not QDRANT_HOST or not QDRANT_API_KEY:
    raise ValueError("QDRANT_HOST and QDRANT_API_KEY environment variables not set.")

qdrant_client = QdrantClient(
    host=QDRANT_HOST,
    api_key=QDRANT_API_KEY,
)

# Function to create Qdrant collection
def create_collection_if_not_exists(client: QdrantClient, collection_name: str, vector_size: int):
    try:
        if not client.collection_exists(collection_name=collection_name):
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=vector_size, distance=models.COSINE),
            )
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")
    except Exception as e:
        print(f"Error managing collection '{collection_name}': {e}")

# Function to get embeddings using Gemini
def get_embedding(text: str) -> list[float]:
    response = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embedding']

# Function to chunk text (character-based)
def chunk_text(text: str, max_chars: int = 1000, overlap_chars: int = 100) -> list[str]:
    chunks = []
    current_position = 0
    while current_position < len(text):
        end_position = min(current_position + max_chars, len(text))
        chunk = text[current_position:end_position]
        
        # Try to break at a sentence boundary if possible
        if end_position < len(text):
            # Look for last period, question mark, or exclamation mark
            sentence_ends = [chunk.rfind('.'), chunk.rfind('?'), chunk.rfind('!')]
            max_sentence_end = max(sentence_ends)
            if max_sentence_end > -1 and len(chunk) - max_sentence_end < (max_chars / 4): # If sentence end is not too far back
                chunk = chunk[:max_sentence_end + 1]

        chunks.append(chunk)
        current_position += len(chunk) - overlap_chars
        if current_position < 0: # Ensure current_position doesn't go negative
            current_position = 0
    return chunks

# Function to extract title from markdown content
def extract_title_and_clean_markdown(markdown_content: str):
    # Extract title from YAML front matter or first heading
    title_match = re.search(r'^---\s*\n(?:sidebar_position:\s*\d+\s*\n)?title:\s*(.*?)\s*\n---\s*\n', markdown_content, re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
        # Remove YAML front matter
        content_without_frontmatter = re.sub(r'^---\s*\n(?:sidebar_position:\s*\d+\s*\n)?title:\s*(.*?)\s*\n---\s*\n', '', markdown_content, 1, re.DOTALL)
    else:
        # Fallback to first H1 as title if no front matter
        h1_match = re.search(r'^#\s*(.*)', markdown_content, re.MULTILINE)
        title = h1_match.group(1).strip() if h1_match else "Untitled Document"
        content_without_frontmatter = markdown_content

    # Remove markdown formatting for embedding
    cleaned_content = re.sub(r'#+\s*', '', content_without_frontmatter) # Remove headings
    cleaned_content = re.sub(r'\[(.*?)\]\(.*?\)','\g<1>', cleaned_content) # Remove links, keep text
    cleaned_content = re.sub(r'\*\*(.*?)\*\*','\g<1>', cleaned_content) # Remove bold
    cleaned_content = re.sub(r'_(.*?)_','\g<1>', cleaned_content) # Remove italics
    cleaned_content = re.sub(r'`(.*?)`','\g<1>', cleaned_content) # Remove inline code
    cleaned_content = re.sub(r'```.*?```', '', cleaned_content, flags=re.DOTALL) # Remove code blocks
    cleaned_content = re.sub(r'---', '', cleaned_content) # Remove horizontal rules
    cleaned_content = re.sub(r'[ \t]*\n[ \t]*\n+', '\n\n', cleaned_content) # Reduce multiple newlines
    cleaned_content = cleaned_content.strip()

    return title, cleaned_content

def ingest_documents(docs_path: str = "my-book/docs"):
    create_collection_if_not_exists(qdrant_client, QDRANT_COLLECTION_NAME, EMBEDDING_DIMENSION)

    markdown_files = glob.glob(f"{docs_path}/**/*.md", recursive=True)
    points = []
    point_id = 0

    print(f"Found {len(markdown_files)} markdown files. Starting ingestion...")

    for file_path in markdown_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        title, cleaned_content = extract_title_and_clean_markdown(content)
        
        # Exclude very short or empty content
        if not cleaned_content or len(cleaned_content.strip()) < 50:
            print(f"Skipping {file_path} due to insufficient content after cleaning.")
            continue

        chunks = chunk_text(cleaned_content)
        
        print(f"Processing '{title}' from {file_path} into {len(chunks)} chunks.")

        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            payload = {
                "file_path": file_path,
                "title": title,
                "chunk_number": i + 1,
                "content": chunk
            }
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload,
                )
            )
            point_id += 1
            
            # Upsert in batches to avoid rate limits and improve performance
            if len(points) >= 100:
                qdrant_client.upsert(
                    collection_name=QDRANT_COLLECTION_NAME,
                    wait=True,
                    points=points
                )
                points = []
                print(f"Upserted {point_id} points so far.")
    
    # Upsert any remaining points
    if points:
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            wait=True,
            points=points
        )
        print(f"Upserted final {len(points)} points. Total points: {point_id}")
    
    print("Ingestion complete.")

if __name__ == "__main__":
    # Ensure the current working directory is the project root
    # so that 'my-book/docs' path is correct
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # For this setup, we assume the script is run from the project root or adjust docs_path accordingly
    
    # A quick check for Google API key
    if not GOOGLE_API_KEY:
        print("Please set your GOOGLE_API_KEY environment variable.")
        print("You can get one from https://makersuite.google.com/k/api")
        exit(1)
        
    # A quick check for Qdrant credentials
    if not QDRANT_HOST or not QDRANT_API_KEY:
        print("Please set your QDRANT_HOST and QDRANT_API_KEY environment variables.")
        print("You can get them from your Qdrant Cloud dashboard (https://cloud.qdrant.io/).")
        exit(1)

    ingest_documents()
