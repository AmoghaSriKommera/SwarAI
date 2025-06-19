"""
Ollama helper for SwarAI.
Handles communication with local Ollama server running LLaMA 3.2.
"""
import time
import json
import requests
from typing import Optional, Dict, Any


def get_response(query: str, model: str = "llama3.2") -> Optional[str]:
    """
    Get response from Ollama.
    
    Args:
        query: The user's query
        model: The model to use (default: llama3.2)
        
    Returns:
        The response string or None if an error occurs
    """
    start_time = time.time()
    
    try:
        # Prepare request payload
        payload = {
            "model": model,
            "prompt": query,
            "stream": False  # As per requirements, do not use streaming
        }
        
        # Send request to Ollama API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=60  # 60 second timeout
        )
        
        # Check for successful response
        if response.status_code == 200:
            result = response.json()
            return result.get("response")
        else:
            print(f"Error from Ollama API: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        # Log any exceptions but don't crash
        print(f"Exception when calling Ollama API: {str(e)}")
        return None
    finally:
        # Log latency for monitoring purposes
        latency = int((time.time() - start_time) * 1000)  # Convert to milliseconds
        print(f"Ollama API latency: {latency}ms")


def get_response_with_metadata(query: str, model: str = "llama3.2") -> Dict[str, Any]:
    """
    Get response from Ollama with metadata.
    
    Args:
        query: The user's query
        model: The model to use (default: llama3.2)
        
    Returns:
        Dictionary containing response text, source, and latency
    """
    start_time = time.time()
    response_text = None
    
    try:
        response_text = get_response(query, model)
    finally:
        latency = int((time.time() - start_time) * 1000)  # Convert to milliseconds
        
    return {
        "response": response_text,
        "source": "ollama",
        "latency_ms": latency
    }