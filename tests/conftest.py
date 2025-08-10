"""Pytest configuration and fixtures."""

import sys
from pathlib import Path
import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up the test environment."""
    # Ensure src is in the path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Set a default model provider for testing
    import os
    if "MODEL_PROVIDER" not in os.environ:
        os.environ["MODEL_PROVIDER"] = "claude"

@pytest.fixture
def temp_model_provider():
    """Fixture to temporarily change model provider."""
    import os
    original = os.environ.get("MODEL_PROVIDER")
    
    def _set_provider(provider):
        os.environ["MODEL_PROVIDER"] = provider
        return provider
    
    yield _set_provider
    
    # Restore original
    if original:
        os.environ["MODEL_PROVIDER"] = original
    elif "MODEL_PROVIDER" in os.environ:
        del os.environ["MODEL_PROVIDER"]
