#!/usr/bin/env python3
"""
Check which Ollama models are available and which support tool calling.
This helps identify models to download for tool calling support.
"""

import requests
import json

def check_ollama_server():
    """Check if Ollama server is running and what models are available."""
    print("🔍 Checking Ollama Server & Available Models")
    print("=" * 50)
    
    try:
        # Check if server is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("❌ Ollama server not responding")
            return False, []
        
        data = response.json()
        models = data.get('models', [])
        
        print(f"✅ Ollama server running on localhost:11434")
        print(f"📋 You have {len(models)} model(s) installed:")
        
        if not models:
            print("   (No models installed)")
            return True, []
        
        for model in models:
            name = model.get('name', 'Unknown')
            size = model.get('size', 0) / (1024**3)  # Convert to GB
            modified = model.get('modified_at', '')
            print(f"   🤖 {name} ({size:.1f} GB)")
        
        return True, [m.get('name', '') for m in models]
        
    except requests.exceptions.ConnectionError:
        print("❌ Ollama server not running")
        print("💡 Start with: ollama serve")
        return False, []
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, []

def get_tool_calling_models():
    """Get list of Ollama models that support tool/function calling."""
    return {
        # Llama family (tool calling support)
        "llama3.1": {
            "supports_tools": True,
            "size": "4.7GB",
            "description": "Meta Llama 3.1 8B - Excellent tool calling support",
            "command": "ollama run llama3.1"
        },
        "llama3.1:70b": {
            "supports_tools": True,
            "size": "40GB",
            "description": "Meta Llama 3.1 70B - Best quality, large size",
            "command": "ollama run llama3.1:70b"
        },
        "llama3.2": {
            "supports_tools": True,
            "size": "2.0GB",
            "description": "Meta Llama 3.2 3B - Smaller, faster, supports tools",
            "command": "ollama run llama3.2"
        },
        
        # Mistral family (excellent tool support)
        "mistral": {
            "supports_tools": True,
            "size": "4.1GB", 
            "description": "Mistral 7B - Great tool calling, efficient",
            "command": "ollama run mistral"
        },
        "mistral-nemo": {
            "supports_tools": True,
            "size": "7.1GB",
            "description": "Mistral Nemo 12B - Excellent tool calling",
            "command": "ollama run mistral-nemo"
        },
        
        # Qwen family (good tool support)
        "qwen2.5": {
            "supports_tools": True,
            "size": "4.7GB",
            "description": "Qwen 2.5 7B - Good tool calling support",
            "command": "ollama run qwen2.5"
        },
        
        # Phi family
        "phi3": {
            "supports_tools": True,
            "size": "2.2GB",
            "description": "Microsoft Phi-3 Mini - Compact with tool support",
            "command": "ollama run phi3"
        },
        
        # Models that DON'T support tools (for reference)
        "llama3": {
            "supports_tools": False,
            "size": "4.7GB",
            "description": "Meta Llama 3 8B - Base version, NO tool calling",
            "command": "ollama run llama3"
        }
    }

def analyze_current_setup(installed_models):
    """Analyze current models and recommend upgrades."""
    print("\n🔍 Analyzing Your Current Setup")
    print("=" * 40)
    
    available_models = get_tool_calling_models()
    
    tool_capable = []
    non_tool_capable = []
    
    for model_name in installed_models:
        # Clean up model name (remove tags)
        base_name = model_name.split(':')[0]
        
        if base_name in available_models:
            model_info = available_models[base_name]
            if model_info["supports_tools"]:
                tool_capable.append((model_name, model_info))
            else:
                non_tool_capable.append((model_name, model_info))
        else:
            # Unknown model, assume no tool support
            non_tool_capable.append((model_name, {"supports_tools": False, "description": "Unknown model"}))
    
    print(f"✅ Models with tool calling support: {len(tool_capable)}")
    for model_name, info in tool_capable:
        print(f"   🛠️ {model_name} - {info['description']}")
    
    print(f"❌ Models without tool calling: {len(non_tool_capable)}")
    for model_name, info in non_tool_capable:
        print(f"   🚫 {model_name} - {info['description']}")
    
    return tool_capable, non_tool_capable

def recommend_models():
    """Recommend models to install for tool calling."""
    print("\n🎯 Recommended Models for Tool Calling")
    print("=" * 45)
    
    recommendations = [
        {
            "name": "llama3.1",
            "priority": "HIGH",
            "reason": "Upgrade from your llama3 - excellent tool support",
            "size": "4.7GB",
            "command": "ollama run llama3.1"
        },
        {
            "name": "mistral",
            "priority": "HIGH", 
            "reason": "Excellent tool calling, very reliable",
            "size": "4.1GB",
            "command": "ollama run mistral"
        },
        {
            "name": "llama3.2",
            "priority": "MEDIUM",
            "reason": "Smaller and faster than 3.1, still good tools",
            "size": "2.0GB", 
            "command": "ollama run llama3.2"
        },
        {
            "name": "phi3",
            "priority": "MEDIUM",
            "reason": "Most compact with tool support",
            "size": "2.2GB",
            "command": "ollama run phi3"
        }
    ]
    
    for rec in recommendations:
        priority_emoji = "🔥" if rec["priority"] == "HIGH" else "⭐"
        print(f"{priority_emoji} {rec['name']} ({rec['size']})")
        print(f"   📋 {rec['reason']}")
        print(f"   💾 Install: {rec['command']}")
        print()

def main():
    """Main function to check setup and provide recommendations."""
    # Check server and current models
    server_ok, installed_models = check_ollama_server()
    
    if not server_ok:
        return
    
    # Analyze what's installed
    if installed_models:
        tool_capable, non_tool_capable = analyze_current_setup(installed_models)
        
        if tool_capable:
            print(f"\n🎉 Good news! You have {len(tool_capable)} model(s) that support tools!")
            print("💡 Update your config to use one of these models.")
        else:
            print(f"\n⚠️ None of your {len(installed_models)} model(s) support tool calling.")
            print("💡 You'll need to install a model that supports tools.")
    else:
        print("\n📥 No models installed yet.")
    
    # Show recommendations
    recommend_models()
    
    # Show next steps
    print("🚀 Next Steps:")
    print("1. Install a recommended model (commands above)")
    print("2. Update src/config/models.yaml with the new model name")
    print("3. Test with: python verify_ollama_local.py")
    print("4. Run your notebook to test tool calling!")

if __name__ == "__main__":
    main()
