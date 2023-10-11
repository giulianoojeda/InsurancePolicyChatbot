from typing import Any
from langchain.base_language import BaseLanguageModel
from langchain.chains.llm import LLMChain


class CustomQAGenerateChain(LLMChain):
    """LLM Chain specifically for generating examples for question answering."""

    def __init__(self, llm: BaseLanguageModel, eval_prompt: str, **kwargs: Any):
        super().__init__(llm=llm, prompt=eval_prompt, **kwargs)

    @classmethod
    def from_llm(cls, llm: BaseLanguageModel, eval_prompt: str, **kwargs: Any):
        """
        Load QA Generate Chain from LLM.

        Parameters:
        - llm (BaseLanguageModel): Language Model to use.
        - eval_prompt (str): Prompt to use for evaluation.
        - kwargs (Any): Additional arguments to pass to the chain.

        Returns:
        - chain (CustomQAGenerateChain): QA Generate Chain.

        """
        return cls(llm=llm, eval_prompt=eval_prompt, **kwargs)
