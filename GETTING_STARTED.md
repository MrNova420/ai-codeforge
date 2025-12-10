# 🚀 Getting Started with AI CodeForge

**New here? This guide will get you up and running in 5 minutes!**

---

## Step 1: Installation (One Command)

```bash
git clone https://github.com/MrNova420/ai-codeforge.git
cd ai-codeforge
./setup.sh
```

**That's it!** The setup automatically:
- ✅ Creates a virtual environment (works on ALL devices)
- ✅ Installs all dependencies
- ✅ Makes everything ready to use

**No activation needed** - all scripts work immediately after setup!

---

## Step 2: Choose Your Starting Point

### 🌟 Option 1: Talk Interface (EASIEST - Start Here!)

**Best for:** Everyone, especially if you're new to AI development tools

Just describe what you want in plain English:

```bash
./talk "I need a login system for my website"
./talk "Create a REST API for a todo app"
./talk "Help me debug this Python function"
```

**No commands to remember** - just chat naturally!

---

### 💻 Option 2: CodeForge CLI (For Developers)

**Best for:** Developers who prefer command-line tools

Quick commands for specific tasks:

```bash
./codeforge code "create a REST API"        # Generate code
./codeforge test "api.py"                   # Generate tests
./codeforge review "src/main.py"            # Code review
./codeforge fix "login bug"                 # Fix issues
./codeforge agents                          # List all 23 agents
./codeforge help                            # Show all commands
```

**Interactive mode:**
```bash
./codeforge
# Then type commands interactively
```

---

### 🌐 Option 3: Web Interface (Visual Dashboard)

**Best for:** Teams, visual users, or those who prefer GUIs

```bash
./webapp
```

Then open your browser to **http://localhost:3000**

**Features:**
- 📊 Visual dashboard with live stats
- 🤖 Manage all 23 agents visually
- 📋 Task tracking and management
- 💻 Built-in code editor
- 👥 Great for sharing with team members

---

### ⚡ Option 4: Full Orchestrator (Power Users)

**Best for:** Complex projects, advanced users, production workflows

```bash
./run
```

**This gives you:**
- All 23 specialized AI agents working together
- Multi-agent collaboration (agents discuss and iterate)
- Vector memory (learns from past work)
- Research capabilities (web search and synthesis)
- Code analysis and understanding
- Self-debugging agents

**When to use:** Large projects, production code, or when you need multiple agents collaborating on complex tasks.

---

## 🔄 All Features Are Accessible Everywhere! (FULLY INTEGRATED)

**Great news:** You don't have to choose just one interface! ALL functionality is accessible from ANY starting point through the unified integration layer.

### From `./talk` (Natural Language):
```bash
./talk "use the full orchestrator to build a complex e-commerce platform"
./talk "list all agents"
./talk "show features"
./talk "activate all 23 agents for this project"
```
**Works!** Natural language interface has direct access to unified system.

### From `./codeforge` (CLI):
```bash
./codeforge orchestrator "complex task"     # Full orchestrator mode
./codeforge features                        # List all features
./codeforge agents                          # List all 23 agents
./codeforge team "task" --mode collaborative
```
**Works!** CLI has unified interface integration with orchestrator command.

### From `./webapp` (Web Interface):
```bash
./webapp  # Then use API endpoints
```
**Works!** WebSocket and REST API provide complete access:
- `/api/agents` - List all agents
- `/api/features` - List all features  
- `/api/execute` - Execute any task
- WebSocket messages for real-time execution
**See WEBAPP_API.md for complete API documentation**

### From `./run` (Orchestrator):
```bash
./run
```
**Works!** This IS the full orchestrator - all features enabled by default.

**Status:** ✅ Full integration complete. Start with any interface, access any feature.

---

## Step 3: Try Your First Task

Let's create something simple to test it out:

### Using Talk (Easiest):
```bash
./talk "Create a simple Python function that calculates factorial"
```

### Using CodeForge CLI:
```bash
./codeforge code "Create a Python function that calculates factorial"
```

### Using WebApp:
1. Start: `./webapp`
2. Open browser to http://localhost:3000
3. Use the task creation interface
4. Enter: "Create a simple Python function that calculates factorial"

---

## Quick Reference

| What I Want to Do | Command to Use |
|-------------------|----------------|
| Generate code | `./talk "create X"` or `./codeforge code "X"` |
| Write tests | `./codeforge test "file.py"` |
| Review code | `./codeforge review "file.py"` |
| Fix a bug | `./talk "fix the login bug"` |
| Complex project | `./run` then describe project |
| Visual interface | `./webapp` |
| See all agents | `./codeforge agents` |
| Get help | `./codeforge help` |

---

## Common Questions

### Q: Which interface should I use?
**A:** Start with `./talk` - it's the easiest! Once comfortable, explore `./codeforge` for more control.

### Q: Do I need to activate the virtual environment?
**A:** No! All scripts automatically use the virtual environment. Just run them directly.

### Q: What are the 23 agents?
**A:** Specialized AI agents for different roles: planners, developers, reviewers, testers, security experts, etc. Use `./codeforge agents` to see them all.

### Q: Can I use this for production code?
**A:** Yes! Use `./run` for the full orchestrator with all advanced features, collaboration, and quality checks.

### Q: What if I get errors?
**A:** 
- Make sure you ran `./setup.sh` first
- Check that Python 3.8+ is installed: `python3 --version`
- Try: `./test_universal_setup.sh` to validate your setup

---

## Next Steps

1. ✅ **Complete Setup:** Run `./setup.sh` if you haven't
2. 🎯 **Start Simple:** Try `./talk "create a hello world function"`
3. 📖 **Learn More:** Check `./codeforge help` for all commands
4. 🚀 **Explore:** Try different interfaces to find your favorite
5. 📚 **Read Docs:** See [README.md](README.md) for detailed features

---

## Need Help?

- 📋 **All commands:** `./codeforge help`
- 🤖 **List agents:** `./codeforge agents`
- 🧪 **Test setup:** `./test_universal_setup.sh`
- 📚 **Documentation:** [README.md](README.md)
- 🐛 **Issues:** https://github.com/MrNova420/ai-codeforge/issues

---

**Happy coding! 🎉**
