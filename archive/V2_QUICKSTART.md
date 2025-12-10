# 🚀 V2 Quick Start Guide

Get up and running with Ultimate AI Dev Team V2 in 2 minutes!

---

## ⚡ Super Quick Start

```bash
cd /home/mrnova420/ai-dev-team

# If first time, run setup
./setup

# Launch V2
./start_v2.sh
```

That's it! You're ready to go! 🎉

---

## 📖 5-Minute Tutorial

### Step 1: Launch V2
```bash
./start_v2.sh
```

You'll see the enhanced menu:
```
Main Menu:
1. 🤝 Team Collaboration Mode (Real multi-agent)
2. 💬 Solo Agent Chat
3. 👥 View All Agents
4. 💾 Memory & History
5. 📁 Workspace Files
6. ⚙️  Configuration
7. ✨ About New Features
8. 🚪 Exit
```

### Step 2: Try Team Collaboration

**Select option 1**

The team status dashboard appears showing all 23 agents.

**Try this example request:**
```
Create a Python calculator with tests
```

**Watch what happens:**
1. Helix (overseer) analyzes your request
2. Tasks are automatically delegated to agents:
   - Aurora might plan the architecture
   - Nova implements the calculator
   - Pulse creates the tests
3. You see real-time status updates
4. All results are presented
5. Code is saved in workspace/

**Result:** Complete calculator with tests, created by your team!

### Step 3: Check the Workspace

**Select option 5** - Browse workspace files

You'll see:
```
Workspace Files:
1. calculator.py
2. test_calculator.py
3. README.md
```

Select a file number to view it!

### Step 4: Try Solo Mode with Streaming

**From main menu, select option 2**

1. Choose an agent (try Nova - Lead Engineer)
2. Enable streaming: Yes
3. Enable tools: Yes

**Try asking:**
```
Explain the calculator code you created
```

Watch the response stream in real-time! ⚡

### Step 5: View History

**Select option 4** - Memory & History

See all your conversations:
```
Saved Conversations:
#  Title                      Messages  Last Updated
1  Team Task: Create a...     8         2025-12-09 20:45
2  Solo chat with Nova        5         2025-12-09 20:50
```

Select a number to view the full conversation!

---

## 🎯 Common Use Cases

### Use Case 1: Build an App
```
Menu → 1 (Team Collaboration)

Your request: "Create a Flask web app with login"

What happens:
- Aurora designs architecture
- Nova writes the Flask code
- Ivy adds security features
- Pulse creates tests
- Files appear in workspace/
```

### Use Case 2: Code Review
```
Menu → 1 (Team Collaboration)

Your request: "Review the code quality in workspace/"

What happens:
- Quinn checks style and practices
- Atlas does perfectionist review
- Mira gives constructive feedback
- You get comprehensive review from 3 perspectives
```

### Use Case 3: Debug Something
```
Menu → 2 (Solo Mode)
Select: Patch (The Fixer)

Your message: "The login isn't working in app.py"

What happens:
- Patch reads the file
- Analyzes the issue
- Suggests fix
- Can even write the fix if you ask
```

### Use Case 4: Learn & Understand
```
Menu → 2 (Solo Mode)
Select: Sage (Research Maven)

Your message: "Explain async/await in Python"

What happens:
- Sage provides deep, researched explanation
- Uses examples
- Streaming response in real-time
- Conversation saved for later
```

---

## 💡 Pro Tips

### Tip 1: Use Team Mode for Complex Tasks
Team collaboration really shines for:
- Building complete applications
- Multi-step processes
- Tasks needing different expertise
- Code review from multiple angles

### Tip 2: Use Solo Mode for Deep Dives
Solo mode is great for:
- Focused conversations
- Learning specific topics
- Iterative development
- Quick questions

### Tip 3: Enable Streaming
Streaming gives you:
- Immediate feedback
- Better experience
- See thinking in real-time
- Cancel if going wrong direction

### Tip 4: Use the Right Agent
Each agent has unique personality:
- **Aurora** - Big picture planning
- **Nova** - Solid implementation
- **Quinn** - Beautiful, clean code
- **Ivy** - Security focus
- **Patch** - Bug hunting
- **Pulse** - Comprehensive testing
- **Atlas** - Perfectionist review
- **Sage** - Deep research

### Tip 5: Check Workspace Often
Agents create files in workspace/:
- Code they write
- Tests they create
- Documentation
- Configuration files

Browse with Menu → Option 5

### Tip 6: Review Conversations
All chats are saved:
- Resume later
- Reference past solutions
- Track your progress
- Learn from history

Access via Menu → Option 4

---

## 🎨 Customization

### Change Models Per Agent
Edit `config.yaml`:
```yaml
agent_models:
  nova: gpt-4              # Use GPT-4 for lead dev
  quinn: codellama:13b     # Use CodeLlama for code review
  aurora: gemini-pro       # Use Gemini for planning
```

### Adjust Timeouts
Edit `orchestrator_v2.py`:
```python
code_executor = CodeExecutor(workspace_dir, timeout=60)  # 60 seconds
```

### Change Workspace Location
Edit at top of `orchestrator_v2.py`:
```python
WORKSPACE_DIR = PROJECT_ROOT / "my_workspace"
```

---

## 🆚 V1 vs V2 Comparison

| Feature | V1 | V2 |
|---------|----|----|
| **Multi-agent** | Simulated | ✅ Real collaboration |
| **Memory** | None | ✅ Persistent across sessions |
| **File ops** | None | ✅ Read/write in workspace |
| **Code execution** | None | ✅ Python/JS/Bash sandbox |
| **Streaming** | No | ✅ Real-time responses |
| **Progress tracking** | No | ✅ Visual dashboard |
| **History** | Lost on exit | ✅ Saved and browsable |

**Recommendation:** Use V2 for all new work!

---

## 🐛 Quick Troubleshooting

### "No API key configured"
→ Run `./setup` to configure your keys

### "Cannot connect to Ollama"
→ For local models, install and run Ollama:
```bash
# Install from https://ollama.ai
ollama serve
```

### "File not found in workspace"
→ Use relative paths from workspace root
→ Example: `app.py` not `/full/path/app.py`

### "Streaming not working"
→ Update OpenAI library:
```bash
pip install openai --upgrade
```

### "Agents not collaborating"
→ Check storage/ directory exists
→ Try restarting the app

---

## 📚 Next Steps

### Learn More
- Read `V2_FEATURES.md` for complete feature list
- Check agent profiles in `*_agents.md` files
- Review `FOR_NEXT_COPILOT_SESSION.md` for V1 context

### Try These Scenarios
1. **Build a game** - "Create a terminal-based snake game"
2. **API wrapper** - "Create a REST API client for GitHub"
3. **Data analysis** - "Analyze CSV file and create visualizations"
4. **Documentation** - "Generate API docs for workspace code"

### Customize Your Team
- Modify agent personalities in markdown files
- Add new models to config
- Adjust collaboration strategies
- Create custom workflows

---

## 🎉 You're Ready!

You now know:
- ✅ How to launch V2
- ✅ Team collaboration mode
- ✅ Solo agent mode
- ✅ Memory and history
- ✅ Workspace management
- ✅ Common use cases
- ✅ Pro tips

**Start creating with your AI dev team!** 🚀

```bash
./start_v2.sh
```

Questions? Check `V2_FEATURES.md` for detailed documentation!
