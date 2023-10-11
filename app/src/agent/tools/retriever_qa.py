""" This module is used to retrieve data from chromaDB database."""

from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.agents import tool
from typing import List


class RetrieverQA:
    """This class is used to retrieve data from chromaDB database."""

    def __init__(
        self,
        chroma_path: str,
        llm: OpenAI,
        document_content_description: str,
        metadata_field_info: List[AttributeInfo],
    ):
        self.vector_store: Chroma = None
        self.embedding: OpenAIEmbeddings = OpenAIEmbeddings(llm)
        self.chroma_path: str = chroma_path
        self.llm: OpenAI = llm
        self.metadata_field_info: List[AttributeInfo] = metadata_field_info
        self.document_content_description: str = document_content_description
        self._load_vector_store()

    def _load_vector_store(self):
        try:
            self.vector_store = Chroma(
                persist_directory=self.chroma_path, embedding_function=self.embedding
            )
        except Exception as e:
            raise e

    @tool
    @classmethod
    def get_retriever_sqr(cls) -> SelfQueryRetriever:
        """Self query retriever tool to retrieve data from chromaDB database.

        Returns
        -------
        SelfQueryRetriever
            A retriever that can be used to retrieve data from chromaDB database.
        """
        if cls.llm is None:
            raise ValueError("llm is not set")

        if cls.document_content_description is None:
            raise ValueError("document_content_description is not set")

        if cls.metadata_field_info is None:
            raise ValueError("metadata_field_info is not set")

        if cls.vector_store is None:
            cls._load_vector_store()

        return SelfQueryRetriever.from_llm(
            cls.llm,
            cls.vector_store,
            cls.document_content_description,
            cls.metadata_field_info,
            verbose=True,
        )

    @tool
    @classmethod
    def get_similarity_search_tool(cls, query: str, top_k: int = 5) -> List[Document]:
        """This function is used to retrieve data from chromaDB database.

        Parameters
        ----------
        query : str
            The query to search in the database.
        top_k : int, optional
            The number of results to return, by default 5.

        Returns
        -------
        list
            A list of documents that match the query.
        """

        if cls.vector_store is None:
            cls._load_vector_store()

        documents = cls.vector_store.similarity_search(query, top_k=top_k)

        return documents

    @tool
    @classmethod
    def get_max_marginal_relevance_search_tool(
        cls, query: str, k: int = 5, fetch_k: int = 10, lambda_: float = 0.5
    ) -> List[Document]:
        """This function is used to retrieve data from chromaDB database.

        Parameters
        ----------
        query : str
            The query to search in the database.
        top_k : int, optional
            The number of results to return, by default 5.
        lambda_ : float, optional
            The lambda parameter for max marginal relevance, by default 0.5.

        Returns
        -------
        list
            A list of documents that match the query.
        """

        if cls.vector_store is None:
            cls._load_vector_store()

        documents = cls.vector_store.max_marginal_relevance_search(
            query, k=k, fetch_k=fetch_k, lambda_=lambda_
        )

        return documents
