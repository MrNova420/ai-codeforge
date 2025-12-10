#!/usr/bin/env python3
"""
Startup Manager - Initialize and configure the entire AI CodeForge system
Handles system initialization, configuration loading, and environment setup

Features:
- System initialization
- Configuration management
- Environment validation
- Dependency checking
- Workspace setup
- Agent initialization
- Performance optimization
- Health checks
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()


class StartupManager:
    """Manages system startup and initialization."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.initialized = False
        self.config_manager = None
        self.issues = []
        self.warnings = []
    
    def initialize(self, mode: str = "auto", verbose: bool = False) -> bool:
        """
        Initialize the entire system.
        
        Args:
            mode: Initialization mode (auto, simple, advanced, expert)
            verbose: Show detailed initialization steps
        
        Returns:
            True if initialization successful
        """
        console.print(Panel.fit(
            "[bold cyan]AI CodeForge Initialization[/bold cyan]\n"
            "Setting up enterprise-grade development environment...",
            border_style="cyan"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Step 1: Load configuration
            task1 = progress.add_task("[cyan]Loading configuration...", total=None)
            config_ok = self._load_configuration()
            progress.update(task1, completed=True)
            
            if config_ok:
                console.print("  ✓ Configuration loaded")
            else:
                console.print("  ⚠ Using default configuration")
                self.warnings.append("Configuration not found, using defaults")
            
            # Step 2: Validate environment
            task2 = progress.add_task("[cyan]Validating environment...", total=None)
            env_ok = self._validate_environment()
            progress.update(task2, completed=True)
            
            if env_ok:
                console.print("  ✓ Environment validated")
            else:
                console.print("  ✗ Environment validation failed")
                return False
            
            # Step 3: Check dependencies
            task3 = progress.add_task("[cyan]Checking dependencies...", total=None)
            deps_ok = self._check_dependencies()
            progress.update(task3, completed=True)
            
            if deps_ok:
                console.print("  ✓ All dependencies available")
            else:
                console.print("  ⚠ Some optional dependencies missing")
                self.warnings.append("Some features may be limited")
            
            # Step 4: Setup workspace
            task4 = progress.add_task("[cyan]Setting up workspace...", total=None)
            workspace_ok = self._setup_workspace()
            progress.update(task4, completed=True)
            
            if workspace_ok:
                console.print("  ✓ Workspace ready")
            else:
                console.print("  ⚠ Workspace setup issues")
                self.warnings.append("Workspace may need manual setup")
            
            # Step 5: Initialize agents
            task5 = progress.add_task("[cyan]Initializing agents...", total=None)
            agents_ok = self._initialize_agents()
            progress.update(task5, completed=True)
            
            if agents_ok:
                console.print("  ✓ Agents initialized")
            else:
                console.print("  ✗ Agent initialization failed")
                self.issues.append("Agent system not available")
            
            # Step 6: Performance optimization
            task6 = progress.add_task("[cyan]Optimizing performance...", total=None)
            perf_ok = self._optimize_performance()
            progress.update(task6, completed=True)
            
            if perf_ok:
                console.print("  ✓ Performance optimized")
            else:
                console.print("  ⚠ Running with default performance")
            
            # Step 7: System health check
            task7 = progress.add_task("[cyan]Running health checks...", total=None)
            health_ok = self._health_check()
            progress.update(task7, completed=True)
            
            if health_ok:
                console.print("  ✓ System healthy")
            else:
                console.print("  ⚠ System has issues")
        
        # Display summary
        self._display_summary()
        
        self.initialized = True
        return len(self.issues) == 0
    
    def _load_configuration(self) -> bool:
        """Load configuration."""
        try:
            from config_manager import get_config_manager
            self.config_manager = get_config_manager()
            return True
        except Exception as e:
            self.warnings.append(f"Config error: {e}")
            return False
    
    def _validate_environment(self) -> bool:
        """Validate environment."""
        try:
            # Check Python version
            if sys.version_info < (3, 8):
                self.issues.append("Python 3.8+ required")
                return False
            
            # Check project structure
            required_dirs = ['agents', 'tools', 'memory', 'teams']
            for dir_name in required_dirs:
                if not (self.project_root / dir_name).exists():
                    self.issues.append(f"Missing directory: {dir_name}")
                    return False
            
            return True
        except Exception as e:
            self.issues.append(f"Environment validation error: {e}")
            return False
    
    def _check_dependencies(self) -> bool:
        """Check dependencies."""
        required = ['rich', 'requests']
        optional = ['psutil', 'numpy', 'chromadb', 'docker', 'fastapi']
        
        missing_required = []
        missing_optional = []
        
        for pkg in required:
            try:
                __import__(pkg)
            except ImportError:
                missing_required.append(pkg)
        
        for pkg in optional:
            try:
                __import__(pkg)
            except ImportError:
                missing_optional.append(pkg)
        
        if missing_required:
            self.issues.append(f"Missing required: {', '.join(missing_required)}")
            return False
        
        if missing_optional:
            self.warnings.append(f"Missing optional: {', '.join(missing_optional)}")
        
        return True
    
    def _setup_workspace(self) -> bool:
        """Setup workspace directories."""
        try:
            if self.config_manager:
                self.config_manager.create_workspace_dirs()
            else:
                # Create basic directories
                for dir_name in ['workspace', 'output', 'logs', 'temp']:
                    Path(dir_name).mkdir(exist_ok=True)
            
            return True
        except Exception as e:
            self.warnings.append(f"Workspace setup error: {e}")
            return False
    
    def _initialize_agents(self) -> bool:
        """Initialize agent system."""
        try:
            from agents.universal_agent_interface import UniversalAgent
            
            # Test initialize one agent
            test_agent = UniversalAgent('felix')
            return True
        except Exception as e:
            self.issues.append(f"Agent initialization error: {e}")
            return False
    
    def _optimize_performance(self) -> bool:
        """Apply performance optimizations."""
        try:
            from performance_optimizer import fast_startup, get_performance_monitor
            
            if self.config_manager and self.config_manager.config.performance.fast_startup:
                fast_startup()
            
            monitor = get_performance_monitor()
            return True
        except Exception as e:
            self.warnings.append(f"Performance optimization error: {e}")
            return False
    
    def _health_check(self) -> bool:
        """Run system health check."""
        try:
            # Check critical systems
            from agents.team_collaboration import AgentTeam
            from teams.master_orchestrator import MasterOrchestrator
            
            return True
        except Exception as e:
            self.warnings.append(f"Health check warning: {e}")
            return False
    
    def _display_summary(self):
        """Display initialization summary."""
        console.print()
        
        if self.issues:
            console.print("[bold red]Issues Found:[/bold red]")
            for issue in self.issues:
                console.print(f"  ✗ {issue}")
            console.print()
        
        if self.warnings:
            console.print("[bold yellow]Warnings:[/bold yellow]")
            for warning in self.warnings:
                console.print(f"  ⚠ {warning}")
            console.print()
        
        if not self.issues and not self.warnings:
            console.print(Panel.fit(
                "[bold green]✓ System Ready![/bold green]\n"
                "All systems operational. Ready for development.",
                border_style="green"
            ))
        elif not self.issues:
            console.print(Panel.fit(
                "[bold cyan]✓ System Ready (with warnings)[/bold cyan]\n"
                "Core systems operational. Some features may be limited.",
                border_style="cyan"
            ))
        else:
            console.print(Panel.fit(
                "[bold red]✗ Initialization Failed[/bold red]\n"
                "Critical issues detected. Please resolve and try again.",
                border_style="red"
            ))
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        info = {
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'project_root': str(self.project_root),
            'initialized': self.initialized,
            'issues_count': len(self.issues),
            'warnings_count': len(self.warnings)
        }
        
        if self.config_manager:
            info['config'] = self.config_manager.get_summary()
        
        return info
    
    def display_system_info(self):
        """Display system information."""
        info = self.get_system_info()
        
        table = Table(title="System Information")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Python Version", info['python_version'])
        table.add_row("Project Root", info['project_root'])
        table.add_row("Initialized", "Yes" if info['initialized'] else "No")
        table.add_row("Issues", str(info['issues_count']))
        table.add_row("Warnings", str(info['warnings_count']))
        
        if 'config' in info:
            table.add_row("", "")  # Separator
            table.add_row("[bold]Configuration[/bold]", "")
            for key, value in info['config'].items():
                table.add_row(f"  {key}", str(value))
        
        console.print(table)


# Global instance
_startup_manager = None


def get_startup_manager() -> StartupManager:
    """Get global startup manager instance."""
    global _startup_manager
    if _startup_manager is None:
        _startup_manager = StartupManager()
    return _startup_manager


def initialize_system(mode: str = "auto", verbose: bool = False) -> bool:
    """Initialize the system."""
    return get_startup_manager().initialize(mode, verbose)


def is_initialized() -> bool:
    """Check if system is initialized."""
    return get_startup_manager().initialized


def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    return get_startup_manager().get_system_info()


if __name__ == '__main__':
    # Standalone initialization
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize AI CodeForge")
    parser.add_argument('--mode', choices=['auto', 'simple', 'advanced', 'expert'],
                       default='auto', help='Initialization mode')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--info', action='store_true', help='Show system info')
    
    args = parser.parse_args()
    
    if args.info:
        mgr = get_startup_manager()
        mgr.display_system_info()
    else:
        success = initialize_system(args.mode, args.verbose)
        sys.exit(0 if success else 1)
