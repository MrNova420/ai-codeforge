# Performance Guide

## Current Performance

### Model Speed (codellama:7b on typical hardware)
- **Generation Speed:** ~4-5 tokens/second
- **Simple Query (10 tokens):** ~2-3 seconds
- **Medium Query (50 tokens):** ~10-12 seconds  
- **Complex Query (200 tokens):** ~40-50 seconds

### Timeout Settings
- **Default:** 120 seconds (was 60s)
- **Covers:** Most queries up to ~500 tokens
- **Fails on:** Very complex multi-step reasoning

## Optimization Tips

### 1. Use Faster Models
```bash
# Smaller, faster models
ollama pull mistral:7b-instruct  # Optimized for instructions
ollama pull phi:latest          # Very fast, smaller

# Update config.yaml to use faster model
```

### 2. Switch to API Models
API models like GPT-4 or Gemini are much faster:
```bash
./setup_proper.py
# Choose OpenAI or Gemini
```

**Speed comparison:**
- Local (codellama:7b): 4-5 tokens/sec
- OpenAI GPT-3.5: 50-100 tokens/sec
- OpenAI GPT-4: 30-50 tokens/sec

### 3. Optimize Prompts
The system automatically:
- Limits response length (500 tokens max)
- Uses temperature 0.7 for balance
- Builds efficient prompts

### 4. Hardware Recommendations

**Minimum (usable):**
- CPU: 4 cores
- RAM: 8GB
- Speed: 3-5 tokens/sec

**Recommended (smooth):**
- CPU: 8+ cores
- RAM: 16GB+
- GPU: NVIDIA with CUDA
- Speed: 15-30 tokens/sec

**With GPU:**
```bash
# If you have NVIDIA GPU
ollama pull codellama:7b
# Ollama auto-detects and uses GPU
```

### 5. Reduce Context Size
Shorter conversations = faster responses:
- Start new chats for new topics
- Be concise in your requests
- Use solo mode for simple tasks

## Benchmarks

### Test: "Write a Python function to check if a number is prime"

| Configuration | Time | Speed |
|--------------|------|-------|
| codellama:7b (CPU) | 14s | 4.5 tok/s |
| mistral:7b (CPU) | 10s | 6.5 tok/s |
| codellama:7b (GPU) | 3s | 21 tok/s |
| GPT-3.5-turbo | 2s | 50 tok/s |
| GPT-4 | 4s | 30 tok/s |

### Test: "Create REST API with CRUD operations"

| Configuration | Time | Speed |
|--------------|------|-------|
| codellama:7b (CPU) | 60-80s | 4-5 tok/s |
| mistral:7b (CPU) | 40-50s | 6-7 tok/s |
| GPT-3.5-turbo | 8-10s | 50 tok/s |

## Troubleshooting

### "Read timed out" Error
Your query is too complex for the timeout:
1. Make request simpler
2. Increase timeout in `agent_chat_enhanced.py`
3. Switch to faster model
4. Use GPU acceleration

### Slow First Response
Normal - model needs to load:
- First query: +5-10 seconds (model loading)
- Subsequent queries: Normal speed
- Keep `ollama serve` running

### System Freezing
Using too much RAM:
```bash
# Check memory usage
free -h

# Use smaller model
ollama pull codellama:7b  # instead of 13b or 34b
```

## Future Improvements

### Planned
- [ ] Streaming responses in collaboration mode
- [ ] Parallel agent execution
- [ ] Response caching
- [ ] Model warm-up on startup

### Ideas
- GPU auto-detection and optimization
- Model switching based on query complexity
- Response quality vs speed tradeoff
