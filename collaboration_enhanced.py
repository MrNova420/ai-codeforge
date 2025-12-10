#!/usr/bin/env python3
"""
Enhanced Collaboration Engine - Real multi-agent coordination
Designed for long-running tasks with proper progress tracking
v2.1 - Now with JSON-based task delegation
"""

import time
import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID

console = Console()


@dataclass
class AgentTask:
    """Represents a task assigned to an agent."""
    agent_name: str
    task: str
    status: str = "pending"  # pending, working, complete, error
    result: str = ""
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    progress: int = 0


class EnhancedCollaboration:
    """Enhanced collaboration with real progress tracking."""
    
    def __init__(self, agent_chats: Dict):
        self.agent_chats = agent_chats
        self.overseer = agent_chats.get('helix')
        self.tasks: List[AgentTask] = []
        self.current_phase = "Planning"
        
    def handle_request(self, user_request: str, timeout: int = 180) -> Dict:
        """
        Handle user request with full multi-agent coordination.
        Shows real-time progress for each agent.
        """
        if not self.overseer:
            return self._error_response("Overseer (Helix) not available")
        
        console.print("\n[bold cyan]🎯 Analyzing Request...[/bold cyan]")
        
        # Phase 1: Overseer analyzes and creates plan
        plan = self._get_overseer_plan(user_request, timeout=60)
        if plan.startswith("Error:"):
            return self._error_response(plan)
        
        # Phase 2: Parse plan and assign tasks
        console.print("\n[bold cyan]📋 Creating Task Assignments...[/bold cyan]")
        self._parse_and_assign_tasks(plan)
        
        if not self.tasks:
            # Simple request - overseer handles directly
            return {
                'plan': plan,
                'tasks': [],
                'results': {},
                'summary': plan
            }
        
        # Phase 3: Execute tasks with live progress
        console.print(f"\n[bold cyan]⚡ Executing {len(self.tasks)} Tasks...[/bold cyan]")
        results = self._execute_tasks_with_progress(timeout)
        
        # Phase 4: Summarize results
        console.print("\n[bold cyan]📊 Compiling Results...[/bold cyan]")
        summary = self._create_summary(results)
        
        return {
            'plan': plan,
            'tasks': self.tasks,
            'results': results,
            'summary': summary
        }
    
    def _get_overseer_plan(self, user_request: str, timeout: int = 60) -> str:
        """Get plan from overseer."""
        prompt = f"""You are Helix, team overseer. Break down this request into agent tasks.

REQUEST: {user_request}

You MUST delegate to the team. Respond EXACTLY in this format:

AGENTS NEEDED:
- aurora: [task for frontend/UI work]
- felix: [task for Python/backend]
- pixel: [task for design/styling]

Available agents: aurora (frontend), felix (python), sage (architecture), ember (creative), orion (fullstack), atlas (databases), mira (AI/ML), vex (security), sol (testing), echo (documentation), nova (backend), quinn (devops), blaze (performance), ivy (data), zephyr (APIs), pixel (design), script (automation), turbo (optimization), sentinel (monitoring), link (integration), patch (debugging), pulse (health), helix (oversight)

Pick 2-4 relevant agents and assign specific tasks. Be concise."""
        
        try:
            response = self.overseer.send_message(prompt, stream=False)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _parse_and_assign_tasks(self, plan: str):
        """Parse plan and create agent tasks."""
        self.tasks = []
        
        # Look for agent assignments
        lines = plan.split('\n')
        in_agents_section = False
        
        for line in lines:
            line = line.strip()
            
            if 'AGENTS NEEDED' in line.upper() or 'TASK BREAKDOWN' in line.upper():
                in_agents_section = True
                continue
            
            if in_agents_section and line:
                # Parse "- agent_name: task" format
                if line.startswith('-') or line.startswith('*'):
                    parts = line[1:].strip().split(':', 1)
                    if len(parts) == 2:
                        agent_name = parts[0].strip().lower()
                        task_desc = parts[1].strip()
                        
                        # Verify agent exists
                        if agent_name in self.agent_chats:
                            self.tasks.append(AgentTask(
                                agent_name=agent_name,
                                task=task_desc
                            ))
    
    def _execute_tasks_with_progress(self, timeout: int = 180) -> Dict:
        """Execute tasks with live progress tracking."""
        results = {}
        
        # Create progress display
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.fields[agent]}[/bold blue]"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("{task.description}"),
            console=console,
            transient=False
        ) as progress:
            
            # Create progress task for each agent
            progress_tasks = {}
            for task in self.tasks:
                task_id = progress.add_task(
                    f"Preparing...",
                    total=100,
                    agent=task.agent_name.capitalize()
                )
                progress_tasks[task.agent_name] = task_id
            
            # Execute each task
            for task in self.tasks:
                task_id = progress_tasks[task.agent_name]
                agent = self.agent_chats.get(task.agent_name)
                
                if not agent:
                    task.status = "error"
                    task.result = f"Agent {task.agent_name} not found"
                    progress.update(task_id, completed=100, description="[red]Not found[/red]")
                    continue
                
                task.status = "working"
                task.start_time = time.time()
                progress.update(task_id, completed=10, description="[yellow]Working...[/yellow]")
                
                try:
                    # Execute task with timeout
                    progress.update(task_id, completed=30, description="[cyan]Generating...[/cyan]")
                    
                    result = agent.send_message(task.task, stream=False)
                    
                    task.status = "complete"
                    task.result = result
                    task.end_time = time.time()
                    results[task.agent_name] = result
                    
                    progress.update(task_id, completed=100, description="[green]Complete ✓[/green]")
                    
                except Exception as e:
                    task.status = "error"
                    task.result = f"Error: {str(e)}"
                    task.end_time = time.time()
                    results[task.agent_name] = task.result
                    progress.update(task_id, completed=100, description=f"[red]Error: {str(e)[:30]}[/red]")
        
        return results
    
    def _create_summary(self, results: Dict) -> str:
        """Create summary of all results."""
        if not results:
            return "No tasks were executed."
        
        summary_parts = []
        
        for agent_name, result in results.items():
            # Find the task
            task = next((t for t in self.tasks if t.agent_name == agent_name), None)
            if task:
                duration = 0
                if task.start_time and task.end_time:
                    duration = task.end_time - task.start_time
                
                summary_parts.append(
                    f"**{agent_name.capitalize()}** ({duration:.1f}s):\n{result[:500]}"
                )
        
        return "\n\n---\n\n".join(summary_parts)
    
    def _error_response(self, error: str) -> Dict:
        """Create error response."""
        return {
            'plan': error,
            'tasks': [],
            'results': {},
            'summary': error
        }
    
    def render_results(self, response: Dict):
        """Render results in a nice format."""
        
        # Show the plan
        if response['plan']:
            console.print(Panel(
                response['plan'],
                title="[cyan]📋 Helix's Plan[/cyan]",
                border_style="cyan"
            ))
        
        # Show task results
        if response['results']:
            console.print("\n[bold yellow]📦 Agent Results:[/bold yellow]\n")
            
            for agent_name, result in response['results'].items():
                # Truncate long results
                display_result = result[:800] + ("..." if len(result) > 800 else "")
                
                console.print(Panel(
                    display_result,
                    title=f"[blue]{agent_name.capitalize()}[/blue]",
                    border_style="blue",
                    padding=(1, 2)
                ))
        
        # Show final summary
        if response.get('summary') and len(response['results']) > 1:
            console.print(Panel(
                response['summary'],
                title="[green]✅ Summary[/green]",
                border_style="green"
            ))
    
    def render_task_status(self):
        """Render current task status table."""
        if not self.tasks:
            return
        
        table = Table(title="Task Status", show_header=True)
        table.add_column("Agent", style="cyan")
        table.add_column("Task", style="white")
        table.add_column("Status", style="yellow")
        table.add_column("Time", style="green")
        
        for task in self.tasks:
            status_icon = {
                'pending': '⏳ Pending',
                'working': '⚙️  Working',
                'complete': '✅ Complete',
                'error': '❌ Error'
            }.get(task.status, task.status)
            
            duration = ""
            if task.start_time:
                if task.end_time:
                    duration = f"{task.end_time - task.start_time:.1f}s"
                else:
                    duration = f"{time.time() - task.start_time:.1f}s"
            
            table.add_row(
                task.agent_name.capitalize(),
                task.task[:40] + ("..." if len(task.task) > 40 else ""),
                status_icon,
                duration
            )
        
        console.print(table)
