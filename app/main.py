""" Python file to serve as the front-end of the chatbot. """

import streamlit as st
from src.agent.llm_agent import LlmAgent
from src import config


import time


def load_agent():
    """Logic for loading the chatbot agent"""
    print("Loading Agent")
    llm = LlmAgent(
        persist_directory=config.CHROMA_PATH,
        openai_api_key=config.OPENAI_API_KEY,
        model_name=config.FAST_LLM_MODEL,
        google_api_key=config.GOOGLE_API_KEY,
        google_cse_id=config.CUSTOM_SEARCH_ENGINE_ID,
    )
    return llm


def get_text():
    input_text = st.text_input("You: ", "Hola, ¿en qué puedo ayudarte?", key="input")
    return input_text


if __name__ == "__main__":
    st.set_page_config(
        page_title="Policy Pro - Insurance Chatbot",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header("📖 Policy Pro: Demostración")

    if not config.OPENAI_API_KEY:
        st.error("Por favor, configure sus credenciales de OpenAI")
    else:
        if "agent" not in st.session_state:
            st.session_state["agent"] = load_agent()

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Hola, ¿en qué puedo ayudarte?"}
            ]

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_input := st.chat_input("Cual es tu pregunta?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                with st.spinner("Policy Pro - 🤖 Estoy pensando..."):
                    output = st.session_state["agent"].agent_executor(
                        {"input": user_input}
                    )
                assistant_response = output["output"]

                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

                # print llm memory
                print(st.session_state["agent"].memory)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
