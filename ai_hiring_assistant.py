import streamlit as st
from streamlit_chat import message
from openai import OpenAI
import os


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key="your-api-key")

# Initialize OpenAI client
client = OpenAI(api_key="your-api-key")  # Replace with your actual API key

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "step" not in st.session_state:
    st.session_state.step = "greet"

def ask_ai(prompt):
    # Prepare messages from chat history in proper format
    messages = []
    for chat in st.session_state.chat_history:
        if chat.startswith("User:"):
            messages.append({"role": "user", "content": chat[6:].strip()})
        elif chat.startswith("AI:"):
            messages.append({"role": "assistant", "content": chat[3:].strip()})  # AI: is 3 chars + colon and space

    # Add current user prompt
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # safer default model
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

st.title("🤖 AI Hiring Assistant Chatbot")

if st.session_state.step == "greet":
    message("Hi! I’m your AI hiring assistant. Can I know your name?")
    st.session_state.step = "get_name"

elif st.session_state.step == "get_name":
    name = st.text_input("Your Name")
    if name:
        st.session_state.chat_history.append(f"User: My name is {name}")
        st.session_state.chat_history.append(f"AI: Nice to meet you, {name}! What is your tech stack?")
        st.session_state.step = "get_stack"
        st.experimental_rerun()

elif st.session_state.step == "get_stack":
    stack = st.text_input("Tech Stack (e.g., Python, React, etc.)")
    if stack:
        st.session_state.chat_history.append(f"User: My tech stack is {stack}")
        st.session_state.chat_history.append(f"AI: Great! Let me generate some interview questions for {stack}.")
        st.session_state.step = "ask_questions"
        st.session_state.stack = stack
        st.experimental_rerun()

elif st.session_state.step == "ask_questions":
    prompt = f"Generate 3 to 5 technical interview questions for someone skilled in {st.session_state.stack}."
    response = ask_ai(prompt)
    st.session_state.chat_history.append(f"AI: {response}")
    st.session_state.step = "thank"
    st.experimental_rerun()

elif st.session_state.step == "thank":
    message("Thanks for your time! All the best for your interviews. 👋")

# Display chat history (user messages then AI messages)
for i in range(0, len(st.session_state.chat_history), 2):
    # Show user message (remove "User: " prefix)
    message(st.session_state.chat_history[i][6:], is_user=True, key=f"user_{i}")
    if i + 1 < len(st.session_state.chat_history):
        # Show AI message (remove "AI: " prefix)
        message(st.session_state.chat_history[i + 1][4:], is_user=False, key=f"ai_{i}")
