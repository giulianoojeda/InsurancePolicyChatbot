from .retriever import Retriever
from .vector_store import VectorStore
from .web_search import WebSearch
from .memory import Memory

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.agents import AgentExecutor, Tool
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
from typing import List


class LlmAgent:
    """
    LlmAgent is responsible for orchestrating the interaction between the user and
    various components of the Language Learning Model (LLM), such as the retriever,
    vector store, and web search. The agent also maintains a memory of chat interactions
    to provide contextual responses.

    Attributes:
        persist_directory (str): Path to the directory where vector embeddings are stored.
        openai_api_key (str): Key for accessing the OpenAI API.
        model_name (str): Identifier for the specific OpenAI model being utilized.
        google_api_key (str): API key for using Google's search services.
        google_cse_id (str): ID for Google's Custom Search Engine.
        document_content_description (str): Brief descriptive text concerning the content being dealt with.
        metadata_field_info (List[AttributeInfo]): Meta-information concerning fields within the content.
        temperature (float, optional): Sampling temperature for the model's responses. Defaults to 0 (deterministic).

    Methods:
        query(input_text: str) -> str: Accepts user's input and retrieves the agent's response.
    """

    # CONSTANTS
    SYSTEM_MESSAGE_CONTENT = """Eres un asistente bien informado centrado en pólizas de seguro y documentos y  
        utilizando el contexto proporcionado de nuestra base de datos de polizas de seguros, 
        responde a la siguiente pregunta relacionada con seguros.
        Solo hablas español. Asegúrate de proporcionar sólo información relevante al contenido de los contratos y pólizas de seguro.
        Mantén la respuesta lo más concisa posible.
        Si no sabes la respuesta, simplemente di que no lo sabes, no intentes inventar una respuesta.
        Utiliza tu herramienta "retriever" para buscar informacion relevante y responder a la pregunta al final.
        Si no encuentras nada en los documentos, puedes usar tu herramienta de "google_search"
        o si te lo pide el usuario explicitamente diciendo "busca en google".
        No busques en google a menos que el usuario lo pida.
        Evita responder a preguntas no relacionadas con este dominio. 
        
        Dado el siguiente historial de conversación:
        {chat_history}
        
        Pregunta: {input}
        Respuesta útil:"""

    def __init__(
        self,
        persist_directory: str,
        openai_api_key: str,
        model_name: str,
        google_api_key: str,
        google_cse_id: str,
        document_content_description: str,
        metadata_field_info: List[AttributeInfo],
        temperature: float = 0,
    ) -> None:
        """Initializes the LlmAgent."""
        # Check that all parameters are provided
        if not all(
            [
                persist_directory,
                openai_api_key,
                model_name,
                google_api_key,
                google_cse_id,
                document_content_description,
                metadata_field_info,
            ]
        ):
            raise ValueError("All parameters must be provided and not be None.")

        # Initialize embedding function
        self.embedding = OpenAIEmbeddings()

        # Initialize vector store
        self.vector_store = VectorStore(
            persist_directory=persist_directory, embedding=self.embedding
        )

        # Initialize web search
        self.web_search = WebSearch(
            google_api_key=google_api_key,
            google_cse_id=google_cse_id,
        )

        # Initialize language model
        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name=model_name,
            temperature=temperature,
        )

        # Initialize retriever
        self.retriever = Retriever(
            llm=self.llm,
            vector_store=self.vector_store.vector_store,
            document_content_description=document_content_description,
            metadata_field_info=metadata_field_info,
        )

        # Initialize toolkit (retriever tool and web search tool)
        self.toolkit = [
            create_retriever_tool(
                retriever=self.retriever.retriever,
                name="retriever",
                description="Util para cuando necesitas buscar informacion relevante en la base de datos de polizas de seguro",
            ),
            Tool(
                name="google_search",
                description="""Util para cuando necesitas buscar en internet acerca de noticias o informacion
                relevante a las polizas de seguro en general que no se encuentran en la base de datos de polizas de seguro""",
                func=self.web_search.google_search_api_wrapper.run,
            ),
        ]

        # Initialize memory
        self.memory_key = "chat_history"
        self.memory = Memory(llm=self.llm, memory_key=self.memory_key)

        # Set up the system message
        self.system_message = SystemMessage(content=self.SYSTEM_MESSAGE_CONTENT)

        # Set up the prompt
        self.prompt = OpenAIFunctionsAgent.create_prompt(
            system_message=self.system_message,
            extra_prompt_messages=[MessagesPlaceholder(variable_name=self.memory_key)],
        )

        # Set up the agent
        self.agent = OpenAIFunctionsAgent(
            llm=self.llm, tools=self.toolkit, prompt=self.prompt
        )

        # Set up the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.toolkit,
            memory=self.memory.memory,
            verbose=True,
            return_intermediate_steps=True,
        )

    def query(cls, input_text: str) -> str:
        """
        Accepts a user's query and returns the response from the LLM agent. This function
        invokes the agent_executor to process the input and generate an appropriate response.

        Args:
            input_text (str): User's query string.

        Returns:
            str: Agent's response.

        Examples:

            >>> from src.agent.llm_agent import LlmAgent
            >>> llm = LlmAgent()
            >>> llm.query("Tell me about insurance policies.")
            "Insurance policies are contracts between the insurer and the insured..."
        """
        return cls.agent_executor({"input": input_text})["output"]
