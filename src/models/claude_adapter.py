"""Anthropic Claude model adapter."""

from typing import Any, List
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import BaseLanguageModel
from langchain_anthropic import ChatAnthropic

from .base import ModelAdapter


class ClaudeAdapter(ModelAdapter):
    """Adapter for Anthropic Claude models."""

    def __init__(self, **kwargs):
        """Initialize Claude adapter."""
        super().__init__(**kwargs)
        
        self.model_id = kwargs.get("model_id", "claude-3-sonnet-20240229")
        self.api_key = kwargs.get("api_key")
        self.max_tokens = kwargs.get("max_tokens", 4096)
        self.temperature = kwargs.get("temperature", 0.1)
        
        # Initialize the Claude model
        claude_kwargs = {
            "model": self.model_id,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        
        if self.api_key:
            claude_kwargs["api_key"] = self.api_key
            
        self.model = ChatAnthropic(**claude_kwargs)

    def invoke(self, messages: str | List[BaseMessage]) -> Any:
        """Invoke the Claude model."""
        if isinstance(messages, str):
            return self.model.invoke(messages)
        return self.model.invoke(messages)

    def get_model_name(self) -> str:
        """Get the Claude model name."""
        return f"Claude-{self.model_id}"

    def supports_tool_calling(self) -> bool:
        """Check if Claude model supports tool calling."""
        # Claude 3 models support tool calling
        return "claude-3" in self.model_id.lower()

    def get_langchain_model(self) -> BaseLanguageModel:
        """Get the underlying LangChain Claude model."""
        return self.model
