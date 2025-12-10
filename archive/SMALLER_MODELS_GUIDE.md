# 🚀 Guide to Using Smaller/Faster Models

**For users with limited RAM or wanting faster responses**

---

## 🎯 Quick Recommendations

### Got 8GB RAM?
```yaml
# Edit config.yaml
agent_models:
  helix: codellama:7b       # Overseer - good coding
  nova: codellama:7b        # Lead dev
  quinn: mistral:7b         # Code review - very fast
  aurora: zephyr:7b         # Planning - efficient
  sage: llama2:7b           # Research
  # ... all others: mistral:7b or zephyr:7b
```

### Got 4GB RAM?
```yaml
# Use tiny models (slower but work)
agent_models:
  helix: phi:latest         # 2.7B params
  nova: phi:latest
  # All agents: phi:latest
```

### Want FAST responses?
```yaml
# Fastest models
agent_models:
  helix: mistral:7b         # Fastest quality model
  nova: zephyr:7b           # Very fast
  quinn: openchat:7b        # Fast chat
  # All agents: mistral:7b or zephyr:7b
```

---

## 📊 Model Comparison by Size

### Tiny Models (2-4GB RAM)
| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| phi:latest | 2.7B | 3GB | ⚡⚡⚡⚡⚡ | ⭐⭐ | Low-end devices |
| tinyllama:latest | 1.1B | 2GB | ⚡⚡⚡⚡⚡ | ⭐ | Very limited RAM |

### Small Models (8GB RAM) ⭐ RECOMMENDED
| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| **mistral:7b** | 7B | 8GB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | **Best balance** |
| **zephyr:7b** | 7B | 8GB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Fast, efficient |
| codellama:7b | 7B | 8GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Coding tasks |
| llama2:7b | 7B | 8GB | ⚡⚡⚡⭐ | ⭐⭐⭐ | General purpose |
| openchat:7b | 7B | 8GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Conversation |
| starling-lm:7b | 7B | 8GB | ⚡⚡⚡⭐ | ⭐⭐⭐⭐ | Helpful answers |
| neural-chat:7b | 7B | 8GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Chat |

### Medium Models (16GB RAM)
| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| codellama:13b | 13B | 16GB | ⚡⚡⭐ | ⭐⭐⭐⭐ | Advanced coding |
| llama2:13b | 13B | 16GB | ⚡⚡⭐ | ⭐⭐⭐⭐ | High quality |
| deepseek-coder:6.7b | 6.7B | 8GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Efficient coding |

### Large Models (32GB+ RAM)
| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| codellama:34b | 34B | 32GB | ⚡⭐ | ⭐⭐⭐⭐ | Professional coding |
| mixtral:8x7b | 47B | 32GB | ⚡⚡ | ⭐⭐⭐⭐ | Best local quality |
| llama2:70b | 70B | 64GB | ⚡ | ⭐⭐⭐⭐⭐ | Maximum quality |

---

## 🎯 Configuration Examples

### Example 1: Fast & Light (8GB RAM)
```yaml
# config.yaml
ollama_url: "http://localhost:11434"

agent_models:
  # Overseer - good quality needed
  helix: mistral:7b
  
  # Developers - fast coding
  nova: codellama:7b
  quinn: mistral:7b
  blaze: zephyr:7b
  ivy: codellama:7b
  zephyr: mistral:7b
  
  # Planners - efficient
  aurora: zephyr:7b
  felix: mistral:7b
  sage: llama2:7b
  ember: zephyr:7b
  orion: mistral:7b
  
  # Critics - quality matters
  atlas: mistral:7b
  mira: openchat:7b
  vex: mistral:7b
  sol: llama2:7b
  echo: mistral:7b
  
  # Assistants - fast is good
  pixel: zephyr:7b
  script: zephyr:7b
  turbo: mistral:7b
  sentinel: zephyr:7b
  link: zephyr:7b
  
  # Specialists
  patch: codellama:7b
  pulse: mistral:7b
```

### Example 2: Ultra Fast (4GB RAM)
```yaml
agent_models:
  helix: phi:latest
  nova: phi:latest
  # ... all agents: phi:latest
```

