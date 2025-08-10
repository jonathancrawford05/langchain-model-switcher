# LangChain Model Switcher

A minimalistic framework for seamlessly switching between different LLM providers in LangChain applications, with MCP (Model Context Protocol) support.

## 🚀 Features

- **🔄 Easy Model Switching**: Switch between IBM Watson, Anthropic Claude, and Ollama with a single environment variable
- **🧩 Unified Interface**: Same code works with any supported model provider
- **🛠️ MCP Integration**: Built-in Model Context Protocol server for external tool access
- **📦 Poetry Management**: Clean dependency management with Poetry
- **🏗️ Extensible Architecture**: Easy to add new model providers
- **🎯 Vector Database Ready**: Perfect foundation for RAG applications

## 📋 Supported Models

| Provider | Models | Tool Calling | Status |
|----------|--------|--------------|--------|
| **IBM Watson** | Granite 3.2, Granite 3.3 | ✅ | Ready |
| **Anthropic Claude** | Claude 3 Sonnet, Haiku, Opus | ✅ | Ready |
| **Ollama** | Llama 3.1, Mistral, Qwen, Phi3 | ✅ | Ready |
| **OpenAI** | GPT-4, GPT-3.5 | ✅ | Configurable |

## 🏗️ Project Structure

```
langchain-model-switcher/
├── src/
│   ├── models/              # Model adapters
│   │   ├── base.py         # Abstract base adapter
│   │   ├── watson_adapter.py
│   │   ├── claude_adapter.py
│   │   └── ollama_adapter.py
│   ├── mcp/                # MCP server and tools
│   │   ├── server.py       # MCP server implementation
│   │   └── tools.py        # Mathematical tools
│   ├── config/             # Configuration management
│   │   ├── settings.py     # Settings and config loading
│   │   └── models.yaml     # Model configurations
│   └── utils/              # Utilities
│       └── model_factory.py # Model factory pattern
├── notebooks/              # Jupyter notebooks
│   └── math_assistant.ipynb # Demo notebook
├── tests/                  # Test suite
├── pyproject.toml         # Poetry configuration
└── README.md
```

## 🚀 Quick Start

### 1. Setup with Poetry

```bash
# Clone or navigate to the project
cd langchain-model-switcher

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### 2. Configure API Keys (Optional)

Create a `.env` file:

```bash
# For Claude
CLAUDE_API_KEY=your_claude_api_key_here

# For OpenAI (if using)
OPENAI_API_KEY=your_openai_api_key_here

# For Ollama (if not using localhost)
OLLAMA_BASE_URL=http://your-ollama-server:11434

# For Watson (if not using Skills Network)
WATSON_API_KEY=your_watson_api_key_here
```

### 3. Run the Demo Notebook

```bash
# Start Jupyter
jupyter notebook notebooks/math_assistant.ipynb
```

### 4. Switch Models Programmatically

```python
from src.utils.model_factory import get_model
import os

# Switch to Claude
os.environ["MODEL_PROVIDER"] = "claude"
claude_model = get_model()

# Switch to Ollama
os.environ["MODEL_PROVIDER"] = "ollama"  
ollama_model = get_model()

# Switch to Watson
os.environ["MODEL_PROVIDER"] = "watson"
watson_model = get_model()
```

## 🛠️ Usage Examples

### Basic Model Usage

```python
from src.utils.model_factory import get_model

# Get current model (based on MODEL_PROVIDER env var)
model_adapter = get_model()
llm = model_adapter.get_langchain_model()

# Use with any LangChain component
response = llm.invoke("What is machine learning?")
print(response.content)
```

### Agent Creation

```python
from langgraph.prebuilt import create_react_agent
from src.mcp.tools import get_math_tools

# Get tools and model
tools = get_math_tools()
llm = get_model().get_langchain_model()

# Create agent (works with any model!)
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="You are a helpful mathematical assistant."
)

# Use the agent
response = agent.invoke({
    "messages": [("human", "Calculate 25 + 15 and multiply by 2")]
})
```

### Vector Database Integration

```python
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from src.utils.model_factory import get_model

# Get any model
llm = get_model().get_langchain_model()

# Set up retrieval chain (example)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,  # Any model works here!
    chain_type='stuff',
    retriever=vectorstore.as_retriever()
)

# Switch models anytime
os.environ['MODEL_PROVIDER'] = 'claude'
qa_chain.llm = get_model().get_langchain_model()
```

## 🌐 MCP Server

Start the MCP server to expose tools externally:

```bash
# Start MCP server
poetry run python -m src.mcp.server

