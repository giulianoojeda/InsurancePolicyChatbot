from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from typing import List


class Retriever:
    """
    The Retriever class provides a simplified interface for fetching data using
    the SelfQueryRetriever.

    Attributes:
        llm (OpenAI): The language model instance.
        vector_store (Chroma): The storage for vector data.
        document_content_description (str): A descriptive text about the content.
        metadata_field_info (List[AttributeInfo]): Information on metadata fields.

    """

    def __init__(
        self,
        llm: OpenAI,
        vector_store: Chroma,
        document_content_description: str,
        metadata_field_info: List[AttributeInfo],
    ):
        """Initialize the Retriever with required components."""
        if not all(
            [llm, vector_store, document_content_description, metadata_field_info]
        ):
            raise ValueError("All parameters must be provided and not be None.")

        self.retriever = self._initialize_retriever(
            llm, vector_store, document_content_description, metadata_field_info
        )

    def _initialize_retriever(
        self,
        llm: OpenAI,
        vector_store: Chroma,
        document_content_description: str,
        metadata_field_info: List[AttributeInfo],
    ) -> SelfQueryRetriever:
        """
        Internal method to initialize the retriever.

        Args:
            llm (OpenAI): LLM object to use for the retriever.
            vector_store (Chroma): Vector store to use for the retriever.
            document_content_description (str): Description of the document content.
            metadata_field_info (List[AttributeInfo]): Document metadata field info.

        Returns:
            SelfQueryRetriever: Initialized retriever instance.
        """

        return SelfQueryRetriever.from_llm(
            llm,
            vector_store,
            document_content_description,
            metadata_field_info,
            verbose=True,
        )
