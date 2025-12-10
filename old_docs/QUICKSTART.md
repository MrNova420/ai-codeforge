# Quick Start Guide

Get your Ultimate AI Dev Team running in under 5 minutes!

## Step 1: Install Dependencies

```bash
cd ai-dev-team
pip install -r requirements.txt
```

Or use the automated launcher:
```bash
./start.sh
```

## Step 2: Get Your API Keys (or Use Local Models)

You have three options:

### Option A: OpenAI (Best quality, requires API key)
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-...`)

### Option B: Gemini (Good quality, free tier available)
1. Go to https://makersuite.google.com/app/apikey
2. Create an API key
3. Copy the key

### Option C: Local Models (Completely free, private)
1. Install Ollama: https://ollama.ai
2. Run: `ollama serve`
3. Pull a model: `ollama pull llama2` or `ollama pull codellama`
4. Configure agents to use `local` in config.yaml

**See [LOCAL_MODELS_GUIDE.md](LOCAL_MODELS_GUIDE.md) for complete local setup.**

## Step 3: Run the Orchestrator

```bash
python3 orchestrator.py
```

On first run, you'll be prompted to enter your API keys. You can:
- Enter both keys
- Enter only one (OpenAI OR Gemini)
- Skip and add them later via the config menu

## Step 4: Choose Your Mode

### Team Mode (Best for complex projects)
```
Select option: 1
```

This launches Helix (the Overseer) who coordinates all 17 agents:
- 5 Planners/Designers
- 5 Critics/Judges  
- 5 Developers
- 5 Developer Assistants
- 1 Debugger/Fixer
- 1 Tester

**Example conversation:**
```
You: I need to build a web API with user authentication

Helix: I'll coordinate the team. Aurora and Felix will design the 
architecture, Sage will research best practices, Nova and Ivy will 
implement it, and Patch and Pulse will test it. Let's start with 
the requirements...
```

### Solo Mode (Best for focused tasks)
```
Select option: 2
```

Choose any agent for specialized work:

**Example with Atlas (Code Reviewer):**
```
You: Review this function [paste code]

Atlas: This code has 3 critical issues:
1. No input validation
2. SQL injection vulnerability  
3. Missing error handling
Here's how to fix it...
```

**Example with Nova (Lead Engineer):**
```
You: How should I structure a microservices architecture?

Nova: For microservices, I recommend...
[detailed architecture advice]
```

## Step 5: Explore Features

### View All Agents
```
Select option: 3
```
See all 17 agents, their roles, and assigned models.

### Change Configuration
```
Select option: 4
```
Update API keys or agent model assignments.

## Tips for Best Results

### 1. Use Team Mode for Big Projects
Let Helix coordinate multiple agents working together:
```
You: Build a complete e-commerce platform with cart, checkout, and admin panel
```

### 2. Use Solo Mode for Specific Tasks
Pick the right specialist:
- **Code review?** → Atlas (The Perfectionist)
- **Architecture?** → Nova (Lead Engineer)
- **Performance?** → Blaze (Performance Guru)
- **Security?** → Ivy (Security Specialist)
- **Bug fixing?** → Patch (The Fixer)

### 3. Customize Agent Models
Edit `config.yaml` to assign different AI models to different agents:

```yaml
agent_models:
  helix: openai     # Helix uses GPT-4 (best for coordination)
  aurora: gemini    # Aurora uses Gemini (good for creative work)
  nova: openai      # Nova uses GPT-4 (best for coding)
  sage: gemini      # Sage uses Gemini (good for research)
```

### 4. Give Clear Instructions
**Good:**
```
Create a REST API for a blog with posts, comments, and user authentication. 
Use Python FastAPI and PostgreSQL. Include proper error handling and tests.
```

**Not as good:**
```
Make an API
```

## Common Issues

### "API key not configured"
**Solution:** Run orchestrator, select option 4, and add your API keys.

### "openai package not installed"  
**Solution:** `pip install -r requirements.txt`

### Agent gives generic responses
**Solution:** Be more specific in your requests, or switch to a different model in config.yaml.

## Next Steps

1. **Read the full README.md** for advanced features
2. **Customize agent personalities** by editing the `.md` files
3. **Experiment with different agents** to find your favorites
4. **Try Team Mode** for a complex project and see the agents collaborate

## Quick Reference

**Start:**
```bash
python3 orchestrator.py
# or
./start.sh
```

**Team Mode Commands:**
- `agents` - List active team members
- `status` - Get project status
- `exit` - End session

**Solo Mode Commands:**
- `exit` or `quit` - End conversation
- Just type your questions naturally!

## Support

- Check `README.md` for full documentation
- Edit `config.yaml` for configuration
- Customize agent profiles in `*_agents.md` files

---

Ready to build something amazing with your AI Dev Team? 🚀
