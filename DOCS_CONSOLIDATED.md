# AI CodeForge - Complete Documentation

**Version 1.0.0 - Universal Setup with Full Integration**

This document consolidates all essential information about AI CodeForge.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Interfaces](#interfaces)
4. [Features](#features)
5. [Agents](#agents)
6. [Configuration](#configuration)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 30-Second Setup

```bash
git clone https://github.com/MrNova420/ai-codeforge.git
cd ai-codeforge
./setup.sh

# Use any interface
./talk "create a REST API"          # Natural language
./codeforge code "create REST API"  # CLI
./webapp                            # Web interface
./run                               # Full orchestrator
```

**Works on ALL devices** - Python 3.8+, including Python 3.12+ with PEP 668 protection.

---

## Installation

### Automatic (Recommended)

```bash
./setup.sh
```

**What it does:**
- ✅ Creates virtual environment automatically
- ✅ Installs all dependencies
- ✅ Creates wrapper scripts
- ✅ Makes everything executable
- ✅ Works on all Python versions (3.8+)
- ✅ Solves PEP 668 errors automatically

### Manual Installation

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# Or: venv\Scripts\activate  # Windows

pip install -r requirements.txt
chmod +x codeforge run talk webapp start
```

### No Activation Needed

All scripts automatically use the virtual environment - no manual activation required!

---

## Interfaces

### 🌟 Talk - Natural Language (Easiest)

**Perfect for beginners and non-technical users**

```bash
./talk "I need a login system"
./talk "create a REST API for todo items"
./talk "list all agents"
./talk "use full orchestrator mode"
```

**Features:**
- Natural language input
- Auto-detects intent
- Selects best agents
- Access to full orchestrator
- No commands to memorize

### 💻 CodeForge - CLI

**Perfect for developers**

```bash
./codeforge code "create REST API"
./codeforge test "api.py"
./codeforge review "main.py"
./codeforge orchestrator "complex task"  # Full mode
./codeforge agents                       # List all
./codeforge features                     # List features
```

**Features:**
- Command-driven
- Fast execution
- Scriptable
- Full orchestrator access
- Agent and feature listing

### 🌐 WebApp - Browser Interface

**Perfect for teams and visual users**

```bash
./webapp
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# WebSocket: ws://localhost:8000/ws
```

**Features:**
- Visual dashboard
- REST API endpoints
- WebSocket real-time updates
- All 23 agents accessible
- Full orchestrator mode
- Task management
- Code editor

**API Endpoints:**
- `GET /api/agents` - List all agents
- `GET /api/features` - List all features
- `POST /api/execute` - Execute task

See [WEBAPP_API.md](WEBAPP_API.md) for complete API documentation.

### ⚡ Run - Full Orchestrator

**Perfect for complex projects**

```bash
./run
```

**Features:**
- All 23 agents active
- V3 advanced features
- Multi-agent collaboration
- Vector memory
- Research capabilities
- Code analysis
- Self-debugging

---

## Features

### Universal Integration

**ALL features accessible from ANY interface!**

The unified interface layer connects everything:

| Feature | Talk | CLI | WebApp | Run |
|---------|------|-----|--------|-----|
| All 23 Agents | ✅ | ✅ | ✅ | ✅ |
| Full Orchestrator | ✅ | ✅ | ✅ | ✅ |
| Collaboration V3 | ✅ | ✅ | ✅ | ✅ |
| Vector Memory | ✅ | ✅ | ✅ | ✅ |
| Research | ✅ | ✅ | ✅ | ✅ |
| Tool Registry | ✅ | ✅ | ✅ | ✅ |
| Code Execution | ✅ | ✅ | ✅ | ✅ |

### Key Capabilities

1. **Multi-Agent Collaboration** - JSON-based task delegation with parallel execution
2. **Vector Memory** - ChromaDB learning system for persistent knowledge
3. **Research Agent** - Web search and knowledge synthesis
4. **Tool Registry** - Extensible tool system
5. **Codebase Analysis** - AST-based code understanding
6. **Self-Debugging** - Agents detect and fix their own errors
7. **File Operations** - Smart file management
8. **Code Execution** - Safe sandbox environment

---

## Agents

### All 23 Specialized Agents

**Planners & Strategists:**
- **aurora** - Product Manager & Strategic Planner
- **sage** - Lead Architect & Technical Strategist
- **felix** - Senior Full-Stack Developer
- **ember** - Creative Director & Innovation Lead

**Critics & Reviewers:**
- **orion** - Senior Code Reviewer & Quality Lead
- **atlas** - Performance & Optimization Specialist
- **mira** - Security Engineer & AppSec Lead
- **vex** - Critical Analyst & Skeptic

**Specialists:**
- **sol** - Backend API Specialist
- **echo** - Frontend & UI Developer
- **nova** - DevOps & Infrastructure Engineer
- **quinn** - QA Lead & Test Automation
- **blaze** - Mobile Development Lead
- **ivy** - Data Engineer & Database Specialist
- **zephyr** - Cloud Architect

**Assistants:**
- **pixel** - UX Designer & Design System Lead
- **script** - Technical Writer & Documentation
- **turbo** - Performance Engineer
- **sentinel** - Monitoring & SRE Lead

**Special Agents:**
- **helix** - Research Lead & Technology Advisor
- **patch** - Bug Hunter & Debugging Specialist
- **pulse** - Integration Specialist
- **link** - Communication & Collaboration Lead

### Using Agents

**From any interface:**
```bash
# Natural language
./talk "list all agents"
./talk "use felix and sol for this task"

# CLI
./codeforge agents
./codeforge chat felix "help with API"

# WebApp API
GET /api/agents
```

---

## Configuration

### Basic Configuration

Configuration file: `config.yaml`

### API Keys

Set environment variables or create `.env` file:

```bash
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

### Virtual Environment

The setup automatically creates `venv/` directory. All scripts use it automatically.

**Manual activation (optional):**
```bash
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

---

## API Reference

### Unified Interface (Python)

```python
from unified_interface import get_unified_interface

# Get interface
unified = get_unified_interface()

# Execute task
result = unified.execute_task(
    task="create a REST API",
    mode="team",  # auto, solo, team, research, full_orchestrator
    agents=["felix", "sol"]  # Optional
)

# List agents
agents = unified.list_all_agents()  # Returns list of 23 agent names

# List features
features = unified.list_all_features()  # Returns dict with feature status

# Get agent info
info = unified.get_agent_info("felix")
# Returns: {"role": "...", "specialty": "..."}
```

### WebApp API (HTTP/WebSocket)

See [WEBAPP_API.md](WEBAPP_API.md) for complete WebApp API documentation including:
- REST endpoints
- WebSocket protocol
- JavaScript examples
- Python client examples

---

## Troubleshooting

### PEP 668 Error (Externally Managed Environment)

**Solution:** Run `./setup.sh` - it automatically creates a virtual environment.

### Import Errors

```bash
# Make sure setup was run
./setup.sh

# Or manually install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Scripts Not Executable

```bash
chmod +x codeforge run talk webapp start
```

### Port Already in Use (WebApp)

Change ports in `webapp.py` or kill existing process:
```bash
# Kill process on port 8000
kill $(lsof -t -i:8000)
```

### Feature Not Available

Some features require optional dependencies:

```bash
# For vector memory
pip install chromadb

# For research
pip install beautifulsoup4 requests-html
```

---

## Quick Reference

### Common Tasks

| Task | Command |
|------|---------|
| Generate code | `./talk "create X"` or `./codeforge code "X"` |
| Write tests | `./codeforge test "file.py"` |
| Review code | `./codeforge review "file.py"` |
| Fix bug | `./talk "fix the login bug"` |
| Deploy | `./talk "deploy to AWS"` |
| Research | `./talk "how do I implement X"` |
| Full orchestrator | `./run` or `./codeforge orchestrator "task"` |
| List agents | `./talk "list agents"` or `./codeforge agents` |
| WebApp | `./webapp` |

### File Structure

```
ai-codeforge/
├── README.md              # Main documentation
├── GETTING_STARTED.md     # Beginner guide
├── DOCS_CONSOLIDATED.md   # This file (complete docs)
├── WEBAPP_API.md          # WebApp API reference
├── setup.sh               # Auto-setup script
├── requirements.txt       # Python dependencies
├── codeforge*             # CLI wrapper
├── run*                   # Orchestrator wrapper
├── talk*                  # Natural language wrapper
├── webapp*                # WebApp wrapper
├── unified_interface.py   # Central integration layer
├── natural_interface.py   # Natural language processing
├── codeforge.py           # CLI implementation
├── webapp.py              # WebApp launcher
├── ui/                    # WebApp frontend & backend
│   ├── frontend/          # HTML/CSS/JS
│   └── backend/           # FastAPI WebSocket server
├── venv/                  # Virtual environment (auto-created)
└── ...                    # Other components
```

---

## Version History

### v1.0.0 (Current)
- ✅ Universal setup with automatic venv
- ✅ Full integration across all interfaces
- ✅ WebApp with complete API access
- ✅ Unified interface layer
- ✅ PEP 668 compliance
- ✅ Works on all devices

---

## Support

- **Documentation:** This file + README.md + GETTING_STARTED.md
- **WebApp API:** WEBAPP_API.md
- **GitHub:** https://github.com/MrNova420/ai-codeforge
- **Issues:** https://github.com/MrNova420/ai-codeforge/issues

---

**Status: Production Ready** ✅

All 23 agents ready | All features operational | All interfaces working | Complete integration
