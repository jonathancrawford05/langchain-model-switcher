"""Simple pytest test to verify the testing setup works."""

import pytest


def test_basic_python():
    """Test that basic Python functionality works."""
    assert 1 + 1 == 2
    assert "hello" + " world" == "hello world"


def test_imports():
    """Test that we can import standard libraries."""
    import json
    import os
    import sys
    from pathlib import Path
    
    assert json is not None
    assert os is not None
    assert sys is not None
    assert Path is not None


def test_project_structure():
    """Test that the project files exist."""
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent
    
    # Test key files exist
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / "src").exists()
    assert (project_root / "src" / "models").exists()
    assert (project_root / "src" / "utils").exists()
    assert (project_root / "src" / "config").exists()


def test_yaml_config():
    """Test that we can read the YAML config."""
    import yaml
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent
    config_file = project_root / "src" / "config" / "models.yaml"
    
    assert config_file.exists()
    
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    assert "models" in config
    assert "claude" in config["models"]
    assert "watson" in config["models"]
    assert "ollama" in config["models"]


if __name__ == "__main__":
    # Run tests directly if called as script
    test_basic_python()
    test_imports()
    test_project_structure()
    test_yaml_config()
    print("✅ All simple tests passed!")
