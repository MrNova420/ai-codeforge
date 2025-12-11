#!/usr/bin/env python3
"""
Webapp Integration Adapter - Connects enhanced collaboration system to webapp
Bridges CollaborationV3, activity logging, and agent statistics to the webapp UI
"""

import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime


class WebappAdapter:
    """
    Adapter to connect enhanced collaboration system to webapp.
    Provides real-time updates, activity streaming, and statistics.
    """
    
    def __init__(self, orchestrator=None):
        """
        Initialize adapter with orchestrator.
        
        Args:
            orchestrator: EnhancedOrchestrator instance
        """
        self.orchestrator = orchestrator
        self.active_tasks = {}
        self.event_callbacks = []
    
    def register_callback(self, callback):
        """Register a callback for events."""
        self.event_callbacks.append(callback)
    
    async def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit an event to all registered callbacks."""
        event = {
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        for callback in self.event_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                print(f"Error in callback: {e}")
    
    async def execute_task_with_streaming(
        self, 
        task: str, 
        mode: str = "auto",
        agents: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute a task with real-time streaming to webapp.
        
        Args:
            task: Task description
            mode: Execution mode
            agents: Optional agent list
        
        Returns:
            Task result with full details
        """
        task_id = f"task_{datetime.now().timestamp()}"
        self.active_tasks[task_id] = {
            'task': task,
            'mode': mode,
            'agents': agents,
            'status': 'starting',
            'start_time': datetime.now().isoformat()
        }
        
        # Emit task start
        await self.emit_event('task_started', {
            'task_id': task_id,
            'task': task,
            'mode': mode,
            'agents': agents
        })
        
        try:
            # Initialize orchestrator if needed
            if not self.orchestrator:
                await self.emit_event('task_progress', {
                    'task_id': task_id,
                    'message': 'Initializing orchestrator...'
                })
                from orchestrator_v2 import EnhancedOrchestrator
                self.orchestrator = EnhancedOrchestrator()
            
            # Initialize collaboration agents
            await self.emit_event('task_progress', {
                'task_id': task_id,
                'message': 'Initializing agents...'
            })
            
            if not self.orchestrator.agent_chats:
                self.orchestrator._init_collaboration_agents()
            
            # Execute through collaboration engine
            await self.emit_event('task_progress', {
                'task_id': task_id,
                'message': 'Analyzing request...'
            })
            
            collab = self.orchestrator.collab_engine
            result = collab.handle_request(task, mode=mode)
            
            # Stream activity logs
            if hasattr(collab, 'activity_log'):
                for activity in collab.activity_log[-20:]:
                    await self.emit_event('activity_update', {
                        'task_id': task_id,
                        'activity': activity
                    })
            
            # Stream task summaries
            if hasattr(collab, 'task_history'):
                for task_summary in collab.task_history:
                    await self.emit_event('agent_summary', {
                        'task_id': task_id,
                        'summary': task_summary
                    })
            
            # Update task status
            self.active_tasks[task_id]['status'] = 'completed'
            self.active_tasks[task_id]['result'] = result
            self.active_tasks[task_id]['end_time'] = datetime.now().isoformat()
            
            # Emit completion
            await self.emit_event('task_completed', {
                'task_id': task_id,
                'result': result
            })
            
            return {
                'task_id': task_id,
                'status': 'completed',
                'result': result,
                'activity_log': collab.activity_log[-50:] if hasattr(collab, 'activity_log') else [],
                'task_history': collab.task_history if hasattr(collab, 'task_history') else []
            }
        
        except Exception as e:
            # Update task status
            self.active_tasks[task_id]['status'] = 'error'
            self.active_tasks[task_id]['error'] = str(e)
            self.active_tasks[task_id]['end_time'] = datetime.now().isoformat()
            
            # Emit error
            await self.emit_event('task_error', {
                'task_id': task_id,
                'error': str(e)
            })
            
            return {
                'task_id': task_id,
                'status': 'error',
                'error': str(e)
            }
    
    def get_activity_feed(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent activity feed."""
        if not self.orchestrator or not self.orchestrator.collab_engine:
            return []
        
        collab = self.orchestrator.collab_engine
        if hasattr(collab, 'activity_log'):
            return collab.activity_log[-limit:]
        return []
    
    def get_task_history(self) -> List[Dict[str, Any]]:
        """Get task execution history."""
        if not self.orchestrator or not self.orchestrator.collab_engine:
            return []
        
        collab = self.orchestrator.collab_engine
        if hasattr(collab, 'task_history'):
            return collab.task_history
        return []
    
    def get_agent_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all agents."""
        if not self.orchestrator or not self.orchestrator.agent_chats:
            return {}
        
        stats = {}
        for agent_name, agent_chat in self.orchestrator.agent_chats.items():
            if hasattr(agent_chat, 'get_agent_stats'):
                try:
                    stats[agent_name] = agent_chat.get_agent_stats()
                except:
                    pass
        
        return stats
    
    def get_agent_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get status for a specific agent."""
        if not self.orchestrator or not self.orchestrator.collab_engine:
            return None
        
        collab = self.orchestrator.collab_engine
        if hasattr(collab, 'agent_statuses') and agent_name in collab.agent_statuses:
            return collab.agent_statuses[agent_name]
        
        return None
    
    def get_all_agent_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status for all agents."""
        if not self.orchestrator or not self.orchestrator.collab_engine:
            return {}
        
        collab = self.orchestrator.collab_engine
        if hasattr(collab, 'agent_statuses'):
            return collab.agent_statuses
        
        return {}
    
    def get_active_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all active tasks."""
        return {
            task_id: task_info 
            for task_id, task_info in self.active_tasks.items()
            if task_info['status'] in ['starting', 'running']
        }
    
    def get_completed_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all completed tasks."""
        return {
            task_id: task_info 
            for task_id, task_info in self.active_tasks.items()
            if task_info['status'] == 'completed'
        }


# Global adapter instance
_adapter_instance = None


def get_webapp_adapter(orchestrator=None):
    """Get or create webapp adapter instance."""
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = WebappAdapter(orchestrator)
    return _adapter_instance
