#!/usr/bin/env python3
"""
Minimal verification - works without any dependencies.
"""

import sys
from pathlib import Path

def verify_minimal():
    """Minimal verification that requires no external dependencies."""
    print("✨ Minimal Project Verification")
    print("=" * 40)
    
    project_root = Path(__file__).parent
    print(f"📁 Project: {project_root.name}")
    
    # Check key files
    key_files = [
        "pyproject.toml",
        "src/__init__.py", 
        "src/models/base.py",
        "src/utils/model_factory.py",
        "notebooks/math_assistant.ipynb"
    ]
    
    all_good = True
    for file_path in key_files:
        full_path = project_root / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} (missing)")
            all_good = False
    
    # Check pyproject.toml content
    try:
        pyproject_path = project_root / "pyproject.toml"
        content = pyproject_path.read_text()
        
        required_deps = ["langchain", "poetry"]
        found_deps = sum(1 for dep in required_deps if dep in content)
        print(f"📦 Dependencies: {found_deps}/{len(required_deps)} found")
        
        if "langchain-model-switcher" in content:
            print("✅ Project name correct")
        else:
            print("⚠️ Project name issue")
            
    except Exception as e:
        print(f"⚠️ Could not read pyproject.toml: {e}")
        all_good = False
    
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 Project structure looks good!")
        print("\n📋 Ready to run:")
        print("  poetry install")
        print("  poetry shell")
        print("  python test_simple.py")
    else:
        print("⚠️ Some issues found")
    
    return all_good

if __name__ == "__main__":
    success = verify_minimal()
    print(f"\n🚀 Status: {'READY' if success else 'NEEDS_SETUP'}")
