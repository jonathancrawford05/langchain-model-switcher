"""Configuration settings for the model switcher."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ModelConfig(BaseModel):
    """Configuration for a specific model."""
    class_name: str = Field(..., description="Model adapter class name")
    model_id: str = Field(..., description="Model identifier")
    api_key: Optional[str] = Field(None, description="API key for the model")
    base_url: Optional[str] = Field(None, description="Base URL for the model")
    url: Optional[str] = Field(None, description="URL for the model")
    project_id: Optional[str] = Field(None, description="Project ID")
    max_tokens: Optional[int] = Field(4096, description="Maximum tokens")
    temperature: Optional[float] = Field(0.1, description="Temperature setting")
    timeout: Optional[int] = Field(60, description="Timeout in seconds")


class Settings(BaseModel):
    """Main settings configuration."""
    models: Dict[str, ModelConfig]
    default_provider: str = Field("claude", description="Default model provider")
    
    @classmethod
    def load_from_file(cls, config_path: Optional[str] = None) -> "Settings":
        """Load settings from YAML file."""
        if config_path is None:
            config_path = Path(__file__).parent / "models.yaml"
        
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Convert model configs to ModelConfig objects
        models = {}
        for provider, config in data['models'].items():
            models[provider] = ModelConfig(**config)
        
        return cls(
            models=models,
            default_provider=data.get('default_provider', 'claude')
        )


def get_model_config(provider: Optional[str] = None) -> ModelConfig:
    """Get model configuration for a specific provider."""
    if provider is None:
        provider = os.getenv("MODEL_PROVIDER")
    
    settings = Settings.load_from_file()
    
    if provider is None:
        provider = settings.default_provider
    
    if provider not in settings.models:
        raise ValueError(f"Provider '{provider}' not found in configuration. Available: {list(settings.models.keys())}")
    
    config = settings.models[provider]
    
    # Override with environment variables if available
    env_overrides = {
        "api_key": os.getenv(f"{provider.upper()}_API_KEY"),
        "base_url": os.getenv(f"{provider.upper()}_BASE_URL"),
        "model_id": os.getenv(f"{provider.upper()}_MODEL_ID"),
    }
    
    # Apply non-None overrides
    config_dict = config.model_dump()
    for key, value in env_overrides.items():
        if value is not None:
            config_dict[key] = value
    
    return ModelConfig(**config_dict)


def get_current_provider() -> str:
    """Get the current model provider."""
    return os.getenv("MODEL_PROVIDER", Settings.load_from_file().default_provider)
