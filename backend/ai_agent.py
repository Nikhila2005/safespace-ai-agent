from .tools import query_medgemma, call_emergency, find_nearby_therapists
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from .config import GROQ_API_KEY
import re


# --------------- LLM -------------------

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY,
    temperature=0.2,
)


# --------------- SYSTEM PROMPT -------------------

SYSTEM_PROMPT = """
You are a mental health AI assistant. You MUST follow these rules EXACTLY:

1. If the user expresses emotional distress (sad, depressed, anxious, hopeless, crying, overwhelmed, stressed, worried, scared):
   → You MUST respond with ONLY this text: "USE_TOOL: ask_mental_health_specialist"
   → Do NOT add any other text. Just that exact phrase.

2. If the user mentions self-harm or suicide:
   → You MUST respond with ONLY: "USE_TOOL: emergency_call_tool"

3. If the user asks to find therapists or counselors (with or without specifying location):
   → If they specify a location: "USE_TOOL: find_nearby_therapists_by_location [location]"
   → If NO location specified: "USE_TOOL: find_nearby_therapists_by_location"
   → Examples: "find therapists", "I need a counselor", "find therapists near me"

4. For greetings or casual conversation (hello, hi, how are you, what's up):
   → Respond normally with a warm greeting.

EXAMPLES:
User: "I am sad"
You: "USE_TOOL: ask_mental_health_specialist"

User: "I feel depressed"
You: "USE_TOOL: ask_mental_health_specialist"

User: "Find therapists near me"
You: "USE_TOOL: find_nearby_therapists_by_location"

User: "I need a therapist"
You: "USE_TOOL: find_nearby_therapists_by_location"

User: "Find therapists in New York"
You: "USE_TOOL: find_nearby_therapists_by_location [New York]"

User: "Hello"
You: "Hello! I'm here to support you. How are you feeling today?"

CRITICAL: When you detect emotional distress or therapist search, you MUST output the tool marker. Do NOT have a conversation first.
"""


# ---------------------- AGENT LOGIC ----------------------

def get_agent_response(user_input: str) -> dict:
    """
    Get response from the agent for a given user input.
    Returns a dict with 'response' and 'tool_called'.
    """
    try:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_input)
        ]
        
        # Get initial response from LLM
        response = llm.invoke(messages)
        response_text = response.content
        
        print(f"🤖 LLM Response: {response_text}")
        
        tool_called = "None"
        final_response = response_text
        
        # Check if LLM wants to use a tool (manual detection)
        if "USE_TOOL: ask_mental_health_specialist" in response_text:
            print(f"🔧 Detected tool call: ask_mental_health_specialist")
            tool_called = "ask_mental_health_specialist"
            # Call MedGemma
            tool_result = query_medgemma(user_input)
            final_response = tool_result
            
        elif "USE_TOOL: emergency_call_tool" in response_text:
            print(f"🔧 Detected tool call: emergency_call_tool")
            tool_called = "emergency_call_tool"
            call_emergency()
            final_response = "I've immediately contacted emergency services. Please stay safe. Help is on the way. If you're in immediate danger, please call your local emergency number (911 in the US, 112 in Europe, etc.)."
            
        elif "USE_TOOL: find_nearby_therapists_by_location" in response_text:
            print(f"🔧 Detected tool call: find_nearby_therapists_by_location")
            tool_called = "find_nearby_therapists_by_location"
            
            # Try to extract location from LLM response first
            location_match = re.search(r'find_nearby_therapists_by_location\s+\[(.+?)\]', response_text)
            
            if location_match:
                location = location_match.group(1)
            else:
                # Extract location from user input
                # Look for patterns like "near X", "in X", "at X", "around X"
                location_patterns = [
                    r'(?:near|in|at|around|for)\s+([A-Za-z\s,]+?)(?:\s+(?:please|pls|thanks|thank you|\.|\?|$))',
                    r'(?:near|in|at|around|for)\s+([A-Za-z\s,]+)',
                    r'therapists?\s+(?:near|in|at|around)\s+([A-Za-z\s,]+)',
                    r'(?:find|show|get|search)\s+.*?(?:near|in|at|around)\s+([A-Za-z\s,]+)',
                ]
                
                location = None
                for pattern in location_patterns:
                    match = re.search(pattern, user_input, re.IGNORECASE)
                    if match:
                        location = match.group(1).strip()
                        # Clean up common words at the end
                        location = re.sub(r'\s+(please|pls|thanks|thank you)$', '', location, flags=re.IGNORECASE)
                        break
                
                # If no location found, pass None for auto-detection
                if not location:
                    location = None
                    print(f"📍 No location specified - will use auto-detection")
                else:
                    print(f"📍 Extracted location: {location}")
            
            # Call the actual function to find therapists
            tool_result = find_nearby_therapists(location)
            final_response = tool_result

        
        return {
            "response": final_response,
            "tool_called": tool_called
        }
        
    except Exception as e:
        print(f"❌ Error in get_agent_response: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "response": f"I'm here to support you. While I'm having some technical difficulties, please know that your feelings are valid. Would you like to tell me more about what you're going through?",
            "tool_called": "Error"
        }


# ---------------------- CLI LOOP ----------------------

if __name__ == "__main__":
    print("AI Mental Health Agent (CLI Mode)")
    print("Type 'exit' or 'quit' to end the session.\n")
    while True:
        try:
            user_input = input("User: ")
            if user_input.strip().lower() in ['exit', 'quit']:
                print("Goodbye! Take care.")
                break
            if not user_input.strip():
                continue
            
            result = get_agent_response(user_input)
            
            print(f"🔧 Tool Called: {result['tool_called']}")
            print(f"Agent: {result['response']}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye! Take care.")
            break
        except Exception as e:
            print(f"Error: {e}\n")
