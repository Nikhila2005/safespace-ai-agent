# Step1: Setup Streamlit
import streamlit as st
import requests


BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 SafeSpace – AI Mental Health Therapist")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step2: User is able to ask question
# Chat input
user_input = st.chat_input("What's on your mind today?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    # AI Agent exists here
    try:
        response = requests.post(BACKEND_URL, json={"message": user_input})
        
        # Check if request was successful
        if response.status_code == 200:
            response_data = response.json()
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": f'{response_data["response"]} WITH TOOL: [{response_data["tool_called"]}]'
            })
        else:
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": f"⚠️ Error: Backend returned status code {response.status_code}. Response: {response.text}"
            })
    except requests.exceptions.JSONDecodeError:
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": f"⚠️ Error: Backend returned invalid JSON. Response: {response.text}"
        })
    except requests.exceptions.ConnectionError:
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": "⚠️ Error: Cannot connect to backend. Make sure the backend is running on http://localhost:8000"
        })
    except Exception as e:
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": f"⚠️ Error: {str(e)}"
        })
        
# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])