"""
Main entry point for SwarAI application.
Runs the FastAPI backend server.
"""
import uvicorn

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)