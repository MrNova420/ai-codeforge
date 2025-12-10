#!/usr/bin/env python3
"""
Hierarchical Task Tree - Complex project management
Part of SCALING_TO_LARGE_PROJECTS.md

Enables:
- Parent-child task relationships
- Dependency graphs
- Recursive task decomposition
- Progress tracking at all levels
- Parallel subtask execution
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    READY = "ready"  # Dependencies met
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    BLOCKED = "blocked"  # Waiting on dependencies


@dataclass
class TaskNode:
    """
    A node in the task tree.
    
    Represents a single task that may have:
    - Parent task (what this is a subtask of)
    - Child tasks (subtasks)
    - Dependencies (other tasks that must complete first)
    - Agent assignment
    - Execution state
    """
    
    task_id: str
    description: str
    agent: str
    parent_id: Optional[str] = None
    children: List['TaskNode'] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)  # Task IDs
    
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    priority: int = 0  # Higher = more important
    estimated_duration: Optional[int] = None  # seconds
    actual_duration: Optional[int] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_child(self, child: 'TaskNode') -> None:
        """Add a subtask."""
        child.parent_id = self.task_id
        self.children.append(child)
    
    def add_dependency(self, task_id: str) -> None:
        """Add a task dependency."""
        self.dependencies.add(task_id)
    
    def is_ready(self, completed_tasks: Set[str]) -> bool:
        """Check if all dependencies are met."""
        return self.dependencies.issubset(completed_tasks)
    
    def can_run(self, completed_tasks: Set[str]) -> bool:
        """Check if task can run now."""
        return (
            self.status == TaskStatus.PENDING and
            self.is_ready(completed_tasks)
        )
    
    def get_progress(self) -> float:
        """
        Get progress of this task and its subtasks.
        
        Returns:
            Progress as float 0.0 to 1.0
        """
        if not self.children:
            # Leaf task
            return 1.0 if self.status == TaskStatus.COMPLETE else 0.0
        
        # Aggregate children progress
        if not self.children:
            return 0.0
        
        total_progress = sum(child.get_progress() for child in self.children)
        return total_progress / len(self.children)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'task_id': self.task_id,
            'description': self.description,
            'agent': self.agent,
            'parent_id': self.parent_id,
            'status': self.status.value,
            'dependencies': list(self.dependencies),
            'children': [child.to_dict() for child in self.children],
            'result': self.result,
            'error': self.error,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'priority': self.priority,
            'progress': self.get_progress(),
            'metadata': self.metadata
        }


class TaskTree:
    """
    Hierarchical task structure for complex projects.
    
    Features:
    - Multi-level task decomposition
    - Dependency management
    - Parallel execution planning
    - Progress aggregation
    - Task visualization
    
    Example:
        tree = TaskTree("Build REST API")
        
        # Add subtasks
        design = tree.add_task("Design API schema", agent="sage", parent=tree.root)
        impl = tree.add_task("Implement endpoints", agent="felix", parent=tree.root, depends_on=[design])
        tests = tree.add_task("Write tests", agent="quinn", parent=tree.root, depends_on=[impl])
        
        # Execute
        ready_tasks = tree.get_ready_tasks()
    """
    
    def __init__(self, root_description: str, root_agent: str = "helix"):
        """
        Initialize task tree with root task.
        
        Args:
            root_description: Description of the root/main task
            root_agent: Agent responsible for root task
        """
        self.root = TaskNode(
            task_id="0",
            description=root_description,
            agent=root_agent
        )
        self.tasks: Dict[str, TaskNode] = {"0": self.root}
        self.next_task_id = 1
        self.completed_tasks: Set[str] = set()
    
    def add_task(
        self,
        description: str,
        agent: str,
        parent: Optional[TaskNode] = None,
        depends_on: Optional[List[TaskNode]] = None,
        priority: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TaskNode:
        """
        Add a new task to the tree.
        
        Args:
            description: Task description
            agent: Agent to execute the task
            parent: Parent task (None = root)
            depends_on: List of tasks this depends on
            priority: Task priority
            metadata: Additional task metadata
            
        Returns:
            Created TaskNode
        """
        task_id = str(self.next_task_id)
        self.next_task_id += 1
        
        task = TaskNode(
            task_id=task_id,
            description=description,
            agent=agent,
            priority=priority,
            metadata=metadata or {}
        )
        
        # Add to parent
        if parent:
            parent.add_child(task)
        else:
            self.root.add_child(task)
        
        # Add dependencies
        if depends_on:
            for dep_task in depends_on:
                task.add_dependency(dep_task.task_id)
        
        self.tasks[task_id] = task
        return task
    
    def get_task(self, task_id: str) -> Optional[TaskNode]:
        """Get task by ID."""
        return self.tasks.get(task_id)
    
    def get_ready_tasks(self) -> List[TaskNode]:
        """
        Get all tasks that are ready to execute.
        
        Returns:
            List of tasks with all dependencies met
        """
        ready = []
        for task in self.tasks.values():
            if task.can_run(self.completed_tasks):
                ready.append(task)
        
        # Sort by priority (highest first)
        ready.sort(key=lambda t: t.priority, reverse=True)
        return ready
    
    def mark_complete(self, task_id: str, result: Optional[str] = None) -> None:
        """
        Mark a task as complete.
        
        Args:
            task_id: Task ID
            result: Optional result data
        """
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.COMPLETE
            task.result = result
            task.completed_at = datetime.now().isoformat()
            self.completed_tasks.add(task_id)
    
    def mark_failed(self, task_id: str, error: str) -> None:
        """
        Mark a task as failed.
        
        Args:
            task_id: Task ID
            error: Error message
        """
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.error = error
            task.completed_at = datetime.now().isoformat()
    
    def mark_running(self, task_id: str) -> None:
        """Mark a task as running."""
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now().isoformat()
    
    def get_progress(self) -> float:
        """Get overall project progress (0.0 to 1.0)."""
        return self.root.get_progress()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tree statistics."""
        stats = {
            'total_tasks': len(self.tasks),
            'pending': 0,
            'ready': 0,
            'running': 0,
            'complete': 0,
            'failed': 0,
            'overall_progress': self.get_progress()
        }
        
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                if task.can_run(self.completed_tasks):
                    stats['ready'] += 1
                else:
                    stats['pending'] += 1
            elif task.status == TaskStatus.RUNNING:
                stats['running'] += 1
            elif task.status == TaskStatus.COMPLETE:
                stats['complete'] += 1
            elif task.status == TaskStatus.FAILED:
                stats['failed'] += 1
        
        return stats
    
    def visualize(self, node: Optional[TaskNode] = None, level: int = 0) -> str:
        """
        Generate ASCII tree visualization.
        
        Args:
            node: Starting node (None = root)
            level: Current depth level
            
        Returns:
            ASCII tree string
        """
        if node is None:
            node = self.root
        
        # Status icon
        status_icons = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.READY: "🟢",
            TaskStatus.RUNNING: "🔄",
            TaskStatus.COMPLETE: "✅",
            TaskStatus.FAILED: "❌",
            TaskStatus.BLOCKED: "🔒"
        }
        icon = status_icons.get(node.status, "❓")
        
        # Build line
        indent = "  " * level
        line = f"{indent}{icon} [{node.task_id}] {node.description} (@{node.agent})\n"
        
        # Add children
        for child in node.children:
            line += self.visualize(child, level + 1)
        
        return line
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire tree to dictionary."""
        return {
            'root': self.root.to_dict(),
            'stats': self.get_stats(),
            'completed_tasks': list(self.completed_tasks)
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def export_graphviz(self) -> str:
        """
        Export as Graphviz DOT format for visualization.
        
        Returns:
            DOT format string
        """
        lines = ["digraph TaskTree {"]
        lines.append("  node [shape=box];")
        
        # Add nodes
        for task_id, task in self.tasks.items():
            color = {
                TaskStatus.COMPLETE: "green",
                TaskStatus.FAILED: "red",
                TaskStatus.RUNNING: "yellow",
                TaskStatus.PENDING: "gray"
            }.get(task.status, "white")
            
            label = f"{task.task_id}: {task.description}\\n@{task.agent}"
            lines.append(f'  "{task_id}" [label="{label}", fillcolor={color}, style=filled];')
        
        # Add edges (parent-child)
        for task in self.tasks.values():
            for child in task.children:
                lines.append(f'  "{task.task_id}" -> "{child.task_id}";')
        
        # Add dependency edges (dashed)
        for task in self.tasks.values():
            for dep_id in task.dependencies:
                lines.append(f'  "{dep_id}" -> "{task.task_id}" [style=dashed, color=blue];')
        
        lines.append("}")
        return "\n".join(lines)
