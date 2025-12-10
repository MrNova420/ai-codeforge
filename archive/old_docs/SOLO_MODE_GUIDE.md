# Solo Agent Mode - Quick Guide

**Status:** ✅ Fully Working  
**Last Tested:** December 10, 2025

---

## Quick Start

```bash
cd ~/ai-dev-team
./run
# Choose option 2 (Solo Agent Chat)
# Select an agent
# Start coding!
```

---

## Agent Selection Guide

Pick the right agent for your task:

### Frontend/Web Development
- **Aurora** - React, Vue, modern frontends
- **Pixel** - CSS, design, styling, layouts
- **Orion** - Full-stack web apps

### Backend Development
- **Felix** - Python, Flask, Django
- **Nova** - Node.js, APIs, databases
- **Atlas** - Database design, SQL, schemas

### Specialized Tasks
- **Sage** - Architecture, system design
- **Sol** - Testing, QA, test cases
- **Vex** - Security, validation, auth
- **Echo** - Documentation, READMEs
- **Patch** - Debugging, fixing bugs
- **Script** - Automation, scripts, CLI tools
- **Turbo** - Performance optimization
- **Blaze** - Speed improvements

### Creative/AI
- **Ember** - Creative solutions, brainstorming
- **Mira** - AI/ML, data science

### DevOps/Infrastructure
- **Quinn** - DevOps, CI/CD, deployment
- **Sentinel** - Monitoring, logging, alerts
- **Link** - API integration, webhooks
- **Pulse** - Health checks, diagnostics

### Management
- **Helix** - Project oversight, planning

---

## Example Sessions

### Build a Python API
```
Agent: Felix (Python specialist)
Task: "Create a Flask API with a /hello endpoint that returns JSON"

Result:
✅ Working Flask app in 94 seconds
✅ Clean, tested code
✅ Ready to run
```

### Create a Website
```
Agent: Aurora (Frontend specialist)
Task: "Build a simple portfolio website with HTML and CSS"

Result:
✅ Responsive HTML structure
✅ Modern CSS styling
✅ Professional layout
```

### Fix a Bug
```
Agent: Patch (Debugging specialist)
Task: "This function throws TypeError, help me fix it: [paste code]"

Result:
✅ Root cause identified
✅ Fixed code provided
✅ Explanation included
```

---

## Tips for Best Results

### 1. Be Specific
❌ "Make a website"
✅ "Create a single-page website with a header, hero section, and contact form using HTML and CSS"

### 2. One Task at a Time
❌ "Build an API, add auth, create frontend, deploy to AWS"
✅ "Create a Flask API with user authentication endpoints"

### 3. Provide Context
❌ "Fix this bug"
✅ "This Python function throws IndexError on line 15 when the list is empty. Here's the code: [paste]"

### 4. Use the Right Agent
- **Complex architecture?** → Sage
- **Quick Python script?** → Felix or Script
- **Website styling?** → Pixel
- **API design?** → Nova or Zephyr

---

## Performance Notes

### Current Setup
- Model: codellama:7b
- Speed: ~2 tokens/second
- Time: 60-120 seconds per response

### To Speed Up
1. Use **mistral:7b** instead (lighter model)
2. Keep prompts concise
3. Avoid asking for long outputs
4. Set realistic expectations for local AI

---

## Common Issues

### Agent is Slow
**Normal.** Local models take 1-2 minutes. This is expected.

### Agent Doesn't Understand
**Rephrase.** Be more specific or break into smaller tasks.

### Code Doesn't Work
**Use Patch or Sol.** Copy the error, paste it, and ask for a fix.

### Want Multiple Agents?
**Team Mode is broken.** For now, use solo mode sequentially:
1. Felix creates backend
2. Aurora creates frontend  
3. Sol writes tests

---

## Files Created

Agents save code to `workspace/` directory:
```
ai-dev-team/
└── workspace/
    └── [your files here]
```

---

## Quick Commands

```bash
# Run system
./run

# Test single agent directly
python3 test_single_agent.py

# Check configuration
cat config.yaml

# See workspace files
ls -la workspace/

# Quick system test
./quick_test.py
```

---

## Next Steps

Once you've used solo mode successfully:
1. Read `PROJECT_REVISION_PLAN.md` for v3 architecture
2. Consider helping implement JSON-based collaboration
3. Check `AGENT_ENHANCEMENT_STRATEGY.md` for memory features

---

**Bottom Line:** Solo mode works great. Use it while team mode gets fixed! 🚀
