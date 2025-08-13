# 🛠️ Ollama Tool Calling Setup Guide

## 🎯 **The Problem**
Your current `llama3` model doesn't support tool/function calling, which means it can't use the mathematical tools in our model switcher.

## ✅ **The Solution**
Upgrade to a model that supports tool calling! Here are your best options:

## 🏆 **Recommended Models (All FREE & Local)**

### **1. Llama 3.1 (BEST UPGRADE)**
```bash
ollama run llama3.1
```
- **Size**: 4.7GB (same as your current llama3)
- **Benefits**: Direct upgrade, excellent tool calling
- **Why**: Same model family, just newer with tool support

### **2. Mistral (ALTERNATIVE)**
```bash
ollama run mistral
```
- **Size**: 4.1GB (slightly smaller)
- **Benefits**: Excellent tool calling, very reliable
- **Why**: Different model family, known for good function calling

### **3. Llama 3.2 (COMPACT)**
```bash
ollama run llama3.2
```
- **Size**: 2.0GB (much smaller)
- **Benefits**: Faster, still supports tools
- **Why**: If you want something more compact

### **4. Phi-3 (SMALLEST)**
```bash
ollama run phi3
```
- **Size**: 2.2GB
- **Benefits**: Microsoft model, compact with tool support
- **Why**: Good for limited resources

## 🚀 **Quick Upgrade Process**

### **Option A: Automated (Recommended)**
```bash
# Run our upgrade assistant
python upgrade_ollama.py
```
This will:
1. Download llama3.1 for you
2. Update your configuration automatically  
3. Test that tool calling works

### **Option B: Manual**
```bash
# 1. Download a tool-capable model
ollama run llama3.1

# 2. Update configuration
# Edit: src/config/models.yaml
# Change: model_id: "llama3" → model_id: "llama3.1"

# 3. Test it works
python test_ollama_tools.py
```

## 🔍 **Check Your Current Setup**

```bash
# See what models you have
python check_ollama_tools.py

# Test if current model supports tools
python test_ollama_tools.py
```

## 📋 **What Models Support Tool Calling?**

| Model | Tool Support | Size | Command |
|-------|-------------|------|---------|
| **llama3** | ❌ No | 4.7GB | `ollama run llama3` |
| **llama3.1** | ✅ Yes | 4.7GB | `ollama run llama3.1` |
| **llama3.2** | ✅ Yes | 2.0GB | `ollama run llama3.2` |
| **mistral** | ✅ Yes | 4.1GB | `ollama run mistral` |
| **phi3** | ✅ Yes | 2.2GB | `ollama run phi3` |
| **qwen2.5** | ✅ Yes | 4.7GB | `ollama run qwen2.5` |

## 🔧 **Configuration Update**

After downloading a new model, update `src/config/models.yaml`:

```yaml
ollama:
  class_name: "OllamaAdapter"
  model_id: "llama3.1"  # ← Change this line
  base_url: "http://localhost:11434"
  temperature: 0.1
  timeout: 60
```

## 🧪 **Verify Tool Calling Works**

```bash
# Test that tool calling works
python test_ollama_tools.py

# Should show:
# ✅ Basic query works
# ✅ Agent created successfully  
# 🎉 SUCCESS! Tool calling works!
```

## 🎯 **Why Tool Calling Matters**

With tool calling, your model can:
- ✅ Use mathematical functions (add, subtract, multiply, divide)
- ✅ Search Wikipedia for information
- ✅ Perform complex multi-step operations
- ✅ Work with your vector database applications

Without tool calling:
- ❌ Model just responds with text, can't use functions
- ❌ Can't perform actual calculations
- ❌ Limited functionality in your applications

## 🏠 **Privacy Guarantee**

All these models run **100% locally** on your machine:
- 🔒 **No data sent to cloud services**
- 🌐 **Works offline after download**
- 💰 **Completely free after initial download**
- ⚡ **No API rate limits**

## 🚀 **Next Steps After Upgrade**

1. **Test the notebook**: `jupyter notebook notebooks/math_assistant.ipynb`
2. **Try mathematical queries**: "Add 10 and 20, then multiply by 3"
3. **Test Wikipedia integration**: "What's the population of Canada? Multiply by 0.5"
4. **Build your vector database applications** with full tool support!

## ❓ **Need Help?**

```bash
# Check what's installed
python check_ollama_tools.py

# Test current setup
python test_ollama_tools.py

# Automated upgrade
python upgrade_ollama.py
```

## 💡 **Pro Tips**

- **Llama 3.1** is the safest upgrade (same family as your current model)
- **Mistral** is great if you want to try a different model family
- **Llama 3.2** is perfect if you want something faster/smaller
- You can have multiple models installed and switch between them!

---

**Bottom Line**: Install `llama3.1` with `ollama run llama3.1` and you'll have tool calling support with the same model family you're already using! 🎉
