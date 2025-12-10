#!/usr/bin/env python3
"""
Collaboration Engine - Manages multi-agent collaboration and coordination
"""

import asyncio
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from datetime import datetime

from task_manager import Task, TaskManager, TaskStatus, TaskPriority
from memory_manager import MemoryManager
from file_manager import FileManager
from code_executor import CodeExecutor

console = Console()


class AgentRole(Enum):
    """Agent role categories."""
    PLANNER = "planner"
    CRITIC = "critic"
    DEVELOPER = "developer"
    ASSISTANT = "assistant"
    SPECIALIST = "specialist"
    OVERSEER = "overseer"


@dataclass
class AgentStatus:
    """Current status of an agent."""
    name: str
    status: str  # 'idle', 'busy', 'waiting'
    current_task: Optional[str] = None
    last_active: Optional[str] = None


class CollaborationEngine:
    """Manages agent collaboration and task delegation."""
    
    def __init__(self, workspace_dir, storage_dir):
        self.task_manager = TaskManager(storage_dir / "tasks.json")
        self.memory_manager = MemoryManager(storage_dir / "conversations")
        self.file_manager = FileManager(workspace_dir)
        self.code_executor = CodeExecutor(workspace_dir)
        
        self.agents = {}  # name -> agent_chat instance
        self.agent_statuses = {}  # name -> AgentStatus
        self.overseer = None
        
        self.active_collaborations = []
    
    def register_agent(self, name: str, agent_chat, role: AgentRole):
        """Register an agent for collaboration."""
        self.agents[name] = agent_chat
        self.agent_statuses[name] = AgentStatus(
            name=name,
            status='idle',
            last_active=datetime.now().isoformat()
        )
    
    def register_overseer(self, overseer_chat):
        """Register the overseer agent."""
        self.overseer = overseer_chat
        self.register_agent('helix', overseer_chat, AgentRole.OVERSEER)
    
    def parse_task_delegation(self, overseer_response: str) -> List[Dict]:
        """Parse overseer's response to extract task delegations."""
        tasks = []
        
        # Simple parsing - look for task delegation patterns
        lines = overseer_response.split('\n')
        current_task = None
        
        for line in lines:
            line = line.strip()
            
            # Look for task assignments like "ASSIGN: Nova - Task description"
            if 'ASSIGN:' in line.upper() or 'DELEGATE:' in line.upper():
                parts = line.split(':', 1)
                if len(parts) == 2:
                    assignment = parts[1].strip()
                    # Extract agent name and task
                    if '-' in assignment:
                        agent_part, task_part = assignment.split('-', 1)
                        agent_name = agent_part.strip().lower()
                        task_desc = task_part.strip()
                        
                        if agent_name in self.agents:
                            tasks.append({
                                'agent': agent_name,
                                'description': task_desc,
                                'priority': TaskPriority.MEDIUM
                            })
            
            # Look for priority indicators
            if current_task and ('PRIORITY:' in line.upper() or 'URGENT' in line.upper()):
                current_task['priority'] = TaskPriority.HIGH
        
        return tasks
    
    def delegate_task(self, agent_name: str, description: str, 
                     priority: TaskPriority = TaskPriority.MEDIUM) -> Optional[Task]:
        """Delegate a task to an agent."""
        if agent_name not in self.agents:
            return None
        
        task = self.task_manager.create_task(
            title=f"Task for {agent_name}",
            description=description,
            assigned_to=agent_name,
            created_by='helix',
            priority=priority
        )
        
        self.agent_statuses[agent_name].status = 'busy'
        self.agent_statuses[agent_name].current_task = task.id
        
        return task
    
    def execute_agent_task(self, agent_name: str, task: Task) -> str:
        """Execute a task with the assigned agent."""
        if agent_name not in self.agents:
            return "Error: Agent not found"
        
        agent_chat = self.agents[agent_name]
        
        # Update task status
        self.task_manager.update_task(task.id, status=TaskStatus.IN_PROGRESS)
        
        # Build context with file operations
        context = f"""You are working on the following task:

Task: {task.description}
Priority: {task.priority.value}

You have access to:
- File operations (read, write, list files)
- Code execution (Python, JavaScript, Bash)
- Previous conversation context

Please provide your solution or response."""
        
        try:
            # Get agent's response
            response = agent_chat.send_message(context)
            
            # Check if agent wants to perform file operations
            response = self._handle_agent_actions(agent_name, response)
            
            # Mark task complete
            self.task_manager.complete_task(task.id, response)
            self.agent_statuses[agent_name].status = 'idle'
            self.agent_statuses[agent_name].current_task = None
            
            return response
        
        except Exception as e:
            self.task_manager.fail_task(task.id, str(e))
            self.agent_statuses[agent_name].status = 'idle'
            return f"Error executing task: {e}"
    
    def _handle_agent_actions(self, agent_name: str, response: str) -> str:
        """Handle file operations and code execution requested by agent."""
        # Simple action parsing
        actions_performed = []
        
        # Look for file read requests: READ_FILE: path/to/file.py
        if 'READ_FILE:' in response:
            for line in response.split('\n'):
                if 'READ_FILE:' in line:
                    file_path = line.split('READ_FILE:')[1].strip()
                    content = self.file_manager.read_file(file_path)
                    if content:
                        actions_performed.append(f"Read {file_path}")
                        response += f"\n\n[File Content: {file_path}]\n{content}\n[End File]"
        
        # Look for file write requests: WRITE_FILE: path/to/file.py
        if 'WRITE_FILE:' in response:
            # Extract file path and content
            # This is simplified - production would need better parsing
            pass
        
        # Look for code execution: EXECUTE_PYTHON: code
        if 'EXECUTE_PYTHON:' in response or 'RUN_CODE:' in response:
            # Extract and execute code
            pass
        
        if actions_performed:
            response += f"\n\nActions performed: {', '.join(actions_performed)}"
        
        return response
    
    def coordinate_team(self, user_request: str) -> Dict[str, Any]:
        """Coordinate team to handle user request."""
        if not self.overseer:
            return {'error': 'No overseer registered'}
        
        # Start new session if needed
        if not self.memory_manager.current_session:
            self.memory_manager.create_session(f"Team Task: {user_request[:50]}")
        
        # Add user request to memory
        self.memory_manager.add_message('user', user_request)
        
        # Get overseer's plan
        overseer_prompt = f"""User Request: {user_request}

As the overseer, analyze this request and:
1. Break it down into tasks
2. Assign tasks to appropriate agents
3. Consider dependencies

Available agents: {', '.join([name for name in self.agents.keys() if name != 'helix'])}

Format your response with:
- ASSIGN: [agent_name] - [task description]
- For each task you want to delegate

Then provide your overall coordination plan."""
        
        console.print("\n[cyan]Helix analyzing request...[/cyan]")
        overseer_response = self.overseer.send_message(overseer_prompt)
        
        # Store overseer response
        self.memory_manager.add_message('assistant', overseer_response, 'helix')
        
        # Parse task delegations
        delegated_tasks = self.parse_task_delegation(overseer_response)
        
        # Execute tasks
        task_results = {}
        for task_info in delegated_tasks:
            agent_name = task_info['agent']
            description = task_info['description']
            priority = task_info.get('priority', TaskPriority.MEDIUM)
            
            console.print(f"\n[yellow]Delegating to {agent_name}...[/yellow]")
            
            task = self.delegate_task(agent_name, description, priority)
            if task:
                result = self.execute_agent_task(agent_name, task)
                task_results[agent_name] = result
                
                # Store result in memory
                self.memory_manager.add_message('assistant', result, agent_name)
        
        return {
            'overseer_response': overseer_response,
            'delegated_tasks': delegated_tasks,
            'task_results': task_results
        }
    
    def get_team_status(self) -> Dict:
        """Get current team status."""
        return {
            'agents': {
                name: {
                    'status': status.status,
                    'current_task': status.current_task,
                    'last_active': status.last_active
                }
                for name, status in self.agent_statuses.items()
            },
            'pending_tasks': len(self.task_manager.get_pending_tasks()),
            'active_session': self.memory_manager.current_session.session_id 
                if self.memory_manager.current_session else None
        }
    
    def render_team_dashboard(self) -> Table:
        """Create a visual dashboard of team status."""
        table = Table(title="Team Status", show_header=True)
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Current Task", style="yellow")
        
        for name, status in self.agent_statuses.items():
            status_color = {
                'idle': 'green',
                'busy': 'yellow',
                'waiting': 'blue'
            }.get(status.status, 'white')
            
            table.add_row(
                name.capitalize(),
                f"[{status_color}]{status.status}[/{status_color}]",
                status.current_task[:40] + "..." if status.current_task 
                    and len(status.current_task) > 40 else status.current_task or "-"
            )
        
        return table
