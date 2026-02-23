# SafeSpace AI - Complete Project Explanation for Interviews

## Table of Contents
1. [Project Overview (30-second pitch)](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Technical Architecture](#technical-architecture)
4. [Key Features](#key-features)
5. [Technology Stack Explained](#technology-stack-explained)
6. [How Each Component Works](#how-each-component-works)
7. [Challenges & Solutions](#challenges-and-solutions)
8. [Code Walkthrough](#code-walkthrough)
9. [API Integration Details](#api-integration-details)
10. [Interview Questions & Answers](#interview-questions-and-answers)

---

## Project Overview (30-second pitch)

**What to say:**
> "I built SafeSpace AI, an intelligent mental health chatbot that provides empathetic counseling and helps users find real therapists near them. It uses AI to detect emotional distress, responds with therapeutic guidance using a medical-grade language model, and can search for actual mental health facilities globally using OpenStreetMap's API. The system is built with a FastAPI backend, Streamlit frontend, and integrates multiple AI models including Groq's LLaMA for intent detection and Ollama's MedGemma for therapeutic responses."

---

## Problem Statement

### The Problem
1. **Mental health crisis**: Many people need immediate emotional support but can't access therapists
2. **Finding therapists is hard**: No easy way to find nearby mental health professionals
3. **24/7 availability**: Traditional therapy isn't available round-the-clock
4. **Cost barrier**: Professional therapy is expensive

### Your Solution
- **AI Therapist**: Provides immediate, empathetic responses using medical AI
- **Real-time Therapist Search**: Finds actual mental health facilities with contact info
- **Always Available**: Works 24/7, no appointments needed
- **Free**: No cost to users

---

## Technical Architecture

### High-Level Architecture

```
User (Browser)
    ↓
Streamlit Frontend (Python)
    ↓ HTTP Request
FastAPI Backend (Python)
    ↓
AI Agent (LangChain + Groq)
    ↓
Tools:
    1. MedGemma (Ollama) - Therapeutic responses
    2. OpenStreetMap API - Find therapists
    3. Twilio - Emergency calls
```

### Why This Architecture?

**Interviewer might ask: "Why did you separate frontend and backend?"**

**Your answer:**
> "I used a microservices architecture to separate concerns. The frontend (Streamlit) handles user interface and user experience, while the backend (FastAPI) handles business logic and AI processing. This separation provides several benefits:
> 
> 1. **Scalability**: I can scale the backend independently if AI processing becomes heavy
> 2. **Security**: Sensitive API keys stay on the backend, never exposed to the browser
> 3. **Flexibility**: I can swap the frontend (maybe build a mobile app) without changing the backend
> 4. **Testing**: I can test backend logic independently using API testing tools like Postman
> 5. **Performance**: The backend can handle multiple frontend requests simultaneously"

---

## Key Features

### 1. Emotional Distress Detection
**What it does:** Automatically detects when users express sadness, anxiety, depression, etc.

**How it works:**
- Uses Groq's LLaMA 3.1 model to analyze user messages
- Looks for keywords and emotional patterns
- Triggers the therapeutic AI when distress is detected

**Example:**
- User: "I am sad"
- System detects: Emotional distress
- Action: Calls MedGemma for empathetic response

### 2. AI-Powered Therapy
**What it does:** Provides empathetic, therapeutic responses

**How it works:**
- Uses MedGemma (medical-grade AI model) via Ollama
- Trained on medical and psychological data
- Responds like a professional therapist

**Example Response:**
> "I can sense how difficult this must be for you. Many people feel this way when going through challenging times. What sometimes helps is talking about what's troubling you. I'm here to listen."

### 3. Real-Time Therapist Search
**What it does:** Finds actual mental health facilities near any location globally

**How it works:**
1. **Geocoding**: Converts location name to coordinates (lat/lon)
2. **Search**: Queries OpenStreetMap for mental health facilities
3. **Parse**: Extracts names, addresses, phones, websites
4. **Display**: Shows results to user

**Example:**
- Input: "Find therapists near Bangalore"
- Output: Real facilities with contact info

### 4. Emergency Response
**What it does:** Calls emergency contacts if user mentions self-harm

**How it works:**
- Detects suicide/self-harm keywords
- Uses Twilio API to make phone calls
- Provides crisis helpline numbers

---

## Technology Stack Explained

### Backend Technologies

#### 1. **FastAPI** (Web Framework)
**What is it?**
- A modern Python web framework for building APIs
- "API" means Application Programming Interface - a way for programs to talk to each other

**Why FastAPI?**
- **Fast**: Built on async Python, handles multiple requests simultaneously
- **Easy**: Simple syntax, automatic documentation
- **Type-safe**: Uses Python type hints to catch errors early
- **Auto-docs**: Generates interactive API documentation automatically

**In your project:**
```python
@app.post("/ask")  # This creates an endpoint at http://localhost:8000/ask
async def ask(query: Query):  # async = can handle multiple requests at once
    result = get_agent_response(query.message)
    return {"response": result["response"]}
```

**What this means:**
- When frontend sends a POST request to `/ask` with a message
- FastAPI receives it, processes it, and sends back a response
- Multiple users can use the chatbot simultaneously

---

#### 2. **LangChain** (AI Framework)
**What is it?**
- A framework for building applications with Large Language Models (LLMs)
- Think of it as a toolkit for working with AI

**Why LangChain?**
- **Simplifies AI integration**: Makes it easy to work with different AI models
- **Prompt management**: Helps structure conversations with AI
- **Memory**: Can remember conversation history
- **Tool integration**: Allows AI to use external tools (like our therapist search)

**In your project:**
```python
llm = ChatGroq(model="llama-3.1-8b-instant")  # Connect to AI model
messages = [
    SystemMessage(content=SYSTEM_PROMPT),  # Instructions for AI
    HumanMessage(content=user_input)       # User's message
]
response = llm.invoke(messages)  # Get AI response
```

**What this means:**
- You give the AI instructions (system prompt)
- You give it the user's message
- It responds based on its training and your instructions

---

#### 3. **Groq** (AI Inference Platform)
**What is it?**
- A company that runs AI models super fast
- They host LLaMA models (made by Meta/Facebook)

**Why Groq?**
- **Speed**: Responds in milliseconds, not seconds
- **Free tier**: Generous free usage
- **LLaMA 3.1**: One of the best open-source AI models

**In your project:**
- Used for intent detection (understanding what user wants)
- Decides which tool to use (therapy, search, emergency)

---

#### 4. **Ollama** (Local AI Runtime)
**What is it?**
- Software that runs AI models on your computer
- Like a "container" for AI models

**Why Ollama?**
- **Privacy**: AI runs locally, data doesn't leave your machine
- **Free**: No API costs
- **MedGemma**: Access to medical-specialized AI model

**In your project:**
```python
response = ollama.chat(
    model='alibayram/medgemma:4b',  # Medical AI model
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
)
```

**What this means:**
- When user expresses distress, we use MedGemma
- It's trained on medical/psychological data
- Gives more appropriate therapeutic responses

---

#### 5. **OpenStreetMap APIs** (Geocoding & Search)
**What is it?**
- Free, open-source mapping service (like Google Maps but free)
- Two APIs used:
  1. **Nominatim**: Converts location names to coordinates
  2. **Overpass**: Searches for places on the map

**Why OpenStreetMap?**
- **100% Free**: No API keys, no payment info
- **Global**: Works worldwide
- **Real data**: Community-maintained, accurate

**How it works:**

**Step 1: Geocoding (Nominatim)**
```python
# User says: "Find therapists near Bangalore"
geocode_url = "https://nominatim.openstreetmap.org/search"
params = {"q": "Bangalore", "format": "json"}
response = requests.get(geocode_url, params=params)
# Returns: {"lat": 12.9716, "lon": 77.5946}
```

**Step 2: Search (Overpass)**
```python
# Now search for mental health facilities near those coordinates
query = """
[out:json];
(
  node["healthcare"="psychotherapist"](around:40000,12.9716,77.5946);
  node["amenity"="clinic"]["healthcare:speciality"~"psychiatry"](around:40000,12.9716,77.5946);
);
out center 10;
"""
# Returns: List of facilities with names, addresses, phones
```

**What this means:**
- First, convert "Bangalore" to coordinates (12.97°N, 77.59°E)
- Then, search for mental health facilities within 25 miles (40km)
- Get real facility data from OpenStreetMap's database

---

#### 6. **Twilio** (Phone Call API)
**What is it?**
- A service that lets programs make phone calls and send SMS

**Why Twilio?**
- **Emergency feature**: Can call emergency contacts
- **Reliable**: Industry-standard for communications
- **Easy API**: Simple to integrate

**In your project:**
```python
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
call = client.calls.create(
    to=EMERGENCY_CONTACT,  # Who to call
    from_=TWILIO_FROM_NUMBER,  # Your Twilio number
    url="http://demo.twilio.com/docs/voice.xml"  # What to say
)
```

---

### Frontend Technologies

#### 1. **Streamlit** (UI Framework)
**What is it?**
- A Python library for building web apps quickly
- No HTML/CSS/JavaScript needed

**Why Streamlit?**
- **Fast development**: Build UI with just Python
- **Interactive**: Real-time updates
- **Beautiful**: Modern, clean design out of the box

**In your project:**
```python
st.title("SafeSpace – AI Mental Health Therapist")
user_input = st.chat_input("Type your message...")
if user_input:
    response = requests.post("http://localhost:8000/ask", 
                            json={"message": user_input})
    st.chat_message("assistant").write(response.json()["response"])
```

**What this means:**
- Creates a chat interface
- When user types, sends to backend
- Displays response in chat

---

## How Each Component Works

### Component 1: Intent Detection (AI Agent)

**File:** `backend/ai_agent.py`

**What it does:** Understands what the user wants

**Step-by-step:**

1. **User sends message**: "I am sad"

2. **System Prompt**: We give the AI instructions
```python
SYSTEM_PROMPT = """
You are a mental health AI assistant. You MUST follow these rules:

1. If user expresses emotional distress (sad, depressed, anxious):
   → Respond with: "USE_TOOL: ask_mental_health_specialist"

2. If user mentions self-harm or suicide:
   → Respond with: "USE_TOOL: emergency_call_tool"

3. If user asks to find therapists:
   → Respond with: "USE_TOOL: find_nearby_therapists_by_location"
"""
```

3. **AI analyzes**: LLaMA reads the message and system prompt

4. **AI decides**: "User is sad → USE_TOOL: ask_mental_health_specialist"

5. **Our code detects**: 
```python
if "USE_TOOL: ask_mental_health_specialist" in response_text:
    tool_result = query_medgemma(user_input)  # Call MedGemma
```

6. **Return therapeutic response**

**Why this approach?**
- **Flexible**: AI can handle variations ("I'm sad", "feeling down", "depressed")
- **Accurate**: LLaMA is good at understanding intent
- **Extensible**: Easy to add new tools/features

---

### Component 2: Therapeutic Response (MedGemma)

**File:** `backend/tools.py` → `query_medgemma()`

**What it does:** Provides empathetic, therapeutic responses

**Step-by-step:**

1. **Receive user's emotional message**: "I am sad"

2. **Create therapist persona**:
```python
system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist.
Respond with:
1. Emotional attunement ("I can sense how difficult this must be...")
2. Gentle normalization ("Many people feel this way when...")
3. Practical guidance ("What sometimes helps is...")
4. Strengths-focused support ("I notice how you're...")
"""
```

3. **Call MedGemma**:
```python
response = ollama.chat(
    model='alibayram/medgemma:4b',
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "I am sad"}
    ],
    options={
        'temperature': 0.7,  # Controls creativity (0=robotic, 1=creative)
        'num_predict': 350   # Maximum response length
    }
)
```

4. **MedGemma generates response**:
> "I can sense you're going through a difficult time right now. Feeling sad is a natural human emotion, and it's okay to acknowledge it. Many people experience sadness when facing challenges or changes in their lives. Would you like to talk about what's making you feel this way? I'm here to listen and support you."

5. **Return to user**

**Why MedGemma specifically?**
- **Medical training**: Trained on medical/psychological literature
- **Appropriate responses**: Understands mental health context
- **Empathetic**: Designed for healthcare interactions

---

### Component 3: Therapist Search (OpenStreetMap)

**File:** `backend/tools.py` → `find_nearby_therapists()`

**What it does:** Finds real mental health facilities

**Step-by-step process:**

#### Step 1: Extract Location
```python
# User says: "Find therapists near Bangalore, India"
# We use regex to extract "Bangalore, India"
location_patterns = [
    r'(?:near|in|at|around)\s+([A-Za-z\s,]+)',  # Matches "near Bangalore, India"
]
location = "Bangalore, India"
```

#### Step 2: Geocode (Convert name to coordinates)
```python
# Call Nominatim API
geocode_url = "https://nominatim.openstreetmap.org/search"
params = {
    "q": "Bangalore, India",
    "format": "json",
    "limit": 1
}
response = requests.get(geocode_url, params=params)

# Response:
{
    "lat": "12.9715987",
    "lon": "77.5945627",
    "display_name": "Bengaluru, Karnataka, India"
}
```

**What happened:**
- Sent location name to Nominatim
- Nominatim searched its database
- Returned coordinates (latitude/longitude)

#### Step 3: Search for Facilities
```python
# Build Overpass query
radius_meters = 25 * 1609.34  # 25 miles in meters = 40,233 meters

overpass_query = f"""
[out:json];
(
  node["healthcare"="psychotherapist"](around:{radius_meters},{lat},{lon});
  node["amenity"="clinic"]["healthcare:speciality"~"psychiatry"](around:{radius_meters},{lat},{lon});
  node["healthcare"="counselling"](around:{radius_meters},{lat},{lon});
);
out center 10;
"""

# Send to Overpass API
response = requests.post("https://overpass-api.de/api/interpreter", 
                        data={"data": overpass_query})
```

**What this query means:**
- `[out:json]`: Return results as JSON
- `node["healthcare"="psychotherapist"]`: Find places tagged as psychotherapist
- `(around:{radius_meters},{lat},{lon})`: Within 40km of Bangalore
- `out center 10`: Return top 10 results

#### Step 4: Parse Results
```python
data = response.json()
facilities = []

for element in data["elements"]:
    tags = element.get("tags", {})
    
    facility = {
        "name": tags.get("name", "Mental Health Facility"),
        "address": tags.get("addr:street", "Address not available"),
        "phone": tags.get("phone", "N/A"),
        "website": tags.get("website", "N/A"),
        "specialty": tags.get("healthcare:speciality", "Mental Health")
    }
    facilities.append(facility)
```

**Example result:**
```json
{
    "name": "The Alternative Story",
    "address": "11th Cross Road, Bengaluru",
    "phone": "N/A",
    "website": "https://alternativestory.in/",
    "specialty": "Mental Health"
}
```

#### Step 5: Format & Return
```python
result = "Here are mental health facilities near Bengaluru:\n\n"
for i, facility in enumerate(facilities, 1):
    result += f"{i}. **{facility['name']}**\n"
    result += f"   📍 {facility['address']}\n"
    result += f"   📞 {facility['phone']}\n"
    result += f"   🌐 {facility['website']}\n\n"
```

**Final output to user:**
```
Here are mental health facilities near Bengaluru:

1. **The Alternative Story**
   📍 11th Cross Road, Bengaluru
   📞 N/A
   🌐 https://alternativestory.in/

2. **Mind Free Counselling Centre**
   📍 5th Main Road
   📞 +91 80502 35032
   🏥 Specialty: Mental Health
```

---

### Component 4: Emergency Response

**File:** `backend/tools.py` → `call_emergency()`

**What it does:** Makes emergency phone calls

**Step-by-step:**

1. **Detect crisis keywords**: "suicide", "kill myself", "end it all"

2. **Trigger emergency tool**:
```python
if "USE_TOOL: emergency_call_tool" in response_text:
    call_emergency()
```

3. **Make phone call**:
```python
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
call = client.calls.create(
    to="+919606326001",  # Emergency contact
    from_="+14352721821",  # Your Twilio number
    url="http://demo.twilio.com/docs/voice.xml"
)
```

4. **Show crisis resources**:
```python
final_response = """
I've contacted emergency services. Please stay safe.
- 988 Suicide & Crisis Lifeline
- Crisis Text Line: Text HOME to 741741
"""
```

---

## Challenges & Solutions

### Challenge 1: Location Extraction

**Problem:**
- User says: "Find therapists near Bangalore"
- AI sometimes doesn't format location correctly
- Default was "United States" - wrong!

**Solution:**
```python
# Instead of relying on AI to format location
# Extract it directly from user's message using regex

location_patterns = [
    r'(?:near|in|at|around)\s+([A-Za-z\s,]+)',
    r'therapists?\s+(?:near|in)\s+([A-Za-z\s,]+)',
]

for pattern in location_patterns:
    match = re.search(pattern, user_input, re.IGNORECASE)
    if match:
        location = match.group(1).strip()
        break
```

**What you learned:**
- Don't rely solely on AI for structured data extraction
- Regex is more reliable for pattern matching
- Always have fallback logic

---

### Challenge 2: OpenStreetMap Data Quality

**Problem:**
- Some areas have no mental health facilities in OpenStreetMap
- Example: "California" (too broad, no specific results)

**Solution:**
```python
if not facilities:
    # Provide alternative resources
    return """
    I couldn't find facilities in the database, but here are resources:
    - Psychology Today: https://www.psychologytoday.com/us/therapists
    - National Helpline: 1-800-662-4357
    """
```

**What you learned:**
- Always have fallback options
- Graceful degradation (still provide value even if primary feature fails)
- User experience matters - never show empty results

---

### Challenge 3: API Rate Limits

**Problem:**
- Nominatim has rate limit: 1 request per second
- Too many requests = blocked

**Solution:**
```python
headers = {
    "User-Agent": "SafeSpace-Mental-Health-App/1.0"  # Required by Nominatim
}
# Be respectful of rate limits
# In production, add caching to reduce API calls
```

**Future improvement:**
- Cache geocoding results (Bangalore always returns same coordinates)
- Reduces API calls, faster responses

---

### Challenge 4: SAMHSA Website Scraping

**Problem:**
- SAMHSA website uses JavaScript (React)
- Simple HTTP requests return empty HTML
- Can't scrape facility data

**Attempted solutions:**
1. ❌ BeautifulSoup scraping - doesn't work (needs JavaScript)
2. ❌ Selenium/Playwright - too complex, resource-heavy
3. ✅ Provide direct link to SAMHSA - simple, works

**Final decision:**
- Removed SAMHSA entirely
- Focus on OpenStreetMap (works globally, no scraping needed)

**What you learned:**
- Not all websites can be scraped
- JavaScript-rendered content needs headless browsers
- Sometimes simpler solutions are better

---

## Code Walkthrough

### File Structure
```
safespace-ai-agent/
├── backend/
│   ├── main.py           # FastAPI server
│   ├── ai_agent.py       # AI logic & intent detection
│   ├── tools.py          # MedGemma, OpenStreetMap, Twilio
│   └── config.py         # API keys
├── frontend.py           # Streamlit UI
└── pyproject.toml        # Dependencies
```

---

### File 1: `backend/main.py` (FastAPI Server)

**Purpose:** Receives requests from frontend, processes them, returns responses

```python
from fastapi import FastAPI
from pydantic import BaseModel
from ai_agent import get_agent_response

app = FastAPI()  # Create FastAPI application

# Define request structure
class Query(BaseModel):
    message: str  # User's message

# Define endpoint
@app.post("/ask")  # POST request to /ask
async def ask(query: Query):
    # Get response from AI agent
    result = get_agent_response(query.message)
    
    # Return JSON response
    return {
        "response": result["response"],
        "tool_called": result["tool_called"]
    }

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

**Key concepts:**

1. **FastAPI app**: `app = FastAPI()`
   - Creates web server

2. **Pydantic model**: `class Query(BaseModel)`
   - Validates incoming data
   - Ensures `message` field exists and is a string

3. **Endpoint**: `@app.post("/ask")`
   - Decorator that creates route
   - POST = sending data to server
   - `/ask` = URL path

4. **async**: `async def ask()`
   - Allows handling multiple requests simultaneously
   - Non-blocking I/O

5. **uvicorn**: `uvicorn.run()`
   - ASGI server (runs FastAPI apps)
   - `reload=True` = auto-restart on code changes

---

### File 2: `backend/ai_agent.py` (AI Logic)

**Purpose:** Determines user intent and calls appropriate tools

```python
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize AI model
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY,
    temperature=0.2  # Low = more consistent, High = more creative
)

# System instructions
SYSTEM_PROMPT = """
You are a mental health AI assistant.

1. If user expresses emotional distress:
   → Respond: "USE_TOOL: ask_mental_health_specialist"

2. If user mentions self-harm:
   → Respond: "USE_TOOL: emergency_call_tool"

3. If user asks to find therapists:
   → Respond: "USE_TOOL: find_nearby_therapists_by_location"
"""

def get_agent_response(user_input: str) -> dict:
    # Create messages
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_input)
    ]
    
    # Get AI response
    response = llm.invoke(messages)
    response_text = response.content
    
    # Check which tool to use
    if "USE_TOOL: ask_mental_health_specialist" in response_text:
        tool_result = query_medgemma(user_input)
        return {
            "response": tool_result,
            "tool_called": "ask_mental_health_specialist"
        }
    
    elif "USE_TOOL: find_nearby_therapists_by_location" in response_text:
        # Extract location from user input
        location = extract_location(user_input)
        tool_result = find_nearby_therapists(location)
        return {
            "response": tool_result,
            "tool_called": "find_nearby_therapists_by_location"
        }
    
    # Default response
    return {
        "response": response_text,
        "tool_called": "None"
    }
```

**Key concepts:**

1. **LangChain**: Framework for AI apps
   - `ChatGroq`: Connects to Groq's API
   - `SystemMessage`: Instructions for AI
   - `HumanMessage`: User's input

2. **Temperature**: Controls randomness
   - 0.0 = Always same response (deterministic)
   - 1.0 = Very creative/random
   - 0.2 = Mostly consistent, slightly varied

3. **Tool detection**: `if "USE_TOOL:" in response_text`
   - Simple string matching
   - Could use function calling (more advanced)

---

### File 3: `backend/tools.py` (Tools Implementation)

#### Tool 1: MedGemma (Therapeutic AI)

```python
import ollama

def query_medgemma(prompt: str) -> str:
    # Define therapist persona
    system_prompt = """
    You are Dr. Emily Hartman, a clinical psychologist.
    Respond with empathy and professional guidance.
    """
    
    # Call Ollama
    response = ollama.chat(
        model='alibayram/medgemma:4b',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        options={
            'num_predict': 350,  # Max tokens
            'temperature': 0.7,  # Creativity level
            'top_p': 0.9        # Nucleus sampling
        }
    )
    
    return response['message']['content'].strip()
```

**Key concepts:**

1. **Ollama**: Runs AI models locally
   - No internet needed (after model download)
   - Privacy-friendly

2. **MedGemma**: Medical AI model
   - Based on Google's Gemma
   - Fine-tuned on medical data

3. **Options:**
   - `num_predict`: Maximum response length (in tokens)
   - `temperature`: Creativity (0.7 = balanced)
   - `top_p`: Probability threshold for word selection

---

#### Tool 2: OpenStreetMap Search

```python
import requests

def find_nearby_therapists(location: str, radius: int = 25) -> str:
    # Step 1: Geocode location
    geocode_url = "https://nominatim.openstreetmap.org/search"
    geocode_params = {
        "q": location,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "SafeSpace-Mental-Health-App/1.0"
    }
    
    geocode_response = requests.get(geocode_url, params=geocode_params, headers=headers)
    geocode_data = geocode_response.json()
    
    # Extract coordinates
    lat = float(geocode_data[0]["lat"])
    lon = float(geocode_data[0]["lon"])
    
    # Step 2: Search for facilities
    radius_meters = int(radius * 1609.34)  # Convert miles to meters
    
    overpass_query = f"""
    [out:json];
    (
      node["healthcare"="psychotherapist"](around:{radius_meters},{lat},{lon});
      node["amenity"="clinic"]["healthcare:speciality"~"psychiatry"](around:{radius_meters},{lat},{lon});
    );
    out center 10;
    """
    
    overpass_response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data={"data": overpass_query}
    )
    
    # Step 3: Parse results
    data = overpass_response.json()
    facilities = []
    
    for element in data["elements"]:
        tags = element.get("tags", {})
        facility = {
            "name": tags.get("name", "Mental Health Facility"),
            "address": tags.get("addr:street", "N/A"),
            "phone": tags.get("phone", "N/A"),
            "website": tags.get("website", "N/A")
        }
        facilities.append(facility)
    
    # Step 4: Format output
    result = f"Here are mental health facilities near {location}:\n\n"
    for i, facility in enumerate(facilities, 1):
        result += f"{i}. **{facility['name']}**\n"
        result += f"   📍 {facility['address']}\n"
        result += f"   📞 {facility['phone']}\n"
        result += f"   🌐 {facility['website']}\n\n"
    
    return result
```

**Key concepts:**

1. **Geocoding**: Location name → Coordinates
   - "Bangalore" → (12.97°N, 77.59°E)

2. **Overpass QL**: Query language for OpenStreetMap
   - `node["healthcare"="psychotherapist"]`: Find psychotherapists
   - `(around:40000,12.97,77.59)`: Within 40km of coordinates
   - `out center 10`: Return 10 results

3. **JSON parsing**: Extract data from API response
   - `tags.get("name", "default")`: Get name, or "default" if missing

---

### File 4: `frontend.py` (Streamlit UI)

```python
import streamlit as st
import requests

# Page config
st.set_page_config(
    page_title="SafeSpace – AI Mental Health Therapist",
    page_icon="🧠"
)

# Title
st.title("SafeSpace – AI Mental Health Therapist")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Type your message..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Send to backend
    response = requests.post(
        "http://localhost:8000/ask",
        json={"message": user_input}
    )
    
    # Get AI response
    ai_response = response.json()["response"]
    
    # Add AI message to chat
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)
```

**Key concepts:**

1. **Streamlit**: Python web framework
   - `st.title()`: Creates heading
   - `st.chat_input()`: Chat input box
   - `st.chat_message()`: Chat bubble

2. **Session state**: Stores data across reruns
   - `st.session_state.messages`: Chat history
   - Persists when user sends new message

3. **Walrus operator**: `:=`
   - `if user_input := st.chat_input()`
   - Assigns AND checks in one line
   - Same as: `user_input = st.chat_input(); if user_input:`

4. **HTTP request**: `requests.post()`
   - Sends user message to backend
   - Receives AI response

---

## API Integration Details

### 1. Groq API

**What:** AI inference platform (runs LLaMA models)

**Endpoint:** `https://api.groq.com/openai/v1/chat/completions`

**Authentication:**
```python
groq_api_key = "gsk_..."  # Your API key
```

**Request format:**
```python
{
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"}
    ],
    "temperature": 0.2
}
```

**Response format:**
```python
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Hello! How can I help you today?"
            }
        }
    ]
}
```

**Rate limits:**
- Free tier: 30 requests/minute
- 14,400 tokens/minute

---

### 2. Ollama API

**What:** Local AI runtime (runs on your computer)

**Endpoint:** `http://localhost:11434/api/chat`

**No authentication needed** (local)

**Request format:**
```python
{
    "model": "alibayram/medgemma:4b",
    "messages": [
        {"role": "system", "content": "You are a therapist"},
        {"role": "user", "content": "I am sad"}
    ],
    "options": {
        "temperature": 0.7,
        "num_predict": 350
    }
}
```

**Response format:**
```python
{
    "message": {
        "role": "assistant",
        "content": "I understand you're feeling sad..."
    }
}
```

**No rate limits** (runs locally)

---

### 3. OpenStreetMap Nominatim API

**What:** Geocoding service (location → coordinates)

**Endpoint:** `https://nominatim.openstreetmap.org/search`

**Authentication:** None (just User-Agent header)

**Request:**
```
GET https://nominatim.openstreetmap.org/search?q=Bangalore&format=json&limit=1
Headers: User-Agent: SafeSpace-Mental-Health-App/1.0
```

**Response:**
```json
[
    {
        "lat": "12.9715987",
        "lon": "77.5945627",
        "display_name": "Bengaluru, Karnataka, India"
    }
]
```

**Rate limit:** 1 request/second

---

### 4. OpenStreetMap Overpass API

**What:** Search for places on map

**Endpoint:** `https://overpass-api.de/api/interpreter`

**Authentication:** None

**Request:**
```
POST https://overpass-api.de/api/interpreter
Body: data=[out:json];(node["healthcare"="psychotherapist"](around:40000,12.97,77.59););out center 10;
```

**Response:**
```json
{
    "elements": [
        {
            "type": "node",
            "id": 123456,
            "lat": 12.9716,
            "lon": 77.5946,
            "tags": {
                "name": "The Alternative Story",
                "healthcare": "psychotherapist",
                "phone": "+91 80 1234 5678",
                "website": "https://alternativestory.in/"
            }
        }
    ]
}
```

**Rate limit:** Reasonable use (no strict limit)

---

### 5. Twilio API

**What:** Phone call service

**Endpoint:** `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Calls.json`

**Authentication:** Account SID + Auth Token

**Request:**
```python
POST https://api.twilio.com/2010-04-01/Accounts/ACd7187.../Calls.json
Auth: Basic (AccountSID:AuthToken)
Body:
{
    "To": "+919606326001",
    "From": "+14352721821",
    "Url": "http://demo.twilio.com/docs/voice.xml"
}
```

**Response:**
```json
{
    "sid": "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "status": "queued"
}
```

**Rate limit:** Depends on account type

---

## Interview Questions & Answers

### Technical Questions

#### Q1: "Explain your project architecture"

**Answer:**
> "I built a microservices architecture with three main components:
> 
> 1. **Frontend (Streamlit)**: Handles user interface - chat interface where users type messages
> 
> 2. **Backend (FastAPI)**: Processes requests - receives messages, determines intent using AI, calls appropriate tools
> 
> 3. **AI Layer**: Two models working together:
>    - Groq's LLaMA 3.1 for intent detection (understanding what user wants)
>    - Ollama's MedGemma for therapeutic responses (providing empathetic counseling)
> 
> The frontend and backend communicate via REST API. When a user sends a message, the frontend makes a POST request to `/ask` endpoint, the backend processes it using AI, and returns a JSON response with the answer.
> 
> I chose this architecture because it's scalable (can handle multiple users), secure (API keys stay on backend), and flexible (can swap frontend without changing backend)."

---

#### Q2: "Why did you use two different AI models?"

**Answer:**
> "I used two AI models because they serve different purposes:
> 
> 1. **Groq's LLaMA 3.1**: Fast, general-purpose model
>    - Used for intent detection (understanding user's request)
>    - Decides which tool to use (therapy, search, emergency)
>    - Responds in milliseconds
>    - Good at classification tasks
> 
> 2. **Ollama's MedGemma**: Medical-specialized model
>    - Used for therapeutic responses
>    - Trained on medical/psychological data
>    - Provides more appropriate, empathetic responses
>    - Runs locally for privacy
> 
> This separation of concerns makes the system more efficient - we use the fast model for routing, and the specialized model only when needed for therapy. It's like having a receptionist (LLaMA) who directs you to the right specialist (MedGemma)."

---

#### Q3: "How does the therapist search work?"

**Answer:**
> "The therapist search has four steps:
> 
> **Step 1 - Location Extraction:**
> I use regex patterns to extract the location from user's message. For example, if user says 'Find therapists near Bangalore', I extract 'Bangalore' using pattern matching.
> 
> **Step 2 - Geocoding:**
> I send the location name to OpenStreetMap's Nominatim API, which converts it to coordinates. 'Bangalore' becomes latitude 12.97, longitude 77.59.
> 
> **Step 3 - Search:**
> I query OpenStreetMap's Overpass API with those coordinates, searching for mental health facilities within 25 miles. The query looks for nodes tagged as 'psychotherapist', 'clinic with psychiatry specialty', etc.
> 
> **Step 4 - Parse & Format:**
> I parse the JSON response, extract facility names, addresses, phone numbers, and websites, then format them nicely for the user.
> 
> I chose OpenStreetMap because it's completely free, works globally, and has real, community-verified data. The alternative was Google Places API, but that requires billing information even for the free tier."

---

#### Q4: "What challenges did you face?"

**Answer:**
> "I faced three main challenges:
> 
> **Challenge 1 - Location Extraction:**
> Initially, I relied on the AI to format the location correctly, but it was inconsistent. Sometimes it would output 'United States' as default instead of the actual location. I solved this by using regex to extract the location directly from the user's message, which is more reliable.
> 
> **Challenge 2 - OpenStreetMap Data Quality:**
> Some areas don't have mental health facilities in OpenStreetMap's database. For example, searching for 'California' (the whole state) returns no results because it's too broad. I solved this by providing fallback resources - if no facilities are found, I show links to Psychology Today and crisis helplines.
> 
> **Challenge 3 - SAMHSA Website Scraping:**
> I initially tried to scrape the SAMHSA government website for therapist data, but it's a React app that loads data with JavaScript. Simple HTTP requests return empty HTML. I would need Selenium or Playwright for browser automation, which is complex and resource-heavy. I decided to remove SAMHSA and focus on OpenStreetMap, which has a proper API and works globally.
> 
> These challenges taught me to always have fallback options and that simpler solutions are often better than complex ones."

---

#### Q5: "How do you handle errors?"

**Answer:**
> "I have error handling at multiple levels:
> 
> **1. API Level:**
> Every API call is wrapped in try-except blocks. If an API fails, I catch the exception and return a user-friendly message instead of crashing.
> 
> ```python
> try:
>     response = requests.get(api_url)
> except Exception as e:
>     return 'Sorry, I encountered an error. Here are crisis resources...'
> ```
> 
> **2. Data Validation:**
> I check if API responses contain expected data before using it:
> 
> ```python
> if not geocode_data:
>     return 'Could not find that location'
> ```
> 
> **3. Graceful Degradation:**
> If the main feature fails, I still provide value. For example, if therapist search fails, I show links to online directories and crisis helplines.
> 
> **4. Logging:**
> I print debug messages to console so I can see what's happening:
> 
> ```python
> print(f'🔍 Searching for therapists near {location}')
> ```
> 
> This helps me debug issues quickly during development."

---

#### Q6: "How would you scale this application?"

**Answer:**
> "To scale this application for production, I would make several improvements:
> 
> **1. Caching:**
> - Cache geocoding results (Bangalore always returns same coordinates)
> - Cache OpenStreetMap results for popular locations
> - Use Redis for fast in-memory caching
> - This reduces API calls and improves response time
> 
> **2. Database:**
> - Store chat history in PostgreSQL
> - Track user sessions
> - Analytics on common queries
> 
> **3. Load Balancing:**
> - Deploy multiple backend instances
> - Use Nginx or AWS Load Balancer
> - Distribute traffic across servers
> 
> **4. Async Processing:**
> - Use Celery for background tasks
> - Queue long-running operations
> - Don't block user while processing
> 
> **5. Monitoring:**
> - Add logging with ELK stack (Elasticsearch, Logstash, Kibana)
> - Track API response times
> - Alert on errors
> 
> **6. Security:**
> - Add rate limiting (prevent abuse)
> - Use HTTPS (encrypt traffic)
> - Sanitize user inputs (prevent injection attacks)
> - Store API keys in environment variables or secrets manager
> 
> **7. Cloud Deployment:**
> - Deploy on AWS/GCP/Azure
> - Use Docker containers
> - Auto-scaling based on traffic
> 
> For a production system serving thousands of users, I'd also consider using a managed AI service like OpenAI's API instead of running Ollama locally, as it's more reliable and scalable."

---

### Behavioral Questions

#### Q7: "Why did you build this project?"

**Answer:**
> "I built this project because I'm passionate about using technology to solve real-world problems. Mental health is a growing crisis, especially among young people, but access to professional help is limited by cost, availability, and stigma.
> 
> I wanted to create something that could provide immediate support to someone in distress, available 24/7, completely free. While AI can't replace human therapists, it can provide a first line of support and help people find professional help when they need it.
> 
> This project also allowed me to learn about AI integration, API development, and building full-stack applications. I learned how to work with multiple AI models, integrate third-party APIs, and create a user-friendly interface.
> 
> The most rewarding part was when I tested the therapist search and found real facilities with accurate contact information - knowing this could actually help someone find professional help made all the effort worthwhile."

---

#### Q8: "What would you improve if you had more time?"

**Answer:**
> "There are several features I'd like to add:
> 
> **1. Conversation Memory:**
> Currently, each message is independent. I'd add conversation history so the AI remembers what we discussed earlier in the session. This would make responses more contextual and personalized.
> 
> **2. User Accounts:**
> Allow users to create accounts, save chat history, and track their mental health journey over time.
> 
> **3. More Data Sources:**
> Integrate additional APIs like:
> - Yelp for therapist reviews
> - Psychology Today for more comprehensive listings
> - Insurance provider APIs to filter by coverage
> 
> **4. Multilingual Support:**
> Add support for multiple languages so it can help people worldwide. The AI models support this, I'd just need to translate the UI.
> 
> **5. Crisis Detection Improvements:**
> Use sentiment analysis to detect subtle signs of crisis, not just keywords. Track mood over time to identify concerning patterns.
> 
> **6. Mobile App:**
> Build a React Native mobile app for better accessibility. Many people prefer using apps over websites.
> 
> **7. Therapist Matching:**
> Add filters for specialty (anxiety, depression, PTSD), insurance accepted, language spoken, etc. Help users find the right therapist, not just any therapist.
> 
> **8. Analytics Dashboard:**
> Track usage patterns, common issues, popular locations to understand how people use the system and improve it."

---

### Conceptual Questions

#### Q9: "Explain how AI language models work"

**Answer:**
> "AI language models like LLaMA work through a process called deep learning:
> 
> **Training Phase:**
> 1. The model reads billions of text documents (books, websites, articles)
> 2. It learns patterns - which words commonly appear together, how sentences are structured, how to answer questions
> 3. It adjusts billions of parameters (numbers) to predict the next word in a sequence
> 
> **Inference Phase (when you use it):**
> 1. You give it a prompt: 'I am sad'
> 2. It breaks this into tokens (pieces of words)
> 3. It processes these tokens through neural network layers
> 4. Each layer transforms the input, extracting meaning
> 5. Finally, it predicts the most likely next words based on its training
> 
> **Key Concepts:**
> - **Tokens**: Words broken into pieces (e.g., 'running' → 'run' + 'ning')
> - **Context Window**: How much text it can remember (8000 tokens for LLaMA 3.1)
> - **Temperature**: Controls randomness (0 = always same answer, 1 = creative)
> - **Transformer Architecture**: The neural network design that makes this possible
> 
> **Important Limitation:**
> The model doesn't 'understand' like humans do - it's pattern matching at a very sophisticated level. It doesn't have real emotions or consciousness, which is why I use it for routing and call a specialized medical model (MedGemma) for actual therapeutic responses."

---

#### Q10: "What is an API and why use them?"

**Answer:**
> "API stands for Application Programming Interface. It's a way for different programs to talk to each other.
> 
> **Simple Analogy:**
> Think of a restaurant:
> - You (the customer) don't go into the kitchen to cook
> - You tell the waiter (API) what you want
> - The waiter tells the kitchen (server)
> - The kitchen prepares your food
> - The waiter brings it back to you
> 
> **In Programming:**
> - Your app (client) wants data
> - You make an API request (like ordering food)
> - The server processes it
> - The server sends back a response (your data)
> 
> **Example from my project:**
> ```python
> # I want to know coordinates of Bangalore
> response = requests.get(
>     'https://nominatim.openstreetmap.org/search',
>     params={'q': 'Bangalore', 'format': 'json'}
> )
> # I get back: {'lat': 12.97, 'lon': 77.59}
> ```
> 
> **Why use APIs:**
> 1. **Don't reinvent the wheel**: OpenStreetMap has map data, I don't need to build my own
> 2. **Always updated**: They maintain the data, I just use it
> 3. **Scalable**: They handle millions of requests
> 4. **Specialized**: They're experts in mapping, I'm not
> 
> **Types of APIs I used:**
> - **REST API**: Most common, uses HTTP (GET, POST, etc.)
> - **JSON format**: Data exchanged as JSON (JavaScript Object Notation)
> - **Rate limits**: Restrictions on how many requests you can make
> 
> In my project, I use 5 different APIs (Groq, Ollama, Nominatim, Overpass, Twilio), each providing a specific service. This modular approach makes the system flexible and maintainable."

---

## Tips for Interview

### 1. Start with the Big Picture
- Don't jump into technical details immediately
- Explain WHAT the project does before HOW it works
- Use the 30-second pitch first

### 2. Use Analogies
- "LLaMA is like a receptionist who directs you to the right specialist"
- "Geocoding is like converting a street address to GPS coordinates"
- "API is like a waiter taking your order to the kitchen"

### 3. Show Problem-Solving
- Don't just say "I used X technology"
- Explain WHY you chose it
- Mention alternatives you considered
- Discuss trade-offs

### 4. Be Honest About Limitations
- "This works well for cities, but needs improvement for rural areas"
- "OpenStreetMap data quality varies by region"
- "I would add caching in production to reduce API calls"

### 5. Demonstrate Learning
- "I initially tried X, but learned that Y works better because..."
- "This challenge taught me..."
- "If I were to rebuild this, I would..."

### 6. Prepare a Demo
- Have the app running on your laptop
- Show it working with different queries
- Demonstrate error handling
- Show the code structure

### 7. Know Your Code
- Be able to explain every line
- Understand the libraries you used
- Know the API documentation
- Be ready to modify code on the spot

### 8. Practice Explaining
- Explain to a friend who's not technical
- Record yourself explaining
- Time yourself (should be 2-3 minutes for overview)
- Prepare for follow-up questions

---

## Common Follow-up Questions

**Q: "Can you show me the code?"**
- Have your IDE open
- Walk through file structure
- Explain key functions
- Show how components connect

**Q: "How did you test this?"**
- Manual testing with various inputs
- Tested edge cases (empty input, long messages, special characters)
- Verified API responses
- Checked error handling

**Q: "What if the API goes down?"**
- Have fallback responses
- Show error messages
- Provide alternative resources
- Log errors for debugging

**Q: "How do you ensure user privacy?"**
- No data stored (currently)
- API keys on backend only
- HTTPS in production
- Could add encryption for chat history

**Q: "What's the cost to run this?"**
- Groq: Free tier (30 req/min)
- Ollama: Free (runs locally)
- OpenStreetMap: Free
- Twilio: Pay per call (~$0.01/min)
- Hosting: ~$5-10/month for small VPS

---

## Final Checklist Before Interview

✅ Can explain project in 30 seconds
✅ Can explain project in 5 minutes
✅ Can explain each technology choice
✅ Can walk through code
✅ Can demonstrate working app
✅ Know all APIs used
✅ Can explain challenges faced
✅ Can discuss improvements
✅ Understand AI concepts (tokens, temperature, etc.)
✅ Can answer "Why this project?"

---

## Confidence Boosters

Remember:
1. **You built something real** - It works, it's useful, it's impressive
2. **You solved real problems** - Location extraction, API integration, error handling
3. **You learned a lot** - AI, APIs, full-stack development
4. **You can explain it** - You understand how it works
5. **You're prepared** - You have this guide

**You've got this! 🚀**

Good luck with your interviews!
