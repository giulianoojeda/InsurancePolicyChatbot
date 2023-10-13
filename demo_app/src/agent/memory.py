from typing import Any, Dict, List
from langchain.llms import OpenAI
from langchain.memory import ConversationSummaryBufferMemory


class Memory:
    """
    The Memory class provides a simplified interface for interacting with the
    ConversationSummaryBufferMemory.

    """

    def __init__(
        self,
        llm: OpenAI,
        memory_key: str,
    ):
        """Initialize the Memory with required components."""
        if not all([llm, memory_key]):
            raise ValueError("All parameters must be provided and not be None.")

        self.memory = self._initialize_memory(llm, memory_key)

    def _initialize_memory(
        self,
        llm: OpenAI,
        memory_key: str,
    ) -> ConversationSummaryBufferMemory:
        """
        Internal method to initialize the memory.

        Args:
            llm (OpenAI): LLM object to use for the memory.
            memory_key (str): Memory key to use for the memory.

        Returns:
            ConversationSummaryBufferMemory: Initialized memory instance.
        """

        return ConversationSummaryBufferMemory(
            memory_key=memory_key,
            llm=llm,
            max_token_limit=2500,
            return_messages=True,
            output_key="output",
            input_key="input",
        )
