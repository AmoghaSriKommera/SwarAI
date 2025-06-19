"""
Main FastAPI application for SwarAI.
Provides endpoints for interacting with hybrid AI system.
"""
import time
import os
import base64
import tempfile
from typing import Optional, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
import requests

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


class TranscriptionResponse(BaseModel):
    text: str
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
    # Create static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)


# Mount static files directory for PWA assets
app.mount("/static", StaticFiles(directory="static"), name="static")


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


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Transcribe audio using Whisper API.
    Accepts audio file and returns transcribed text.
    """
    start_time = time.time()
    
    # Check if WHISPER_API_KEY is set
    whisper_api_key = os.getenv("WHISPER_API_KEY")
    if not whisper_api_key:
        raise HTTPException(
            status_code=500,
            detail="WHISPER_API_KEY environment variable not set"
        )
    
    try:
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file_path = temp_file.name
            # Read and write in chunks to handle large files
            content = await audio.read()
            temp_file.write(content)
        
        # Send file to Whisper API
        headers = {
            "Authorization": f"Bearer {whisper_api_key}"
        }
        
        with open(temp_file_path, "rb") as audio_file:
            files = {
                "file": audio_file,
                "model": (None, "whisper-1"),
                "language": (None, "en")  # Optional, can be omitted for auto-detection
            }
            
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers=headers,
                files=files
            )
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        # Check response
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Whisper API error: {response.text}"
            )
        
        # Parse response
        transcription = response.json().get("text", "")
        
        # Calculate latency
        latency_ms = int((time.time() - start_time) * 1000)
        
        return {
            "text": transcription,
            "latency_ms": latency_ms
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription error: {str(e)}"
        )


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