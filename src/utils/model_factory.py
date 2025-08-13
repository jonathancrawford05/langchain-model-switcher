"""Model factory for creating model adapters."""

import os
from typing import Optional, Dict, Any

from ..models import ModelAdapter, WatsonAdapter, ClaudeAdapter, OllamaAdapter, OpenAIAdapter, PhiAdapter
from ..config import get_model_config, get_current_provider


class ModelFactory:
    """Factory for creating model adapters."""
    
    _adapters = {
        "WatsonAdapter": WatsonAdapter,
        "ClaudeAdapter": ClaudeAdapter, 
        "OllamaAdapter": OllamaAdapter,
        "OpenAIAdapter": OpenAIAdapter,
        "PhiAdapter": PhiAdapter,
    }
    
    @classmethod
    def create_model(cls, provider: Optional[str] = None, **kwargs) -> ModelAdapter:
        """Create a model adapter for the specified provider."""
        if provider is None:
            provider = get_current_provider()
        
        config = get_model_config(provider)
        
        # Get the adapter class
        adapter_class_name = config.class_name
        if adapter_class_name not in cls._adapters:
            raise ValueError(f"Unknown adapter class: {adapter_class_name}")
        
        adapter_class = cls._adapters[adapter_class_name]
        
        # Merge config with any additional kwargs
        adapter_kwargs = config.model_dump()
        adapter_kwargs.update(kwargs)
        
        # Remove class_name from kwargs as it's not needed by the adapter
        adapter_kwargs.pop('class_name', None)
        
        return adapter_class(**adapter_kwargs)
    
    @classmethod
    def get_current_model(cls) -> ModelAdapter:
        """Get the current model based on environment configuration."""
        return cls.create_model()
    
    @classmethod
    def list_available_providers(cls) -> list[str]:
        """List all available model providers."""
        from ..config.settings import Settings
        settings = Settings.load_from_file()
        return list(settings.models.keys())
    
    @classmethod
    def register_adapter(cls, name: str, adapter_class: type) -> None:
        """Register a new adapter class."""
        cls._adapters[name] = adapter_class


# Convenience function for getting the current model
def get_model(provider: Optional[str] = None) -> ModelAdapter:
    """Get a model adapter instance."""
    return ModelFactory.create_model(provider)
