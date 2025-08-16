"""GPT opem source 20b model adapter."""

from typing import Any, List
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import BaseLanguageModel
from langchain_ollama import ChatOllama

from .base import ModelAdapter


class GPTAdapter(ModelAdapter):
    """Adapter for GPT-oss models via Ollama."""

    def __init__(self, **kwargs):
        """Initialize GPToss adapter."""
        super().__init__(**kwargs)
        
        self.model_id = kwargs.get("model_id", "gpt-oss:20b")
        self.base_url = kwargs.get("base_url", "http://localhost:11434")
        self.temperature = kwargs.get("temperature", 0.1)
        self.timeout = kwargs.get("timeout", 60)
        
        # Initialize the Ollama model with GPToss
        self.model = ChatOllama(
            model=self.model_id,
            base_url=self.base_url,
            temperature=self.temperature,
            timeout=self.timeout,
        )

    def invoke(self, messages: str | List[BaseMessage]) -> Any:
        """Invoke the GPToss model."""
        if isinstance(messages, str):
            return self.model.invoke(messages)
        return self.model.invoke(messages)

    def get_model_name(self) -> str:
        """Get the GPToss model name."""
        return f"{self.model_id}"

    def supports_tool_calling(self) -> bool:
        """Check if GPToss model supports tool calling."""
        # GPToss model supporting tool calling
        gpt_models_with_tools = ["gpt-oss:20b"]
        
        model_lower = self.model_id.lower()
        return any(gpt_model in model_lower for gpt_model in gpt_models_with_tools)

    def get_langchain_model(self) -> BaseLanguageModel:
        """Get the underlying LangChain Ollama model."""
        return self.model

    def get_model_info(self) -> dict:
        """Get detailed model information."""
        return {
            "provider": "gpt",
            "model_id": self.model_id,
            "base_url": self.base_url,
            "architecture": "gpt-oss:20b",
            "size": "~13GB",
            "features": ["tool_calling", "compact", "efficient"],
            "description": "GPT open source 20b: Large model with excellent performance"
        }
