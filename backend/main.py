# Step1: Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from .ai_agent import get_agent_response

app = FastAPI(title="SafeSpace AI Agent API", version="1.0.0")


@app.get("/")
async def root():
    return {
        "message": "Welcome to SafeSpace AI Agent API",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "ask": "/ask (POST)",
            "health": "/health (GET)"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "safespace-ai-agent"}


# Step2: Receive and validate request from Frontend

class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask(query: Query):
    try:
        print(f"\n{'='*50}")
        print(f"📥 Received message: {query.message}")
        print(f"{'='*50}\n")
        
        # Get response from agent
        result = get_agent_response(query.message)
        
        print(f"✅ Response: {result['response'][:100]}...")
        print(f"🔧 Tool called: {result['tool_called']}\n")
        
        # Step3: Send response to the frontend
        return {
            "response": result["response"],
            "tool_called": result["tool_called"]
        }
    except Exception as e:
        print(f"\n{'='*50}")
        print(f"❌ ERROR in /ask endpoint: {str(e)}")
        print(f"{'='*50}")
        import traceback
        traceback.print_exc()
        print(f"{'='*50}\n")
        return {
            "response": f"Sorry, I encountered an error: {str(e)}",
            "tool_called": "Error"
        }



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)