#!/usr/bin/env python3
"""
Quick demo script to show the model switcher in action.
Run this after setting up the project to see how it works.
"""

import os
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

def demo_basic_functionality():
    """Demonstrate basic model switching functionality."""
    print("🚀 LangChain Model Switcher Demo")
    print("=" * 50)
    
    try:
        from utils.model_factory import ModelFactory, get_model
        from config.settings import get_current_provider
        from mcp.tools import get_math_tools
        
        print("✅ Successfully imported all modules")
        
        # Show available providers
        providers = ModelFactory.list_available_providers()
        print(f"📋 Available providers: {providers}")
        
        # Show available tools
        tools = get_math_tools()
        print(f"🛠️  Available tools: {[tool.name for tool in tools]}")
        
        # Test tool functionality
        print("\n🧮 Testing mathematical tools:")
        from mcp.tools import add_numbers, multiply_numbers
        
        result1 = add_numbers.invoke("10 20 30")
        print(f"  Addition (10 + 20 + 30): {result1}")
        
        result2 = multiply_numbers.invoke("3 4 5")
        print(f"  Multiplication (3 × 4 × 5): {result2}")
        
        # Test model switching (without actually invoking models)
        print("\n🔄 Testing model adapter creation:")
        
        test_providers = ["claude", "watson", "ollama"]
        for provider in test_providers:
            try:
                os.environ["MODEL_PROVIDER"] = provider
                adapter = get_model()
                print(f"  ✅ {provider}: {adapter.get_model_name()}")
                print(f"     - Supports tool calling: {adapter.supports_tool_calling()}")
            except Exception as e:
                print(f"  ⚠️  {provider}: {str(e)[:60]}...")
        
        print("\n🎉 Demo completed successfully!")
        print("\n📖 Next steps:")
        print("1. Set up API keys in .env file")
        print("2. Run: poetry shell")
        print("3. Start notebook: jupyter notebook notebooks/math_assistant.ipynb")
        print("4. Or start MCP server: python -m src.mcp.server")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you've run: poetry install")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Check your Python path and dependencies")

if __name__ == "__main__":
    demo_basic_functionality()
