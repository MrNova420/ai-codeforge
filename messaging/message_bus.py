#!/usr/bin/env python3
"""
Message Bus - Event-driven communication system
Part of PROJECT_REVISION_PLAN.md Phase 4

Enables:
- Agent-to-agent messaging
- Real-time event broadcasting
- Pub/Sub pattern for scalability
- WebSocket integration for UI updates
"""

import asyncio
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class EventType(Enum):
    """Standard event types in the system."""
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    AGENT_MESSAGE = "agent.message"
    CODE_EXECUTED = "code.executed"
    FILE_MODIFIED = "file.modified"
    MEMORY_STORED = "memory.stored"
    ERROR_OCCURRED = "error.occurred"
    SYSTEM_STATUS = "system.status"


@dataclass
class Event:
    """Event message in the system."""
    event_type: str
    source: str  # Agent or component name
    data: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    event_id: str = field(default_factory=lambda: f"{datetime.now().timestamp()}")
    priority: int = 0  # 0=normal, 1=high, 2=critical
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'event_type': self.event_type,
            'source': self.source,
            'data': self.data,
            'timestamp': self.timestamp,
            'event_id': self.event_id,
            'priority': self.priority
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


class MessageBus:
    """
    Event-driven message bus for agent communication.
    
    Features:
    - Publish/Subscribe pattern
    - Topic-based routing
    - Async event handling
    - Event history for debugging
    - WebSocket broadcasting
    
    Usage:
        bus = MessageBus()
        
        # Subscribe to events
        bus.subscribe('task.completed', on_task_complete)
        
        # Publish events
        await bus.publish('task.started', source='felix', data={'task_id': '123'})
    """
    
    def __init__(self, max_history: int = 1000):
        """
        Initialize message bus.
        
        Args:
            max_history: Maximum number of events to keep in history
        """
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_history: List[Event] = []
        self.max_history = max_history
        self.websocket_clients: List[Any] = []  # WebSocket connections
        self.running = False
        
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Event type to subscribe to (e.g., 'task.completed')
            callback: Async function to call when event occurs
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Event type
            callback: Callback function to remove
        """
        if event_type in self.subscribers:
            if callback in self.subscribers[event_type]:
                self.subscribers[event_type].remove(callback)
    
    async def publish(
        self,
        event_type: str,
        source: str,
        data: Dict[str, Any],
        priority: int = 0
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event
            source: Source agent/component
            data: Event data
            priority: Event priority (0=normal, 1=high, 2=critical)
        """
        # Create event
        event = Event(
            event_type=event_type,
            source=source,
            data=data,
            priority=priority
        )
        
        # Add to history
        self._add_to_history(event)
        
        # Notify subscribers
        if event_type in self.subscribers:
            tasks = []
            for callback in self.subscribers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        tasks.append(callback(event))
                    else:
                        # Wrap sync callbacks
                        callback(event)
                except Exception as e:
                    print(f"Error in subscriber callback: {e}")
            
            # Wait for all async callbacks
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
        
        # Broadcast to WebSocket clients
        await self._broadcast_to_websockets(event)
    
    def _add_to_history(self, event: Event) -> None:
        """Add event to history, maintaining max_history limit."""
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)
    
    async def _broadcast_to_websockets(self, event: Event) -> None:
        """Broadcast event to all connected WebSocket clients."""
        if not self.websocket_clients:
            return
        
        message = event.to_json()
        dead_clients = []
        
        for client in self.websocket_clients:
            try:
                await client.send(message)
            except Exception:
                dead_clients.append(client)
        
        # Remove dead connections
        for client in dead_clients:
            self.websocket_clients.remove(client)
    
    def add_websocket_client(self, client: Any) -> None:
        """Add a WebSocket client for event broadcasting."""
        self.websocket_clients.append(client)
    
    def remove_websocket_client(self, client: Any) -> None:
        """Remove a WebSocket client."""
        if client in self.websocket_clients:
            self.websocket_clients.remove(client)
    
    def get_event_history(
        self,
        event_type: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 100
    ) -> List[Event]:
        """
        Get event history with optional filtering.
        
        Args:
            event_type: Filter by event type
            source: Filter by source
            limit: Maximum number of events to return
            
        Returns:
            List of events (newest first)
        """
        events = self.event_history[::-1]  # Reverse for newest first
        
        # Filter by event type
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        # Filter by source
        if source:
            events = [e for e in events if e.source == source]
        
        return events[:limit]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get message bus statistics."""
        event_counts = {}
        for event in self.event_history:
            event_counts[event.event_type] = event_counts.get(event.event_type, 0) + 1
        
        return {
            'total_events': len(self.event_history),
            'event_types': list(self.subscribers.keys()),
            'subscriber_count': sum(len(subs) for subs in self.subscribers.values()),
            'websocket_clients': len(self.websocket_clients),
            'event_counts': event_counts
        }
    
    def clear_history(self) -> None:
        """Clear event history."""
        self.event_history.clear()


# Global message bus instance
_global_bus = None


def get_message_bus() -> MessageBus:
    """Get the global message bus instance (singleton)."""
    global _global_bus
    if _global_bus is None:
        _global_bus = MessageBus()
    return _global_bus


# Convenience functions
async def publish_event(event_type: str, source: str, data: Dict[str, Any], priority: int = 0) -> None:
    """Publish an event to the global message bus."""
    bus = get_message_bus()
    await bus.publish(event_type, source, data, priority)


def subscribe_to_event(event_type: str, callback: Callable) -> None:
    """Subscribe to an event on the global message bus."""
    bus = get_message_bus()
    bus.subscribe(event_type, callback)


# Example event handlers
async def log_task_completion(event: Event) -> None:
    """Example: Log when a task completes."""
    print(f"[{event.timestamp}] Task completed by {event.source}: {event.data.get('task_id')}")


async def notify_on_error(event: Event) -> None:
    """Example: Handle error events."""
    print(f"[ERROR] {event.source}: {event.data.get('error')}")


async def update_ui(event: Event) -> None:
    """Example: Update UI when system status changes."""
    print(f"[UI UPDATE] {event.event_type}: {event.data}")
