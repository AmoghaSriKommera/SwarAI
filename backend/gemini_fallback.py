"""
Gemini Pro fallback service for SwarAI.
Handles communication with Google's Gemini Pro API when Ollama is unavailable.
"""
import os
import time
import json
import requests
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variable
DEFAULT_API_KEYS = [key.strip() for key in os.getenv("GEMINI_API_KEYS", "").split(",") if key.strip()]


class GeminiFallbackError(Exception):
    """Exception raised when all Gemini API keys fail."""
    pass


def get_response(
    query: str, 
    api_keys: Optional[List[str]] = None,
    model: str = "gemini-pro"
) -> str:
    """
    Get response from Gemini Pro API.
    
    Args:
        query: The user's query
        api_keys: List of Gemini API keys to use (rotates if one fails)
        model: The model to use (default: gemini-pro)
        
    Returns:
        The response string
        
    Raises:
        GeminiFallbackError: If all API keys fail
    """
    # Use provided API keys or default from environment
    keys_to_try = api_keys if api_keys else DEFAULT_API_KEYS
    
    if not keys_to_try:
        raise GeminiFallbackError("No Gemini API keys available")
    
    errors = []
    
    # Try each API key until one works
    for api_key in keys_to_try:
        try:
            # Base URL for Gemini API
            base_url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent"
            
            # Prepare request headers and payload according to Gemini API docs
            headers = {
                "Content-Type": "application/json",
            }
            
            # Add API key as query parameter
            params = {
                "key": api_key
            }
            
            # Prepare request payload according to Gemini API docs
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": query
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }
            
            # Send request to Gemini API
            response = requests.post(
                base_url,
                headers=headers,
                params=params,
                json=payload,
                timeout=30
            )
            
            # Handle successful response
            if response.status_code == 200:
                result = response.json()
                
                # Extract text from response according to documented structure
                if (
                    "candidates" in result and 
                    len(result["candidates"]) > 0 and
                    "content" in result["candidates"][0] and
                    "parts" in result["candidates"][0]["content"] and
                    len(result["candidates"][0]["content"]["parts"]) > 0 and
                    "text" in result["candidates"][0]["content"]["parts"][0]
                ):
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    errors.append(f"Unexpected response structure: {json.dumps(result)}")
            else:
                errors.append(f"API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            errors.append(f"Exception: {str(e)}")
    
    # If we get here, all API keys failed
    error_message = "All Gemini API keys failed: " + "; ".join(errors)
    raise GeminiFallbackError(error_message)


def get_response_with_metadata(
    query: str,
    api_keys: Optional[List[str]] = None,
    model: str = "gemini-pro"
) -> Dict[str, Any]:
    """
    Get response from Gemini with metadata.
    
    Args:
        query: The user's query
        api_keys: List of Gemini API keys to use (rotates if one fails)
        model: The model to use (default: gemini-pro)
        
    Returns:
        Dictionary containing response text, source, and latency
    """
    start_time = time.time()
    response_text = None
    
    try:
        response_text = get_response(query, api_keys, model)
        return {
            "response": response_text,
            "source": "gemini",
            "latency_ms": int((time.time() - start_time) * 1000)
        }
    except GeminiFallbackError as e:
        print(f"Gemini Fallback Error: {str(e)}")
        return {
            "response": None,
            "source": "gemini",
            "latency_ms": int((time.time() - start_time) * 1000),
            "error": str(e)
        }