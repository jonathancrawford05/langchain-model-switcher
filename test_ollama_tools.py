#!/usr/bin/env python3
"""
Test tool calling capability with Ollama models.
This specifically tests if a model can handle function/tool calling.
"""

import sys
import json
from pathlib import Path

def test_tool_calling():
    """Test if the current Ollama model supports tool calling."""
    print("🧪 Testing Ollama Tool Calling Support")
    print("=" * 45)
    
    # Setup project imports
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    try:
        import os
        from src.utils.model_factory import get_model
        
        # Set to use Ollama
        os.environ["MODEL_PROVIDER"] = "ollama"
        
        print("1️⃣ Getting Ollama adapter...")
        adapter = get_model()
        model = adapter.get_langchain_model()
        
        print(f"   📋 Model: {adapter.get_model_name()}")
        print(f"   🔗 URL: {model.base_url}")
        print(f"   🤖 Model ID: {model.model}")
        print(f"   🛠️ Adapter says tools supported: {adapter.supports_tool_calling()}")
        
        # Test 1: Simple query (should work with any model)
        print("\n2️⃣ Testing basic query...")
        try:
            response = model.invoke("What is 2+2? Answer with just the number.")
            print(f"   ✅ Basic query works: {response.content}")
        except Exception as e:
            print(f"   ❌ Basic query failed: {e}")
            return False
        
        # Test 2: Tool calling test
        print("\n3️⃣ Testing tool calling capability...")
        
        # Import our tools
        from src.mcp.tools import add_numbers
        from langgraph.prebuilt import create_react_agent
        
        # Create agent with tools
        try:
            agent = create_react_agent(
                model=model,
                tools=[add_numbers],
                prompt="You are a helpful assistant. Use tools when needed."
            )
            print("   ✅ Agent created successfully")
            
            # Test with a query that requires tool use
            print("\n4️⃣ Testing actual tool usage...")
            test_query = "Add the numbers 10, 20, and 30 together"
            
            response = agent.invoke({
                "messages": [("human", test_query)]
            })
            
            final_message = response["messages"][-1].content
            print(f"   🎯 Query: {test_query}")
            print(f"   🤖 Response: {final_message}")
            
            # Check if the tool was actually used
            tool_used = any(
                hasattr(msg, 'name') and msg.name == 'add_numbers' 
                for msg in response["messages"]
            )
            
            if tool_used:
                print("   🎉 SUCCESS! Tool calling works!")
                return True
            else:
                print("   ⚠️ Model responded but didn't use tools")
                print("   💡 This model may not support function calling")
                return False
                
        except Exception as e:
            print(f"   ❌ Tool calling test failed: {e}")
            print("   💡 This usually means the model doesn't support function calling")
            return False
            
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def show_upgrade_instructions():
    """Show instructions for upgrading to a tool-capable model."""
    print("\n🔧 How to Upgrade to Tool-Capable Model")
    print("=" * 45)
    
    print("📥 RECOMMENDED: Install Llama 3.1 (upgrade from Llama 3)")
    print("   Command: ollama run llama3.1")
    print("   Size: ~4.7GB")
    print("   Benefits: Same size as llama3, but with tool calling!")
    print()
    
    print("🏃 ALTERNATIVE: Install Mistral (different model family)")
    print("   Command: ollama run mistral")
    print("   Size: ~4.1GB") 
    print("   Benefits: Excellent tool calling, slightly smaller")
    print()
    
    print("⚡ COMPACT OPTION: Install Llama 3.2 (smaller & faster)")
    print("   Command: ollama run llama3.2")
    print("   Size: ~2.0GB")
    print("   Benefits: Smaller, faster, still supports tools")
    print()
    
    print("🔄 After installing, update your config:")
    print("   Edit: src/config/models.yaml")
    print("   Change: model_id: 'llama3' → model_id: 'llama3.1'")
    print("   (or whatever model you installed)")

def update_config_for_model(model_name):
    """Update the configuration file for a new model."""
    print(f"\n🔧 Updating config for {model_name}...")
    
    config_path = Path(__file__).parent / "src/config/models.yaml"
    
    try:
        # Read current config
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Update the model_id for ollama
        import re
        pattern = r'(ollama:\s*\n\s*class_name:\s*"OllamaAdapter"\s*\n\s*model_id:\s*")[^"]*(")'
        replacement = f'\\1{model_name}\\2'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            # Write back
            with open(config_path, 'w') as f:
                f.write(new_content)
            print(f"   ✅ Updated config to use {model_name}")
            return True
        else:
            print(f"   ⚠️ Could not automatically update config")
            print(f"   💡 Manually edit src/config/models.yaml")
            print(f"   Change ollama model_id to: {model_name}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error updating config: {e}")
        return False

def main():
    """Main function."""
    # Test current setup
    tool_calling_works = test_tool_calling()
    
    if tool_calling_works:
        print("\n🎉 EXCELLENT! Your current model supports tool calling!")
        print("🚀 Your model switcher is ready to use with tools!")
    else:
        print("\n📋 Summary: Your current model doesn't support tool calling")
        show_upgrade_instructions()
        
        print("\n❓ Want to upgrade now? Here's what to do:")
        print("1. Run: ollama run llama3.1")
        print("2. Wait for download to complete")
        print("3. Run this script again to test")
        print("4. Update your config if needed")

if __name__ == "__main__":
    main()
