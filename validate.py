"""
Validate the project setup without requiring external dependencies.
This is a minimal test that can run without Poetry installation.
"""

import sys
from pathlib import Path

def validate_project_structure():
    """Validate that all required files and directories exist."""
    print("🔍 Validating project structure...")
    
    project_root = Path(__file__).parent
    
    required_paths = [
        # Core directories
        "src",
        "src/models", 
        "src/config",
        "src/utils",
        "src/mcp",
        "notebooks",
        "tests",
        
        # Core files
        "pyproject.toml",
        "README.md",
        "src/__init__.py",
        "src/models/__init__.py",
        "src/models/base.py",
        "src/models/watson_adapter.py",
        "src/models/claude_adapter.py", 
        "src/models/ollama_adapter.py",
        "src/models/openai_adapter.py",
        "src/config/__init__.py",
        "src/config/settings.py",
        "src/config/models.yaml",
        "src/utils/__init__.py",
        "src/utils/model_factory.py",
        "src/mcp/__init__.py",
        "src/mcp/server.py",
        "src/mcp/tools.py",
        "notebooks/math_assistant.ipynb",
        "tests/__init__.py",
        "tests/test_basic.py",
    ]
    
    missing_paths = []
    for path_str in required_paths:
        path = project_root / path_str
        if not path.exists():
            missing_paths.append(path_str)
    
    if missing_paths:
        print(f"❌ Missing paths: {missing_paths}")
        return False
    else:
        print(f"✅ All {len(required_paths)} required paths exist")
        return True

def validate_file_contents():
    """Validate that key files have expected content."""
    print("📄 Validating file contents...")
    
    project_root = Path(__file__).parent
    
    # Check pyproject.toml
    pyproject = project_root / "pyproject.toml"
    content = pyproject.read_text()
    
    required_deps = [
        "langchain", "langchain-community", "langchain-anthropic", 
        "langchain-ollama", "langchain-ibm", "langchain-openai"
    ]
    
    missing_deps = []
    for dep in required_deps:
        if dep not in content:
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"❌ Missing dependencies in pyproject.toml: {missing_deps}")
        return False
    
    # Check models.yaml
    models_yaml = project_root / "src/config/models.yaml"
    yaml_content = models_yaml.read_text()
    
    required_models = ["claude", "watson", "ollama", "openai"]
    missing_models = []
    for model in required_models:
        if model not in yaml_content:
            missing_models.append(model)
    
    if missing_models:
        print(f"❌ Missing models in models.yaml: {missing_models}")
        return False
    
    print("✅ Key files have expected content")
    return True

def main():
    """Main validation function."""
    print("🔬 LangChain Model Switcher - Project Validation")
    print("=" * 50)
    
    structure_ok = validate_project_structure()
    content_ok = validate_file_contents()
    
    if structure_ok and content_ok:
        print("\n🎉 Project validation successful!")
        print("\n📋 Ready for setup. Run one of:")
        print("  bash quick_setup.sh     # Automated setup")
        print("  poetry install          # Manual setup")
        print("  python run_tests.py     # Full tests")
        
        return True
    else:
        print("\n❌ Project validation failed")
        print("Some files may be missing or corrupted")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
