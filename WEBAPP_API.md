# WebApp API Documentation

## Overview

The AI CodeForge WebApp now has **complete access to all features** through an integrated backend API. The webapp is effectively **the whole project** accessible through a web interface.

## Features Available in WebApp

✅ **All 23 AI Agents** - Access any agent individually or as a team  
✅ **Full Orchestrator Mode** - All agents + V3 advanced features  
✅ **Collaboration Engines** - V3 JSON-based multi-agent collaboration  
✅ **Vector Memory** - Persistent learning across sessions  
✅ **Research Capabilities** - Web search and knowledge synthesis  
✅ **Tool Registry** - All registered tools accessible  
✅ **File Operations** - Smart file management  
✅ **Code Execution** - Safe sandbox execution  
✅ **Codebase Analysis** - AST-based code understanding  

## API Endpoints

### REST API

#### GET `/api/agents`
Get list of all 23 available agents with their roles and specialties.

**Response:**
```json
{
  "agents": [
    {
      "name": "felix",
      "role": "Senior Developer",
      "specialty": "Full-stack development"
    },
    ...
  ],
  "total": 23,
  "timestamp": "2025-12-10T09:57:00"
}
```

#### GET `/api/features`
Get list of all available features and their status.

**Response:**
```json
{
  "features": {
    "orchestrator": true,
    "collaboration_v3": true,
    "vector_memory": true,
    "researcher": true,
    "tool_registry": true,
    "file_manager": true,
    "code_executor": true
  },
  "timestamp": "2025-12-10T09:57:00"
}
```

#### POST `/api/execute`
Execute a task using the unified interface.

**Request:**
```json
{
  "task": "Create a REST API for user management",
  "mode": "auto",
  "agents": ["felix", "sol", "quinn"]
}
```

**Modes:**
- `"auto"` - Auto-detect best mode
- `"solo"` - Single agent
- `"team"` - Multi-agent collaboration
- `"research"` - Research mode
- `"full_orchestrator"` - Full orchestrator with all 23 agents + V3 features

**Response:**
```json
{
  "task": "Create a REST API for user management",
  "mode": "team",
  "result": {
    "status": "team",
    "task": "...",
    "agents": ["felix", "sol", "quinn"]
  },
  "status": "success",
  "timestamp": "2025-12-10T09:57:00"
}
```

### WebSocket API

Connect to `ws://localhost:8000/ws` for real-time communication.

#### Client Messages

**Execute Task:**
```json
{
  "type": "execute_task",
  "data": {
    "task": "Build a login system",
    "mode": "full_orchestrator"
  }
}
```

**List All Agents:**
```json
{
  "type": "list_agents"
}
```

**List Features:**
```json
{
  "type": "list_features"
}
```

**Get Agent Info:**
```json
{
  "type": "get_agent_info",
  "data": {
    "agent_name": "felix"
  }
}
```

**Full Orchestrator Mode:**
```json
{
  "type": "full_orchestrator",
  "data": {
    "task": "Build complex e-commerce platform"
  }
}
```

#### Server Responses

**Task Result:**
```json
{
  "type": "task_result",
  "data": {
    "task": "...",
    "mode": "...",
    "result": {...},
    "status": "success"
  },
  "timestamp": "2025-12-10T09:57:00"
}
```

**Agents List:**
```json
{
  "type": "agents_list",
  "data": {
    "agents": [...],
    "total": 23
  },
  "timestamp": "2025-12-10T09:57:00"
}
```

**Features List:**
```json
{
  "type": "features_list",
  "data": {
    "features": {...}
  },
  "timestamp": "2025-12-10T09:57:00"
}
```

## Usage Examples

### From JavaScript Frontend

```javascript
// REST API
async function executeTask(task, mode = 'auto') {
  const response = await fetch('http://localhost:8000/api/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task, mode })
  });
  return await response.json();
}

// WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};

// Execute task via WebSocket
ws.send(JSON.stringify({
  type: 'execute_task',
  data: {
    task: 'Create a REST API',
    mode: 'team'
  }
}));

// Get all agents
ws.send(JSON.stringify({ type: 'list_agents' }));

// Use full orchestrator
ws.send(JSON.stringify({
  type: 'full_orchestrator',
  data: { task: 'Build complex application' }
}));
```

### From Python

```python
import requests
import json

# Execute task via REST API
response = requests.post('http://localhost:8000/api/execute', json={
    'task': 'Create a login system',
    'mode': 'full_orchestrator'
})
result = response.json()
print(result)

# Get all agents
response = requests.get('http://localhost:8000/api/agents')
agents = response.json()
print(f"Total agents: {agents['total']}")
```

## Feature Access Matrix

| Feature | REST API | WebSocket | Status |
|---------|----------|-----------|--------|
| Execute Tasks | ✅ | ✅ | Full |
| List Agents | ✅ | ✅ | Full |
| List Features | ✅ | ✅ | Full |
| Agent Info | ❌ | ✅ | WS Only |
| Full Orchestrator | ✅ | ✅ | Full |
| Real-time Updates | ❌ | ✅ | WS Only |
| Task Progress | ❌ | ✅ | WS Only |

## Complete Integration

The webapp backend now integrates with `unified_interface.py`, which provides access to:

1. **All 23 Agents** - Individual or collaborative
2. **Full Orchestrator** - Complete V3 system with all advanced features
3. **Collaboration Engines** - Multi-agent coordination
4. **Memory Systems** - Vector memory, persistent storage
5. **Research Agent** - Web search and synthesis
6. **Tool Registry** - All available tools
7. **File & Code Operations** - Complete file and code management
8. **Codebase Analysis** - AST parsing and semantic queries

## Starting the WebApp

```bash
# Start with the wrapper (auto-uses venv)
./webapp

# Or directly with Python
python3 webapp.py

# Access at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# WebSocket: ws://localhost:8000/ws
```

## Summary

**The webapp is now the whole project!** 🎉

Every feature, agent, capability, and mode that exists in AI CodeForge is accessible through the webapp's backend API. Users can:

- Execute any task from the web interface
- Use full orchestrator mode with all 23 agents
- Access all V3 advanced features
- Get real-time updates via WebSocket
- Switch between different execution modes
- Access individual agents or full team collaboration

No need to switch to CLI or other interfaces - everything is available in the webapp!
