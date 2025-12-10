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


async def get_system_status() -> Dict[str, Any]:
    """Get current system status."""
    # This would integrate with Sentinel agent and other components
    return {
        "health": "healthy",
        "active_agents": 23,
        "running_tasks": 0,
        "completed_tasks": 0,
        "uptime": "1h 23m"
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


# Start server with: uvicorn websocket_server:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
