#!/usr/bin/env python3
"""
Advanced Interface - For power users who want full control
Features:
- Multi-agent orchestration
- Custom workflows
- Pipeline creation
- Advanced configuration
- Real-time monitoring
- Custom tool chains
"""

from typing import Dict, List, Optional, Any, Callable
from agents.team_collaboration import AgentTeam, get_agent_team
from agents.universal_agent_interface import UniversalAgent
from tasks.task_tree import TaskTree, TaskNode
from messaging.message_bus import get_message_bus
from performance_optimizer import get_performance_monitor
from agents.sentinel_agent import SentinelAgent
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from datetime import datetime
import asyncio


console = Console()


class AdvancedInterface:
    """
    Advanced interface for power users.
    
    Full control over:
    - Agent selection and configuration
    - Task delegation and orchestration
    - Custom workflows and pipelines
    - Performance monitoring
    - System health
    - Real-time updates
    
    Example:
        interface = AdvancedInterface()
        
        # Create custom workflow
        workflow = interface.create_workflow("feature_development")
        workflow.add_stage("design", agents=["aurora"])
        workflow.add_stage("implement", agents=["felix", "nova"])
        workflow.add_stage("test", agents=["quinn"])
        workflow.add_stage("review", agents=["orion", "mira"])
        
        result = await interface.execute_workflow(workflow, "Build REST API")
    """
    
    def __init__(self):
        """Initialize advanced interface."""
        self.team = get_agent_team()
        self.message_bus = get_message_bus()
        self.monitor = get_performance_monitor()
        self.sentinel = SentinelAgent()
        
        # Initialize all agents
        self._init_all_agents()
        
        # Custom workflows
        self.workflows: Dict[str, 'Workflow'] = {}
        
        # Pipeline chains
        self.pipelines: Dict[str, 'Pipeline'] = {}
    
    def _init_all_agents(self):
        """Initialize all 23 agents for team use."""
        agent_names = [
            # Planners
            'aurora', 'felix', 'sage', 'ember',
            # Critics
            'orion', 'atlas', 'mira', 'vex',
            # Developers
            'sol', 'echo', 'nova', 'quinn', 'blaze', 'ivy', 'zephyr',
            # Assistants
            'pixel', 'script', 'turbo', 'sentinel',
            # Specialists
            'helix', 'patch', 'pulse', 'link'
        ]
        
        for name in agent_names:
            self.team.add_agent(name, UniversalAgent(name))
        
        console.print(f"[green]✓ Initialized {len(agent_names)} agents[/green]")
    
    def create_workflow(self, name: str) -> 'Workflow':
        """
        Create custom workflow.
        
        Args:
            name: Workflow name
            
        Returns:
            Workflow instance
        """
        workflow = Workflow(name)
        self.workflows[name] = workflow
        return workflow
    
    async def execute_workflow(
        self,
        workflow: 'Workflow',
        task: str,
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        Execute custom workflow.
        
        Args:
            workflow: Workflow to execute
            task: Task description
            show_progress: Show progress UI
            
        Returns:
            Workflow result
        """
        if show_progress:
            return await self._execute_with_progress(workflow, task)
        else:
            return await workflow.execute(task, self.team)
    
    async def _execute_with_progress(
        self,
        workflow: 'Workflow',
        task: str
    ) -> Dict[str, Any]:
        """Execute workflow with progress display."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task_progress = progress.add_task(
                f"[cyan]Executing {workflow.name}...",
                total=len(workflow.stages)
            )
            
            result = await workflow.execute(task, self.team, progress, task_progress)
            
            progress.update(task_progress, completed=len(workflow.stages))
            
        return result
    
    def create_pipeline(self, name: str) -> 'Pipeline':
        """
        Create processing pipeline.
        
        Pipelines chain operations: input → step1 → step2 → ... → output
        
        Args:
            name: Pipeline name
            
        Returns:
            Pipeline instance
        """
        pipeline = Pipeline(name)
        self.pipelines[name] = pipeline
        return pipeline
    
    async def execute_pipeline(
        self,
        pipeline: 'Pipeline',
        input_data: Any
    ) -> Any:
        """Execute processing pipeline."""
        return await pipeline.execute(input_data, self.team)
    
    def create_task_tree(self, root_task: str) -> TaskTree:
        """
        Create hierarchical task tree.
        
        Args:
            root_task: Root task description
            
        Returns:
            TaskTree instance
        """
        return TaskTree(root_task)
    
    async def execute_task_tree(
        self,
        tree: TaskTree,
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Execute hierarchical task tree.
        
        Args:
            tree: Task tree to execute
            parallel: Execute independent tasks in parallel
            
        Returns:
            Execution results
        """
        results = {}
        
        while True:
            # Get ready tasks
            ready_tasks = tree.get_ready_tasks()
            
            if not ready_tasks:
                break
            
            # Execute tasks
            if parallel and len(ready_tasks) > 1:
                # Parallel execution
                task_results = await asyncio.gather(*[
                    self._execute_tree_task(task, tree)
                    for task in ready_tasks
                ])
                
                for task, result in zip(ready_tasks, task_results):
                    results[task.task_id] = result
            else:
                # Sequential execution
                for task in ready_tasks:
                    result = await self._execute_tree_task(task, tree)
                    results[task.task_id] = result
        
        return {
            'success': True,
            'results': results,
            'progress': tree.get_progress(),
            'stats': tree.get_stats()
        }
    
    async def _execute_tree_task(self, task: TaskNode, tree: TaskTree) -> Any:
        """Execute single task from tree."""
        tree.mark_running(task.task_id)
        
        agent = self.team.agents.get(task.agent)
        if not agent:
            tree.mark_failed(task.task_id, f"Agent {task.agent} not found")
            return None
        
        try:
            result = agent(task.description)
            tree.mark_complete(task.task_id, str(result))
            return result
        except Exception as e:
            tree.mark_failed(task.task_id, str(e))
            return None
    
    def monitor_system(self) -> Dict[str, Any]:
        """Get comprehensive system monitoring."""
        return {
            'health': self.sentinel.get_system_health_report(),
            'performance': self.monitor.get_report(),
            'team': self.team.get_team_stats(),
            'timestamp': datetime.now().isoformat()
        }
    
    def show_dashboard(self):
        """Show real-time dashboard."""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        # Header
        layout["header"].update(
            Panel("[bold cyan]AI CodeForge - Advanced Interface[/bold cyan]",
                  border_style="cyan")
        )
        
        # System status
        health = self.sentinel.monitor_system()
        status_table = Table(title="System Status")
        status_table.add_column("Metric", style="cyan")
        status_table.add_column("Value", style="green")
        
        for metric_name, metric in health.items():
            status_table.add_row(metric.name, f"{metric.value:.1f}{metric.unit}")
        
        layout["left"].update(Panel(status_table, title="Health"))
        
        # Team status
        team_stats = self.team.get_team_stats()
        team_table = Table(title="Team")
        team_table.add_column("Metric", style="cyan")
        team_table.add_column("Value", style="yellow")
        
        team_table.add_row("Total Agents", str(team_stats['total_agents']))
        team_table.add_row("Active Tasks", str(team_stats['active_tasks']))
        team_table.add_row("Messages", str(team_stats['messages_exchanged']))
        
        layout["right"].update(Panel(team_table, title="Team"))
        
        # Footer
        layout["footer"].update(
            Panel(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}",
                  border_style="dim")
        )
        
        console.print(layout)
    
    def configure_agent(
        self,
        agent_name: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        system_prompt_override: Optional[str] = None
    ):
        """Configure individual agent parameters."""
        agent = self.team.agents.get(agent_name)
        if agent:
            # Apply configuration
            agent.config['temperature'] = temperature
            agent.config['max_tokens'] = max_tokens
            if system_prompt_override:
                agent.config['system_override'] = system_prompt_override
            
            console.print(f"[green]✓ Configured {agent_name}[/green]")
        else:
            console.print(f"[red]✗ Agent {agent_name} not found[/red]")
    
    def create_agent_chain(
        self,
        name: str,
        agents: List[str]
    ) -> 'AgentChain':
        """
        Create chain of agents that process sequentially.
        
        Output of agent N becomes input to agent N+1.
        
        Args:
            name: Chain name
            agents: Ordered list of agent names
            
        Returns:
            AgentChain instance
        """
        return AgentChain(name, agents, self.team)
    
    def get_conversation_log(self, format: str = "text") -> str:
        """Get formatted conversation log between agents."""
        if format == "text":
            return self.team.visualize_conversation()
        elif format == "json":
            import json
            return json.dumps(self.team.get_conversation_history(), indent=2)
        else:
            return str(self.team.get_conversation_history())


class Workflow:
    """
    Custom workflow with multiple stages.
    
    Each stage can have different agents working on it.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.stages: List[Dict[str, Any]] = []
    
    def add_stage(
        self,
        name: str,
        agents: List[str],
        dependencies: Optional[List[str]] = None
    ) -> 'Workflow':
        """Add stage to workflow."""
        self.stages.append({
            'name': name,
            'agents': agents,
            'dependencies': dependencies or [],
            'result': None
        })
        return self
    
    async def execute(
        self,
        task: str,
        team: AgentTeam,
        progress: Optional[Any] = None,
        progress_task: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Execute workflow."""
        results = {}
        
        for stage in self.stages:
            if progress:
                progress.update(
                    progress_task,
                    description=f"[cyan]Stage: {stage['name']}..."
                )
            
            # Execute stage
            stage_result = await team.collaborative_task(
                f"{task} - Stage: {stage['name']}",
                required_roles=stage['agents']
            )
            
            stage['result'] = stage_result
            results[stage['name']] = stage_result
            
            if progress:
                progress.advance(progress_task)
        
        return {
            'workflow': self.name,
            'success': True,
            'stages': results
        }


class Pipeline:
    """
    Processing pipeline: input → step1 → step2 → ... → output
    """
    
    def __init__(self, name: str):
        self.name = name
        self.steps: List[Dict[str, Any]] = []
    
    def add_step(
        self,
        name: str,
        agent: str,
        transform: Optional[Callable] = None
    ) -> 'Pipeline':
        """Add step to pipeline."""
        self.steps.append({
            'name': name,
            'agent': agent,
            'transform': transform
        })
        return self
    
    async def execute(self, input_data: Any, team: AgentTeam) -> Any:
        """Execute pipeline."""
        current_data = input_data
        
        for step in self.steps:
            agent = team.agents.get(step['agent'])
            if not agent:
                continue
            
            # Process with agent
            result = agent(str(current_data))
            
            # Apply transform if provided
            if step['transform']:
                current_data = step['transform'](result)
            else:
                current_data = result
        
        return current_data


class AgentChain:
    """Chain of agents processing sequentially."""
    
    def __init__(self, name: str, agents: List[str], team: AgentTeam):
        self.name = name
        self.agents = agents
        self.team = team
    
    async def execute(self, input_data: str) -> Any:
        """Execute chain."""
        current_output = input_data
        
        for agent_name in self.agents:
            agent = self.team.agents.get(agent_name)
            if agent:
                current_output = str(agent(str(current_output)))
        
        return current_output


# Example usage
if __name__ == "__main__":
    async def demo():
        interface = AdvancedInterface()
        
        print("\n=== Advanced Interface Demo ===\n")
        
        # 1. Custom Workflow
        print("1. Creating custom workflow...")
        workflow = interface.create_workflow("full_development")
        workflow.add_stage("design", agents=["aurora"])
        workflow.add_stage("implement", agents=["felix", "nova"])
        workflow.add_stage("test", agents=["quinn"])
        workflow.add_stage("review", agents=["orion"])
        
        # 2. Task Tree
        print("2. Creating task tree...")
        tree = interface.create_task_tree("Build REST API")
        design = tree.add_task("Design API", agent="aurora")
        impl = tree.add_task("Implement", agent="felix", depends_on=[design])
        tests = tree.add_task("Tests", agent="quinn", depends_on=[impl])
        
        # 3. System Monitoring
        print("3. System monitoring...")
        interface.show_dashboard()
        
        print("\n✓ Demo complete!")
    
    asyncio.run(demo())
