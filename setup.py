#!/usr/bin/env python3
"""
Setup script for LangChain Model Switcher.
This script helps users quickly set up and test the project.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_poetry():
    """Check if Poetry is installed."""
    try:
        subprocess.run(['poetry', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    """Main setup function."""
    print("🚀 LangChain Model Switcher Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('pyproject.toml').exists():
        print("❌ Error: pyproject.toml not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check Poetry installation
    if not check_poetry():
        print("❌ Poetry is not installed or not in PATH.")
        print("📖 Please install Poetry first: https://python-poetry.org/docs/#installation")
        print("   curl -sSL https://install.python-poetry.org | python3 -")
        sys.exit(1)
    
    print("✅ Poetry is installed")
    
    # Install dependencies
    if not run_command("poetry install", "Installing dependencies"):
        print("💡 If this fails, try: poetry install --no-dev")
        return
    
    # Copy environment file
    if not Path('.env').exists() and Path('.env.example').exists():
        run_command("cp .env.example .env", "Creating .env file from template", check=False)
        print("📝 Please edit .env file with your API keys")
    
    # Run basic tests
    print("\n🧪 Running basic tests...")
    if run_command("poetry run python tests/test_basic.py", "Running basic functionality tests", check=False):
        print("\n✅ Basic setup completed successfully!")
    else:
        print("\n⚠️  Some tests failed, but basic setup is complete.")
    
    # Show next steps
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your API keys (optional for some providers)")
    print("2. Activate the environment: poetry shell")
    print("3. Start Jupyter: jupyter notebook notebooks/math_assistant.ipynb")
    print("4. Or run MCP server: poetry run python -m src.mcp.server")
    print("\n📖 See README.md for full documentation")
    
    # Test if we can import the main module
    print("\n🔍 Testing imports...")
    try:
        sys.path.insert(0, 'src')
        from utils.model_factory import ModelFactory
        providers = ModelFactory.list_available_providers()
        print(f"✅ Available providers: {providers}")
    except Exception as e:
        print(f"⚠️  Import test failed: {e}")

if __name__ == "__main__":
    main()
