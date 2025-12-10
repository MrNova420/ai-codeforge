# Usage Guide

Complete guide to using the AI Dev Team effectively.

## Quick Start

### First Time
```bash
./setup_proper.py   # Configure once
./run               # Launch anytime
```

### Every Time
```bash
./run
```

## Two Modes

### 1. Team Collaboration Mode
**Best for:** Complex projects, multi-step tasks, learning

The Overseer (Helix) analyzes your request and coordinates multiple agents.

**Example Flow:**
```
You: "Create a REST API with user authentication"
  ↓
Helix: Analyzes request
  ↓
Aurora: Plans architecture
  ↓
Sol & Nova: Write backend code
  ↓
Sentinel: Adds tests
  ↓
Orion: Reviews code
  ↓
Results delivered to you
```

**Commands in collaboration mode:**
- `agents` - List all agents
- `files` - Show workspace files
- `exit` - Leave mode

### 2. Solo Agent Chat
**Best for:** Quick questions, specific expertise, direct conversation

Talk directly to one specialized agent.

**Available Agents:**

**Planners & Designers:**
- **Aurora** - System Architect (big picture design)
- **Felix** - UI/UX Designer (interfaces)
- **Sage** - Product Manager (requirements)
- **Ember** - Creative Strategist (innovation)

**Critics & Judges:**
- **Orion** - Code Reviewer (quality assurance)
- **Atlas** - Performance Analyst (optimization)
- **Mira** - Security Expert (vulnerabilities)
- **Vex** - Devil's Advocate (edge cases)

**Developers:**
- **Sol** - Full-Stack Developer (web apps)
- **Echo** - Frontend Developer (UI code)
- **Nova** - Backend Developer (APIs, databases)
- **Quinn** - Mobile Developer (iOS/Android)
- **Blaze** - DevOps Engineer (deployment)
- **Ivy** - Data Engineer (data pipelines)
- **Zephyr** - ML Engineer (AI/ML)

**Assistants:**
- **Pixel** - Documentation Writer (docs)
- **Script** - Automation Expert (scripts)
- **Turbo** - Optimization Specialist (performance)
- **Sentinel** - Testing Expert (test code)

**Specialists:**
- **Link** - Integration Specialist (APIs)
- **Patch** - Debugger/Fixer (bug fixes)
- **Pulse** - Monitoring Expert (observability)

**Overseer:**
- **Helix** - Team Coordinator (management)

## Effective Prompting

### Be Specific
❌ Bad: "Make a website"
✅ Good: "Create a Flask web app with login, user dashboard, and SQLite database"

### Include Context
❌ Bad: "Fix the bug"
✅ Good: "The login function in auth.py returns 500 error when password is empty. Add validation."

### Break Down Complex Tasks
❌ Bad: "Build a complete e-commerce platform"
✅ Good:
1. "Design database schema for products, users, and orders"
2. "Create REST API for product management"
3. "Add user authentication with JWT"
4. (Continue step by step)

## Examples

### Example 1: Quick Function
**Mode:** Solo Agent (Nova - Backend Developer)
**Prompt:** "Write a Python function to validate email addresses using regex"
**Time:** ~15 seconds

### Example 2: REST API
**Mode:** Solo Agent (Sol - Full-Stack Developer)
**Prompt:** "Create a Flask REST API for a todo list with CRUD operations"
**Time:** ~60 seconds

### Example 3: Full Feature
**Mode:** Team Collaboration
**Prompt:** "Design and implement a user authentication system with JWT tokens, password hashing, and refresh tokens"
**Time:** ~2-3 minutes
**Agents involved:** Helix, Aurora, Nova, Orion, Sentinel

### Example 4: Code Review
**Mode:** Solo Agent (Orion - Code Reviewer)
**Prompt:** "Review this function: [paste code]"
**Time:** ~20 seconds

### Example 5: Debugging
**Mode:** Solo Agent (Patch - Debugger)
**Prompt:** "This code throws IndexError on line 42. Help me fix it: [paste code]"
**Time:** ~30 seconds

## File Operations

Agents can work with files in the `workspace/` directory:

**Automatic:**
- Code generated → Saved to workspace
- Files you mention → Read from workspace

**Manual:**
```bash
# Check workspace
ls workspace/

# Edit files
nano workspace/myfile.py

# Ask agent to modify
"Update the validate_user function in auth.py to check email format"
```

## Memory & History

### Conversations are Saved
```bash
# View saved conversations
./run → Option 4 (Memory & History)
```

### Continue Previous Work
Each agent remembers your conversation within the session.

### Reset if Needed
Exit and restart `./run` for fresh start.

## Tips & Tricks

### 1. Start Simple
Test with small tasks before complex projects.

### 2. Use the Right Agent
- **Quick code:** Solo mode with specific developer
- **Architecture:** Aurora or Sage
- **Review:** Orion
- **Full project:** Team Collaboration

### 3. Iterate
Agents can improve their output:
```
You: "Make it more efficient"
You: "Add error handling"
You: "Write tests for this"
```

### 4. Save Your Work
```bash
# Copy from workspace
cp workspace/myproject.py ~/projects/

# Or work directly in workspace
cd workspace/
git init
```

### 5. Check Performance
If responses are slow:
```bash
./quick_test.py  # Run diagnostics
```
See `docs/PERFORMANCE.md` for optimization.

## Keyboard Shortcuts

- **Ctrl+C** - Cancel current operation
- **Ctrl+D** - Exit (in chat)
- **↑/↓** - Command history (in terminal)

## Common Issues

### "Model not found"
```bash
ollama pull codellama:7b
```

### "Connection refused"
```bash
ollama serve
```

### "Timeout error"
Query too complex for local model. Try:
1. Simpler prompt
2. API model (faster)
3. See PERFORMANCE.md

### "No config found"
```bash
./setup_proper.py
```

## Next Steps

1. ✅ Run `./quick_test.py` to verify setup
2. ✅ Try solo mode with simple question
3. ✅ Test team mode with small project
4. ✅ Read examples in `examples/`
5. ✅ Build something cool! 🚀
