#!/usr/bin/env python3
"""
Agent State Manager - Persistent scratchpad for multi-step tasks
Part of AGENT_ENHANCEMENT_STRATEGY.md implementation

This allows agents to maintain state across multiple LLM calls,
enabling complex multi-step workflows without losing context.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class TaskState:
    """
    Persistent scratchpad for an agent task.
    
    Allows agents to "remember" information between LLM calls:
    - Variables and data
    - Files that have been read
    - Commands that have been executed
    - Current step in multi-step process
    - Complete history of actions
    """
    
    task_id: str
    agent_name: str
    task_description: str
    
    # State storage
    variables: Dict[str, Any] = field(default_factory=dict)
    files_read: Dict[str, str] = field(default_factory=dict)
    files_written: List[str] = field(default_factory=list)
    commands_run: List[Dict[str, Any]] = field(default_factory=list)
    
    # Progress tracking
    current_step: int = 0
    total_steps: int = 0
    status: str = 'pending'  # pending, running, complete, error
    
    # History
    history: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def remember(self, key: str, value: Any) -> None:
        """
        Store a value in the scratchpad.
        
        Args:
            key: Variable name
            value: Value to store
        """
        self.variables[key] = value
        self._log(f"Stored variable: {key} = {str(value)[:100]}")
        self._update_timestamp()
    
    def recall(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a value from the scratchpad.
        
        Args:
            key: Variable name
            default: Default value if key doesn't exist
            
        Returns:
            Stored value or default
        """
        value = self.variables.get(key, default)
        self._log(f"Recalled variable: {key}")
        return value
    
    def remember_file(self, filepath: str, content: str) -> None:
        """
        Remember that a file was read and its content.
        
        Args:
            filepath: Path to file
            content: File content
        """
        self.files_read[filepath] = content
        self._log(f"Read file: {filepath} ({len(content)} chars)")
        self._update_timestamp()
    
    def recall_file(self, filepath: str) -> Optional[str]:
        """
        Recall a previously read file's content.
        
        Args:
            filepath: Path to file
            
        Returns:
            File content if previously read, else None
        """
        return self.files_read.get(filepath)
    
    def log_file_write(self, filepath: str) -> None:
        """
        Log that a file was written.
        
        Args:
            filepath: Path to file written
        """
        self.files_written.append(filepath)
        self._log(f"Wrote file: {filepath}")
        self._update_timestamp()
    
    def log_command(self, command: str, result: Dict[str, Any]) -> None:
        """
        Log a command execution.
        
        Args:
            command: Command that was run
            result: Result of command (success, output, error)
        """
        self.commands_run.append({
            'command': command,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        self._log(f"Ran command: {command}")
        self._update_timestamp()
    
    def advance_step(self, description: str = "") -> None:
        """
        Advance to next step in multi-step task.
        
        Args:
            description: Description of step completed
        """
        self.current_step += 1
        self._log(f"Step {self.current_step}/{self.total_steps}: {description}")
        self._update_timestamp()
    
    def set_total_steps(self, steps: int) -> None:
        """Set the total number of steps in this task."""
        self.total_steps = steps
        self._update_timestamp()
    
    def get_progress(self) -> float:
        """
        Get task progress as percentage.
        
        Returns:
            Progress (0.0 to 1.0)
        """
        if self.total_steps == 0:
            return 0.0
        return min(1.0, self.current_step / self.total_steps)
    
    def set_status(self, status: str) -> None:
        """
        Update task status.
        
        Args:
            status: New status (pending, running, complete, error)
        """
        self.status = status
        self._log(f"Status changed to: {status}")
        self._update_timestamp()
    
    def get_summary(self) -> str:
        """
        Get a summary of the current state.
        
        Returns:
            Human-readable summary
        """
        summary = f"""Task State Summary:
Task: {self.task_description}
Agent: {self.agent_name}
Status: {self.status}
Progress: {self.get_progress():.1%} ({self.current_step}/{self.total_steps} steps)

Variables stored: {len(self.variables)}
Files read: {len(self.files_read)}
Files written: {len(self.files_written)}
Commands run: {len(self.commands_run)}

Recent history:
"""
        for item in self.history[-5:]:
            summary += f"  - {item}\n"
        
        return summary
    
    def get_context_for_llm(self) -> str:
        """
        Generate context string to inject into LLM prompt.
        
        This gives the agent full awareness of its current state.
        
        Returns:
            Context string for LLM
        """
        context = f"""[AGENT STATE - Current Task Context]
Task: {self.task_description}
Progress: Step {self.current_step} of {self.total_steps}

"""
        
        # Add variables
        if self.variables:
            context += "Variables in memory:\n"
            for key, value in self.variables.items():
                context += f"  - {key}: {str(value)[:100]}\n"
            context += "\n"
        
        # Add recently read files
        if self.files_read:
            context += f"Files already read ({len(self.files_read)}):\n"
            for filepath in list(self.files_read.keys())[-3:]:
                context += f"  - {filepath}\n"
            context += "\n"
        
        # Add recent commands
        if self.commands_run:
            context += "Recent commands:\n"
            for cmd in self.commands_run[-3:]:
                context += f"  - {cmd['command']}: {'✓' if cmd['result'].get('success') else '✗'}\n"
            context += "\n"
        
        context += "[END STATE]\n"
        return context
    
    def _log(self, message: str) -> None:
        """Add entry to history."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history.append(f"[{timestamp}] {message}")
    
    def _update_timestamp(self) -> None:
        """Update the last modified timestamp."""
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            'task_id': self.task_id,
            'agent_name': self.agent_name,
            'task_description': self.task_description,
            'variables': self.variables,
            'files_read': self.files_read,
            'files_written': self.files_written,
            'commands_run': self.commands_run,
            'current_step': self.current_step,
            'total_steps': self.total_steps,
            'status': self.status,
            'history': self.history,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskState':
        """Create TaskState from dictionary."""
        return cls(**data)


class StateManager:
    """
    Manages task states for all active agent tasks.
    
    This is the central registry that tracks scratchpads for all ongoing tasks.
    """
    
    def __init__(self, persist_dir: str = "./storage/task_states"):
        """
        Initialize state manager.
        
        Args:
            persist_dir: Directory to persist task states
        """
        self.persist_dir = persist_dir
        self.active_states: Dict[str, TaskState] = {}
        
        # Create storage directory
        import os
        os.makedirs(persist_dir, exist_ok=True)
    
    def create_state(
        self,
        task_id: str,
        agent_name: str,
        task_description: str
    ) -> TaskState:
        """
        Create a new task state.
        
        Args:
            task_id: Unique task identifier
            agent_name: Name of agent
            task_description: Description of task
            
        Returns:
            New TaskState
        """
        state = TaskState(
            task_id=task_id,
            agent_name=agent_name,
            task_description=task_description
        )
        self.active_states[task_id] = state
        return state
    
    def get_state(self, task_id: str) -> Optional[TaskState]:
        """
        Get task state by ID.
        
        Args:
            task_id: Task identifier
            
        Returns:
            TaskState if found, else None
        """
        return self.active_states.get(task_id)
    
    def save_state(self, task_id: str) -> None:
        """
        Persist task state to disk.
        
        Args:
            task_id: Task identifier
        """
        state = self.active_states.get(task_id)
        if not state:
            return
        
        filepath = f"{self.persist_dir}/{task_id}.json"
        with open(filepath, 'w') as f:
            json.dump(state.to_dict(), f, indent=2)
    
    def load_state(self, task_id: str) -> Optional[TaskState]:
        """
        Load task state from disk.
        
        Args:
            task_id: Task identifier
            
        Returns:
            TaskState if found, else None
        """
        filepath = f"{self.persist_dir}/{task_id}.json"
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            state = TaskState.from_dict(data)
            self.active_states[task_id] = state
            return state
        except FileNotFoundError:
            return None
    
    def complete_state(self, task_id: str) -> None:
        """
        Mark a task state as complete and archive it.
        
        Args:
            task_id: Task identifier
        """
        state = self.active_states.get(task_id)
        if state:
            state.set_status('complete')
            self.save_state(task_id)
            # Keep in active states for now
    
    def cleanup_old_states(self, keep_last_n: int = 100) -> None:
        """
        Clean up old task states, keeping only the most recent.
        
        Strategy: Keep completed/error states for analysis, remove old pending states.
        
        Args:
            keep_last_n: Number of recent states to keep
        """
        from pathlib import Path
        
        # Get all saved states
        state_files = list(Path(self.persist_dir).glob('*.json'))
        
        if len(state_files) <= keep_last_n:
            return  # Nothing to clean
        
        # Sort by modification time
        state_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        
        # Keep recent ones, remove old
        for state_file in state_files[keep_last_n:]:
            try:
                os.remove(state_file)
                task_id = state_file.stem
                if task_id in self.active_states:
                    del self.active_states[task_id]
            except Exception:
                pass  # Ignore errors during cleanup
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about active states."""
        return {
            'active_tasks': len(self.active_states),
            'pending': sum(1 for s in self.active_states.values() if s.status == 'pending'),
            'running': sum(1 for s in self.active_states.values() if s.status == 'running'),
            'complete': sum(1 for s in self.active_states.values() if s.status == 'complete'),
            'error': sum(1 for s in self.active_states.values() if s.status == 'error')
        }


# Alias for compatibility
AgentStateManager = StateManager
