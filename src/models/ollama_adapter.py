"""Ollama model adapter."""

from typing import Any, List
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import BaseLanguageModel
from langchain_ollama import ChatOllama

from .base import ModelAdapter


class OllamaAdapter(ModelAdapter):
    """Adapter for Ollama models."""

    def __init__(self, **kwargs):
        """Initialize Ollama adapter."""
        super().__init__(**kwargs)
        
        self.model_id = kwargs.get("model_id", "llama3")
        self.base_url = kwargs.get("base_url", "http://localhost:11434")
        self.temperature = kwargs.get("temperature", 0.1)
        self.timeout = kwargs.get("timeout", 60)
        
        # Initialize the Ollama model
        self.model = ChatOllama(
            model=self.model_id,
            base_url=self.base_url,
            temperature=self.temperature,
            timeout=self.timeout,
        )

    def invoke(self, messages: str | List[BaseMessage]) -> Any:
        """Invoke the Ollama model."""
        if isinstance(messages, str):
            return self.model.invoke(messages)
        return self.model.invoke(messages)

    def get_model_name(self) -> str:
        """Get the Ollama model name."""
        return f"Ollama-{self.model_id}"

    def supports_tool_calling(self) -> bool:
        """Check if Ollama model supports tool calling."""
        # Define models that support tool calling
        tool_calling_models = {
            "llama3.1": True,
            "llama3.2": True, 
            "mistral": True,
            "mistral-nemo": True,
            "qwen2.5": True,
            "qwen": True,
            "phi3": True,
            "llama3": False,  # Base llama3 does NOT support tools
            "llama2": False,
        }
        
        # Check if the model ID matches any known tool-capable models
        model_lower = self.model_id.lower()
        
        # First check exact matches
        for model_name, supports_tools in tool_calling_models.items():
            if model_name in model_lower:
                return supports_tools
        
        # Default to True for unknown models (optimistic)
        # Most modern models support tool calling
        return True

    def get_langchain_model(self) -> BaseLanguageModel:
        """Get the underlying LangChain Ollama model."""
        return self.model
