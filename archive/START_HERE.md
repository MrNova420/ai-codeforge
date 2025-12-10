# 🚀 AI DEV TEAM - START HERE

## Brand New Setup (First Time)

### Step 1: Run Setup
```bash
cd ~/ai-dev-team
./setup_proper.py
```

**What it does:**
1. Checks your Python version
2. Creates virtual environment
3. Installs all packages
4. Asks what you want:
   - **FREE** → Local models (Ollama)
   - **PAID** → API models (OpenAI/Gemini)
5. Downloads/configures everything
6. Creates config for all 23 agents

**Takes:** 5-10 minutes (mostly downloading models if local)

### Step 2: Run System
```bash
./run
```

That's it! Pick Team or Solo mode and start using it.

---

## Already Setup?

Just run:
```bash
./run
```

---

## What You Get

### 23 AI Agents Ready To Work:

**Planners & Designers** (4 agents)
- Aurora - Product Visionary
- Felix - UX Architect  
- Sage - System Designer
- Ember - Creative Director

**Critics & Quality** (4 agents)
- Orion - Code Critic
- Atlas - Architecture Judge
- Mira - Security Analyst
- Vex - Performance Critic

**Developers** (7 agents)
- Sol - Full-Stack Dev
- Echo - Frontend Specialist
- Nova - Backend Architect
- Quinn - Database Expert
- Blaze - DevOps Engineer
- Ivy - Mobile Developer
- Zephyr - API Specialist

**Assistants** (4 agents)
- Pixel - Documentation Writer
- Script - Code Generator
- Turbo - Quick Scripter
- Sentinel - Error Hunter

**Specialists** (3 agents)
- Link - Integration Specialist
- Patch - Bug Fixer
- Pulse - Health Monitor

**Overseer** (1 agent)
- Helix - Team Coordinator

---

## Two Modes

### 1. Team Collaboration Mode
- Tell Helix what you want
- Helix analyzes and explains approach
- Agents work together (conceptually)
- Great for complex projects

### 2. Solo Agent Chat  
- Pick one specific agent
- Chat directly with them
- Get specialized help
- Faster for simple tasks

---

## System Requirements

### Minimum (Local Mode)
- **RAM:** 8GB (can run 1 small model)
- **Disk:** 4-5GB free
- **OS:** Linux/Mac/Windows

### Recommended (Local Mode)
- **RAM:** 16GB+ (can run bigger models)
- **Disk:** 10GB+
- **GPU:** Optional (speeds things up)

### API Mode (OpenAI/Gemini)
- **RAM:** 2GB (just runs the interface)
- **Disk:** 500MB
- **Internet:** Required
- **Cost:** ~$0.01-0.10 per conversation

---

## Optimization for Low Resources

The system is **optimized** to work well even on low-end devices:

### Single Model Mode (Default)
- All 23 agents use the **same model**
- Only loads model **once** into RAM
- **Memory usage:** ~4-6GB total
- Works perfectly on 8GB RAM systems

### How It Works
1. You pick ONE model during setup
2. All agents share it
3. They get unique personalities through prompts
4. No performance loss, same quality

### Benefits
✅ Low RAM usage  
✅ Fast responses (model stays loaded)  
✅ Works on budget hardware  
✅ Still get 23 specialized agents  

---

## Troubleshooting

### "Setup not complete" error
```bash
./setup_proper.py
```

### Ollama not found
```bash
# Install Ollama first
curl https://ollama.ai/install.sh | sh

# Then run setup
./setup_proper.py
```

### Responses too slow
- **Local:** Use smaller model (mistral:7b vs codellama:34b)
- **API:** Check internet connection

### Out of memory
- **Local:** Use smaller model or close other apps
- **API:** Switch to API mode (uses less RAM)

---

## What's Different Here

### NOT Like Other Systems
❌ No hard-coded models  
❌ No forced choices  
❌ No hidden assumptions  
❌ No "must have X installed"  

### What We DO
✅ Ask what YOU want  
✅ Install what YOU need  
✅ Configure for YOUR system  
✅ Work with YOUR resources  

### User-Friendly = Real
- First-time user with nothing? ✅ Works
- Power user with everything? ✅ Works
- Low-end laptop? ✅ Works  
- Server with 128GB RAM? ✅ Works

---

## Files Overview

### You Need To Know
- `setup_proper.py` - First-time setup wizard
- `run` - Launch the system
- `config.yaml` - Your settings (created by setup)

### You Can Ignore
- Everything else (system handles it)

---

## Quick Start (TL;DR)

Brand new:
```bash
./setup_proper.py  # 5-10 mins
./run              # instant
```

Already setup:
```bash
./run  # instant
```

**That's literally it.**

---

## Need Help?

Check the error message - they explain exactly what to do.

Examples:
- "Ollama not found" → Install Ollama
- "Setup not complete" → Run ./setup_proper.py
- "Model not found" → Re-run setup or pull model

The system tells you what's wrong and how to fix it.

---

## Summary

✅ Real first-time setup  
✅ Works on any system  
✅ Optimized for low resources  
✅ 23 specialized agents  
✅ Free or paid options  
✅ Actually user-friendly  

**Ready?** Run `./setup_proper.py` and let's go! 🚀
