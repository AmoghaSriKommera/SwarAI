"""
Database models for SwarAI.
Defines SQLAlchemy models for storing query logs.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID

try:
    from .database import Base
except ImportError:
    from database import Base


class QueryLog(Base):
    """
    Model for storing query logs.
    Records user queries, AI responses, and metadata.
    """
    __tablename__ = "query_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    source = Column(String(50), nullable=False)  # "ollama" or "gemini"
    latency_ms = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<QueryLog(id={self.id}, source={self.source}, latency_ms={self.latency_ms})>"
    
    def to_dict(self):
        """
        Convert model to dictionary.
        Returns a dictionary representation of the model.
        """
        return {
            "id": str(self.id),
            "timestamp": self.timestamp.isoformat(),
            "query": self.query,
            "response": self.response,
            "source": self.source,
            "latency_ms": self.latency_ms
        }