""" Python file to serve as the front-end of the chatbot. """

import streamlit as st
from src.agent.llm_agent import LlmAgent
from src import config
from src.sidebar import sidebar
from langchain.chains.query_constructor.base import AttributeInfo


import time


def load_agent() -> LlmAgent:
    """
    Logic for loading the chatbot agent and its components.

    Args:
        None

    Returns:
        LlmAgent: The chatbot agent

    """
    print("🔧 Console: Loading agent..." + "\n")

    # set up the metadata field info
    metadata_field_info = [
        AttributeInfo(
            name="source",
            type="string",
            description="el nombre de archivo y codigo de la poliza de donde vino este chunk, el formato del codigo es POL{codigo de poliza}.pdf",
        ),
        AttributeInfo(
            name="page",
            type="integer",
            description="El numero de pagina de la poliza",
        ),
        AttributeInfo(
            name="title", type="string", description="El titulo de la poliza"
        ),
    ]

    # setup the document content description
    document_content_description = "Colección de polizas de seguros"

    # initialize the agent
    llm = LlmAgent(
        persist_directory=config.CHROMA_PATH,
        openai_api_key=config.OPENAI_API_KEY,
        model_name=config.FAST_LLM_MODEL,
        google_api_key=config.GOOGLE_API_KEY,
        google_cse_id=config.CUSTOM_SEARCH_ENGINE_ID,
        document_content_description=document_content_description,
        metadata_field_info=metadata_field_info,
    )
    return llm


def get_text():
    input_text = st.text_input("You: ", "Hola, ¿en qué puedo ayudarte?", key="input")
    return input_text


if __name__ == "__main__":
    st.set_page_config(
        page_title="🔒 Policy Pro - Insurance Chatbot",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header("🤖 Policy Pro: Demostración")
    sidebar()

    if not config.OPENAI_API_KEY:
        st.error("⚠️ Por favor, configure sus credenciales de OpenAI")
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

        if user_input := st.chat_input("❓ Cual es tu pregunta?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                with st.spinner("🧠 Estoy pensando..."):
                    assistant_response = output = st.session_state["agent"].query(
                        user_input
                    )

                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
