"""LangChain Model Switcher - A minimalistic framework for switching between LLM providers."""

from .models import ModelAdapter, WatsonAdapter, ClaudeAdapter, OllamaAdapter, OpenAIAdapter
from .utils import ModelFactory, get_model
from .config import get_model_config, get_current_provider

__version__ = "0.1.0"

__all__ = [
    "ModelAdapter",
    "WatsonAdapter", 
    "ClaudeAdapter",
    "OllamaAdapter",
    "OpenAIAdapter",
    "ModelFactory",
    "get_model",
    "get_model_config",
    "get_current_provider",
]
