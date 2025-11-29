# RAG Chatbot API

This API provides a Retrieval Augmented Generation (RAG) chatbot that answers questions based on the content of the "Physical AI Humanoid Robotics Course Book". It uses Google's Gemini API for embeddings and text generation, and Qdrant as the vector database for storing and retrieving document chunks.

## Setup

### 1. Environment Variables

Create a `.env` file in the `rag_chatbot_api` directory with the following variables:

```
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
QDRANT_HOST="YOUR_QDRANT_HOST"
QDRANT_API_KEY="YOUR_QDRANT_API_KEY"
QDRANT_COLLECTION_NAME="book_content" # Optional, defaults to "book_content"
DATABASE_URL="postgresql+asyncpg://user:password@localhost/dbname" # Required for chat history storage
```

*   **`GOOGLE_API_KEY`**: Obtain this from Google AI Studio ([https://makersuite.google.com/k/api](https://makersuite.google.com/k/api)).
*   **`QDRANT_HOST`** and **`QDRANT_API_KEY`**: Obtain these from your Qdrant Cloud dashboard ([https://cloud.qdrant.io/](https://cloud.qdrant.io/)). You can use their free tier.
*   **`DATABASE_URL`**: PostgreSQL database connection string for storing chat history. Format: `postgresql+asyncpg://username:password@host:port/database_name`. You can use a local PostgreSQL instance or a cloud service.

### 2. Install Dependencies

Navigate to the `rag_chatbot_api` directory and install the required Python packages:

```bash
cd rag_chatbot_api
pip install -r requirements.txt
```

## Usage

### 1. Ingest Book Content

Before running the chatbot, you need to ingest the book's markdown content into the Qdrant database. Make sure you have your `.env` file configured.

Run the ingestion script from the `rag_chatbot_api` directory:

```bash
python ingest_data.py
```

This script will read the markdown files from `../my-book/docs`, chunk them, generate embeddings using the Gemini API, and store them in your Qdrant collection.

### 2. Start the API

Once the ingestion is complete, you can start the FastAPI application:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be running at `http://0.0.0.0:8000`.

### 3. Test the API

You can test the API using `curl` or any API client (like Postman or Insomnia).

**Endpoint**: `POST /chat`
**Headers**: `Content-Type: application/json`

**Example Request**:

```bash
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{
    "message": "What is kinematics?",
    "session_id": "user123"
}'
```

**Example Response**:

```json
{
    "response": "Kinematics is the branch of mechanics that describes the motion of points, bodies (objects), and systems of bodies without considering the forces that cause them to move. It is often described as the 'geometry of motion'."
}
```

You can also include `selected_text` in your request for additional context:

```bash
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{
    "message": "What is the main idea here?",
    "session_id": "user123",
    "selected_text": "Robotics is an interdisciplinary field that integrates computer science and engineering. Robotics involves the design, construction, operation, and use of robots."
}'
```

This will leverage the provided `selected_text` as additional context for the Gemini model to generate a more informed response.
