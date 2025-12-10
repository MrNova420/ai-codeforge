#!/usr/bin/env python3
"""
Collaboration V3 - Following PROJECT_REVISION_PLAN.md
- Uses agent_manager.py for threading and resilience
- Forces JSON output from Helix
- Parallel task execution
- Proper error handling
"""

import json
import re
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from agent_manager import AgentManager, AgentResponse

console = Console()


@dataclass
class Task:
    """Task with dependencies."""
    task_id: int
    agent: str
    description: str
    dependencies: List[int]
    status: str = "pending"  # pending, running, complete, error
    result: Optional[str] = None
    error: Optional[str] = None


class CollaborationV3:
    """
    V3 Collaboration Engine - Following the architectural plan.
    
    Key improvements:
    1. Uses AgentManager for non-blocking execution
    2. Forces JSON output from Helix
    3. Parallel task execution
    4. Dependency graph management
    """
    
    def __init__(self, agent_chats: Dict):
        self.agent_chats = agent_chats
        self.overseer = agent_chats.get('helix')
        self.agent_manager = AgentManager()
        self.tasks: List[Task] = []
        
    def handle_request(self, user_request: str, timeout: int = 180) -> Dict:
        """Handle user request with parallel multi-agent execution."""
        if not self.overseer:
            return self._error_response("Helix (Overseer) not available")
        
        console.print("\n[bold cyan]🎯 Analyzing Request...[/bold cyan]")
        
        # Step 1: Get task breakdown from Helix (increased timeout for slower models)
        task_json = self._get_task_breakdown(user_request, timeout=180)
        if task_json.startswith("Error:"):
            return self._error_response(task_json)
        
        # Step 2: Parse JSON into tasks
        console.print("\n[bold cyan]📋 Parsing Task Plan...[/bold cyan]")
        if not self._parse_tasks(task_json):
            # Fallback: treat as simple request
            return {
                'plan': task_json,
                'tasks': [],
                'results': {'helix': task_json},
                'summary': "Helix handled this request directly."
            }
        
        # Step 3: Execute tasks with dependency management
        console.print(f"\n[bold cyan]⚡ Executing {len(self.tasks)} Tasks...[/bold cyan]")
        results = self._execute_tasks_parallel(timeout)
        
        # Step 4: Summarize
        console.print("\n[bold cyan]📊 Summary...[/bold cyan]")
        summary = self._create_summary(results)
        
        return {
            'plan': task_json,
            'tasks': self.tasks,
            'results': results,
            'summary': summary
        }
    
    def _get_task_breakdown(self, user_request: str, timeout: int = 60) -> str:
        """
        Get task breakdown from Helix with FORCED JSON output.
        Uses multiple strategies to extract JSON.
        """
        prompt = f"""You are Helix, the team orchestrator. Break down this request into tasks for your team.

REQUEST: {user_request}

You MUST respond with a JSON object following this schema:
{{
  "tasks": [
    {{"task_id": 1, "agent": "felix", "description": "Create Python function", "dependencies": []}},
    {{"task_id": 2, "agent": "sol", "description": "Write tests", "dependencies": [1]}}
  ]
}}

Available agents and their specialties:
- felix: Python, Flask, Django, backend
- aurora: React, Vue, frontend, HTML/CSS
- nova: Node.js, Express, APIs
- pixel: CSS, design, styling, layouts
- sage: Architecture, system design
- orion: Full-stack development
- atlas: Databases, SQL, schemas
- sol: Testing, QA, unit tests
- vex: Security, authentication
- script: Scripts, automation, CLI
- patch: Debugging, bug fixes
- echo: Documentation

Pick 2-4 agents. Each task needs task_id (number), agent (name), description (string), dependencies (list of task_ids).

CRITICAL: Output ONLY the JSON object. No markdown, no code blocks, no explanation.

JSON:"""

        try:
            # Use AgentManager for resilient execution
            response = self.agent_manager.execute_agent_task(
                self.overseer,
                'helix',
                prompt,
                timeout=timeout
            )
            
            if response.success:
                return self._extract_json(response.content)
            else:
                return f"Error: {response.error}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _extract_json(self, text: str) -> str:
        """
        Extract JSON from response even if wrapped in markdown or text.
        Multiple extraction strategies.
        """
        # Strategy 1: Try direct JSON parse
        try:
            json.loads(text)
            return text
        except:
            pass
        
        # Strategy 2: Extract from markdown code block
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            try:
                json.loads(json_match.group(1))
                return json_match.group(1)
            except:
                pass
        
        # Strategy 3: Find JSON object in text
        json_match = re.search(r'\{.*"tasks".*\}', text, re.DOTALL)
        if json_match:
            try:
                json.loads(json_match.group(0))
                return json_match.group(0)
            except:
                pass
        
        # Strategy 4: Clean and try again
        cleaned = text.strip().replace('```json', '').replace('```', '').strip()
        try:
            json.loads(cleaned)
            return cleaned
        except:
            pass
        
        # Failed - return original
        return text
    
    def _parse_tasks(self, task_json: str) -> bool:
        """Parse JSON task list into Task objects."""
        try:
            data = json.loads(task_json)
            
            if 'tasks' not in data or not isinstance(data['tasks'], list):
                return False
            
            self.tasks = []
            for t in data['tasks']:
                # Validate required fields
                if not all(k in t for k in ['task_id', 'agent', 'description']):
                    continue
                
                # Check if agent exists
                agent_name = t['agent'].lower()
                if agent_name not in self.agent_chats:
                    console.print(f"[yellow]Warning: Agent '{agent_name}' not found, skipping[/yellow]")
                    continue
                
                task = Task(
                    task_id=t['task_id'],
                    agent=agent_name,
                    description=t['description'],
                    dependencies=t.get('dependencies', [])
                )
                self.tasks.append(task)
            
            return len(self.tasks) > 0
            
        except json.JSONDecodeError as e:
            console.print(f"[yellow]JSON parse failed: {e}[/yellow]")
            return False
        except Exception as e:
            console.print(f"[yellow]Task parsing error: {e}[/yellow]")
            return False
    
    def _execute_tasks_parallel(self, timeout: int = 180) -> Dict:
        """
        Execute tasks in parallel where possible, respecting dependencies.
        Uses AgentManager for non-blocking execution.
        """
        results = {}
        completed_task_ids = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.fields[agent]}[/bold blue]"),
            BarColumn(),
            TextColumn("{task.description}"),
            console=console
        ) as progress:
            
            # Create progress bars for each task
            progress_bars = {}
            for task in self.tasks:
                bar_id = progress.add_task(
                    f"Waiting...",
                    total=100,
                    agent=task.agent.capitalize()
                )
                progress_bars[task.task_id] = bar_id
            
            # Execute in rounds based on dependencies
            max_rounds = 10
            for round_num in range(max_rounds):
                # Find tasks that can run (dependencies met)
                ready_tasks = [
                    t for t in self.tasks
                    if t.status == "pending" and
                    all(dep in completed_task_ids for dep in t.dependencies)
                ]
                
                if not ready_tasks:
                    break  # All done or stuck
                
                # Execute ready tasks
                for task in ready_tasks:
                    task.status = "running"
                    bar_id = progress_bars[task.task_id]
                    progress.update(bar_id, description="[cyan]Running...[/cyan]", completed=30)
                    
                    # Execute via AgentManager
                    agent_chat = self.agent_chats[task.agent]
                    
                    try:
                        response = self.agent_manager.execute_agent_task(
                            agent_chat,
                            task.agent,
                            task.description,
                            timeout=timeout,
                            on_progress=lambda p, _: progress.update(bar_id, completed=min(30 + p//2, 90))
                        )
                        
                        if response.success:
                            task.status = "complete"
                            task.result = response.content
                            results[task.agent] = response.content
                            completed_task_ids.append(task.task_id)
                            progress.update(bar_id, completed=100, description="[green]✓ Complete[/green]")
                        else:
                            task.status = "error"
                            task.error = response.error or "Unknown error"
                            progress.update(bar_id, completed=100, description=f"[red]✗ Error[/red]")
                    
                    except Exception as e:
                        task.status = "error"
                        task.error = str(e)
                        progress.update(bar_id, completed=100, description=f"[red]✗ {str(e)[:20]}[/red]")
        
        return results
    
    def _create_summary(self, results: Dict) -> str:
        """Create summary of results."""
        summary_lines = []
        summary_lines.append("Task Execution Summary:")
        
        for task in self.tasks:
            status_icon = {
                'complete': '✅',
                'error': '❌',
                'pending': '⏳',
                'running': '🔄'
            }.get(task.status, '❓')
            
            summary_lines.append(f"{status_icon} {task.agent.capitalize()}: {task.status}")
            if task.error:
                summary_lines.append(f"   Error: {task.error}")
        
        return "\n".join(summary_lines)
    
    def _error_response(self, error: str) -> Dict:
        """Create error response."""
        return {
            'plan': error,
            'tasks': [],
            'results': {},
            'summary': f"Error: {error}"
        }
    
    def render_results(self, response: Dict):
        """Render the results to console."""
        # Show summary
        if response.get('summary'):
            console.print(Panel(
                response['summary'],
                title="[cyan]Summary[/cyan]",
                border_style="cyan"
            ))
        
        # Show individual results
        for agent, result in response.get('results', {}).items():
            console.print(Panel(
                result[:500] + ("..." if len(result) > 500 else ""),
                title=f"[cyan]{agent.capitalize()}[/cyan]",
                border_style="cyan"
            ))
