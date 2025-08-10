"""Base model adapter interface for unified model access."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import BaseLanguageModel


class ModelAdapter(ABC):
    """Abstract base class for model adapters."""

    def __init__(self, **kwargs):
        """Initialize the model adapter with configuration."""
        self.config = kwargs

    @abstractmethod
    def invoke(self, messages: str | List[BaseMessage]) -> Any:
        """Invoke the model with messages."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name/identifier."""
        pass

    @abstractmethod
    def supports_tool_calling(self) -> bool:
        """Check if the model supports tool calling."""
        pass

    @abstractmethod
    def get_langchain_model(self) -> BaseLanguageModel:
        """Get the underlying LangChain model object."""
        pass

    def __str__(self) -> str:
        """String representation of the adapter."""
        return f"{self.__class__.__name__}({self.get_model_name()})"

    def __repr__(self) -> str:
        """Detailed representation of the adapter."""
        return f"{self.__class__.__name__}(model={self.get_model_name()}, config={self.config})"
