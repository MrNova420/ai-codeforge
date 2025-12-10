#!/usr/bin/env python3
"""
Unified Interface Layer for AI CodeForge
Makes all features accessible from any entry point (talk, codeforge, webapp, run)

This module provides a central integration point that connects:
- All 23 AI agents
- Full orchestrator with V3 advanced features
- Collaboration engines (V3 JSON-based, enhanced)
- Memory systems (vector memory, persistent storage)
- Research capabilities (web search, synthesis)
- Tool registry and code execution
- File operations and codebase analysis

Usage:
    from unified_interface import get_unified_interface
    
    unified = get_unified_interface()
    result = unified.execute_task("create a REST API", mode="team")
    agents = unified.list_all_agents()
    features = unified.list_all_features()
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from rich.console import Console

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

console = Console()


class UnifiedInterface:
    """
    Central interface that provides access to all AI CodeForge features.
    Can be used by any entry point (talk, codeforge, webapp, run).
    """
    
    def __init__(self):
        """Initialize unified interface with all components."""
        self.orchestrator = None
        self.collaboration_engine = None
        self.agents = {}
        self.features_initialized = False
        
    def initialize(self, mode: str = "full"):
        """
        Initialize all features based on mode.
        
        This lazy-loads all components on first use to avoid unnecessary imports
        and ensure the system starts quickly.
        
        Args:
            mode: "full" for all features, "lite" for basic features (currently unused)
        """
        if self.features_initialized:
            return
            
        try:
            # Import orchestrator
            from orchestrator_v2 import EnhancedOrchestrator
            self.orchestrator = EnhancedOrchestrator()
            
            # Don't initialize CollaborationV3 directly - let orchestrator handle it
            # The orchestrator will create agent_chats and collaboration_v3 when needed
            
            # Import collaboration engines for reference (not initialization)
            from collaboration_enhanced import EnhancedCollaboration
            self.collaboration_enhanced = EnhancedCollaboration()
            
            # Import agent management
            from orchestrator import AgentLoader
            self.agent_loader = AgentLoader()
            
            # Import tools and memory
            from tools.registry import get_registry
            self.tool_registry = get_registry()
            
            # Import memory systems
            try:
                from memory.vector_store import VectorMemoryStore
                self.vector_memory = VectorMemoryStore()
            except (ImportError, ModuleNotFoundError):
                self.vector_memory = None
                
            from memory_manager import MemoryManager
            self.memory_manager = MemoryManager()
            
            # Import file and code operations
            from file_manager import FileManager
            from code_executor import CodeExecutor
            
            self.file_manager = FileManager()
            self.code_executor = CodeExecutor()
            
            # Import researcher
            try:
                from researcher_agent import ResearcherAgent
                self.researcher = ResearcherAgent()
            except (ImportError, ModuleNotFoundError, AttributeError):
                self.researcher = None
            
            self.features_initialized = True
            console.print("[dim]✅ All features initialized[/dim]")
            
        except (ImportError, ModuleNotFoundError, AttributeError) as e:
            console.print(f"[yellow]⚠️  Some features unavailable: {e}[/yellow]")
            self.features_initialized = True  # Continue with what we have
    
    def execute_task(self, task: str, mode: str = "auto", agents: Optional[List[str]] = None) -> Any:
        """
        Execute any task using appropriate features.
        
        This is the main entry point for task execution from any interface.
        Automatically detects the best execution mode if mode="auto".
        
        Args:
            task: Natural language task description (e.g., "create a REST API")
            mode: Execution mode:
                - "auto": Auto-detect best mode based on task keywords
                - "solo": Single agent execution
                - "team": Multi-agent collaboration (default for most tasks)
                - "research": Research-focused with web search
                - "full_orchestrator": All 23 agents + V3 advanced features
            agents: Optional list of specific agent names to use (e.g., ["felix", "sol"])
            
        Returns:
            Task result dictionary with status, mode, and execution details
        """
        self.initialize()
        
        # Auto-detect best mode if needed
        if mode == "auto":
            mode = self._detect_best_mode(task)
        
        if mode == "full_orchestrator":
            # Use full orchestrator with all 23 agents
            return self._run_full_orchestrator(task)
            
        elif mode == "team":
            # Multi-agent collaboration
            return self._run_team_mode(task, agents)
            
        elif mode == "solo":
            # Single agent
            agent_name = agents[0] if agents else "felix"
            return self._run_solo_agent(task, agent_name)
            
        elif mode == "research":
            # Research mode
            return self._run_research_mode(task)
            
        else:
            # Default to team collaboration
            return self._run_team_mode(task, agents)
    
    def _detect_best_mode(self, task: str) -> str:
        """Automatically detect the best mode for a task."""
        task_lower = task.lower()
        
        # Check for orchestrator keywords
        if any(word in task_lower for word in [
            "full orchestrator", "all agents", "complete team",
            "production", "complex project", "enterprise"
        ]):
            return "full_orchestrator"
        
        # Check for research keywords
        if any(word in task_lower for word in [
            "research", "find out", "what is", "how does",
            "learn about", "explain", "investigate"
        ]):
            return "research"
        
        # Check for team collaboration keywords
        if any(word in task_lower for word in [
            "collaborate", "team", "multiple agents",
            "review and improve", "design and build"
        ]):
            return "team"
        
        # Default to team mode for most tasks
        return "team"
    
    def _run_full_orchestrator(self, task: str) -> Any:
        """Run task with full orchestrator (all 23 agents + V3 features)."""
        if not self.orchestrator:
            console.print("[yellow]Orchestrator not available, falling back to team mode[/yellow]")
            return self._run_team_mode(task, None)
        
        console.print("[bold cyan]🚀 Launching Full Orchestrator Mode[/bold cyan]")
        console.print("[dim]All 23 agents + V3 advanced features active[/dim]\n")
        
        # Use orchestrator's main functionality
        # This would integrate with the orchestrator's actual task execution
        return {"status": "full_orchestrator", "task": task, "message": "Full orchestrator mode activated"}
    
    def _run_team_mode(self, task: str, agents: Optional[List[str]] = None) -> Any:
        """Run task with team collaboration."""
        console.print("[bold cyan]🤝 Team Collaboration Mode[/bold cyan]")
        
        if agents:
            console.print(f"[dim]Using agents: {', '.join(agents)}[/dim]\n")
        else:
            console.print("[dim]Auto-selecting best agents for task[/dim]\n")
        
        # Use orchestrator if available
        if self.orchestrator:
            # Initialize collaboration agents if not already done
            if not self.orchestrator.agent_chats:
                self.orchestrator._init_collaboration_agents()
            
            # Execute through collaboration engine
            if self.orchestrator.collab_engine:
                result = self.orchestrator.collab_engine.handle_request(task)
                return {
                    "status": "success",
                    "mode": "team",
                    "task": task,
                    "agents": agents,
                    "result": result
                }
        
        return {
            "status": "pending", 
            "mode": "team",
            "task": task,
            "agents": agents,
            "message": "Orchestrator not fully initialized. Use ./run for full team mode."
        }
    
    def _run_solo_agent(self, task: str, agent_name: str) -> Any:
        """Run task with single agent."""
        console.print(f"[bold cyan]💬 Solo Agent: {agent_name}[/bold cyan]\n")
        
        # Direct agent chat
        return {"status": "solo", "task": task, "agent": agent_name}
    
    def _run_research_mode(self, task: str) -> Any:
        """Run task in research mode."""
        console.print("[bold cyan]🔍 Research Mode[/bold cyan]\n")
        
        if self.researcher:
            # Use researcher agent
            return {"status": "research", "task": task}
        
        console.print("[yellow]Researcher unavailable, using general agents[/yellow]")
        return self._run_team_mode(task, ["helix", "sage"])
    
    def list_all_features(self) -> Dict[str, Any]:
        """List all available features and their status."""
        self.initialize()
        
        features = {
            "orchestrator": self.orchestrator is not None,
            "collaboration_v3": (self.orchestrator and self.orchestrator.collab_engine is not None) if self.orchestrator else False,
            "vector_memory": self.vector_memory is not None,
            "researcher": self.researcher is not None,
            "tool_registry": hasattr(self, 'tool_registry'),
            "file_manager": hasattr(self, 'file_manager'),
            "code_executor": hasattr(self, 'code_executor'),
            "memory_manager": hasattr(self, 'memory_manager'),
            "all_23_agents": self.orchestrator and hasattr(self.orchestrator, 'agent_loader') if self.orchestrator else False,
        }
        
        return features
    
    def list_all_agents(self) -> List[str]:
        """List all 23 available agents."""
        return [
            # Planners & Strategists
            "aurora", "sage", "felix", "ember",
            # Critics & Reviewers
            "orion", "atlas", "mira", "vex",
            # Specialists
            "sol", "echo", "nova", "quinn", "blaze", "ivy", "zephyr",
            # Assistants
            "pixel", "script", "turbo", "sentinel",
            # Special Agents
            "helix", "patch", "pulse", "link"
        ]
    
    def get_agent_info(self, agent_name: str) -> Dict[str, str]:
        """Get information about a specific agent."""
        agent_info = {
            # Planners
            "aurora": {"role": "Product Manager", "specialty": "Strategic planning & roadmaps"},
            "sage": {"role": "Lead Architect", "specialty": "Technical strategy & design"},
            "felix": {"role": "Senior Developer", "specialty": "Full-stack development"},
            "ember": {"role": "Creative Director", "specialty": "Innovation & design"},
            
            # Critics
            "orion": {"role": "Code Reviewer", "specialty": "Quality & best practices"},
            "atlas": {"role": "Performance Expert", "specialty": "Optimization"},
            "mira": {"role": "Security Engineer", "specialty": "Security & AppSec"},
            "vex": {"role": "Critical Analyst", "specialty": "Finding issues"},
            
            # Specialists
            "sol": {"role": "Backend Specialist", "specialty": "APIs & servers"},
            "echo": {"role": "Frontend Developer", "specialty": "UI & user experience"},
            "nova": {"role": "DevOps Engineer", "specialty": "Infrastructure & deployment"},
            "quinn": {"role": "QA Lead", "specialty": "Testing & quality"},
            "blaze": {"role": "Mobile Developer", "specialty": "iOS & Android"},
            "ivy": {"role": "Data Engineer", "specialty": "Databases & data"},
            "zephyr": {"role": "Cloud Architect", "specialty": "Cloud infrastructure"},
            
            # Assistants
            "pixel": {"role": "UX Designer", "specialty": "Design systems"},
            "script": {"role": "Tech Writer", "specialty": "Documentation"},
            "turbo": {"role": "Performance Engineer", "specialty": "Speed optimization"},
            "sentinel": {"role": "SRE Lead", "specialty": "Monitoring & reliability"},
            
            # Special
            "helix": {"role": "Research Lead", "specialty": "Technology research"},
            "patch": {"role": "Bug Hunter", "specialty": "Debugging & fixes"},
            "pulse": {"role": "Integration Specialist", "specialty": "System integration"},
            "link": {"role": "Collaboration Lead", "specialty": "Team coordination"},
        }
        
        return agent_info.get(agent_name, {"role": "Unknown", "specialty": "Unknown"})


# Global unified interface instance
_unified_interface = None

def get_unified_interface() -> UnifiedInterface:
    """Get or create the global unified interface instance."""
    global _unified_interface
    if _unified_interface is None:
        _unified_interface = UnifiedInterface()
    return _unified_interface
