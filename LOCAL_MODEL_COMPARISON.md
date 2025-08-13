# 🔄 Local Model Comparison Guide

## 🏠 **Two Local Models, One Framework**

You now have two distinct local model providers that both run through Ollama but are treated separately in the framework:

| Provider | Model | Size | Strengths | Use Case |
|----------|-------|------|-----------|----------|
| **`ollama`** | Llama 3.1 | 4.7GB | More capable, better reasoning | Complex tasks, detailed analysis |
| **`phi`** | Microsoft Phi-3 | 2.2GB | Compact, fast, efficient | Quick tasks, resource-constrained |

## 🎯 **Quick Switching Examples**

### **In Your Notebook:**
```python
# Test with Llama 3.1 (larger, more capable)
MODEL_PROVIDER = "ollama"
os.environ["MODEL_PROVIDER"] = MODEL_PROVIDER

# Test with Phi-3 (smaller, faster)  
MODEL_PROVIDER = "phi"
os.environ["MODEL_PROVIDER"] = MODEL_PROVIDER
```

### **From Command Line:**
```bash
# Use Llama 3.1
export MODEL_PROVIDER=ollama
python test_working.py

# Use Phi-3
export MODEL_PROVIDER=phi  
python test_working.py
```

## 🧪 **Comparison Testing**

### **Performance Test:**
```python
def compare_local_models():
    models_to_test = ["ollama", "phi"]
    query = "Calculate 15 * 20 + 30, then explain the steps"
    
    for provider in models_to_test:
        os.environ["MODEL_PROVIDER"] = provider
        adapter = get_model()
        
        start_time = time.time()
        # Your test here
        end_time = time.time()
        
        print(f"{provider}: {adapter.get_model_name()}")
        print(f"Time: {end_time - start_time:.2f}s")
```

### **Tool Calling Test:**
```python
def test_tool_calling(provider):
    os.environ["MODEL_PROVIDER"] = provider
    adapter = get_model()
    
    # Create agent with tools
    agent = create_react_agent(
        model=adapter.get_langchain_model(),
        tools=get_math_tools()
    )
    
    # Test complex mathematical operation
    result = agent.invoke({
        "messages": [("human", "Add 25 and 15, multiply by 3, then subtract 10")]
    })
    
    return result["messages"][-1].content
```

## 📊 **When to Use Which Model**

### **Use `ollama` (Llama 3.1) When:**
- ✅ Complex reasoning tasks
- ✅ Detailed explanations needed
- ✅ Multi-step problem solving
- ✅ You have sufficient resources (4.7GB)

### **Use `phi` (Phi-3) When:**
- ✅ Quick calculations needed
- ✅ Resource constraints (smaller memory footprint)
- ✅ Faster response times preferred
- ✅ Simple tool calling tasks

## 🔧 **Configuration Details**

Both models use the same Ollama server but different configurations:

```yaml
# Llama 3.1 configuration
ollama:
  class_name: "OllamaAdapter"
  model_id: "llama3.1"
  base_url: "http://localhost:11434"

# Phi-3 configuration  
phi:
  class_name: "PhiAdapter"
  model_id: "phi3"
  base_url: "http://localhost:11434"
```

## 🚀 **Setup Commands**

```bash
# Install both models
ollama run llama3.1    # Larger, more capable
ollama run phi3        # Smaller, faster

# Test the integration
python test_phi_integration.py

# Compare performance
python test_working.py  # Test with current MODEL_PROVIDER
```

## 💡 **Pro Tips**

1. **Development**: Use `phi` for quick iterations
2. **Production**: Use `ollama` for final results  
3. **Comparison**: Test the same query with both models
4. **Resource Management**: Both can run simultaneously but consume memory

## 🎯 **Example Notebook Usage**

```python
# Cell 1: Setup
from src.utils.model_factory import get_model
import os

# Cell 2: Test Llama 3.1
os.environ["MODEL_PROVIDER"] = "ollama"
llama_model = get_model()
print(f"Using: {llama_model.get_model_name()}")

# Cell 3: Test Phi-3
os.environ["MODEL_PROVIDER"] = "phi"
phi_model = get_model()
print(f"Using: {phi_model.get_model_name()}")

# Cell 4: Same query, different models
query = "What is 25 * 4 + 10?"
# Previous cells set the MODEL_PROVIDER, so get_model() returns the right one
```

## 🏆 **Best Practices**

- **Start with `phi`** for quick testing
- **Switch to `ollama`** for complex tasks
- **Use environment variables** for easy switching
- **Both are 100% local** - your data never leaves your machine
- **Both support tool calling** - full functionality with mathematical tools

---

**Summary**: You now have a flexible local model comparison setup where `ollama` = powerful and `phi` = efficient, both accessible through the same unified interface! 🎉
