#!/usr/bin/env python3
"""
Simple verification that the project structure is correct.
This can run without any dependencies installed.
"""

import sys
from pathlib import Path

# Basic validation
project_root = Path(__file__).parent
src_dir = project_root / "src"

print("🔍 LangChain Model Switcher - Structure Check")
print("=" * 50)

# Check if main directories exist
dirs_to_check = ["src", "notebooks", "tests", "src/models", "src/config", "src/utils", "src/mcp"]
all_dirs_exist = True

for dir_name in dirs_to_check:
    dir_path = project_root / dir_name
    if dir_path.exists():
        print(f"✅ {dir_name}")
    else:
        print(f"❌ {dir_name}")
        all_dirs_exist = False

# Check key files
files_to_check = [
    "pyproject.toml", 
    "README.md",
    "src/models/base.py",
    "src/models/claude_adapter.py",
    "src/models/watson_adapter.py", 
    "src/models/ollama_adapter.py",
    "src/utils/model_factory.py",
    "src/config/models.yaml",
    "notebooks/math_assistant.ipynb"
]

all_files_exist = True
for file_name in files_to_check:
    file_path = project_root / file_name
    if file_path.exists():
        print(f"✅ {file_name}")
    else:
        print(f"❌ {file_name}")
        all_files_exist = False

# Summary
print("\n" + "=" * 50)
if all_dirs_exist and all_files_exist:
    print("🎉 Project structure is correct!")
    print("\n📋 Next steps:")
    print("1. poetry install              # Install dependencies")
    print("2. poetry shell               # Activate environment") 
    print("3. python run_tests.py        # Run comprehensive tests")
    print("4. jupyter notebook notebooks/ # Start demo notebook")
else:
    print("❌ Some files or directories are missing")

print(f"\n📁 Project location: {project_root}")
