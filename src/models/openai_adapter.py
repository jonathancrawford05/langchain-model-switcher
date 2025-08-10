"""OpenAI model adapter."""

from typing import Any, List
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai import ChatOpenAI

from .base import ModelAdapter


class OpenAIAdapter(ModelAdapter):
    """Adapter for OpenAI models."""

    def __init__(self, **kwargs):
        """Initialize OpenAI adapter."""
        super().__init__(**kwargs)
        
        self.model_id = kwargs.get("model_id", "gpt-4.1-nano")
        self.api_key = kwargs.get("api_key")
        self.max_tokens = kwargs.get("max_tokens", 4096)
        self.temperature = kwargs.get("temperature", 0.1)
        
        # Initialize the OpenAI model
        openai_kwargs = {
            "model": self.model_id,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        
        if self.api_key:
            openai_kwargs["api_key"] = self.api_key
            
        self.model = ChatOpenAI(**openai_kwargs)

    def invoke(self, messages: str | List[BaseMessage]) -> Any:
        """Invoke the OpenAI model."""
        if isinstance(messages, str):
            return self.model.invoke(messages)
        return self.model.invoke(messages)

    def get_model_name(self) -> str:
        """Get the OpenAI model name."""
        return f"OpenAI-{self.model_id}"

    def supports_tool_calling(self) -> bool:
        """Check if OpenAI model supports tool calling."""
        # Most OpenAI models support tool calling
        return True

    def get_langchain_model(self) -> BaseLanguageModel:
        """Get the underlying LangChain OpenAI model."""
        return self.model
