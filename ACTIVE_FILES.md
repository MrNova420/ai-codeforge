# AI CodeForge - Active File Guide

This document clarifies which files are ACTIVE and which are deprecated/legacy.

## ✅ ACTIVE FILES (Use These)

### Core Orchestrators
- **orchestrator_v2.py** - MAIN orchestrator with full V3 features
  - Use this for: `./run` command
  - Has: Team collaboration, solo chat, research mode, memory, files
  - Status: ✅ ACTIVE - Fully integrated

### Collaboration Engines
- **collaboration_v3.py** - MAIN collaboration engine
  - Use this for: Multi-agent task delegation with JSON
  - Has: Parallel execution, dependency management, AgentManager
  - Status: ✅ ACTIVE - Used by orchestrator_v2

### Agent Chat
- **agent_chat_enhanced.py** - MAIN agent chat interface
  - Use this for: Direct agent communication with tools
  - Has: File manager, code executor, streaming support
  - Status: ✅ ACTIVE - Used by orchestrator_v2

### Natural Interface
- **natural_interface.py** - MAIN natural language interface
  - Use this for: `./talk` command
  - Has: Intent detection, agent selection, unified interface
  - Status: ✅ ACTIVE - Just fixed (no more hardcoded auth code)

### Research
- **researcher_agent.py** - MAIN research agent
  - Use this for: Web search and knowledge synthesis
  - Has: WebSearchTool, WebPageReaderTool integration
  - Status: ✅ ACTIVE - Just improved error handling

## ⚠️ LEGACY/DEPRECATED FILES (Don't Use)

### Old Collaboration Engines
- **collaboration_simple.py** - DEPRECATED
  - Why: Basic implementation, no advanced features
  - Replace with: collaboration_v3.py
  
- **collaboration_enhanced.py** - DEPRECATED  
  - Why: Superseded by v3
  - Replace with: collaboration_v3.py
  
- **collaboration_engine.py** - DEPRECATED
  - Why: Old version, replaced by v3
  - Replace with: collaboration_v3.py

### Old Orchestrator
- **orchestrator.py** - DEPRECATED
  - Why: No V3 features, basic implementation
  - Replace with: orchestrator_v2.py

### Old Agent Chat
- **agent_chat.py** - DEPRECATED
  - Why: Basic version without enhanced features
  - Replace with: agent_chat_enhanced.py

## 🔄 Migration Path

If you're using old files:

1. **Replace collaboration_simple/enhanced/engine** → **collaboration_v3.py**
   - All have same interface: `handle_request(task, timeout)`
   - V3 adds: JSON parsing, parallel execution, better error handling

2. **Replace orchestrator.py** → **orchestrator_v2.py**
   - Same command-line interface
   - V2 adds: Full V3 features, memory, files, research

3. **Replace agent_chat.py** → **agent_chat_enhanced.py**
   - Same interface: `send_message(message, stream=False)`
   - Enhanced adds: File operations, code execution, better tools

## 📝 How to Clean Up

To remove deprecated files (AFTER ensuring everything works):

```bash
# Move to archive
mkdir -p archive/deprecated_v1
mv collaboration_simple.py archive/deprecated_v1/
mv collaboration_enhanced.py archive/deprecated_v1/
mv collaboration_engine.py archive/deprecated_v1/
mv orchestrator.py archive/deprecated_v1/
mv agent_chat.py archive/deprecated_v1/
```

## 🎯 Which File Does What?

### User Commands
- `./talk` → natural_interface.py → unified_interface.py
- `./run` → orchestrator_v2.py → collaboration_v3.py
- `./codeforge` → codeforge.py → (various modes)
- `./webapp` → webapp.py → ui/backend/websocket_server.py

### Backend Flow
```
User Input
    ↓
natural_interface.py (intent detection)
    ↓
unified_interface.py (task routing)
    ↓
orchestrator_v2.py (if complex task)
    ↓
collaboration_v3.py (multi-agent delegation)
    ↓
agent_chat_enhanced.py (individual agent execution)
    ↓
Result back to user
```

## 🔧 Integration Status

### Fully Integrated ✅
- WebSocket server → unified_interface ✅
- orchestrator_v2 → collaboration_v3 ✅
- orchestrator_v2 → agent_chat_enhanced ✅
- natural_interface → unified_interface ✅
- researcher_agent → web search tools ✅

### Files Without Duplicates ✅
- unified_interface.py (single source of truth)
- code_executor.py (single implementation)
- file_manager.py (single implementation)
- memory_manager.py (single implementation)
- researcher_agent.py (single implementation)

## 📊 Merge Complete

As of this commit:
- ✅ orchestrator_v2 uses collaboration_v3 (not old versions)
- ✅ orchestrator_v2 uses agent_chat_enhanced (not basic)
- ✅ natural_interface fixed to use actual results (not hardcoded)
- ✅ researcher_agent improved error handling
- ✅ All interfaces access full project features

**Status: NO MORE 20+ DUPLICATE VERSIONS - EVERYTHING INTEGRATED!**
