# Test Scripts Usage Guide

## ✅ RECOMMENDED SCRIPTS (Use These)

### 1. Installation Check
```bash
python check_install.py
```
- Tests that dependencies are installed
- Verifies project structure
- No package imports needed

### 2. Basic Demo
```bash
python demo_working.py
```
- Shows basic functionality
- Tests model switching
- Tests mathematical tools

### 3. Full Functionality Test
```bash
python test_working.py
```
- Complete test suite
- Tests all adapters
- Tests configuration system
- Tests tools and MCP integration

### 4. Pytest Tests
```bash
# Option A: Use the helper script (recommended)
python run_pytest.py

# Option B: Direct pytest (may need path setup)
poetry run pytest tests/

# Option C: Run specific test file
poetry run pytest tests/test_simple_pytest.py -v
```

## ❌ DEPRECATED SCRIPTS (Don't Use These)

### These scripts have import issues:
- `test_simple.py.old` - Has incorrect import logic
- `test_integration.py.old` - Has incorrect import logic
- `run_tests.py.old` - Has incorrect import logic

## 🚀 Quick Start Sequence

```bash
# 1. Verify installation
python check_install.py

# 2. See basic demo
python demo_working.py  

# 3. Run full tests
python test_working.py

# 4. Run pytest suite
python run_pytest.py

# 5. If all pass, use the notebook
jupyter notebook notebooks/math_assistant.ipynb
```

## 💡 Why This Structure?

- **Package files** (`src/`) use relative imports (`.models`, `.config`)
- **Test scripts** import the package externally (`src.models`, `src.config`)
- **Pytest** needs special path setup to handle package imports
- This follows Python packaging best practices

## 🧪 Test File Overview

| Test File | Purpose | Import Style |
|-----------|---------|-------------|
| `test_simple_pytest.py` | Basic pytest functionality | Standard imports |
| `test_basic.py` | Model switcher functionality | `from src.* import` |
| `conftest.py` | Pytest configuration | Automatic setup |
