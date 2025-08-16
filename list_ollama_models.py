#!/usr/bin/env python3
"""
List all Ollama models available locally and their tool calling capabilities.
This helps identify which models you have and which support tools.
"""

import subprocess
import requests
import json
from datetime import datetime

def list_ollama_models_cli():
    """List models using Ollama CLI."""
    print("📋 Ollama Models (via CLI)")
    print("-" * 30)
    
    try:
        result = subprocess.run(['ollama', 'list'], 
                               capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"❌ CLI failed: {result.stderr}")
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"❌ Ollama CLI not available: {e}")
        return False

def list_ollama_models_api():
    """List models using Ollama API."""
    print("\n🔗 Ollama Models (via API)")
    print("-" * 30)
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            if not models:
                print("No models found")
                return []
            
            print(f"Found {len(models)} model(s):")
            print()
            
            model_list = []
            for model in models:
                name = model.get('name', 'Unknown')
                size = model.get('size', 0) / (1024**3)  # Convert to GB
                modified = model.get('modified_at', '')
                
                # Parse modified date
                try:
                    if modified:
                        dt = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                        date_str = dt.strftime('%Y-%m-%d %H:%M')
                    else:
                        date_str = 'Unknown'
                except:
                    date_str = 'Unknown'
                
                print(f"🤖 {name}")
                print(f"   💾 Size: {size:.1f} GB")
                print(f"   📅 Modified: {date_str}")
                print()
                
                model_list.append({
                    'name': name,
                    'size_gb': round(size, 1),
                    'modified': date_str
                })
            
            return model_list
            
        else:
            print(f"❌ API failed: {response.status_code}")
            return []
            
    except requests.exceptions.ConnectionError:
        print("❌ Ollama server not running on localhost:11434")
        print("💡 Start with: ollama serve")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def check_tool_calling_support(model_name):
    """Check if a model supports tool calling based on known capabilities."""
    
    # Known tool-calling models
    tool_calling_models = {
        # Llama family
        "llama3.1": True,
        "llama3.2": True,
        "llama3": False,  # Base llama3 doesn't support tools
        "llama2": False,
        
        # Mistral family  
        "mistral": True,
        "mistral-nemo": True,
        "mixtral": True,
        
        # Microsoft family
        "phi3": True,
        "phi3.5": True,
        
        # Qwen family
        "qwen2.5": True,
        "qwen2": True,
        "qwen": True,
        
        # CodeLlama
        "codellama": True,
        
        # Other models
        "gemma": True,
        "gemma2": True,
        
        # GPT models (if available through Ollama)
        "gpt": True,
        "gpt-oss": True,  # Open source GPT models generally support tools
        
        # Vicuna
        "vicuna": False,  # Generally doesn't support structured outputs
        
        # Orca
        "orca": False,
    }
    
    model_lower = model_name.lower()
    
    # Check for exact or partial matches
    for known_model, supports_tools in tool_calling_models.items():
        if known_model in model_lower:
            return supports_tools, f"Known: {known_model}"
    
    # Special checks
    if "instruct" in model_lower or "chat" in model_lower:
        return True, "Likely (instruct/chat model)"
    
    if any(version in model_lower for version in ["1.5", "2.0", "3.0", "3.1", "3.2"]):
        return True, "Likely (recent version)"
    
    # Default to unknown
    return None, "Unknown"

def analyze_models_for_tools(models):
    """Analyze which models support tool calling."""
    print("🛠️ Tool Calling Analysis")
    print("=" * 30)
    
    tool_capable = []
    no_tools = []
    unknown = []
    
    for model in models:
        name = model['name']
        supports_tools, reason = check_tool_calling_support(name)
        
        if supports_tools is True:
            tool_capable.append((name, reason))
        elif supports_tools is False:
            no_tools.append((name, reason))
        else:
            unknown.append((name, reason))
    
    print(f"✅ Models with tool calling ({len(tool_capable)}):")
    for name, reason in tool_capable:
        print(f"   🛠️ {name} - {reason}")
    
    print(f"\n❌ Models without tool calling ({len(no_tools)}):")
    for name, reason in no_tools:
        print(f"   🚫 {name} - {reason}")
    
    print(f"\n❓ Unknown tool support ({len(unknown)}):")
    for name, reason in unknown:
        print(f"   ❓ {name} - {reason}")
    
    return tool_capable, no_tools, unknown

def check_running_models():
    """Check which models are currently running."""
    print("\n🏃 Currently Running Models")
    print("-" * 30)
    
    try:
        result = subprocess.run(['ollama', 'ps'], 
                               capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if output and "NAME" in output:  # Has header, so has models
                print(result.stdout)
            else:
                print("No models currently running")
        else:
            print(f"❌ Failed to check running models: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error checking running models: {e}")

def main():
    """Main function to list and analyze models."""
    print("🔍 Ollama Model Inventory")
    print("=" * 50)
    
    # Method 1: CLI
    cli_success = list_ollama_models_cli()
    
    # Method 2: API (more detailed)
    models = list_ollama_models_api()
    
    if models:
        # Analyze tool calling capabilities
        tool_capable, no_tools, unknown = analyze_models_for_tools(models)
        
        # Show recommendations
        print(f"\n💡 Recommendations:")
        if tool_capable:
            print(f"   • Use these for our model switcher: {[m[0].split(':')[0] for m in tool_capable[:3]]}")
            print(f"   • All support mathematical tools and function calling")
        
        if no_tools:
            print(f"   • These won't work with tools: {[m[0].split(':')[0] for m in no_tools]}")
        
        if unknown:
            print(f"   • Test these manually: {[m[0].split(':')[0] for m in unknown]}")
    
    # Check running models
    check_running_models()
    
    print(f"\n🔧 Useful Commands:")
    print(f"   ollama list                    # List all downloaded models")
    print(f"   ollama ps                      # Show running models")
    print(f"   ollama run <model>             # Start/download a model")
    print(f"   ollama rm <model>              # Remove a model")
    print(f"   python test_ollama_tools.py    # Test tool calling with current model")

if __name__ == "__main__":
    main()
