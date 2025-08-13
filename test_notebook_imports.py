#!/usr/bin/env python3
"""
Test the notebook import fix to verify it works.
Run this script to confirm the import approach works.
"""

import sys
from pathlib import Path

def test_notebook_imports():
    """Test the same import approach used in the notebook."""
    print("🧪 Testing Notebook Import Approach")
    print("=" * 40)
    
    # Simulate notebook environment
    # Add project root to path (same as notebook)
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    print(f"📁 Project root: {project_root}")
    print(f"🐍 Added to sys.path: {str(project_root) in sys.path}")
    
    try:
        # Test the imports (same as notebook)
        print("\n1️⃣ Testing imports...")
        from src.utils.model_factory import ModelFactory, get_model
        from src.config.settings import get_current_provider, get_model_config
        from src.mcp.tools import get_math_tools
        print("   ✅ All imports successful!")
        
        # Test basic functionality
        print("\n2️⃣ Testing functionality...")
        providers = ModelFactory.list_available_providers()
        print(f"   📋 Available providers: {providers}")
        
        tools = get_math_tools()
        print(f"   🛠️ Available tools: {[t.name for t in tools]}")
        
        # Test model creation
        print("\n3️⃣ Testing model creation...")
        import os
        os.environ["MODEL_PROVIDER"] = "claude"
        
        adapter = get_model()
        print(f"   🤖 Created adapter: {adapter.get_model_name()}")
        print(f"   🛠️ Supports tools: {adapter.supports_tool_calling()}")
        
        print("\n🎉 SUCCESS! The notebook import approach works perfectly!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def explain_the_fix():
    """Explain why this approach works."""
    print("\n" + "=" * 50)
    print("🎓 WHY THIS WORKS:")
    print("=" * 50)
    print()
    print("1. 🏗️ Project Structure:")
    print("   project_root/")
    print("   ├── src/              ← This is our PACKAGE")
    print("   │   ├── utils/")
    print("   │   │   └── model_factory.py  ← Has: from ..models import")
    print("   │   └── models/")
    print("   └── notebooks/")
    print()
    print("2. 🔧 The Fix:")
    print("   ❌ OLD: sys.path.insert(0, 'src') + from utils.model_factory import")
    print("   ✅ NEW: sys.path.insert(0, project_root) + from src.utils.model_factory import")
    print()
    print("3. 🎯 Key Insight:")
    print("   - Relative imports like 'from ..models import' need PACKAGE CONTEXT")
    print("   - By importing 'from src.utils', Python sees 'src' as a package")
    print("   - This allows relative imports within the package to work")
    print()
    print("4. 🏆 Result:")
    print("   - Jupyter notebook can import our package")
    print("   - Package modules can use relative imports")
    print("   - Everyone is happy! 🎉")

if __name__ == "__main__":
    success = test_notebook_imports()
    explain_the_fix()
    
    if success:
        print("\n🚀 Your notebook should now work! Try running:")
        print("   jupyter notebook notebooks/math_assistant.ipynb")
    else:
        print("\n💡 If this failed, check:")
        print("   1. You're in the project root directory")
        print("   2. Poetry environment is activated")
        print("   3. All dependencies are installed")
