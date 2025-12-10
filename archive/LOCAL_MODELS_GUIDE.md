# Local Models Setup Guide

Use your Ultimate AI Dev Team with **local models** (completely free, no API keys needed)!

## 🎯 Why Use Local Models?

✅ **Free** - No API costs  
✅ **Private** - Your data never leaves your machine  
✅ **Offline** - Works without internet  
✅ **Fast** - No network latency (with good hardware)  
✅ **Unlimited** - No rate limits or token costs  

## 📦 What You Need

### Recommended Hardware
- **Minimum:** 8GB RAM, decent CPU
- **Recommended:** 16GB+ RAM, GPU (NVIDIA with CUDA)
- **Best:** 32GB+ RAM, RTX 3080+ or similar

### Storage
- ~4GB per model (e.g., Llama 2 7B)
- ~8GB for larger models (e.g., Llama 2 13B)

## 🚀 Setup Ollama (Easiest Method)

### Step 1: Install Ollama

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS:**
```bash
brew install ollama
# or download from https://ollama.ai/download
```

**Windows:**
Download from https://ollama.ai/download

### Step 2: Start Ollama Service

```bash
ollama serve
```

Keep this terminal open while using local models.

### Step 3: Download a Model

Open a new terminal and pull a model:

```bash
# For general tasks (7B parameters, ~4GB)
ollama pull llama2

# For coding (7B, optimized for code)
ollama pull codellama

# Smaller, faster model (7B)
ollama pull mistral

# Larger, more capable (13B, ~8GB)
ollama pull llama2:13b

# Even more capable (70B, ~40GB - needs powerful hardware)
ollama pull llama2:70b
```

### Step 4: Test Your Model

```bash
ollama run llama2
>>> Hello, how are you?
[Model responds...]
>>> /bye
```

### Step 5: Configure Your AI Dev Team

Edit `config.yaml`:

```yaml
# Ollama settings
ollama_url: "http://localhost:11434"
ollama_model: "llama2"  # or codellama, mistral, etc.

# Assign local models to agents
agent_models:
  # Use local models for some agents
  aurora: local
  felix: local
  sage: local
  
  # Use OpenAI for critical agents (if you have API key)
  helix: openai
  nova: openai
  
  # Or use ALL local models (completely free)
  atlas: local
  mira: local
  vex: local
  sol: local
  echo: local
  quinn: local
  blaze: local
  ivy: local
  zephyr: local
  pixel: local
  script: local
  turbo: local
  sentinel: local
  link: local
  patch: local
  pulse: local
  ember: local
  orion: local
```

### Step 6: Launch Your Team

```bash
python3 orchestrator.py
```

Choose Solo or Team Mode - agents will use local models automatically!

## 🎨 Recommended Model Assignments

### For Best Results (Mixed):
```yaml
agent_models:
  # Coordination & critical thinking - use best models
  helix: openai      # Overseer needs GPT-4
  nova: openai       # Lead engineer needs GPT-4
  
  # Coding & technical - use CodeLlama
  quinn: local       # codellama
  blaze: local       # codellama
  ivy: local         # codellama
  zephyr: local      # codellama
  patch: local       # codellama
  
  # Creative & planning - use Llama2/Mistral
  aurora: local      # llama2
  felix: local       # llama2
  sage: local        # llama2
  ember: local       # llama2
  
  # Others
  atlas: local
  mira: local
  vex: local
  sol: local
  echo: local
  pulse: local
```

Then set the model in config:
```yaml
ollama_model: "codellama"  # or llama2, mistral, etc.
```

### For Completely Free (All Local):
```yaml
ollama_model: "llama2"

agent_models:
  # All agents use local models
  helix: local
  aurora: local
  felix: local
  sage: local
  ember: local
  orion: local
  atlas: local
  mira: local
  vex: local
  sol: local
  echo: local
  nova: local
  quinn: local
  blaze: local
  ivy: local
  zephyr: local
  pixel: local
  script: local
  turbo: local
  sentinel: local
  link: local
  patch: local
  pulse: local
```

## 📊 Model Comparison

| Model | Size | RAM Needed | Best For | Speed |
|-------|------|------------|----------|-------|
| **llama2:7b** | 4GB | 8GB | General tasks | Fast |
| **codellama:7b** | 4GB | 8GB | Coding | Fast |
| **mistral:7b** | 4GB | 8GB | Fast responses | Very Fast |
| **llama2:13b** | 8GB | 16GB | Better reasoning | Medium |
| **codellama:13b** | 8GB | 16GB | Complex code | Medium |
| **llama2:70b** | 40GB | 64GB+ | Best quality | Slow |

