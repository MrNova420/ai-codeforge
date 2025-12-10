# 🤖 AI CodeForge v1.0.0

**Complete AAA-Grade AI Development Team - Production Ready**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](VERSION)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Production Ready](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()
[![Ready to Use](https://img.shields.io/badge/ready-100%25-success.svg)]()

> **Just talk to it!** 23 specialized AI agents working as a complete development team. No code required - describe what you want in plain English and watch it build!

**🎉 NEW: Natural Language Interface** - "I need a login system" → Complete working code!

---

## ⚡ 60-Second Quick Start

```bash
# 1. Setup (creates virtual environment automatically)
./setup.sh

# 2. Start talking! (no activation needed - wrappers handle it)
./talk "I need a login system for my website"
```

**That's it!** Works on all devices, all Python versions.

**📖 New to AI CodeForge?** Read [GETTING_STARTED.md](GETTING_STARTED.md) for a complete beginner's guide!

---

---

## 🌟 Highlights

- **🤝 Multi-Agent Collaboration** - JSON-based task delegation with parallel execution
- **🧠 Self-Learning Memory** - Vector database that learns from past experiences
- **🔍 Deep Code Understanding** - AST-based codebase analysis and semantic queries
- **🐛 Self-Debugging** - Agents automatically detect and fix their own errors
- **🌐 Web Research** - Search and synthesize information from online sources
- **📊 Impact Analysis** - Understand consequences before making changes

---

## 🎯 Choose Your Interface

AI CodeForge offers **4 interfaces** - pick the one that fits your style:

### 🌟 1. Talk - Natural Language (Easiest!)
**Best for:** Everyone, especially beginners

```bash
./talk "I need a login system for my website"
./talk "Create a REST API for a todo app"
```

**No commands to remember** - just describe what you want!

### 💻 2. CodeForge CLI - Command Line
**Best for:** Developers who like terminal commands

```bash
./codeforge code "create REST API"       # Generate code
./codeforge test "api.py"                # Write tests
./codeforge review "main.py"             # Code review
./codeforge agents                       # List all agents
```

Fast and command-driven with specific operations.

### 🌐 3. WebApp - Browser Interface
**Best for:** Teams, visual users, dashboards

```bash
./webapp
# Open http://localhost:3000 in your browser
```

**Features:**
- 📊 Real-time dashboard with live stats
- 🤖 Visual agent management (all 23 agents)
- 📋 Task creation and tracking
- 💻 Built-in code editor
- 👥 Perfect for team collaboration

### ⚡ 4. Run - Full Orchestrator (Power Users)
**Best for:** Complex projects, production workflows

```bash
./run
```

**Advanced features:**
- All 23 agents collaborating
- Vector memory and learning
- Web research capabilities
- Code analysis and understanding
- Self-debugging agents

---

## 🚀 Quick Start

### Prerequisites

```bash
- Python 3.8+
- Ollama (for local LLMs) OR API keys (OpenAI/Gemini)
```

### Easy Installation (Recommended)

```bash
# Clone and setup in one go
git clone https://github.com/MrNova420/ai-codeforge.git
cd ai-codeforge
./setup.sh

# That's it! No activation needed - all scripts auto-detect venv

# Choose your interface:
./codeforge              # Interactive CLI with commands (code, test, review, etc.)
./run                    # Full orchestrator - All 23 agents + V3 advanced features
./talk "create an API"   # Natural language - Just describe what you want
./webapp                 # Web UI - Visual dashboard and management
```

**Which interface should you use?**

| Interface | Best For | When to Use |
|-----------|----------|-------------|
| **`./talk`** | **Beginners, non-technical users** | Just describe what you want in plain English. No commands to remember! Start here if you're new. |
| **`./codeforge`** | **Developers who like CLIs** | When you want specific operations (code, test, review, fix). Fast and command-driven. |
| **`./webapp`** | **Teams, visual users** | When you prefer a web dashboard, need to share with team members, or want visual task management. |
| **`./run`** | **Power users, complex projects** | When you need all 23 agents collaborating, advanced memory, research capabilities, and full V3 features. |

**🎯 Start here:** New users should try `./talk` first - it's the easiest!

**✨ Universal Design:** Works on all devices and Python versions (3.8+). The setup automatically:
- Creates a virtual environment (solves PEP 668 externally-managed-environment errors)
- Installs all dependencies
- Creates wrapper scripts that auto-use the venv

**💡 Optional:** Use `source activate.sh` to manually activate the venv for custom commands

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/MrNova420/ai-codeforge.git
cd ai-codeforge

# Create virtual environment (recommended for all devices)
python3 -m venv venv

# Install dependencies (using venv)
venv/bin/pip install -r requirements.txt    # On Linux/Mac
# Or: venv\Scripts\pip install -r requirements.txt  # On Windows

# Make scripts executable
chmod +x codeforge run talk webapp start

# Run directly (no activation needed!)
./codeforge              # CLI with specific commands (code, test, review)
./run                    # Full orchestrator with all 23 agents + V3 features
./talk "build an API"    # Natural language interface
./webapp                 # Web browser UI
# Or run Python directly: python3 orchestrator_v2.py
```

### CLI Commands

```bash
# Interactive mode
codeforge                              # Start interactive shell

# Quick commands
codeforge code "create REST API"       # Generate code
codeforge test "api.py"                # Generate tests
codeforge review "src/api.py"          # Review code
codeforge fix "login bug"              # Fix issue
codeforge design "checkout flow"       # Design feature
codeforge security "src/"              # Security audit
codeforge research "GraphQL"           # Research technology
codeforge team "build app"             # Full team collaboration

# Team modes
codeforge team --parallel "task"       # All agents simultaneously
codeforge team --sequential "task"     # Production pipeline
codeforge team --collaborative "task"  # Agents discuss & iterate
codeforge team --autonomous "task"     # Agents self-organize

# Production cycle
codeforge build "E-commerce Platform"  # Complete 6-phase workflow

# Information
codeforge help                         # Show all commands
codeforge agents                       # List all 23 agents
codeforge status                       # System status
```

---

## 💡 Key Features (V3 - Fully Integrated)

### 1. Collaboration V3 ✨
JSON-based multi-agent coordination with automatic task delegation, parallel execution, and AgentManager for resilient threading.

### 2. Vector Memory System 🧠
Persistent learning using ChromaDB with semantic search across past solutions, errors, code snippets, and feedback.

### 3. Codebase Graph 📊
Deep code understanding through AST parsing, relationship tracking, and semantic queries like "what calls this function?" and impact analysis.

### 4. Self-Correcting Agents 🔄
Agents that test their own code, detect errors, learn from past failures, and automatically retry with improvements up to 3 times.

### 5. Researcher Agent 🔍
Web search integration that finds information, synthesizes documentation, extracts code examples, and generates research reports with citations.

### 6. Tool Registry 🛠️
Extensible tool system with centralized management, role-based access control, and usage tracking for all agent capabilities.

### 7. Complete Agent Ecosystem 👥
23 specialized agents working in harmony, each wrapped with advanced features like self-correction and memory access.

---

## 📖 Usage

### Team Mode (Collaborative)

```bash
./run
# Choose option 1
# Enter: "Build a Flask REST API with JWT authentication"
```

The system will:
1. Analyze the request
2. Delegate to appropriate agents (Felix for backend, Vex for security)
3. Coordinate parallel work
4. Integrate results

### Solo Mode (Single Agent)

```bash
./run
# Choose option 2
# Select agent (e.g., Felix - Python Expert)
# Chat directly with that agent
```

### Programmatic Usage

```python
# Code Understanding
from codebase import CodebaseGraphManager, QueryEngine

graph = CodebaseGraphManager(project_root="./myproject")
query = QueryEngine(graph)
impact = query.impact_of_changing("MyClass")

# Research
from researcher_agent import ResearcherAgent

researcher = ResearcherAgent()
report = researcher.research("How to implement OAuth2")

# Self-Correction
from agents.specialized import SelfCorrectingAgent

corrector = SelfCorrectingAgent(agent, memory)
result = corrector.generate_and_test(task="Create a safe divide function")
```

---

## 🏗️ Architecture

```
AI CodeForge
│
├── 🎭 Orchestrator V2          # Main coordination
├── 🤝 Collaboration V3         # Multi-agent delegation  
├── ⚙️  Agent Manager            # Threading & execution
├── 🔧 Tool System              # Extensible tools
├── 💾 Memory System            # Vector storage
├── 🗺️  Codebase Graph          # Code understanding
│
└── 🤖 23+ Specialized Agents
    ├── Aurora (Frontend)
    ├── Felix (Python)
    ├── Vex (Security)
    ├── Researcher (Web)
    └── ...and 19 more
```

---

## 📊 What's Implemented

### ✅ Complete (v0.1.0)

- Multi-agent collaboration system
- Tool registry & standardized interface
- ChromaDB vector memory
- AST-based codebase graph
- Self-correction framework
- Web research capabilities
- Background code indexing
- Impact analysis

### 🔄 In Progress

- QA Engineer agent
- Comprehensive test suite
- Enhanced documentation

### 📋 Roadmap

- Hierarchical task trees
- Architect agent
- Git workflow integration
- Docker sandboxing
- WebSocket UI
- DevOps agents (CI/CD, Infrastructure)

---

## 📚 Documentation

- **[Strategic Plans](MASTER_IMPLEMENTATION_ROADMAP.md)** - Full implementation roadmap
- **[Solo Mode Guide](SOLO_MODE_GUIDE.md)** - How to use individual agents
- **[V3 Implementation](V3_IMPLEMENTATION_SUCCESS.md)** - Technical details
- **[Progress Summary](PROGRESS_SUMMARY_FULL.md)** - What we've built

---

## 🤝 Contributing

Contributions welcome! Please submit a Pull Request.

```bash
# Development setup
pip install -r requirements-dev.txt
pytest  # Run tests
```

---

## 📝 License

MIT License - See [LICENSE](LICENSE)

---

## 🙏 Credits

- **[Ollama](https://ollama.ai/)** - Local LLM support
- **[ChromaDB](https://www.trychroma.com/)** - Vector database
- **[Rich](https://github.com/Textualize/rich)** - Beautiful terminal UI

---

## ⭐ Support

If you find this useful, please star the repo!

**Questions?** Open an [Issue](https://github.com/YOUR_USERNAME/ai-codeforge/issues)

---

**Built with ❤️ and AI**
