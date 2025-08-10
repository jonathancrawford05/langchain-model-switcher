"""IBM Watson model adapter."""

from typing import Any, List
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import BaseLanguageModel
from langchain_ibm import ChatWatsonx

from .base import ModelAdapter


class WatsonAdapter(ModelAdapter):
    """Adapter for IBM Watson models."""

    def __init__(self, **kwargs):
        """Initialize Watson adapter."""
        super().__init__(**kwargs)
        
        self.model_id = kwargs.get("model_id", "ibm/granite-3-2-8b-instruct")
        self.url = kwargs.get("url", "https://us-south.ml.cloud.ibm.com")
        self.project_id = kwargs.get("project_id", "skills-network")
        self.api_key = kwargs.get("api_key")
        
        # Initialize the Watson model
        watson_kwargs = {
            "model_id": self.model_id,
            "url": self.url,
            "project_id": self.project_id,
        }
        
        if self.api_key:
            watson_kwargs["api_key"] = self.api_key
            
        self.model = ChatWatsonx(**watson_kwargs)

    def invoke(self, messages: str | List[BaseMessage]) -> Any:
        """Invoke the Watson model."""
        if isinstance(messages, str):
            return self.model.invoke(messages)
        return self.model.invoke(messages)

    def get_model_name(self) -> str:
        """Get the Watson model name."""
        return f"Watson-{self.model_id}"

    def supports_tool_calling(self) -> bool:
        """Check if Watson model supports tool calling."""
        # Most Watson models support structured outputs but may vary
        return True

    def get_langchain_model(self) -> BaseLanguageModel:
        """Get the underlying LangChain Watson model."""
        return self.model
