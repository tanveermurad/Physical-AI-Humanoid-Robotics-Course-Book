# Dockerfile for FastAPI RAG Chatbot API

# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for asyncpg and psycopg2-binary
# These are necessary for connecting to PostgreSQL from Python
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY rag_chatbot_api/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY rag_chatbot_api/ ./rag_chatbot_api/

# Expose the port that FastAPI runs on
EXPOSE 8000

# Define environment variables
ENV PYTHONUNBUFFERED 1

# Run the Uvicorn server when the container starts
# Use gunicorn with uvicorn workers for production deployment
# CMD ["gunicorn", "rag_chatbot_api.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

# For development, you can use uvicorn directly (hot-reloads on code changes)
CMD ["uvicorn", "rag_chatbot_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
