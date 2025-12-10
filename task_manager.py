#!/usr/bin/env python3
"""
Task Manager - Handles multi-agent collaboration and task delegation
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path


class TaskStatus(Enum):
    """Task status states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Task:
    """Represents a task assigned to an agent."""
    id: str
    title: str
    description: str
    assigned_to: str
    created_by: str
    status: TaskStatus
    priority: TaskPriority
    created_at: str
    updated_at: str
    dependencies: List[str]
    result: Optional[str] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['status'] = self.status.value
        data['priority'] = self.priority.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create from dictionary."""
        data['status'] = TaskStatus(data['status'])
        data['priority'] = TaskPriority(data['priority'])
        return cls(**data)


class TaskManager:
    """Manages task creation, assignment, and execution."""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.tasks: Dict[str, Task] = {}
        self.load_tasks()
    
    def create_task(
        self,
        title: str,
        description: str,
        assigned_to: str,
        created_by: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        dependencies: List[str] = None
    ) -> Task:
        """Create a new task."""
        task_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            assigned_to=assigned_to,
            created_by=created_by,
            status=TaskStatus.PENDING,
            priority=priority,
            created_at=now,
            updated_at=now,
            dependencies=dependencies or []
        )
        
        self.tasks[task_id] = task
        self.save_tasks()
        return task
    
    def update_task(self, task_id: str, **updates) -> Optional[Task]:
        """Update task with new data."""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        task.updated_at = datetime.now().isoformat()
        self.save_tasks()
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        return self.tasks.get(task_id)
    
    def get_tasks_by_agent(self, agent_name: str) -> List[Task]:
        """Get all tasks assigned to an agent."""
        return [t for t in self.tasks.values() if t.assigned_to == agent_name]
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        return [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
    
    def can_start_task(self, task_id: str) -> bool:
        """Check if task dependencies are satisfied."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        for dep_id in task.dependencies:
            dep_task = self.tasks.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        
        return True
    
    def complete_task(self, task_id: str, result: str) -> Optional[Task]:
        """Mark task as completed."""
        return self.update_task(
            task_id,
            status=TaskStatus.COMPLETED,
            result=result
        )
    
    def fail_task(self, task_id: str, error: str) -> Optional[Task]:
        """Mark task as failed."""
        return self.update_task(
            task_id,
            status=TaskStatus.FAILED,
            error=error
        )
    
    def save_tasks(self):
        """Save tasks to disk."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {tid: task.to_dict() for tid, task in self.tasks.items()}
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_tasks(self):
        """Load tasks from disk."""
        if not self.storage_path.exists():
            return
        
        try:
            with open(self.storage_path) as f:
                data = json.load(f)
                self.tasks = {tid: Task.from_dict(tdata) for tid, tdata in data.items()}
        except Exception:
            pass  # Start fresh if load fails
