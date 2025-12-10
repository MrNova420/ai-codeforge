# 🤖 AI CodeForge

**Autonomous Multi-Agent AI Development System**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/status-active-brightgreen.svg)]()

> An intelligent, self-learning multi-agent system with 23+ specialized AI agents that autonomously develop software, debug code, and collaborate like a real development team.

---

## 🌟 Highlights

- **🤝 Multi-Agent Collaboration** - JSON-based task delegation with parallel execution
- **🧠 Self-Learning Memory** - Vector database that learns from past experiences
- **🔍 Deep Code Understanding** - AST-based codebase analysis and semantic queries
- **🐛 Self-Debugging** - Agents automatically detect and fix their own errors
- **🌐 Web Research** - Search and synthesize information from online sources
- **📊 Impact Analysis** - Understand consequences before making changes

---

## 🚀 Quick Start

### Prerequisites

```bash
- Python 3.8+
- Ollama (for local LLMs) OR API keys (OpenAI/Gemini)
```

### Installation

```bash
# Clone
git clone https://github.com/MrNova420/ai-codeforge.git
cd ai-codeforge

# Install dependencies
pip install -r requirements.txt

# Setup (first time - 5-10 min)
python3 setup_proper.py

# Run (instant after setup)
python3 start.py
# or: ./run
# or: python3 orchestrator_v2.py
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
