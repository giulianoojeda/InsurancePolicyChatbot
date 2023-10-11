# import langchain related modules
import chromadb
from chromadb.config import Settings

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.agents import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import (
    AgentTokenBufferMemory,
)
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.agents import AgentExecutor


class LlmAgent:
    def __init__(
        self,
        persist_directory: str,
        openai_api_key: str,
        model_name: str,
        google_api_key: str,
        google_cse_id: str,
        temperature: float = 0,
    ) -> None:
        self.embedding = OpenAIEmbeddings()
        self.vector_store = self._initialize_vector_store(
            persist_directory, self.embedding
        )
        print(self.vector_store._persist_directory)
        print(self.vector_store._client_settings)

        self.metadata_field_info = (
            self._setup_metadata_info()
        )  # TODO : Make this a parameter
        self.llm = llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name=model_name,
            temperature=temperature,
        )
        self.retriever_sqr = self._initialize_retriever(
            "Polizas de Seguro"
        )  # TODO : Make this a parameter
        self.toolkit = [
            create_retriever_tool(
                retriever=self.retriever_sqr,
                name="retriever",
                description="""Util para cuando necesitas buscar en la base de datos de polizas de seguro para responder preguntas""",
            )
        ]
        self.memory = self._setup_memory()
        self.system_message = self._setup_system_message()
        self.prompt = self._setup_prompt()
        self.agent = OpenAIFunctionsAgent(
            llm=self.llm, tools=self.toolkit, prompt=self.prompt
        )
        self.agent_executor = self._initialize_agent_executor()

    def query(cls, input: str) -> str:
        """Interacts with the agent to get an answer for the given query.

        Args:
            input (str): Input query

        Returns:
            str: Response
        """
        return cls.agent_executor({"input": input})["output"]

    def _initialize_vector_store(
        cls, persist_directory: str, embedding: OpenAIEmbeddings
    ) -> Chroma:
        """Initialize the vector store

        Args:
            persist_directory (str): Path to the directory where the vector store is located
            embedding (OpenAIEmbeddings): Embedding function to use

        Returns:
            Chroma: Vector store
        """
        settings = Settings(
            chroma_db_impl="sqlite",
            persist_directory=persist_directory,
            anonymized_telemetry=False,
        )
        return Chroma(
            embedding_function=embedding,
            client_settings=settings,
            persist_directory=persist_directory,
        )

    def _setup_metadata_info(self):
        return [
            AttributeInfo(
                name="source",
                type="string",
                description="el nombre de archivo y codigo de la poliza de donde vino este fragmento, el formato es POL{codigo de poliza}.pdf",
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

    def _initialize_retriever(
        self, document_content_description: str
    ) -> SelfQueryRetriever:
        """
        Initialize the retriever

        Args:
            document_content_description (str): Description of the document content

        Returns:
            SelfQueryRetriever: The retriever
        """
        return SelfQueryRetriever.from_llm(
            self.llm,
            self.vector_store,
            document_content_description,
            self.metadata_field_info,
            verbose=True,
        )

    def _setup_memory(self):
        return AgentTokenBufferMemory(
            memory_key="chat_history", llm=self.llm, max_token_limit=2500
        )

    def _setup_system_message(self):
        return SystemMessage(
            content=(
                """Eres un asistente bien informado centrado en pólizas de seguro y documentos. 
        Utilizando el contexto proporcionado de nuestra base de datos de polizas de seguros, responde a la siguiente pregunta relacionada con seguros.
        Asegúrate de proporcionar sólo información relevante a las pólizas de seguro y documentos y evita responder a preguntas no relacionadas con este dominio. 
        Sientete libre de utilizar las tu herramienta de "retriever" para buscar informacion relevante y responder a la pregunta al final.
        Solo puedes usar tu herramienta de "google_search" si te lo pide el usuario explicitamente diciendo "busca en google". No lo hagas si no te lo pide explicitamente.
        Si no sabes la respuesta, simplemente di que no lo sabes, no intentes inventar una respuesta.
        Mantén la respuesta lo más concisa posible.
        
        Dado el siguiente historial de conversación:
        {chat_history}
        
        Pregunta: {input}
        Respuesta útil:"""
            )
        )

    def _setup_prompt(self):
        return OpenAIFunctionsAgent.create_prompt(
            system_message=self.system_message,
            extra_prompt_messages=[MessagesPlaceholder(variable_name="chat_history")],
        )

    def _initialize_agent_executor(self):
        return AgentExecutor(
            agent=self.agent,
            tools=self.toolkit,
            memory=self.memory,
            verbose=True,
            return_intermediate_steps=True,
        )
