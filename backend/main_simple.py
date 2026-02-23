# Minimal FastAPI to test deployment
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="SafeSpace AI Agent API", version="1.0.0")


@app.get("/")
async def root():
    return {
        "message": "Welcome to SafeSpace AI Agent API",
        "status": "running",
        "environment": "production"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/test")
async def test():
    """Test environment variables."""
    return {
        "groq_key_set": bool(os.getenv("GROQ_API_KEY")),
        "python_version": os.getenv("PYTHON_VERSION", "not set")
    }


class Query(BaseModel):
    message: str


@app.post("/ask")
async def ask(query: Query):
    """Simple echo endpoint for testing."""
    return {
        "response": f"Received your message: {query.message}",
        "tool_called": "None"
    }