### Example 3: Quality on Budget (8GB)
```yaml
agent_models:
  # Important agents get best 7B models
  helix: openchat:7b          # Overseer
  nova: codellama:7b          # Lead dev
  quinn: openchat:7b          # Code review
  
  # Others get fastest
  aurora: mistral:7b
  felix: mistral:7b
  sage: mistral:7b
  # ... rest: mistral:7b
```

---

## 💡 Tips for Better Performance

### 1. Use Mistral for Most Agents
**Why?** Mistral:7b is the fastest quality model
```yaml
# Set most agents to mistral:7b
agent_models:
  helix: mistral:7b
  nova: mistral:7b
  quinn: mistral:7b
  # ... most agents
```

### 2. Save Best Models for Key Agents
```yaml
# Only use codellama for actual coding
agent_models:
  nova: codellama:7b        # Lead developer
  quinn: codellama:7b       # Code reviewer
  patch: codellama:7b       # Bug fixer
  # Others: mistral:7b
```

### 3. Mix Model Sizes
```yaml
# Use smaller for simple tasks
agent_models:
  helix: codellama:13b      # Overseer - needs quality
  nova: codellama:7b        # Developer
  pixel: mistral:7b         # Assistant - speed ok
  script: zephyr:7b         # Assistant - very fast
```

### 4. Start Ollama with Memory Limit
```bash
# If you have limited RAM
OLLAMA_MAX_LOADED_MODELS=1 ollama serve
```

---

## 🚀 Quick Setup Steps

### Step 1: Install Ollama
```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai
```

### Step 2: Pull Recommended Models
```bash
# Start with the fastest
ollama pull mistral:7b
ollama pull zephyr:7b

# Add coding support
ollama pull codellama:7b

# Optional: better quality
ollama pull openchat:7b
ollama pull llama2:7b
```

### Step 3: Start Ollama
```bash
ollama serve
```

### Step 4: Configure AI Dev Team
```bash
cd ai-dev-team
./setup
# Choose: Free Setup
# Choose model: mistral:7b
```

### Step 5: Test
```bash
./start_v2.sh
# Select Solo Mode
# Try: mistral:7b agent
```

---

## 🎯 Troubleshooting

### "Out of Memory" Error
**Solution:** Use smaller models
```bash
# Instead of codellama:13b
ollama pull codellama:7b

# Or use mistral (fastest/smallest quality)
ollama pull mistral:7b
```

### Slow Responses
**Solution:** Use faster models
```bash
# Mistral is fastest quality model
ollama pull mistral:7b

# Zephyr is also very fast
ollama pull zephyr:7b
```

### Model Not Found
**Solution:** Pull the model first
```bash
ollama pull <model-name>

# Example
ollama pull mistral:7b
```

---

## 📊 Speed Comparison

**Approximate tokens/second on average hardware:**

| Model | Speed | Quality | RAM | Recommended |
|-------|-------|---------|-----|-------------|
| mistral:7b | ~45 tok/s | ⭐⭐⭐⭐ | 8GB | ⭐ **BEST** |
| zephyr:7b | ~50 tok/s | ⭐⭐⭐ | 8GB | Very good |
| codellama:7b | ~40 tok/s | ⭐⭐⭐ | 8GB | For coding |
| openchat:7b | ~45 tok/s | ⭐⭐⭐⭐ | 8GB | Great chat |
| llama2:7b | ~35 tok/s | ⭐⭐⭐ | 8GB | General |
| codellama:13b | ~25 tok/s | ⭐⭐⭐⭐ | 16GB | Better coding |
| llama2:13b | ~20 tok/s | ⭐⭐⭐⭐ | 16GB | High quality |

---

## 🎯 Bottom Line

### For 8GB RAM (Most Users)
```bash
ollama pull mistral:7b
# Use mistral:7b for everything!
```

### For 16GB RAM
```bash
ollama pull codellama:13b
ollama pull mistral:7b
# Use 13b for important, 7b for rest
```

### For 4GB RAM
```bash
ollama pull phi:latest
# Use phi for everything
```

---

## 📚 Next Steps

1. **Choose your models** from tables above
2. **Pull them:** `ollama pull <model-name>`
3. **Configure:** Edit `config.yaml` or run `./setup`
4. **Test:** Try different models in solo mode
5. **Optimize:** Keep what works, change what doesn't

**Start with mistral:7b - it's the best balance!** ⚡

---

Need help? Check: `START_HERE_V2.md` or `V2_FEATURES.md`
