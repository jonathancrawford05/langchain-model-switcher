# Contributing to LangChain Model Switcher

Thank you for your interest in contributing to the LangChain Model Switcher!

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd langchain-model-switcher
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   poetry shell
   ```

3. **Run tests:**
   ```bash
   python run_pytest.py
   ```

## Project Structure

- `src/` - Main package code
- `tests/` - Test suite
- `notebooks/` - Demo notebooks
- `docs/` - Documentation (if added)

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to public functions
- Run tests before committing

## Adding New Model Providers

1. Create adapter in `src/models/new_provider_adapter.py`
2. Add to `src/models/__init__.py`
3. Register in `src/utils/model_factory.py`
4. Add config to `src/config/models.yaml`
5. Add tests

## Submitting Changes

1. Create a feature branch
2. Make your changes
3. Run tests: `python run_pytest.py`
4. Update documentation if needed
5. Submit a pull request

## Questions?

Open an issue for questions or suggestions!
