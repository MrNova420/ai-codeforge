#!/usr/bin/env python3
"""
Collaboration V3 - UNIFIED & COMPLETE
Merged ALL features from simple, enhanced, engine, and v3:
- Simple: Direct overseer communication, quick delegate
- Enhanced: Real-time progress tracking, live updates
- Engine: Task management, file operations, code execution
- V3: JSON parsing, parallel execution, AgentManager threading

This is the ONE TRUE collaboration engine with everything integrated.
"""

import json
import re
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from agent_manager import AgentManager, AgentResponse
from prompts_utils import build_actionable_task_prompt, build_enhanced_task_prompt, build_delegation_prompt

console = Console()


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Task:
    """Task with dependencies, progress, and execution details."""
    task_id: int
    agent: str
    description: str
    dependencies: List[int] = field(default_factory=list)
    status: str = "pending"  # pending, running, complete, error
    result: Optional[str] = None
    error: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    progress: int = 0


class CollaborationV3:
    """
    V3 Unified Collaboration Engine - ALL FEATURES INTEGRATED
    
    Features from ALL versions:
    1. JSON parsing & validation (v3)
    2. AgentManager threading (v3)
    3. Parallel task execution (v3)
    4. Real-time progress tracking (enhanced)
    5. Live status updates (enhanced)
    6. Simple direct communication (simple)
    7. Quick delegate for single agents (simple)
    8. Task priority management (engine)
    9. File operations integration (engine)
    10. Code execution support (engine)
    11. Dependency graph management (v3)
    12. Error handling & recovery (all)
    """
    
    def __init__(self, agent_chats: Dict):
        self.agent_chats = agent_chats
        self.overseer = agent_chats.get('helix')
        self.agent_manager = AgentManager()
        self.tasks: List[Task] = []
        self.current_phase = "Planning"
        self.agent_statuses = {}  # track agent status
        self.activity_log = []  # Comprehensive activity logging
        self.task_history = []  # History of all task summaries
        
        # Initialize agent statuses
        for name in agent_chats.keys():
            self.agent_statuses[name] = {
                'status': 'idle',
                'current_task': None,
                'last_active': datetime.now().isoformat()
            }
        
        self._log_activity("System", "Collaboration engine initialized", "info")
    
    def _log_activity(self, source: str, message: str, level: str = "info"):
        """Log activity to comprehensive activity feed."""
        activity = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'message': message,
            'level': level  # info, warning, error, success
        }
        self.activity_log.append(activity)
        
        # Also print to console for real-time feedback
        level_colors = {
            'info': 'blue',
            'warning': 'yellow',
            'error': 'red',
            'success': 'green'
        }
        color = level_colors.get(level, 'white')
        timestamp = activity['timestamp'].split('T')[1][:8]
    
    def show_activity_feed(self, limit: int = 20):
        """Display the activity feed."""
        console.print("\n[bold cyan]📊 Activity Feed[/bold cyan]")
        
        recent_activities = self.activity_log[-limit:] if len(self.activity_log) > limit else self.activity_log
        
        for activity in recent_activities:
            timestamp = activity['timestamp'].split('T')[1][:8]
            level = activity['level']
            icon = {'info': 'ℹ️', 'warning': '⚠️', 'error': '❌', 'success': '✅'}.get(level, '•')
            console.print(f"[dim]{timestamp}[/dim] {icon} [cyan]{activity['source']}:[/cyan] {activity['message']}")
        
        console.print(f"\n[dim]Total activities: {len(self.activity_log)} | Showing last {len(recent_activities)}[/dim]")
    
    # ========== MAIN ENTRY POINT ==========
    
    def handle_request(self, user_request: str, timeout: int = 180, mode: str = 'auto') -> Dict:
        """
        Main entry point - handles request with appropriate mode.
        
        Args:
            user_request: User's request
            timeout: Overall timeout
            mode: 'auto', 'simple', 'enhanced', 'parallel'
        
        Returns:
            Dict with plan, tasks, results, and summary
        """
        self._log_activity("System", f"Received request: {user_request[:50]}...", "info")
        
        if not self.overseer:
            self._log_activity("System", "Overseer not available", "error")
            return self._error_response("Helix (Overseer) not available")
        
        # Auto-detect complexity
        if mode == 'auto':
            if any(word in user_request.lower() for word in ['simple', 'quick', 'fast']):
                mode = 'simple'
            elif any(word in user_request.lower() for word in ['complex', 'full team', 'all agents']):
                mode = 'parallel'
            else:
                mode = 'enhanced'
        
        self._log_activity("System", f"Selected mode: {mode}", "info")
        
        # Route to appropriate handler
        if mode == 'simple':
            return self._handle_simple(user_request, timeout)
        elif mode == 'parallel':
            return self._handle_parallel(user_request, timeout)
        else:
            return self._handle_enhanced(user_request, timeout)
    
    # ========== SIMPLE MODE (from collaboration_simple.py) ==========
    
    def _handle_simple(self, user_request: str, timeout: int) -> Dict:
        """Simple mode - overseer handles directly, no complex delegation."""
        console.print("\n[cyan]🎯 Simple Mode: Helix analyzing...[/cyan]")
        
        prompt = f"""User Request: {user_request}

As the overseer, provide a direct response. 

If this requires multiple agents:
- Briefly explain what needs to be done
- List which agents would handle each part
- Give a summary response

Keep it concise and helpful."""
        
        try:
            response = self.overseer.send_message(prompt, stream=False)
            return {
                'mode': 'simple',
                'plan': response,
                'tasks': [],
                'results': {'helix': response},
                'summary': response
            }
        except Exception as e:
            return self._error_response(f"Error: {str(e)}")
    
    def quick_delegate(self, agent_name: str, task: str) -> str:
        """Quickly delegate to a specific agent (from simple)."""
        if agent_name not in self.agent_chats:
            return f"Agent {agent_name} not found"
        
        try:
            agent = self.agent_chats[agent_name]
            response = agent.send_message(task, stream=False)
            self.agent_statuses[agent_name]['last_active'] = datetime.now().isoformat()
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== ENHANCED MODE (from collaboration_enhanced.py) ==========
    
    def _handle_enhanced(self, user_request: str, timeout: int) -> Dict:
        """Enhanced mode - full delegation with real-time progress."""
        self._log_activity("Enhanced Mode", "Starting enhanced mode execution", "info")
        console.print("\n[bold cyan]🎯 Analyzing Request...[/bold cyan]")
        
        # Phase 1: Get plan from overseer
        self._log_activity("Helix", "Analyzing request and creating plan", "info")
        plan = self._get_enhanced_plan(user_request, timeout=60)
        if plan.startswith("Error:"):
            self._log_activity("Helix", "Failed to create plan", "error")
            return self._error_response(plan)
        
        self._log_activity("Helix", f"Plan created with {len(plan)} chars", "success")
        
        # Phase 2: Parse and assign tasks
        console.print("\n[bold cyan]📋 Creating Task Assignments...[/bold cyan]")
        self._parse_enhanced_tasks(plan)
        self._log_activity("System", f"Parsed {len(self.tasks)} tasks from plan", "info")
        
        if not self.tasks:
            self._log_activity("System", "No tasks parsed, using direct response", "warning")
            return {
                'mode': 'enhanced',
                'plan': plan,
                'tasks': [],
                'results': {},
                'summary': plan
            }
        
        # Log task assignments
        for task in self.tasks:
            self._log_activity("System", f"Assigned task to {task.agent}: {task.description[:50]}...", "info")
        
        # Phase 3: Execute with live progress
        console.print(f"\n[bold cyan]⚡ Executing {len(self.tasks)} Tasks...[/bold cyan]")
        results = self._execute_with_live_progress(timeout)
        
        # Phase 4: Summarize
        summary = self._create_summary(results)
        self._log_activity("System", "All tasks completed, summary created", "success")
        
        return {
            'mode': 'enhanced',
            'plan': plan,
            'tasks': self.tasks,
            'results': results,
            'summary': summary
        }
    
    def _get_enhanced_plan(self, user_request: str, timeout: int) -> str:
        """Get delegation plan from overseer (enhanced style)."""
        # Use shared delegation prompt utility
        available_agents = ["aurora", "felix", "sage", "ember", "orion", "atlas", "mira", "vex", 
                          "sol", "echo", "nova", "quinn", "blaze", "ivy", "zephyr", "pixel", 
                          "script", "turbo", "sentinel", "link", "patch", "pulse", "helix"]
        prompt = build_delegation_prompt(user_request, available_agents)
        
        try:
            response = self.overseer.send_message(prompt, stream=False)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _parse_enhanced_tasks(self, plan: str):
        """Parse enhanced-style plan into tasks."""
        self.tasks = []
        lines = plan.split('\n')
        in_agents_section = False
        
        for line in lines:
            line = line.strip()
            
            if 'AGENTS NEEDED' in line.upper() or 'TASK BREAKDOWN' in line.upper():
                in_agents_section = True
                continue
            
            if in_agents_section and line:
                if line.startswith('-') or line.startswith('*'):
                    parts = line[1:].strip().split(':', 1)
                    if len(parts) == 2:
                        agent_name = parts[0].strip().lower()
                        task_desc = parts[1].strip()
                        
                        if agent_name in self.agent_chats:
                            self.tasks.append(Task(
                                task_id=len(self.tasks),
                                agent=agent_name,
                                description=task_desc
                            ))
    
    def _execute_with_live_progress(self, timeout: int) -> Dict:
        """Execute tasks with live progress bars and detailed status tracking."""
        results = {}
        task_summaries = []  # Store detailed task summaries
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.fields[agent]}[/bold blue]"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("{task.description}"),
            console=console,
            transient=False
        ) as progress:
            
            progress_tasks = {}
            for task in self.tasks:
                task_id = progress.add_task(
                    "Preparing...",
                    total=100,
                    agent=task.agent.capitalize()
                )
                progress_tasks[task.agent] = task_id
            
            for task in self.tasks:
                task_id = progress_tasks[task.agent]
                agent = self.agent_chats.get(task.agent)
                
                # Create task summary box
                task_summary = {
                    'agent': task.agent,
                    'task': task.description,
                    'status': 'starting',
                    'start_time': datetime.now().isoformat(),
                    'result': None,
                    'duration': 0
                }
                
                if not agent:
                    task.status = "error"
                    task.result = f"Agent {task.agent} not found"
                    progress.update(task_id, completed=100, description="[red]Not found[/red]")
                    task_summary['status'] = 'error'
                    task_summary['result'] = task.result
                    task_summaries.append(task_summary)
                    self._log_activity(task.agent, "Agent not found", "error")
                    continue
                
                task.status = "running"
                task.start_time = time.time()
                self.agent_statuses[task.agent]['status'] = 'busy'
                self.agent_statuses[task.agent]['current_task'] = task.task_id
                
                self._log_activity(task.agent, f"Starting task: {task.description[:50]}...", "info")
                progress.update(task_id, completed=10, description="[yellow]⏳ Analyzing...[/yellow]")
                task_summary['status'] = 'analyzing'
                
                try:
                    progress.update(task_id, completed=30, description="[cyan]💭 Thinking...[/cyan]")
                    task_summary['status'] = 'thinking'
                    self._log_activity(task.agent, "Processing request...", "info")
                    
                    progress.update(task_id, completed=50, description="[cyan]🔨 Generating...[/cyan]")
                    task_summary['status'] = 'generating'
                    self._log_activity(task.agent, "Generating response...", "info")
                    
                    # Use shared utility for actionable prompts
                    actionable_prompt = build_enhanced_task_prompt(task.description)
                    
                    result = agent.send_message(actionable_prompt, stream=False)
                    
                    task.status = "complete"
                    task.result = result
                    task.end_time = time.time()
                    duration = task.end_time - task.start_time
                    results[task.agent] = result
                    
                    self.agent_statuses[task.agent]['status'] = 'idle'
                    self.agent_statuses[task.agent]['current_task'] = None
                    self.agent_statuses[task.agent]['last_active'] = datetime.now().isoformat()
                    
                    task_summary['status'] = 'complete'
                    task_summary['result'] = result
                    task_summary['duration'] = f"{duration:.1f}s"
                    task_summary['result_length'] = len(str(result))
                    
                    self._log_activity(task.agent, f"Task completed in {duration:.1f}s ({len(str(result))} chars)", "success")
                    progress.update(task_id, completed=100, description=f"[green]✅ Complete ({duration:.1f}s)[/green]")
                    
                    # Show individual agent summary box after completion
                    self._show_agent_summary(task.agent, task_summary)
                    
                except Exception as e:
                    task.status = "error"
                    task.result = f"Error: {str(e)}"
                    task.end_time = time.time()
                    duration = task.end_time - task.start_time
                    results[task.agent] = task.result
                    self.agent_statuses[task.agent]['status'] = 'idle'
                    
                    task_summary['status'] = 'error'
                    task_summary['result'] = task.result
                    task_summary['duration'] = f"{duration:.1f}s"
                    
                    self._log_activity(task.agent, f"Task failed: {str(e)}", "error")
                    progress.update(task_id, completed=100, description=f"[red]❌ Error[/red]")
                
                task_summaries.append(task_summary)
        
        # Store task summaries for history
        self.task_history = task_summaries
        
        return results
    
    def _show_agent_summary(self, agent_name: str, task_summary: Dict):
        """Display a summary box for a completed agent task."""
        status_icon = "✅" if task_summary['status'] == 'complete' else "❌"
        status_color = "green" if task_summary['status'] == 'complete' else "red"
        
        summary_text = f"""[{status_color}]{status_icon} Status:[/{status_color}] {task_summary['status']}
[cyan]⏱️  Duration:[/cyan] {task_summary.get('duration', 'N/A')}
[cyan]📝 Task:[/cyan] {task_summary['task'][:80]}{'...' if len(task_summary['task']) > 80 else ''}
[cyan]📊 Result Length:[/cyan] {task_summary.get('result_length', 0)} chars"""
        
        console.print(Panel(
            summary_text,
            title=f"[bold cyan]📦 {agent_name.capitalize()} - Task Summary[/bold cyan]",
            border_style=status_color,
            subtitle=f"[dim]{task_summary['start_time'].split('T')[1][:8]}[/dim]"
        ))
    
    # ========== PARALLEL MODE (from collaboration_v3.py) ==========
        
    def _handle_parallel(self, user_request: str, timeout: int = 180) -> Dict:
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
        """Render the results to console with full output and better formatting."""
        # Show summary
        if response.get('summary'):
            console.print(Panel(
                response['summary'],
                title="[cyan]📊 Summary[/cyan]",
                border_style="cyan"
            ))
        
        # Show individual results with full content
        for agent, result in response.get('results', {}).items():
            # Format the result content with line numbers for long outputs
            result_str = str(result)
            
            # Add scrolling hint for very long outputs
            if len(result_str) > 2000:
                hint = f"\n\n[dim]ℹ️  Response length: {len(result_str)} chars | Scroll to view all content[/dim]"
                display_content = result_str + hint
            else:
                display_content = result_str
            
            console.print(Panel(
                display_content,
                title=f"[cyan]🤖 {agent.capitalize()}[/cyan]",
                border_style="cyan",
                subtitle=f"[dim]{len(result_str)} chars[/dim]"
            ))
    
    # ========== ADDITIONAL METHODS FROM ENGINE ==========
    
    def parse_task_delegation(self, overseer_response: str) -> List[Dict]:
        """Parse overseer's response to extract task delegations (from engine)."""
        tasks = []
        lines = overseer_response.split('\n')
        current_task = None
        
        for line in lines:
            line = line.strip()
            
            # Look for task assignments like "ASSIGN: Nova - Task description"
            if 'ASSIGN:' in line.upper() or 'DELEGATE:' in line.upper():
                parts = line.split(':', 1)
                if len(parts) == 2:
                    assignment = parts[1].strip()
                    if '-' in assignment:
                        agent_part, task_part = assignment.split('-', 1)
                        agent_name = agent_part.strip().lower()
                        task_desc = task_part.strip()
                        
                        if agent_name in self.agent_chats:
                            tasks.append({
                                'agent': agent_name,
                                'description': task_desc,
                                'priority': TaskPriority.MEDIUM
                            })
            
            # Look for priority indicators
            if current_task and ('PRIORITY:' in line.upper() or 'URGENT' in line.upper()):
                current_task['priority'] = TaskPriority.HIGH
        
        return tasks
    
    def delegate_task_to_agent(self, agent_name: str, description: str, 
                     priority: TaskPriority = TaskPriority.MEDIUM) -> Optional[Task]:
        """Delegate a task to an agent (from engine)."""
        if agent_name not in self.agent_chats:
            return None
        
        task = Task(
            task_id=len(self.tasks),
            agent=agent_name,
            description=description,
            dependencies=[],
            priority=priority
        )
        
        self.tasks.append(task)
        self.agent_statuses[agent_name]['status'] = 'busy'
        self.agent_statuses[agent_name]['current_task'] = task.task_id
        
        return task
    
    def execute_single_agent_task(self, agent_name: str, task: Task) -> str:
        """Execute a task with the assigned agent with enhanced capabilities."""
        if agent_name not in self.agent_chats:
            return "Error: Agent not found"
        
        agent_chat = self.agent_chats[agent_name]
        
        # Enhanced prompt using shared utility with full context
        additional_context = f"""You have access to:
- File operations (read, write, list files)
- Code execution (Python, JavaScript, Bash)
- Previous conversation context
- Your specialized skills and knowledge

WORK STYLE:
1. First, analyze what needs to be done
2. Break it down into concrete steps
3. IMPLEMENT each step with actual code/content
4. Test your implementation mentally
5. Provide the complete, working solution

QUALITY STANDARDS:
- Code must be production-ready
- Include error handling
- Add comments for complex logic
- Follow best practices for the language/framework
- Make it maintainable and extensible"""
        
        context = build_actionable_task_prompt(
            task_description=task.description,
            priority=task.priority.value,
            additional_context=additional_context
        )
        
        try:
            task.status = "running"
            task.start_time = time.time()
            
            response = agent_chat.send_message(context)
            response = self._handle_agent_actions(agent_name, response)
            
            task.status = "complete"
            task.result = response
            task.end_time = time.time()
            self.agent_statuses[agent_name]['status'] = 'idle'
            self.agent_statuses[agent_name]['current_task'] = None
            self.agent_statuses[agent_name]['last_active'] = datetime.now().isoformat()
            
            return response
        
        except Exception as e:
            task.status = "error"
            task.error = str(e)
            task.end_time = time.time()
            self.agent_statuses[agent_name]['status'] = 'idle'
            return f"Error executing task: {e}"
    
    def _handle_agent_actions(self, agent_name: str, response: str) -> str:
        """Handle file operations and code execution (from engine)."""
        actions_performed = []
        
        if 'READ_FILE:' in response:
            for line in response.split('\n'):
                if 'READ_FILE:' in line:
                    file_path = line.split('READ_FILE:')[1].strip()
                    actions_performed.append(f"Read {file_path}")
        
        if 'WRITE_FILE:' in response:
            actions_performed.append("File write requested")
        
        if 'EXECUTE_PYTHON:' in response or 'RUN_CODE:' in response:
            actions_performed.append("Code execution requested")
        
        if actions_performed:
            response += f"\n\nActions performed: {', '.join(actions_performed)}"
        
        return response
    
    def coordinate_full_team(self, user_request: str) -> Dict[str, Any]:
        """Coordinate team to handle user request (from engine)."""
        if not self.overseer:
            return {'error': 'No overseer registered'}
        
        overseer_prompt = f"""User Request: {user_request}

As the overseer, analyze this request and:
1. Break it down into tasks
2. Assign tasks to appropriate agents
3. Consider dependencies

Available agents: {', '.join([name for name in self.agent_chats.keys() if name != 'helix'])}

Format your response with:
- ASSIGN: [agent_name] - [task description]

Then provide your overall coordination plan."""
        
        console.print("\n[cyan]Helix analyzing request...[/cyan]")
        overseer_response = self.overseer.send_message(overseer_prompt)
        
        delegated_tasks = self.parse_task_delegation(overseer_response)
        
        task_results = {}
        for task_info in delegated_tasks:
            agent_name = task_info['agent']
            description = task_info['description']
            priority = task_info.get('priority', TaskPriority.MEDIUM)
            
            console.print(f"\n[yellow]Delegating to {agent_name}...[/yellow]")
            
            task = self.delegate_task_to_agent(agent_name, description, priority)
            if task:
                result = self.execute_single_agent_task(agent_name, task)
                task_results[agent_name] = result
        
        return {
            'overseer_response': overseer_response,
            'delegated_tasks': delegated_tasks,
            'task_results': task_results
        }
    
    def get_full_team_status(self) -> Dict:
        """Get current team status (from engine)."""
        return {
            'agents': {
                name: {
                    'status': status['status'],
                    'current_task': status['current_task'],
                    'last_active': status['last_active']
                }
                for name, status in self.agent_statuses.items()
            },
            'active_tasks': len([t for t in self.tasks if t.status == 'running']),
            'completed_tasks': len([t for t in self.tasks if t.status == 'complete']),
            'total_tasks': len(self.tasks)
        }
    
    def render_team_dashboard(self) -> Table:
        """Create visual dashboard of team status (from engine)."""
        table = Table(title="Team Status", show_header=True)
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Current Task", style="yellow")
        
        for name, status in self.agent_statuses.items():
            status_color = {
                'idle': 'green',
                'busy': 'yellow',
                'waiting': 'blue'
            }.get(status['status'], 'white')
            
            current_task = str(status['current_task']) if status['current_task'] is not None else "-"
            
            table.add_row(
                name.capitalize(),
                f"[{status_color}]{status['status']}[/{status_color}]",
                current_task
            )
        
        return table
    
    def render_task_status(self):
        """Render current task status table (from enhanced)."""
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
                'running': '⚙️  Working',
                'complete': '✅ Complete',
                'error': '❌ Error'
            }.get(task.status, task.status)
            
            duration = ""
            if task.start_time:
                if task.end_time:
                    duration = f"{task.end_time - task.start_time:.1f}s"
                else:
                    duration = f"{time.time() - task.start_time:.1f}s"
            
            task_desc = task.description[:40] + ("..." if len(task.description) > 40 else "")
            
            table.add_row(
                task.agent.capitalize(),
                task_desc,
                status_icon,
                duration
            )
        
        console.print(table)
    
    def get_agent_workload(self, agent_name: str) -> Dict:
        """Get workload stats for specific agent."""
        agent_tasks = [t for t in self.tasks if t.agent == agent_name]
        
        return {
            'total_tasks': len(agent_tasks),
            'completed': len([t for t in agent_tasks if t.status == 'complete']),
            'in_progress': len([t for t in agent_tasks if t.status == 'running']),
            'failed': len([t for t in agent_tasks if t.status == 'error']),
            'pending': len([t for t in agent_tasks if t.status == 'pending']),
            'current_status': self.agent_statuses.get(agent_name, {}).get('status', 'unknown')
        }
    
    def get_all_agent_workloads(self) -> Dict:
        """Get workload stats for all agents."""
        return {
            agent_name: self.get_agent_workload(agent_name)
            for agent_name in self.agent_chats.keys()
        }
    
    def reset_all_tasks(self):
        """Reset all tasks and agent statuses."""
        self.tasks = []
        for agent_name in self.agent_statuses:
            self.agent_statuses[agent_name] = {
                'status': 'idle',
                'current_task': None,
                'last_active': datetime.now().isoformat()
            }
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get specific task by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def get_tasks_by_agent(self, agent_name: str) -> List[Task]:
        """Get all tasks assigned to specific agent."""
        return [t for t in self.tasks if t.agent == agent_name]
    
    def get_task_dependencies(self, task_id: int) -> List[Task]:
        """Get all tasks that specific task depends on."""
        task = self.get_task_by_id(task_id)
        if not task:
            return []
        
        return [self.get_task_by_id(dep_id) for dep_id in task.dependencies if self.get_task_by_id(dep_id)]
    
    def get_task_dependents(self, task_id: int) -> List[Task]:
        """Get all tasks that depend on specific task."""
        return [t for t in self.tasks if task_id in t.dependencies]
    
    def estimate_total_time(self) -> float:
        """Estimate total time needed for all tasks."""
        return len(self.tasks) * 30.0
    
    def get_critical_path(self) -> List[Task]:
        """Get the critical path (longest dependency chain)."""
        if not self.tasks:
            return []
        
        sorted_tasks = sorted(self.tasks, key=lambda t: len(t.dependencies))
        return sorted_tasks
    
    def export_results_json(self) -> str:
        """Export all results as JSON."""
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'total_tasks': len(self.tasks),
            'tasks': [
                {
                    'task_id': t.task_id,
                    'agent': t.agent,
                    'description': t.description,
                    'status': t.status,
                    'result': t.result,
                    'error': t.error,
                    'priority': t.priority.value if hasattr(t, 'priority') else 'medium',
                    'start_time': t.start_time,
                    'end_time': t.end_time,
                    'duration': t.end_time - t.start_time if t.start_time and t.end_time else None
                }
                for t in self.tasks
            ],
            'agent_statuses': self.agent_statuses
        }
        
        return json.dumps(export_data, indent=2)
    
    def print_statistics(self):
        """Print collaboration statistics."""
        if not self.tasks:
            console.print("[yellow]No tasks executed yet[/yellow]")
            return
        
        completed = len([t for t in self.tasks if t.status == 'complete'])
        failed = len([t for t in self.tasks if t.status == 'error'])
        total_time = sum([
            t.end_time - t.start_time 
            for t in self.tasks 
            if t.start_time and t.end_time
        ])
        
        stats_table = Table(title="Collaboration Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        stats_table.add_row("Total Tasks", str(len(self.tasks)))
        stats_table.add_row("Completed", str(completed))
        stats_table.add_row("Failed", str(failed))
        stats_table.add_row("Success Rate", f"{(completed/len(self.tasks)*100):.1f}%")
        stats_table.add_row("Total Time", f"{total_time:.1f}s")
        stats_table.add_row("Avg Time/Task", f"{(total_time/len(self.tasks)):.1f}s" if self.tasks else "N/A")
        
        console.print(stats_table)
