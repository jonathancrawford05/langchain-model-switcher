#!/usr/bin/env python3
"""
Quick upgrade script to install tool-capable Ollama models.
This guides the user through upgrading their setup.
"""

import subprocess
import time
import sys
from pathlib import Path

def check_ollama_available():
    """Check if Ollama is installed and available."""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Ollama is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama command failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Ollama not found in PATH")
        print("💡 Install from: https://ollama.ai")
        return False

def download_model(model_name):
    """Download an Ollama model."""
    print(f"\n📥 Downloading {model_name}...")
    print("⏳ This may take a few minutes depending on your internet speed...")
    
    try:
        # Use ollama run to download and start the model
        process = subprocess.Popen(
            ['ollama', 'run', model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send a simple test message and exit
        stdout, stderr = process.communicate(input="hello\n/bye\n", timeout=300)
        
        if process.returncode == 0:
            print(f"✅ {model_name} downloaded and ready!")
            return True
        else:
            print(f"❌ Download failed: {stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"⏰ Download timed out. Try running manually: ollama run {model_name}")
        return False
    except Exception as e:
        print(f"❌ Error downloading: {e}")
        return False

def update_config_file(model_name):
    """Update the configuration to use the new model."""
    config_path = Path(__file__).parent / "src/config/models.yaml"
    
    try:
        # Read current config
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Replace the model_id for ollama
        import re
        
        # Pattern to find the ollama section and update model_id
        pattern = r'(ollama:\s*\n(?:\s*[^:]+:[^\n]*\n)*\s*model_id:\s*")[^"]*(")'
        replacement = f'\\1{model_name}\\2'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            # Create backup
            backup_path = config_path.with_suffix('.yaml.backup')
            with open(backup_path, 'w') as f:
                f.write(content)
            
            # Write new config
            with open(config_path, 'w') as f:
                f.write(new_content)
            
            print(f"✅ Updated config to use {model_name}")
            print(f"💾 Backup saved as: {backup_path}")
            return True
        else:
            print("⚠️ Could not automatically update config")
            return False
            
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

def test_new_setup():
    """Test that the new model works with tools."""
    print("\n🧪 Testing new setup...")
    
    try:
        # Run our tool test script
        result = subprocess.run([sys.executable, 'test_ollama_tools.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if "SUCCESS! Tool calling works!" in result.stdout:
            print("🎉 SUCCESS! Your new model supports tool calling!")
            return True
        else:
            print("⚠️ Test completed but tool calling may not work")
            print("💡 Check the output above for details")
            return False
            
    except Exception as e:
        print(f"❌ Error testing setup: {e}")
        return False

def main():
    """Main upgrade process."""
    print("🚀 Ollama Tool Calling Upgrade Assistant")
    print("=" * 50)
    
    # Check if Ollama is available
    if not check_ollama_available():
        return
    
    # Show current situation
    print(f"\n📋 Current Situation:")
    print(f"   - You have 'llama3' which doesn't support tool calling")
    print(f"   - We'll upgrade you to 'llama3.1' which does!")
    print(f"   - Size: ~4.7GB (similar to what you have)")
    print(f"   - Benefits: Same performance + tool calling support")
    
    # Ask for confirmation
    print(f"\n❓ Would you like to proceed with the upgrade?")
    print(f"   This will:")
    print(f"   1. Download llama3.1 model (~4.7GB)")
    print(f"   2. Update your configuration")
    print(f"   3. Test tool calling functionality")
    
    response = input("\n💡 Continue? (y/N): ").strip().lower()
    
    if response not in ['y', 'yes']:
        print("👋 Upgrade cancelled. You can run this anytime!")
        return
    
    # Start upgrade process
    print(f"\n🔄 Starting upgrade process...")
    
    # Step 1: Download model
    if not download_model("llama3.1"):
        print("❌ Download failed. Please try manually: ollama run llama3.1")
        return
    
    # Step 2: Update config
    if not update_config_file("llama3.1"):
        print("⚠️ Please manually update src/config/models.yaml")
        print("   Change: model_id: 'llama3' → model_id: 'llama3.1'")
    
    # Step 3: Test
    if test_new_setup():
        print(f"\n🎉 UPGRADE COMPLETE!")
        print(f"✅ llama3.1 is installed and working")
        print(f"✅ Configuration updated")
        print(f"✅ Tool calling verified")
        print(f"\n🚀 You can now run your notebook with full tool support!")
        print(f"💡 Try: jupyter notebook notebooks/math_assistant.ipynb")
    else:
        print(f"\n⚠️ Upgrade completed but testing had issues")
        print(f"💡 Try running: python test_ollama_tools.py")

if __name__ == "__main__":
    main()
