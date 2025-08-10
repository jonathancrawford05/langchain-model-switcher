#!/usr/bin/env python3
"""
Simple demo of the model switcher functionality.
This shows the correct way to import and use the package.
"""

import os
import sys
from pathlib import Path

def demo():
    """Demo the model switcher."""
    print("🚀 LangChain Model Switcher Demo")
    print("=" * 40)
    
    # Add project root to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    try:
        # Import the package correctly
        from src.utils.model_factory import ModelFactory, get_model
        from src.mcp.tools import add_numbers, multiply_numbers
        
        print("✅ Imports successful")
        
        # Show available providers
        providers = ModelFactory.list_available_providers()
        print(f"📋 Available providers: {providers}")
        
        # Test tools
        print("\n🧮 Testing tools:")
        result1 = add_numbers.invoke("15 25")
        result2 = multiply_numbers.invoke("6 7")
        print(f"   15 + 25 = {result1['result']}")
        print(f"   6 × 7 = {result2['result']}")
        
        # Test model switching
        print("\n🔄 Testing model switching:")
        for provider in ["claude", "watson"]:
            try:
                os.environ["MODEL_PROVIDER"] = provider
                adapter = get_model()
                print(f"   ✅ {provider}: {adapter.get_model_name()}")
            except Exception as e:
                print(f"   ⚠️ {provider}: {str(e)[:40]}...")
        
        print("\n🎉 Demo completed!")
        print("\n📖 Usage:")
        print("   os.environ['MODEL_PROVIDER'] = 'claude'")
        print("   model = get_model().get_langchain_model()")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    demo()
