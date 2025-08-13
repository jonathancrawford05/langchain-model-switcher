# Single Ollama Instance Setup Guide

This guide explains the **recommended approach** for using both Ollama (Llama) and Phi models through a single Ollama instance.

## 🎯 **Recommended Approach: Single Instance + Model Switching**

Both `ollama` and `phi` providers use the **same Ollama server** but switch between different models. This avoids port conflicts and is more resource-efficient.

## 📊 Configuration

| Model Provider | Port | Model ID | Ollama Instance |
|----------------|------|----------|-----------------|
| `ollama` | 11434 | `llama3.1` | **Same Instance** |
| `phi` | 11434 | `llama3.2` | **Same Instance** |

## 🚀 Setup Instructions

### 1. Start Single Ollama Instance

```bash
# Start Ollama (uses default port 11434)
ollama serve
```

### 2. Install Both Models

```bash
# Install Llama 3.1
ollama pull llama3.1

# Install Phi 3
ollama pull llama3.2

# Verify both models are available
ollama list
```

### 3. Test Model Switching

```bash
# Test the framework
python verify_phi_extension.py
```

## 🔄 Usage Examples

### Python Code

```python
import os
from src.utils.model_factory import get_model

# Use Llama 3.1 through Ollama provider
os.environ['MODEL_PROVIDER'] = 'ollama'
llama_model = get_model()
print(f"Using: {llama_model.get_model_name()}")  # Ollama-llama3.1

# Use llama3.2 through Phi provider  
os.environ['MODEL_PROVIDER'] = 'phi'
phi_model = get_model()
print(f"Using: {phi_model.get_model_name()}")    # Phi-phi3

# Both hit the same Ollama server but use different models!
```

### Jupyter Notebook

```python
# Cell 1: Test Llama 3.1
import os
os.environ['MODEL_PROVIDER'] = 'ollama'
from src.utils.model_factory import get_model

model = get_model()
response = model.invoke("What is a vector database?")
print(f"Llama 3.1 Response: {response.content}")
```

```python
# Cell 2: Test llama3.2 
os.environ['MODEL_PROVIDER'] = 'phi'
model = get_model()

response = model.invoke("What is a vector database?")
print(f"Phi 3 Response: {response.content}")
```

## ✅ **Why This Approach Works Better**

### ❌ **Multiple Instances Problems:**
- Port conflicts (`OLLAMA_HOST` variable confusion)
- Resource wastage (2 Ollama servers)
- Complex setup (multiple terminals)
- Environment variable conflicts

### ✅ **Single Instance Benefits:**
- **No port conflicts** - Uses standard port 11434
- **Resource efficient** - One Ollama server
- **Simple setup** - Just `ollama serve`
- **Easy switching** - Change `MODEL_PROVIDER` only
- **Same interface** - Both use Ollama's ChatOllama class

## 🔍 **How It Works Under the Hood**

```python
# When MODEL_PROVIDER='ollama'
ollama_adapter = OllamaAdapter(
    model_id="llama3.1",           # ← Different model
    base_url="http://localhost:11434"
)

# When MODEL_PROVIDER='phi'  
phi_adapter = PhiAdapter(
    model_id="llama3.2",               # ← Different model
    base_url="http://localhost:11434"  # ← Same server!
)
```

Both adapters hit the same Ollama server but request different models. Ollama automatically loads the requested model.

## 🧪 **Verification**

```bash
# 1. Check Ollama is running
curl http://localhost:11434/api/tags

# 2. Test both models are available
ollama list

# 3. Run framework tests
python test_phi_integration.py

# 4. Verify configuration
python verify_phi_extension.py
```

## 🎯 **Model Comparison**

| Feature | Ollama (Llama 3.1) | Phi (llama3.2) |
|---------|-------------------|-------------|
| **Model Size** | ~4.7GB | ~2.0GB |
| **Speed** | Moderate | **Fast** |
| **Reasoning** | **Excellent** | Good |
| **Memory Usage** | Higher | **Lower** |
| **Best For** | Complex analysis | Quick responses |
| **Tool Calling** | ✅ Yes | ✅ Yes |

## 🛠️ **Troubleshooting**

### Model Not Found
```bash
# Check available models
ollama list

# Install missing model
ollama pull llama3.1
ollama pull llama3.2
```

### Connection Issues
```bash
# Check Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### Provider Switching Not Working
```python
# Clear any cached model instances
import importlib
importlib.reload(src.utils.model_factory)

# Then switch provider
os.environ['MODEL_PROVIDER'] = 'phi'
```

## 🎉 **Summary**

✅ **Single Ollama instance** running on port 11434  
✅ **Two model providers** (`ollama` and `phi`)  
✅ **Different models** (Llama 3.1 vs llama3.2)  
✅ **Same interface** - easy switching  
✅ **No conflicts** - clean and simple  

This approach gives you the best of both worlds: easy model comparison without the complexity of multiple server instances!
