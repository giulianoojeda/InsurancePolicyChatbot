import glob
import os

from chromadb.config import Settings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


class VectorStore:
    """
    The VectorStore class provides a simplified interface for fetching data using
    the Chroma vector store.

    Attributes:
        persist_directory (str): The directory where the vector store will be saved.
        embedding (OpenAIEmbeddings): The OpenAIEmbeddings instance.

    """

    def __init__(self, persist_directory: str, embedding: OpenAIEmbeddings):
        # Check that all parameters are provided
        if not all([persist_directory, embedding]):
            raise ValueError("All parameters must be provided and not be None.")

        # Check if there is a vector store in the persist directory path
        if not glob.glob(os.path.join(persist_directory, "*.parquet")):
            raise ValueError("No vector store found in the persist directory.")

        self.vector_store = self._initialize_vector_store(persist_directory, embedding)

    def _initialize_vector_store(
        self, persist_directory: str, embedding: OpenAIEmbeddings
    ) -> Chroma:
        """Initialize the vector store."""
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
