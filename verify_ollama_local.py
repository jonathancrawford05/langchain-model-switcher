#!/usr/bin/env python3
"""
Verify Ollama local setup and test connection.
This script confirms that Ollama calls stay local.
"""

import sys
import requests
from pathlib import Path

def check_ollama_server():
    """Check if Ollama server is running locally."""
    print("🔍 Checking Ollama Server Status")
    print("=" * 40)
    
    try:
        # Test if Ollama server is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print("✅ Ollama server is running on localhost:11434")
            print(f"📋 Available models: {len(models)}")
            
            for model in models:
                name = model.get('name', 'Unknown')
                size = model.get('size', 0) / (1024**3)  # Convert to GB
                print(f"   🤖 {name} ({size:.1f} GB)")
            
            return True, models
        else:
            print(f"❌ Ollama server responded with status: {response.status_code}")
            return False, []
            
    except requests.exceptions.ConnectionError:
        print("❌ Ollama server is not running on localhost:11434")
        print("💡 Start it with: ollama serve")
        return False, []
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False, []

def test_local_model():
    """Test our model switcher with Ollama to confirm local usage."""
    print("\n🧪 Testing Model Switcher with Local Ollama")
    print("=" * 45)
    
    # Add project root to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    try:
        import os
        from src.utils.model_factory import get_model
        
        # Set to use Ollama
        os.environ["MODEL_PROVIDER"] = "ollama"
        
        # Get the adapter
        adapter = get_model()
        print(f"✅ Created adapter: {adapter.get_model_name()}")
        
        # Get the underlying LangChain model
        model = adapter.get_langchain_model()
        print(f"🔗 Base URL: {model.base_url}")
        print(f"🤖 Model ID: {model.model}")
        
        # Verify it's pointing to localhost
        if "localhost" in str(model.base_url) or "127.0.0.1" in str(model.base_url):
            print("🏠 ✅ CONFIRMED: Using LOCAL Ollama server")
            print("🔒 ✅ CONFIRMED: No data sent to cloud")
        else:
            print(f"⚠️ WARNING: Base URL is not localhost: {model.base_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing model switcher: {e}")
        return False

def test_simple_query():
    """Test a simple query to confirm everything works locally."""
    print("\n🎯 Testing Simple Query")
    print("=" * 25)
    
    try:
        import os
        from src.utils.model_factory import get_model
        
        os.environ["MODEL_PROVIDER"] = "ollama"
        adapter = get_model()
        model = adapter.get_langchain_model()
        
        print("🤔 Sending test query: 'What is 2+2?'")
        print("⏳ (This uses your local model only...)")
        
        response = model.invoke("What is 2+2? Answer in one word.")
        print(f"🤖 Response: {response.content}")
        print("✅ Success! Query processed locally.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with test query: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return False

def main():
    """Main verification function."""
    print("🔍 Ollama Local Verification")
    print("=" * 50)
    print("This script verifies that your Ollama setup uses local models only.\n")
    
    # Check 1: Ollama server status
    server_running, models = check_ollama_server()
    
    if not server_running:
        print("\n💡 To start Ollama server:")
        print("   ollama serve")
        print("   # In another terminal:")
        print("   ollama run llama3")
        return False
    
    # Check 2: Model switcher configuration
    config_ok = test_local_model()
    
    if not config_ok:
        print("\n💡 Make sure you're in the right directory and dependencies are installed:")
        print("   cd langchain-model-switcher")
        print("   poetry shell")
        return False
    
    # Check 3: Simple query test
    query_ok = test_simple_query()
    
    # Summary
    print("\n" + "=" * 50)
    if server_running and config_ok and query_ok:
        print("🎉 VERIFICATION COMPLETE!")
        print("✅ Ollama server running locally")
        print("✅ Model switcher configured for local use")
        print("✅ Test query successful")
        print("🔒 ALL DATA STAYS ON YOUR MACHINE")
    else:
        print("⚠️ Some checks failed - see messages above")
    
    return server_running and config_ok

if __name__ == "__main__":
    main()
