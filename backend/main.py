"""
Main FastAPI application for SwarAI.
Provides endpoints for interacting with hybrid AI system.
"""
import time
from typing import Optional, Dict, Any
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .database import get_db, init_db
from .models import QueryLog
from . import ollama_helper
from . import gemini_fallback


# Request and response models
class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str
    source: str  # "ollama" or "gemini"
    latency_ms: int


# Create FastAPI application
app = FastAPI(
    title="SwarAI API",
    description="Voice-enabled AI assistant with hybrid LLM support",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()


# Main query endpoint
@app.post("/ask", response_model=QueryResponse)
async def ask(
    request: QueryRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Process a user query through the hybrid AI system.
    First tries local Ollama, then falls back to Gemini if needed.
    """
    start_time = time.time()
    query = request.query
    
    # Try Ollama first
    ollama_result = ollama_helper.get_response_with_metadata(query)
    
    # If Ollama fails, try Gemini
    if ollama_result["response"] is None:
        result = gemini_fallback.get_response_with_metadata(query)
    else:
        result = ollama_result
    
    # Calculate total latency
    total_latency_ms = int((time.time() - start_time) * 1000)
    
    # Return error if both services failed
    if result["response"] is None:
        raise HTTPException(
            status_code=503,
            detail="Both local and fallback AI services failed to respond"
        )
    
    # Log query to database
    log_entry = QueryLog(
        query=query,
        response=result["response"],
        source=result["source"],
        latency_ms=total_latency_ms
    )
    db.add(log_entry)
    db.commit()
    
    # Return response
    return {
        "response": result["response"],
        "source": result["source"],
        "latency_ms": total_latency_ms
    }


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    Returns status information about the API.
    """
    return {"status": "ok"}


# If run directly, start server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)