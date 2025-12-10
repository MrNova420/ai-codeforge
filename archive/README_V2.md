# 🤖 Ultimate AI Dev Team V2

> **Elite AI development team with real collaboration, persistent memory, and code execution**

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/yourusername/ai-dev-team)
[![Status](https://img.shields.io/badge/status-production--ready-green.svg)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)]()

---

## 🌟 What is This?

An orchestration system that manages **23 unique AI agents**, each with distinct personalities and expertise, working together as a real development team. Now with **real collaboration**, **persistent memory**, **file operations**, and **code execution**.

### Why V2?

**V1** was great - 23 agents, 20+ models, beautiful interface. But agents didn't actually *work together*.

**V2** changes everything:
- ✅ Agents **really collaborate** on tasks
- ✅ Conversations **saved** across sessions  
- ✅ Agents **read/write** files
- ✅ Agents **execute** code
- ✅ **Real-time streaming** responses
- ✅ **Visual progress** tracking

---

## ⚡ Quick Start

```bash
# Navigate to project
cd /home/mrnova420/ai-dev-team

# First time only - run setup
./setup

# Launch V2
./start_v2.sh
```

**That's it!** 🎉

---

## 🎯 What Can It Do?

### Real Multi-Agent Collaboration
```
You: "Create a web server with authentication and tests"

→ Helix (Overseer): Analyzes and delegates
  ├─ Aurora: Designs architecture
  ├─ Nova: Implements web server
  ├─ Ivy: Adds secure authentication
  └─ Pulse: Creates comprehensive tests

→ All work in parallel
→ Results aggregated
→ Complete solution delivered
```

### Persistent Memory
```
Session 1: "Create a calculator"
→ Calculator created in workspace/

[Exit and restart]

Session 2: "Add trigonometry functions"
→ Agent remembers previous work
→ Extends existing calculator
→ All history preserved
```

### File Operations
```
You: "Review the code in workspace/app.py"

→ Agent reads the file
→ Analyzes code quality
→ Suggests improvements
→ Can write fixes directly
```

### Code Execution
```
You: "Test if the calculator works"

→ Agent executes: python workspace/calculator.py
→ Captures output: "All tests passed ✓"
→ Validates functionality
```

---

## 🎭 Meet the Team

### 👔 Planners & Designers (5 agents)
- **Aurora** - Visionary strategist, big picture thinking
- **Felix** - Detail architect, meticulous blueprints
- **Sage** - Research maven, deep analysis
- **Ember** - Creative designer, UI/UX expert
- **Orion** - Systems planner, process optimizer

### 🎯 Critics & Judges (5 agents)
- **Atlas** - The Perfectionist, uncompromising standards
- **Mira** - Constructive analyst, balanced feedback
- **Vex** - The Challenger, questions assumptions
- **Sol** - The Veteran, wisdom and experience
- **Echo** - Data-driven judge, metrics focus

### 💻 Developers (5 agents)
- **Nova** - Lead engineer, system architecture
- **Quinn** - Code artisan, clean beautiful code
- **Blaze** - Performance guru, optimization expert
- **Ivy** - Security specialist, compliance focus
- **Zephyr** - Integration expert, APIs and automation

### 🛠️ Developer Assistants (5 agents)
- **Pixel** - Nova's assistant
- **Script** - Quinn's assistant
- **Turbo** - Blaze's assistant
- **Sentinel** - Ivy's assistant
- **Link** - Zephyr's assistant

### 🔧 Specialists (3 agents)
- **Patch** - The Fixer, bug hunting expert
- **Pulse** - The Tester, comprehensive QA
- **Helix** - The Overseer, team coordinator

---

## 🚀 Key Features

### V2 Enhancements

| Feature | Description | Status |
|---------|-------------|--------|
| **Real Collaboration** | Agents actually work together, not simulated | ✅ |
| **Task System** | Automatic task delegation and tracking | ✅ |
| **Persistent Memory** | All conversations saved and retrievable | ✅ |
| **File Operations** | Read, write, modify code files safely | ✅ |
| **Code Execution** | Python, JavaScript, Bash sandbox | ✅ |
| **Streaming** | Real-time token-by-token responses | ✅ |
| **Progress Dashboard** | Visual team status and activity | ✅ |
| **History Browser** | Browse and resume past conversations | ✅ |

### Original Features (V1)

| Feature | Description | Status |
|---------|-------------|--------|
| **23 Unique Agents** | Each with distinct personality | ✅ |
| **20+ AI Models** | OpenAI, Gemini, Local (Ollama) | ✅ |
| **Per-Agent Models** | Different model for each agent | ✅ |
| **Setup Wizard** | Easy configuration in 2 minutes | ✅ |
| **Team Mode** | Coordinate entire team | ✅ |
| **Solo Mode** | Chat with individual agents | ✅ |
| **Rich UI** | Beautiful terminal interface | ✅ |

---

## 📖 Usage Examples

### Example 1: Build a Complete App
```bash
./start_v2.sh
→ Select: 1 (Team Collaboration)

You: "Create a Todo app with Flask backend and HTML frontend"

Result:
✓ Architecture designed by Aurora
✓ Backend implemented by Nova
✓ Frontend created by Ember
✓ Security added by Ivy
✓ Tests written by Pulse
✓ All files in workspace/
```

### Example 2: Code Review
```bash
→ Select: 1 (Team Collaboration)

You: "Review the code quality in workspace/"

Result:
✓ Quinn: Style and best practices review
✓ Atlas: Perfectionist critique
✓ Mira: Constructive improvements
✓ Comprehensive multi-perspective review
```

### Example 3: Debug Issue
```bash
→ Select: 2 (Solo Mode)
→ Choose: Patch (The Fixer)

You: "The login function isn't working"

Patch:
✓ Reads the file
✓ Identifies the bug
✓ Explains the issue
✓ Suggests fix
✓ Can write the fix directly
```

### Example 4: Learn Something
```bash
→ Select: 2 (Solo Mode)
→ Choose: Sage (Research Maven)
→ Enable streaming: Yes

You: "Explain async/await in detail"

Sage:
✓ Streams comprehensive explanation
✓ Provides code examples
✓ Covers edge cases
✓ Conversation saved for reference
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│          Orchestrator V2 (Main UI)              │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│ Agent Loader │  │ Collaboration    │
│ (23 Agents)  │  │ Engine           │
└──────────────┘  └────────┬─────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │ Task    │    │ Memory   │    │ File     │
    │ Manager │    │ Manager  │    │ Manager  │
    └─────────┘    └──────────┘    └──────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Code         │
                  │ Executor     │
                  └──────────────┘
```

---

## 🎮 Interface Modes

### 1. Team Collaboration Mode
- Helix coordinates the team
- Tasks automatically delegated
- Parallel execution
- Real-time status updates
- Comprehensive results

### 2. Solo Agent Chat
- Direct 1-on-1 with any agent
- Optional streaming
- Optional file/code tools
- Deep focused conversations
- All personalities available

### 3. Memory & History
- Browse past conversations
- Resume any session
- View full history
- Delete old sessions
- Search through messages

### 4. Workspace Browser
- View created files
- Read file contents
- Check agent output
- Create example projects
- File management

---

## 🛠️ Installation

### Requirements
- Python 3.8+
- pip
- Optional: Ollama (for local models)

### Dependencies
```bash
pip install -r requirements.txt
```

Installs:
- rich (terminal UI)
- pyyaml (configuration)
- openai (GPT models)
- google-generativeai (Gemini)
- requests (HTTP/Ollama)
- prompt-toolkit (enhanced input)
- questionary (interactive prompts)

### API Keys
You'll need at least one:
- OpenAI API key (paid)
- Google Gemini API key (free tier available)
- Ollama local setup (completely free)

Configure via the setup wizard: `./setup`

---

## 🎨 Configuration

### Model Assignment
Edit `config.yaml`:
```yaml
agent_models:
  helix: gpt-4              # Overseer gets best model
  nova: gpt-4               # Lead dev gets GPT-4
  quinn: codellama:13b      # Code review uses CodeLlama
  aurora: gemini-pro        # Planning uses Gemini
  sage: llama2:13b          # Research uses Llama2
  # ... configure all 23 agents
```

### Mix Models Freely
```yaml
agent_models:
  helix: gpt-4              # Paid OpenAI
  nova: gemini-pro          # Free Gemini
  quinn: codellama:13b      # Free local
  patch: gpt-3.5-turbo      # Cheaper OpenAI
```

### Workspace Settings
```python
# orchestrator_v2.py
WORKSPACE_DIR = PROJECT_ROOT / "workspace"  # Change location
```

---

## 📁 Project Structure

```
ai-dev-team/
├── 🎯 Core V2 (Enhanced)
│   ├── orchestrator_v2.py           ⭐ Main application
│   ├── collaboration_engine.py      ⭐ Multi-agent coordination
│   ├── agent_chat_enhanced.py       ⭐ Streaming + tools
│   ├── task_manager.py              ⭐ Task system
│   ├── memory_manager.py            ⭐ Persistent memory
│   ├── file_manager.py              ⭐ File operations
│   └── code_executor.py             ⭐ Code sandbox
│
├── 📚 Core V1 (Original)
│   ├── orchestrator.py
│   ├── agent_chat.py
│   └── setup_wizard.py
│
├── 👥 Agents (23 profiles)
│   ├── planner_designer_agents.md
│   ├── critic_judge_agents.md
│   ├── developer_agents.md
│   ├── developer_assistant_agents.md
│   ├── debugger_fixer_agent.md
│   ├── tester_agent.md
│   └── overseer_agent.md
│
├── 💾 Data & Storage
│   ├── workspace/                   # Agent-created files
│   └── storage/
│       ├── conversations/           # Saved chats
│       └── tasks.json              # Task database
│
├── 🚀 Launchers
│   ├── start_v2.sh                 ⭐ Launch V2
│   ├── start.sh                     # Launch V1
│   └── setup                        # Setup wizard
│
├── ⚙️ Configuration
│   ├── config.yaml
│   └── requirements.txt
│
└── 📖 Documentation
    ├── README_V2.md                ⭐ This file
    ├── V2_FEATURES.md              ⭐ Complete feature guide
    ├── V2_QUICKSTART.md            ⭐ Quick tutorial
    └── [15+ other guides]
```

---

## 🔒 Safety & Security

### File Operations
- ✅ Sandboxed to workspace only
- ✅ Whitelist of safe extensions
- ✅ No system file access
- ✅ All operations logged

### Code Execution
- ✅ Isolated environment
- ✅ Timeout limits
- ✅ No network access
- ✅ Resource restrictions

### Memory
- ✅ Local storage only
- ✅ No external uploads
- ✅ User-controlled data

---

## 🎯 Roadmap

### V2.0 ✅ (Current)
- [x] Real multi-agent collaboration
- [x] Persistent memory
- [x] File operations
- [x] Code execution
- [x] Streaming responses
- [x] Progress tracking

### V2.1 (Next)
- [ ] Optional Web UI
- [ ] Git integration
- [ ] More languages (Go, Rust, Java)
- [ ] Advanced task dependencies
- [ ] Agent feedback learning

### V3.0 (Future)
- [ ] Voice interaction
- [ ] Image generation
- [ ] Database operations
- [ ] API integration tools
- [ ] Deployment automation

---

## 🤝 Contributing

This is a personal project, but ideas welcome!

### Areas for Contribution
- New agent personalities
- Additional AI model integrations
- Enhanced collaboration strategies
- Performance optimizations
- Documentation improvements

---

## 📄 License

MIT License - See LICENSE file

---

## 🙏 Acknowledgments

Built with:
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal UI
- [OpenAI](https://openai.com) - GPT models
- [Google Gemini](https://ai.google.dev/) - Gemini models
- [Ollama](https://ollama.ai) - Local model runtime

Inspired by the dream of AI agents that truly collaborate!

---

## 📞 Support

### Quick Links
- **Quick Start:** See `V2_QUICKSTART.md`
- **Full Features:** See `V2_FEATURES.md`
- **V1 Context:** See `FOR_NEXT_COPILOT_SESSION.md`

### Common Issues
- **No API key:** Run `./setup`
- **Ollama error:** Install from https://ollama.ai
- **Streaming issues:** Update openai: `pip install openai --upgrade`
- **File errors:** Check workspace/ permissions

---

## 🎉 Ready to Start?

```bash
./start_v2.sh
```

**Experience the power of real AI team collaboration!** 🚀

---

**Version 2.0** | Production Ready | December 2025
