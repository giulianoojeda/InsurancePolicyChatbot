""" Python file to serve as the front-end of the chatbot. """

import streamlit as st
from src.agent.llm_agent import LlmAgent
from src import config

llm = LlmAgent(
    persist_directory=config.CHROMA_PATH,
    openai_api_key=config.OPENAI_API_KEY,
    model_name=config.FAST_LLM_MODEL,
    google_api_key=config.GOOGLE_API_KEY,
    google_cse_id=config.CUSTOM_SEARCH_ENGINE_ID,
)

st.title("Test Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Puedes preguntar!!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Get assistant response
    response = llm.query(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
