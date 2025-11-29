import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Text, DateTime, func, JSON
from sqlalchemy.dialects.postgresql import JSONB
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in environment variables for chat history.")

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=True)  # Link to Better Auth user
    user_message = Column(Text, nullable=False)
    assistant_message = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)  # For text selection feature
    metadata = Column(JSON, nullable=True)  # Store sources, tool calls, etc.
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ChatHistory(session_id='{self.session_id}', user_id='{self.user_id}', user_message='{self.user_message[:50]}...')>"

# Create engine with connection pooling for Neon Postgres
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,          # Max connections in pool
    max_overflow=10,      # Extra connections if pool full
    pool_recycle=3600,    # Recycle connections after 1 hour
)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
