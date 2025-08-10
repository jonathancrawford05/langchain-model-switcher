#!/bin/bash
# Quick setup script for LangChain Model Switcher

echo "🚀 LangChain Model Switcher - Quick Setup"
echo "=========================================="

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry not found. Please install Poetry first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo "✅ Poetry found"

# Install dependencies
echo "📦 Installing dependencies..."
poetry install

# Create .env from template if it doesn't exist
if [ ! -f .env ] && [ -f .env.example ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys"
fi

# Run tests
echo "🧪 Running tests..."
poetry run python run_tests.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. poetry shell                    # Activate environment"
echo "2. Edit .env file with API keys   # Optional for some providers"
echo "3. jupyter notebook notebooks/    # Start the demo notebook"
echo "4. python -m src.mcp.server      # Or start MCP server"
echo ""
echo "📖 See README.md for full documentation"