# Or with custom host/port
poetry run python -m src.mcp.server --host 0.0.0.0 --port 8765
```

### MCP Client Example

```python
import websockets
import json
import asyncio

async def test_mcp_client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # List available tools
        message = {"method": "tools/list", "params": {}}
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        print("Available tools:", json.loads(response))
        
        # Call a tool
        message = {
            "method": "tools/call",
            "params": {
                "name": "add_numbers",
                "arguments": {"inputs": "10 20 30"}
            }
        }
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        print("Tool result:", json.loads(response))

asyncio.run(test_mcp_client())
```

## ⚙️ Configuration

### Model Configuration (src/config/models.yaml)

```yaml
models:
  claude:
    class_name: "ClaudeAdapter"
    model_id: "claude-3-sonnet-20240229"
    max_tokens: 4096
    temperature: 0.1
    
  ollama:
    class_name: "OllamaAdapter"
    model_id: "llama3.1"
    base_url: "http://localhost:11434"
    temperature: 0.1
    
  watson:
    class_name: "WatsonAdapter"
    model_id: "ibm/granite-3-2-8b-instruct"
    url: "https://us-south.ml.cloud.ibm.com"
    project_id: "skills-network"

default_provider: "claude"
```

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MODEL_PROVIDER` | Current model provider | `claude`, `watson`, `ollama` |
| `CLAUDE_API_KEY` | Claude API key | `sk-ant-...` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `WATSON_API_KEY` | Watson API key | `your-watson-key` |

## 🔧 Adding New Model Providers

1. **Create a new adapter** in `src/models/`:

```python
# src/models/new_provider_adapter.py
from .base import ModelAdapter
from some_provider import SomeProviderLLM

class NewProviderAdapter(ModelAdapter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = SomeProviderLLM(**kwargs)
    
    def invoke(self, messages):
        return self.model.invoke(messages)
    
    def get_model_name(self):
        return f"NewProvider-{self.model_id}"
    
    def supports_tool_calling(self):
        return True
    
    def get_langchain_model(self):
        return self.model
```

2. **Register the adapter** in `src/utils/model_factory.py`:

```python
from ..models.new_provider_adapter import NewProviderAdapter

class ModelFactory:
    _adapters = {
        # ... existing adapters
        "NewProviderAdapter": NewProviderAdapter,
    }
```

3. **Add configuration** in `src/config/models.yaml`:

```yaml
models:
  # ... existing models
  newprovider:
    class_name: "NewProviderAdapter"
    model_id: "some-model-id"
    api_key: null
    # ... other config
```

## 🧪 Testing

Run tests with the provided scripts:

```bash
# 1. Check installation and dependencies
python check_install.py

# 2. Run basic functionality demo
python demo_working.py

# 3. Run comprehensive functionality test
python test_working.py

# 4. Run unit tests with pytest
python run_pytest.py               # Recommended pytest runner
# OR
poetry run pytest tests/           # Direct pytest
```

### Test Scripts Overview

| Script | Purpose | Dependencies |
|--------|---------|-------------|
| `check_install.py` | Verify installation | None |
| `demo_working.py` | Basic demo | Poetry env |
| `test_working.py` | Full test suite | Poetry env |

**Note**: See `TESTING.md` for detailed testing information.

## 📊 Performance Comparison

Test the same query across different models:

```python
def compare_models(query: str):
    results = {}
    for provider in ["claude", "watson", "ollama"]:
        os.environ["MODEL_PROVIDER"] = provider
        model = get_model()
        start_time = time.time()
        response = model.invoke(query)
        end_time = time.time()
        
        results[provider] = {
            "response": response.content,
            "time": end_time - start_time,
            "model": model.get_model_name()
        }
    return results
```

## 🚀 Deployment

### Local Development

```bash
poetry install
poetry shell
jupyter notebook notebooks/
```

### Production MCP Server

```bash
# Install in production environment
poetry install --only=main

# Start MCP server
poetry run python -m src.mcp.server --host 0.0.0.0 --port 8765
```

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --only=main

COPY src/ ./src/
EXPOSE 8765

CMD ["poetry", "run", "python", "-m", "src.mcp.server", "--host", "0.0.0.0"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `poetry run pytest`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain** for the fantastic framework
- **IBM Watson** for providing accessible AI models
- **Anthropic** for Claude's excellent capabilities
- **Ollama** for making local LLM deployment easy
- **Skills Network** for the original notebook inspiration

## 📞 Support

- 📖 [Documentation](./docs/)
- 🐛 [Issue Tracker](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)

---

**Built with ❤️ for the LangChain community**
