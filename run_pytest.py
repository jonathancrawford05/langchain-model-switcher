#!/usr/bin/env python3
"""
Run pytest with proper setup for the model switcher project.
This script ensures the correct Python path and environment.
"""

import sys
import subprocess
from pathlib import Path
import os

def run_pytest():
    """Run pytest with proper configuration."""
    print("🧪 Running pytest for LangChain Model Switcher")
    print("=" * 50)
    
    # Set up environment
    project_root = Path(__file__).parent
    
    # Add project root to PYTHONPATH
    env = os.environ.copy()
    pythonpath = env.get('PYTHONPATH', '')
    if pythonpath:
        env['PYTHONPATH'] = f"{project_root}:{pythonpath}"
    else:
        env['PYTHONPATH'] = str(project_root)
    
    # Set default model provider for tests
    env['MODEL_PROVIDER'] = 'claude'
    
    print(f"📁 Project root: {project_root}")
    print(f"🐍 PYTHONPATH: {env['PYTHONPATH']}")
    print(f"🤖 MODEL_PROVIDER: {env['MODEL_PROVIDER']}")
    print()
    
    # Run pytest
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '-v', 
            '--tb=short',
            '--no-header'
        ], 
        cwd=project_root,
        env=env,
        capture_output=False
        )
        
        if result.returncode == 0:
            print("\n🎉 All tests passed!")
        else:
            print(f"\n⚠️ Some tests failed (exit code: {result.returncode})")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return False

if __name__ == "__main__":
    success = run_pytest()
    sys.exit(0 if success else 1)
