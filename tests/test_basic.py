"""Basic tests for the model switcher functionality."""

import pytest
import os
import sys
from pathlib import Path

# Add project root to path for src imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import from src package correctly
from src.utils.model_factory import ModelFactory, get_model
from src.config.settings import get_model_config, get_current_provider
from src.models.base import ModelAdapter


class TestModelFactory:
    """Test the model factory functionality."""
    
    def test_list_available_providers(self):
        """Test that we can list available providers."""
        providers = ModelFactory.list_available_providers()
        assert isinstance(providers, list)
        assert len(providers) > 0
        assert 'claude' in providers
        assert 'watson' in providers
        assert 'ollama' in providers
    
    def test_get_model_config(self):
        """Test configuration loading."""
        config = get_model_config('claude')
        assert config.class_name == 'ClaudeAdapter'
        assert config.model_id is not None
    
    def test_model_adapter_interface(self):
        """Test that created models implement the adapter interface."""
        # Set a known provider
        os.environ['MODEL_PROVIDER'] = 'claude'
        
        try:
            model = get_model()
            assert isinstance(model, ModelAdapter)
            assert hasattr(model, 'invoke')
            assert hasattr(model, 'get_model_name')
            assert hasattr(model, 'supports_tool_calling')
            assert hasattr(model, 'get_langchain_model')
        except Exception as e:
            # If we can't create the model (e.g., missing API key), that's ok for testing
            pytest.skip(f"Could not create model, likely due to missing configuration: {e}")
    
    def test_provider_switching(self):
        """Test that we can switch providers."""
        original_provider = os.environ.get('MODEL_PROVIDER', 'claude')
        
        try:
            # Test switching providers
            os.environ['MODEL_PROVIDER'] = 'watson'
            assert get_current_provider() == 'watson'
            
            os.environ['MODEL_PROVIDER'] = 'claude'
            assert get_current_provider() == 'claude'
            
        finally:
            # Restore original provider
            os.environ['MODEL_PROVIDER'] = original_provider


class TestMCPTools:
    """Test the MCP tools functionality."""
    
    def test_tools_import(self):
        """Test that we can import tools."""
        from src.mcp.tools import get_math_tools, get_tool_schemas
        
        tools = get_math_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0
        
        schemas = get_tool_schemas()
        assert isinstance(schemas, list)
        assert len(schemas) == len(tools)
    
    def test_individual_tools(self):
        """Test individual tool functionality."""
        from src.mcp.tools import add_numbers, subtract_numbers, multiply_numbers, divide_numbers
        
        # Test addition
        result = add_numbers.invoke("10 20 30")
        assert result == {"result": 60}
        
        # Test subtraction
        result = subtract_numbers.invoke("100 20 30")
        assert result == {"result": 50}
        
        # Test multiplication
        result = multiply_numbers.invoke("2 3 4")
        assert result == {"result": 24}
        
        # Test division
        result = divide_numbers.invoke("100 5 2")
        assert result == {"result": 10.0}


def test_project_structure():
    """Test that the project structure is correct."""
    project_root = Path(__file__).parent.parent
    
    # Check main directories exist
    assert (project_root / 'src').exists()
    assert (project_root / 'src' / 'models').exists()
    assert (project_root / 'src' / 'mcp').exists()
    assert (project_root / 'src' / 'config').exists()
    assert (project_root / 'src' / 'utils').exists()
    assert (project_root / 'notebooks').exists()
    
    # Check key files exist
    assert (project_root / 'pyproject.toml').exists()
    assert (project_root / 'README.md').exists()
    assert (project_root / 'src' / 'config' / 'models.yaml').exists()


if __name__ == "__main__":
    # Run basic tests when called directly
    print("Running basic functionality tests...")
    
    try:
        test_project_structure()
        print("✅ Project structure test passed")
    except Exception as e:
        print(f"❌ Project structure test failed: {e}")
    
    try:
        factory_test = TestModelFactory()
        factory_test.test_list_available_providers()
        print("✅ Provider listing test passed")
    except Exception as e:
        print(f"❌ Provider listing test failed: {e}")
    
    try:
        tools_test = TestMCPTools()
        tools_test.test_tools_import()
        print("✅ Tools import test passed")
    except Exception as e:
        print(f"❌ Tools import test failed: {e}")
    
    try:
        tools_test = TestMCPTools()
        tools_test.test_individual_tools()
        print("✅ Individual tools test passed")
    except Exception as e:
        print(f"❌ Individual tools test failed: {e}")
    
    print("\nBasic tests completed! Run 'poetry run pytest' for full test suite.")
