#!/usr/bin/env python3
"""
Installation verification script.
Tests that the package is properly installed and importable.
"""

def test_installation():
    """Test that the package is properly installed."""
    print("🔍 Testing Package Installation")
    print("=" * 40)
    
    try:
        # Test 1: Basic imports
        print("1️⃣ Testing basic imports...")
        import yaml
        import pydantic
        print("   ✅ Basic dependencies work")
        
        # Test 2: LangChain imports
        print("2️⃣ Testing LangChain imports...")
        import langchain
        from langchain_core.tools import tool
        print("   ✅ LangChain imports work")
        
        # Test 3: Project structure
        print("3️⃣ Testing project structure...")
        from pathlib import Path
        
        project_root = Path(__file__).parent
        required_dirs = ["src", "src/models", "src/config", "src/utils", "src/mcp"]
        
        for dir_name in required_dirs:
            if not (project_root / dir_name).exists():
                print(f"   ❌ Missing directory: {dir_name}")
                return False
        
        print("   ✅ Project structure correct")
        
        print("\n🎉 Installation verification passed!")
        print("\n📋 Next steps:")
        print("   python test_working.py    # Test functionality")
        print("   python demo_working.py    # See demo")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   💡 Run: poetry install")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_installation()
