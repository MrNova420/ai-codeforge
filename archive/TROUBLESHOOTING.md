# 🔧 Troubleshooting Guide

Quick fixes for common issues.

---

## 🚨 "Error: No module named 'openai'"

**Cause:** Packages not installed in virtual environment

**Fix:**
```bash
cd /home/mrnova420/ai-dev-team
./fix_setup.sh
```

Or manually:
```bash
source venv/bin/activate
pip install openai google-generativeai rich pyyaml requests
```

---

## 🚨 "Cannot connect to Ollama" / Connection Refused

**Cause:** Ollama server not running

**Fix:**
```bash
# Install Ollama first (if not installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve

# In another terminal, pull a model
ollama pull mistral:7b

# Now try again
./start_v2.sh
```

---

## 🚨 "externally-managed-environment"

**Cause:** Python PEP 668 prevents system-wide installs

**Fix:** Use virtual environment (already set up!)
```bash
# Run the fix script
./fix_setup.sh

# Or manually activate venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚨 "BrokenPipeError" / Gemini CLI Issues

**Cause:** Using wrong orchestrator (old one)

**Fix:** Use the correct launchers
```bash
# Use V2 (recommended)
./start_v2.sh

# Or V1
./start.sh

# Don't use:
python3 ai_dev_team_orchestrator.py  # ❌ Old version
```

---

## 🚨 No Models Configured / Empty Responses

**Cause:** No API keys and Ollama not running

**Fix Option 1 - Free Local Models:**
```bash
# Install and start Ollama
ollama serve

# Pull a model
ollama pull mistral:7b

# Run setup
./setup
# Choose: Free Setup
# Model: mistral:7b
```

**Fix Option 2 - Paid Models:**
```bash
./setup
# Choose: Quick Setup
# Add OpenAI or Gemini API key
```

---

## 🚨 Out of Memory / Model Too Large

**Cause:** Model too big for your RAM

**Fix:** Use smaller models
```bash
# For 8GB RAM
ollama pull mistral:7b

# For 4GB RAM
ollama pull phi:latest

# Edit config.yaml
agent_models:
  helix: mistral:7b
  nova: mistral:7b
  # ... all agents: mistral:7b
```

See `SMALLER_MODELS_GUIDE.md` for details.

---

## 🚨 Slow Responses

**Cause:** Model too large or slow

**Fix:** Use faster models
```bash
ollama pull mistral:7b    # Fastest quality
ollama pull zephyr:7b     # Very fast

# Update config.yaml to use these
```

---

## 🚨 "Command not found: ./start_v2.sh"

**Cause:** Not executable or wrong directory

**Fix:**
```bash
cd /home/mrnova420/ai-dev-team
chmod +x start_v2.sh start.sh
./start_v2.sh
```

---

## 🚨 Agents Not Responding / Stuck

**Cause:** Various - check error messages

**Common Fixes:**

### Check 1: Is Ollama running?
```bash
# In another terminal
ps aux | grep ollama

# If not running
ollama serve
```

### Check 2: Is model pulled?
```bash
ollama list

# If empty, pull one
ollama pull mistral:7b
```

### Check 3: Check config
```bash
cat config.yaml

# Should have either:
# - API keys (openai_api_key or gemini_api_key)
# - Or ollama configured with models
```

---

## 🚨 Import Errors

**Fix:** Reinstall in venv
```bash
cd /home/mrnova420/ai-dev-team
source venv/bin/activate
pip install --force-reinstall rich pyyaml openai google-generativeai requests
```

---

## 🚨 Can't Find Files / Workspace Empty

**Cause:** Need to actually use agents first

**Fix:**
```bash
./start_v2.sh
# Select: Team Collaboration
# Request: "Create a simple Python hello world program"
# Then check: workspace/
```

---

## 🚨 Models Keep Failing

**Diagnosis Steps:**

### Step 1: Check what you're using
```bash
cat config.yaml | grep -A 5 agent_models
```

### Step 2: If using local (Ollama)
```bash
# Is it running?
curl http://localhost:11434/api/tags

# Should return JSON with models
```

### Step 3: If using OpenAI/Gemini
```bash
# Check API key is set
cat config.yaml | grep api_key

# Test it works
python3 -c "import openai; print('OK')"
```

---

## 🚨 Permission Denied

**Fix:**
```bash
chmod +x start_v2.sh start.sh fix_setup.sh setup
```

---

## 🎯 Quick Diagnostic

Run this to check everything:

```bash
cd /home/mrnova420/ai-dev-team

echo "=== Checking Setup ==="

# Check venv
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "❌ No venv - run ./fix_setup.sh"
fi

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
    echo "Models available:"
    curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*"' | cut -d'"' -f4
else
    echo "❌ Ollama not running - start with: ollama serve"
fi

# Check config
if [ -f "config.yaml" ]; then
    echo "✅ Config exists"
else
    echo "❌ No config - run ./setup"
fi

# Check Python packages
source venv/bin/activate 2>/dev/null
python3 -c "import rich, openai; print('✅ Packages installed')" 2>/dev/null || echo "❌ Packages missing - run ./fix_setup.sh"
```

---

## 🆘 Still Having Issues?

### Option 1: Fresh Start
```bash
cd /home/mrnova420/ai-dev-team

# Remove old venv
rm -rf venv

# Run fix
./fix_setup.sh

# Reconfigure
./setup
```

### Option 2: Use Simpler V1
```bash
./start.sh
# V1 is simpler, might work better
```

### Option 3: Check Logs
```bash
# Run with verbose output
./start_v2.sh 2>&1 | tee debug.log
# Share debug.log for help
```

---

## 📋 Common Error Messages Decoded

| Error | Meaning | Fix |
|-------|---------|-----|
| "No module named..." | Package not installed | `./fix_setup.sh` |
| "Connection refused" | Ollama not running | `ollama serve` |
| "Model not found" | Model not pulled | `ollama pull mistral:7b` |
| "API key not configured" | No API key | `./setup` |
| "Out of memory" | Model too big | Use smaller model |
| "BrokenPipeError" | Wrong orchestrator | Use `./start_v2.sh` |
| "externally-managed" | System Python | Use venv (automatic) |

---

## ✅ Verification Checklist

Before asking for help, verify:

- [ ] `venv` directory exists
- [ ] Can activate venv: `source venv/bin/activate`
- [ ] Packages installed: `pip list | grep rich`
- [ ] Ollama running (if using local): `curl http://localhost:11434`
- [ ] Model pulled: `ollama list`
- [ ] Config exists: `ls config.yaml`
- [ ] Using correct launcher: `./start_v2.sh` not `python3 ai_dev_team_orchestrator.py`

---

## 🎯 Most Common Issue

**90% of issues are:**
1. Ollama not running
2. No model pulled
3. Wrong Python environment

**Quick fix:**
```bash
ollama serve &
ollama pull mistral:7b
./fix_setup.sh
./start_v2.sh
```

---

**Still stuck? Check:**
- `START_HERE_V2.md` - Getting started guide
- `SMALLER_MODELS_GUIDE.md` - Model selection help
- `V2_FEATURES.md` - Feature documentation
