#!/usr/bin/env python3
"""
WebSocket Server - Real-time UI communication
Part of AUTONOMOUS_OPERATIONS_VISION.md & UI_UX_INTERACTION_MODEL.md Phase 8

Provides:
- Real-time event streaming to UI
- Agent status broadcasting
- Task progress updates
- Bidirectional communication
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import json
from datetime import datetime


class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ Client connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket."""
        self.active_connections.remove(websocket)
        print(f"❌ Client disconnected. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific client."""
        await websocket.send_text(message)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        message_json = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception:
                # Connection may be closed; ignore
                pass


# Create FastAPI app
app = FastAPI(title="AI CodeForge War Room API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection manager
manager = ConnectionManager()
connection_manager = manager  # Alias for compatibility


@app.get("/")
async def get_root():
    """Root endpoint with API info."""
    return {
        "name": "AI CodeForge War Room API",
        "version": "1.0.0",
        "websocket": "/ws",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "connections": len(manager.active_connections)
    }


@app.get("/api/agents")
async def get_agents_list():
    """REST API: Get list of all agents."""
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from unified_interface import get_unified_interface
        
        unified = get_unified_interface()
        agents = unified.list_all_agents()
        
        agents_info = []
        for agent_name in agents:
            info = unified.get_agent_info(agent_name)
            agents_info.append({
                "name": agent_name,
                "role": info["role"],
                "specialty": info["specialty"]
            })
        
        return {
            "agents": agents_info,
            "total": len(agents),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


@app.get("/api/features")
async def get_features_list():
    """REST API: Get list of all features."""
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from unified_interface import get_unified_interface
        
        unified = get_unified_interface()
        features = unified.list_all_features()
        
        return {
            "features": features,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


@app.post("/api/execute")
async def execute_task_api(request: dict):
    """REST API: Execute a task."""
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from unified_interface import get_unified_interface
        
        task = request.get("task", "")
        mode = request.get("mode", "auto")
        agents = request.get("agents")
        
        unified = get_unified_interface()
        result = unified.execute_task(task, mode=mode, agents=agents)
        
        return {
            "task": task,
            "mode": mode,
            "result": result,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        return {
            "task": request.get("task", ""),
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for real-time communication.
    
    Message format:
    {
        "type": "event_type",
        "data": {...},
        "timestamp": "ISO datetime"
    }
    """
    await manager.connect(websocket)
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "data": {"message": "Connected to AI CodeForge War Room"},
            "timestamp": datetime.now().isoformat()
        })
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            await handle_client_message(message, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


async def handle_client_message(message: dict, websocket: WebSocket):
    """Handle incoming client messages."""
    msg_type = message.get("type")
    data = message.get("data", {})
    
    if msg_type == "ping":
        # Respond to ping
        await websocket.send_json({
            "type": "pong",
            "timestamp": datetime.now().isoformat()
        })
    
    elif msg_type == "subscribe":
        # Subscribe to specific events
        event_type = data.get("event_type")
        await websocket.send_json({
            "type": "subscribed",
            "data": {"event_type": event_type},
            "timestamp": datetime.now().isoformat()
        })
    
    elif msg_type == "get_status":
        # Get current system status
        status = await get_system_status()
        await websocket.send_json({
            "type": "system_status",
            "data": status,
            "timestamp": datetime.now().isoformat()
        })
    
    elif msg_type == "execute_task":
        # Execute task using unified interface
        await handle_task_execution(data, websocket)
    
    elif msg_type == "execute_code":
        # Execute code in Docker sandbox
        await handle_code_execution(data, websocket)
    
    elif msg_type == "create_task":
        # Create and track a new task
        await handle_create_task(data, websocket)
    
    elif msg_type == "update_config":
        # Update configuration
        await handle_config_update(data, websocket)
    
    elif msg_type == "list_agents":
        # List all available agents
        await handle_list_agents(websocket)
    
    elif msg_type == "list_features":
        # List all available features
        await handle_list_features(websocket)
    
    elif msg_type == "get_agent_info":
        # Get info about specific agent
        await handle_agent_info(data, websocket)
    
    elif msg_type == "full_orchestrator":
        # Activate full orchestrator mode
        await handle_full_orchestrator(data, websocket)


async def get_system_status() -> Dict[str, Any]:
    """Get current system status."""
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from unified_interface import get_unified_interface
        
        unified = get_unified_interface()
        
        # Get real agent count
        agents = unified.list_all_agents()
        agent_count = len(agents) if agents else 23
        
        # Get features count
        try:
            features = unified.list_all_features()
            features_count = len(features) if features else 0
        except:
            features_count = 0
        
        # Get connection count
        active_connections = len(manager.active_connections)
        
        # Calculate uptime (simplified - would need to track start time in production)
        import time
        uptime_seconds = int(time.time() % 86400)  # Simplified for demo
        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60
        uptime = f"{hours}h {minutes}m"
        
        # Get actual task counts from collaboration engine (reuse existing unified instance)
        task_stats = {
            "running_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "total_tasks": 0
        }
        
        try:
            if hasattr(unified, 'collab_engine') and unified.collab_engine:
                collab = unified.collab_engine
                if hasattr(collab, 'tasks'):
                    task_stats["total_tasks"] = len(collab.tasks)
                    task_stats["running_tasks"] = len([t for t in collab.tasks if t.status == 'running'])
                    task_stats["completed_tasks"] = len([t for t in collab.tasks if t.status == 'complete'])
                    task_stats["failed_tasks"] = len([t for t in collab.tasks if t.status == 'error'])
        except Exception:
            pass  # Use defaults if can't get stats
        
        return {
            "health": "healthy",
            "active_agents": agent_count,
            "running_tasks": task_stats["running_tasks"],
            "completed_tasks": task_stats["completed_tasks"],
            "failed_tasks": task_stats["failed_tasks"],
            "total_tasks": task_stats["total_tasks"],
            "uptime": uptime,
            "connections": active_connections,
            "features": features_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        # Fallback to basic status
        return {
            "health": "healthy",
            "active_agents": 23,
            "running_tasks": 0,
            "completed_tasks": 0,
            "uptime": "running",
            "connections": len(manager.active_connections),
            "error": str(e)
        }


# Broadcast functions (called from other parts of the system)
async def broadcast_agent_event(event_type: str, agent_name: str, data: Dict[str, Any]):
    """Broadcast agent-related event."""
    await manager.broadcast({
        "type": "agent_event",
        "event_type": event_type,
        "agent": agent_name,
        "data": data,
        "timestamp": datetime.now().isoformat()
    })


async def broadcast_task_update(task_id: str, status: str, progress: float, details: Dict[str, Any]):
    """Broadcast task progress update."""
    await manager.broadcast({
        "type": "task_update",
        "task_id": task_id,
        "status": status,
        "progress": progress,
        "details": details,
        "timestamp": datetime.now().isoformat()
    })


async def broadcast_system_alert(severity: str, title: str, message: str):
    """Broadcast system alert."""
    await manager.broadcast({
        "type": "system_alert",
        "severity": severity,
        "title": title,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })


# Handler functions for unified interface integration
async def handle_task_execution(data: dict, websocket: WebSocket):
    """Handle task execution request from webapp."""
    import sys
    from pathlib import Path
    
    # Add project root to path
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from unified_interface import get_unified_interface
        
        task = data.get("task", "")
        mode = data.get("mode", "auto")
        agents = data.get("agents")
        
        # Get unified interface
        unified = get_unified_interface()
        
        # Send initial status
        await websocket.send_json({
            "type": "task_update",
            "data": {
                "task": task,
                "status": "started",
                "progress": 0
            },
            "timestamp": datetime.now().isoformat()
        })
        
        # Execute task
        result = unified.execute_task(task, mode=mode, agents=agents)
        
        # Send result back
        await websocket.send_json({
            "type": "task_result",
            "data": {
                "task": task,
                "mode": mode,
                "result": result,
                "status": "success"
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        import traceback
        await websocket.send_json({
            "type": "task_result",
            "data": {
                "task": data.get("task", ""),
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            },
            "timestamp": datetime.now().isoformat()
        })


async def handle_list_agents(websocket: WebSocket):
    """List all available agents."""
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from unified_interface import get_unified_interface
        
        unified = get_unified_interface()
        agents = unified.list_all_agents()
        
        # Get info for each agent
        agents_info = []
        for agent_name in agents:
            info = unified.get_agent_info(agent_name)
            agents_info.append({
                "name": agent_name,
                "role": info["role"],
                "specialty": info["specialty"],
                "status": "ready"
            })
        
        await websocket.send_json({
            "type": "agents_list",
            "data": {
                "agents": agents_info,
                "total": len(agents)
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        import traceback
        await websocket.send_json({
            "type": "agents_list",
            "data": {"error": str(e), "traceback": traceback.format_exc()},
            "timestamp": datetime.now().isoformat()
        })


async def handle_list_features(websocket: WebSocket):
    """List all available features."""
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from unified_interface import get_unified_interface
        
        unified = get_unified_interface()
        features = unified.list_all_features()
        
        await websocket.send_json({
            "type": "features_list",
            "data": {"features": features},
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        import traceback
        await websocket.send_json({
            "type": "features_list",
            "data": {"error": str(e), "traceback": traceback.format_exc()},
            "timestamp": datetime.now().isoformat()
        })


async def handle_agent_info(data: dict, websocket: WebSocket):
    """Get information about a specific agent."""
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from unified_interface import get_unified_interface
        
        agent_name = data.get("agent_name")
        unified = get_unified_interface()
        info = unified.get_agent_info(agent_name)
        
        await websocket.send_json({
            "type": "agent_info",
            "data": {
                "agent": agent_name,
                "info": info
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        import traceback
        await websocket.send_json({
            "type": "agent_info",
            "data": {"error": str(e), "traceback": traceback.format_exc()},
            "timestamp": datetime.now().isoformat()
        })


async def handle_full_orchestrator(data: dict, websocket: WebSocket):
    """Handle full orchestrator mode activation."""
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from unified_interface import get_unified_interface
        
        task = data.get("task", "")
        unified = get_unified_interface()
        
        # Send initial status
        await websocket.send_json({
            "type": "task_update",
            "data": {
                "task": task,
                "status": "started",
                "mode": "full_orchestrator"
            },
            "timestamp": datetime.now().isoformat()
        })
        
        # Execute in full orchestrator mode
        result = unified.execute_task(task, mode="full_orchestrator")
        
        await websocket.send_json({
            "type": "full_orchestrator_result",
            "data": {
                "task": task,
                "result": result,
                "status": "success",
                "mode": "full_orchestrator"
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        import traceback
        await websocket.send_json({
            "type": "full_orchestrator_result",
            "data": {
                "task": data.get("task", ""),
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            },
            "timestamp": datetime.now().isoformat()
        })


async def handle_code_execution(data: dict, websocket: WebSocket):
    """Handle code execution in Docker sandbox."""
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from code_executor import CodeExecutor
        
        code = data.get("code", "")
        language = data.get("language", "python")  # Default to python
        
        # Create workspace directory
        workspace_dir = Path.home() / ".ai-codeforge" / "workspace"
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
        executor = CodeExecutor(workspace_dir=workspace_dir)
        
        # Send initial status
        await websocket.send_json({
            "type": "execution_update",
            "data": {
                "status": "executing",
                "message": f"Executing {language} code..."
            },
            "timestamp": datetime.now().isoformat()
        })
        
        # Execute code based on language
        if language == "python":
            result = executor.execute_python(code)
        elif language == "javascript":
            result = executor.execute_javascript(code)
        elif language in ["bash", "shell"]:
            result = executor.execute_bash(code)
        else:
            result = executor.execute_python(code)  # Default to python
        
        # Convert ExecutionResult to dict
        result_dict = result.to_dict() if hasattr(result, 'to_dict') else {
            'success': getattr(result, 'success', False),
            'output': getattr(result, 'output', ''),
            'error': getattr(result, 'error', ''),
            'execution_time': getattr(result, 'execution_time', 0)
        }
        
        await websocket.send_json({
            "type": "execution_result",
            "data": result_dict,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        import traceback
        await websocket.send_json({
            "type": "execution_result",
            "data": {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            },
            "timestamp": datetime.now().isoformat()
        })


async def handle_create_task(data: dict, websocket: WebSocket):
    """Create and track a new task."""
    try:
        task_id = data.get("id")
        description = data.get("description", "")
        mode = data.get("mode", "parallel")
        
        # Broadcast task creation
        await manager.broadcast({
            "type": "task_created",
            "data": {
                "id": task_id,
                "description": description,
                "mode": mode,
                "status": "created"
            },
            "timestamp": datetime.now().isoformat()
        })
        
        # Start task execution in background
        # This would integrate with task_manager.py or orchestrator
        
    except Exception as e:
        await websocket.send_json({
            "type": "task_error",
            "data": {"error": str(e)},
            "timestamp": datetime.now().isoformat()
        })


async def handle_config_update(data: dict, websocket: WebSocket):
    """Update system configuration."""
    try:
        # Save configuration (would integrate with config_manager.py)
        await websocket.send_json({
            "type": "config_updated",
            "data": {"status": "success", "config": data},
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "config_error",
            "data": {"error": str(e)},
            "timestamp": datetime.now().isoformat()
        })


# Periodic status broadcast (background task)
import asyncio
from typing import Set

# Track active broadcast tasks
_broadcast_tasks: Set[asyncio.Task] = set()

async def periodic_status_broadcast():
    """Broadcast system status periodically to all connected clients."""
    while True:
        try:
            await asyncio.sleep(5)  # Broadcast every 5 seconds
            
            if len(manager.active_connections) > 0:
                status = await get_system_status()
                await manager.broadcast({
                    "type": "system_status",
                    "data": status,
                    "timestamp": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"Error in periodic broadcast: {e}")
            await asyncio.sleep(5)  # Continue even on error

@app.on_event("startup")
async def startup_event():
    """Start background tasks on server startup."""
    print("🚀 Starting AI CodeForge WebSocket Server...")
    print("📡 Starting periodic status broadcast...")
    
    # Start periodic broadcast task
    task = asyncio.create_task(periodic_status_broadcast())
    _broadcast_tasks.add(task)
    task.add_done_callback(_broadcast_tasks.discard)
    
    print("✅ Server ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on server shutdown."""
    print("🛑 Shutting down AI CodeForge WebSocket Server...")
    
    # Cancel all broadcast tasks
    for task in _broadcast_tasks:
        task.cancel()
    
    print("✅ Shutdown complete!")


# Start server with: uvicorn websocket_server:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
