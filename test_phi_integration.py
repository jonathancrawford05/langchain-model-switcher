#!/usr/bin/env python3
"""
Test the new Phi adapter to verify it works correctly.
This tests that phi3 is treated as a separate model provider.
"""

import sys
import os
from pathlib import Path

def test_phi_adapter():
    """Test the new Phi adapter functionality."""
    print("🧪 Testing Phi Adapter Integration")
    print("=" * 45)
    
    # Setup project imports
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    try:
        # Test 1: Import the new adapter
        print("1️⃣ Testing imports...")
        from src.utils.model_factory import ModelFactory, get_model
        from src.models.phi_adapter import PhiAdapter
        print("   ✅ PhiAdapter imports successfully")
        
        # Test 2: Check it's registered in the factory
        print("\n2️⃣ Testing factory registration...")
        providers = ModelFactory.list_available_providers()
        print(f"   📋 Available providers: {providers}")
        
        if "phi" in providers:
            print("   ✅ Phi provider is registered")
        else:
            print("   ❌ Phi provider not found in available providers")
            return False
        
        # Test 3: Create phi adapter
        print("\n3️⃣ Testing phi adapter creation...")
        os.environ["MODEL_PROVIDER"] = "phi"
        
        adapter = get_model()
        print(f"   🤖 Created adapter: {adapter}")
        print(f"   🏷️ Model name: {adapter.get_model_name()}")
        print(f"   🛠️ Tool support: {adapter.supports_tool_calling()}")
        
        # Verify it's the right type
        if isinstance(adapter, PhiAdapter):
            print("   ✅ Correct adapter type (PhiAdapter)")
        else:
            print(f"   ❌ Wrong adapter type: {type(adapter)}")
            return False
        
        # Test 4: Check model info
        print("\n4️⃣ Testing model information...")
        model_info = adapter.get_model_info()
        print(f"   📊 Provider: {model_info['provider']}")
        print(f"   🔧 Architecture: {model_info['architecture']}")
        print(f"   💾 Size: {model_info['size']}")
        print(f"   ⚡ Features: {model_info['features']}")
        
        # Test 5: Compare with ollama adapter
        print("\n5️⃣ Testing provider switching...")
        
        # Switch to ollama
        os.environ["MODEL_PROVIDER"] = "ollama"
        ollama_adapter = get_model()
        print(f"   🦙 Ollama adapter: {ollama_adapter.get_model_name()}")
        
        # Switch back to phi
        os.environ["MODEL_PROVIDER"] = "phi"
        phi_adapter = get_model()
        print(f"   🔬 Phi adapter: {phi_adapter.get_model_name()}")
        
        # Verify they're different
        if ollama_adapter.get_model_name() != phi_adapter.get_model_name():
            print("   ✅ Different model names - providers are distinct")
        else:
            print("   ❌ Same model names - providers not properly separated")
            return False
        
        # Test 6: Check underlying configuration
        print("\n6️⃣ Testing configuration...")
        from src.config.settings import get_model_config
        
        phi_config = get_model_config("phi")
        ollama_config = get_model_config("ollama")
        
        print(f"   🔬 Phi model ID: {phi_config.model_id}")
        print(f"   🦙 Ollama model ID: {ollama_config.model_id}")
        print(f"   🏭 Phi adapter class: {phi_config.class_name}")
        print(f"   🏭 Ollama adapter class: {ollama_config.class_name}")
        
        if phi_config.class_name == "PhiAdapter" and ollama_config.class_name == "OllamaAdapter":
            print("   ✅ Correct adapter classes configured")
        else:
            print("   ❌ Incorrect adapter class configuration")
            return False
        
        print("\n🎉 SUCCESS! Phi adapter is properly integrated!")
        print("\n📋 Summary:")
        print(f"   • 'phi' provider → {phi_adapter.get_model_name()}")
        print(f"   • 'ollama' provider → {ollama_adapter.get_model_name()}")
        print(f"   • Both use localhost:11434 but are treated as separate models")
        print(f"   • Easy switching: MODEL_PROVIDER=phi or MODEL_PROVIDER=ollama")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_usage_examples():
    """Show how to use the new phi provider."""
    print("\n🎯 Usage Examples")
    print("=" * 20)
    
    print("💡 In your notebook or scripts:")
    print()
    print("# Switch to Phi3 model")
    print("os.environ['MODEL_PROVIDER'] = 'phi'")
    print("phi_model = get_model()")
    print("print(f'Using: {phi_model.get_model_name()}')")
    print()
    print("# Switch to Llama 3.1 model") 
    print("os.environ['MODEL_PROVIDER'] = 'ollama'")
    print("llama_model = get_model()")
    print("print(f'Using: {llama_model.get_model_name()}')")
    print()
    print("🔄 Easy comparison in notebook:")
    print("   Cell 1: MODEL_PROVIDER = 'phi'")
    print("   Cell 2: MODEL_PROVIDER = 'ollama'")
    print("   → Same code, different models!")

def main():
    """Main test function."""
    success = test_phi_adapter()
    
    if success:
        show_usage_examples()
        print("\n🚀 Ready for testing! You now have:")
        print("   • 'phi' → Microsoft Phi3 (compact, efficient)")
        print("   • 'ollama' → Llama 3.1 (larger, more capable)")
        print("   • Both support tool calling")
        print("   • Both run locally via Ollama")
        print("   • Treated as separate providers for easy comparison")
    else:
        print("\n❌ Integration test failed")
        print("💡 Check the error messages above")

if __name__ == "__main__":
    main()
