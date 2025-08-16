"""Microsoft Phi-3 model adapter."""

from typing import Any, List
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import BaseLanguageModel
from langchain_ollama import ChatOllama

from .base import ModelAdapter


class PhiAdapter(ModelAdapter):
    """Adapter for Microsoft Phi-3 models via Ollama."""

    def __init__(self, **kwargs):
        """Initialize Phi adapter."""
        super().__init__(**kwargs)
        
        self.model_id = kwargs.get("model_id", "phi3")
        self.base_url = kwargs.get("base_url", "http://localhost:11434")
        self.temperature = kwargs.get("temperature", 0.1)
        self.timeout = kwargs.get("timeout", 60)
        
        # Initialize the Ollama model with Phi3
        self.model = ChatOllama(
            model=self.model_id,
            base_url=self.base_url,
            temperature=self.temperature,
            timeout=self.timeout,
        )

    def invoke(self, messages: str | List[BaseMessage]) -> Any:
        """Invoke the Phi model."""
        if isinstance(messages, str):
            return self.model.invoke(messages)
        return self.model.invoke(messages)

    def get_model_name(self) -> str:
        """Get the Phi model name."""
        return f"Phi-{self.model_id}"

    def supports_tool_calling(self) -> bool:
        """Check if Phi model supports tool calling."""
        # Phi3 and related models support tool calling
        phi_models_with_tools = ["phi3", "phi3.5", "phi3:mini", "phi3:medium"]
        
        model_lower = self.model_id.lower()
        return any(phi_model in model_lower for phi_model in phi_models_with_tools)

    def get_langchain_model(self) -> BaseLanguageModel:
        """Get the underlying LangChain Ollama model."""
        return self.model

    def get_model_info(self) -> dict:
        """Get detailed model information."""
        return {
            "provider": "phi",
            "model_id": self.model_id,
            "base_url": self.base_url,
            "architecture": "Microsoft Phi-3",
            "size": "~2.2GB",
            "features": ["tool_calling", "compact", "efficient"],
            "description": "Microsoft Phi-3: Compact model with excellent performance"
        }