## 🔧 Advanced Configuration

### Use Different Models for Different Agents

You can't easily assign different local models per agent in the current setup, but you can:

1. Run multiple Ollama instances on different ports
2. Modify config for specific use cases
3. Switch models as needed

### Performance Tips

**Speed up inference:**
```bash
# Use GPU (if available)
ollama run llama2 --gpu

# Use quantized models (smaller, faster)
ollama pull llama2:7b-q4_0  # 4-bit quantized
```

**Reduce memory usage:**
```bash
# Use smaller models
ollama pull llama2:7b

# Use quantized versions
ollama pull codellama:7b-q4_0
```

## 🐛 Troubleshooting

### "Cannot connect to Ollama"
```bash
# Make sure Ollama is running
ollama serve

# Check if it's responding
curl http://localhost:11434/api/tags
```

### "Model not found"
```bash
# Pull the model first
ollama pull llama2

# List installed models
ollama list
```

### Slow responses
- Use smaller models (7B instead of 13B)
- Use quantized versions (q4_0, q5_0)
- Check your hardware (RAM, GPU)
- Close other applications

### Out of memory
- Use smaller models
- Reduce context length in requests
- Add more RAM or use GPU

## 🎓 Model Recommendations by Task

### Code Review (Atlas, Mira)
**Best:** `codellama:13b`  
**Good:** `codellama:7b`  
**Budget:** `llama2:7b`

### Software Architecture (Nova, Aurora)
**Best:** `llama2:70b` or GPT-4  
**Good:** `llama2:13b`  
**Budget:** `llama2:7b`

### Coding (Quinn, Blaze, Ivy, Zephyr)
**Best:** `codellama:13b`  
**Good:** `codellama:7b`  
**Budget:** `codellama:7b-q4_0`

### Creative/Design (Ember)
**Best:** `llama2:13b`  
**Good:** `mistral:7b`  
**Budget:** `llama2:7b`

### Research/Planning (Sage, Felix, Orion)
**Best:** `llama2:13b`  
**Good:** `llama2:7b`  
**Budget:** `mistral:7b`

### Testing/Debugging (Patch, Pulse)
**Best:** `codellama:13b`  
**Good:** `codellama:7b`  
**Budget:** `llama2:7b`

## 🌟 Complete Free Setup (No API Keys)

### Quick Setup
```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Start Ollama
ollama serve &

# 3. Download models
ollama pull llama2        # General
ollama pull codellama     # Coding

# 4. Configure AI Dev Team
cd /home/mrnova420/ai-dev-team
python3 orchestrator.py

# 5. Select option 4 (Configure Settings)
# Leave API keys blank
# Edit config.yaml and set all agents to 'local'

# 6. Use your team!
python3 orchestrator.py
```

### Config for Free Setup
```yaml
# No API keys needed!
openai_api_key: ""
gemini_api_key: ""

# Ollama settings
ollama_url: "http://localhost:11434"
ollama_model: "codellama"  # For coding tasks

# All agents use local models
agent_models:
  helix: local
  aurora: local
  felix: local
  sage: local
  ember: local
  orion: local
  atlas: local
  mira: local
  vex: local
  sol: local
  echo: local
  nova: local
  quinn: local
  blaze: local
  ivy: local
  zephyr: local
  pixel: local
  script: local
  turbo: local
  sentinel: local
  link: local
  patch: local
  pulse: local
```

## 📚 Resources

- **Ollama:** https://ollama.ai
- **Model Library:** https://ollama.ai/library
- **Documentation:** https://github.com/ollama/ollama/blob/main/docs/api.md
- **Discord Community:** https://discord.gg/ollama

## ✅ Quick Test

After setup, test your local model:

```bash
python3 orchestrator.py
# Select: 2 (Solo Mode)
# Choose: 11 (Nova)

You: Write a simple Python function to add two numbers

Nova: [Response using local model...]
```

## 💡 Tips

1. **Start with smaller models** (7B) to test
2. **Use CodeLlama for coding** tasks
3. **Mix local and API models** for best results
4. **Keep Ollama running** in background
5. **Download models ahead** of time
6. **Use GPU** if available for better speed

---

**You can now run your entire AI Dev Team completely free with local models!** 🎉

No API keys, no costs, complete privacy! 🚀
