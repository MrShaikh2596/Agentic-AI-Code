import streamlit as st
import requests

# App configuration
st.set_page_config(page_title="FastAPI Chat Client", page_icon="💬")
st.title("💬 FastAPI Chat Client")

# Define backend API URL
FASTAPI_URL = "http://localhost:8000/llm-chat"

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle new user input
if user_input := st.chat_input("Type your message here..."):
    
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 2. Query the FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                
                response = requests.post(FASTAPI_URL, params={"user_message": user_input})
                
                if response.status_code == 200:
                    bot_reply = response.text
                else:
                    bot_reply = f"Error: Received status code {response.status_code}"
            except requests.exceptions.ConnectionError:
                bot_reply = requests.post(FASTAPI_URL, params={"user_message": user_input})

            # 3. Display and store assistant response
            st.write(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
