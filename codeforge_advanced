#!/usr/bin/env python3
"""
CodeForge Advanced CLI - Professional Command Line Interface
Enterprise-grade CLI with full control and advanced features

Features:
- Argument parsing with subcommands
- Configuration management
- History tracking
- Export capabilities
- Watch mode
- JSON output
- Custom workflows
- Direct agent communication
- Batch operations
- Performance monitoring
"""

import sys
import argparse
import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.tree import Tree

console = Console()


class CodeForgeAdvancedCLI:
    """Advanced CLI with full features."""
    
    VERSION = "2.0.0"
    
    def __init__(self):
        self.config_file = Path.home() / ".codeforge" / "config.json"
        self.history_file = Path.home() / ".codeforge" / "history.json"
        self.config = self.load_config()
        self.history = self.load_history()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration."""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    return json.load(f)
            except:
                pass
        return {
            'default_agent': 'felix',
            'default_mode': 'sequential',
            'output_format': 'text',
            'auto_save': True,
            'theme': 'dark'
        }
    
    def save_config(self):
        """Save configuration."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_history(self) -> List[Dict[str, Any]]:
        """Load command history."""
        if self.history_file.exists():
            try:
                with open(self.history_file) as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_history(self, command: str, result: Any):
        """Save to history."""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'success': result is not None
        })
        # Keep last 1000 entries
        self.history = self.history[-1000:]
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def print_banner(self):
        """Print enhanced banner."""
        banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🔨 AI CODEFORGE - AAA Production Development Team v2.0        ║
║                                                                  ║
║   23 Specialized AI Agents • Enterprise-Grade • Production-Ready ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
        console.print(banner, style="bold cyan")
    
    async def code_command(self, task: str, language: Optional[str] = None, 
                          output: Optional[str] = None, agent: Optional[str] = None):
        """Generate code with advanced options."""
        from agents.universal_agent_interface import UniversalAgent
        
        agent_name = agent or self.config.get('default_agent', 'felix')
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task_obj = progress.add_task(f"[cyan]Generating code with {agent_name}...", total=None)
            
            try:
                agent = UniversalAgent(agent_name)
                
                prompt = task
                if language:
                    prompt += f" (in {language})"
                
                result = agent(prompt)
                
                # Display result
                console.print(Panel(result, title=f"Code by {agent_name}", border_style="green"))
                
                # Save if requested
                if output:
                    Path(output).write_text(result)
                    console.print(f"[green]✓[/green] Saved to {output}")
                
                self.save_history(f"code: {task}", result)
                return result
            
            except Exception as e:
                console.print(f"[red]✗ Error:[/red] {str(e)}")
                self.save_history(f"code: {task}", None)
                return None
    
    async def team_command(self, task: str, mode: str = "sequential", 
                          agents: Optional[List[str]] = None):
        """Team collaboration with advanced options."""
        from teams.master_orchestrator import MasterOrchestrator, WorkMode
        
        mode_map = {
            'parallel': WorkMode.PARALLEL,
            'sequential': WorkMode.SEQUENTIAL,
            'collaborative': WorkMode.COLLABORATIVE,
            'autonomous': WorkMode.AUTONOMOUS
        }
        
        work_mode = mode_map.get(mode, WorkMode.SEQUENTIAL)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task_obj = progress.add_task(f"[cyan]Team working in {mode} mode...", total=None)
            
            try:
                orchestrator = MasterOrchestrator()
                result = await orchestrator.all_agents_work_together(task, mode=work_mode)
                
                console.print(Panel(str(result), title=f"Team Result ({mode})", border_style="green"))
                self.save_history(f"team {mode}: {task}", result)
                return result
            
            except Exception as e:
                console.print(f"[red]✗ Error:[/red] {str(e)}")
                self.save_history(f"team {mode}: {task}", None)
                return None
    
    async def security_command(self, path: str, report: bool = False, 
                              output: Optional[str] = None):
        """Security audit with advanced options."""
        from security.security_operations import SecurityOpsCenter
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Running security audit...", total=None)
            
            try:
                sec_ops = SecurityOpsCenter()
                result = await sec_ops.comprehensive_security_audit(path)
                
                if report:
                    report_text = sec_ops.generate_security_report(result)
                    console.print(Panel(report_text, title="Security Report", border_style="yellow"))
                    
                    if output:
                        Path(output).write_text(report_text)
                        console.print(f"[green]✓[/green] Report saved to {output}")
                else:
                    console.print(Panel(str(result), title="Security Audit", border_style="yellow"))
                
                self.save_history(f"security: {path}", result)
                return result
            
            except Exception as e:
                console.print(f"[red]✗ Error:[/red] {str(e)}")
                self.save_history(f"security: {path}", None)
                return None
    
    def agents_command(self, json_output: bool = False, verbose: bool = False):
        """List all agents with options."""
        agents_data = {
            "Planners & Strategists": ["aurora", "sage", "felix", "ember"],
            "Critics & Reviewers": ["orion", "atlas", "mira", "vex"],
            "Specialists": ["sol", "echo", "nova", "quinn", "blaze", "ivy", "zephyr"],
            "Assistants": ["pixel", "script", "turbo", "sentinel"],
            "Special Agents": ["helix", "patch", "pulse", "link"]
        }
        
        if json_output:
            print(json.dumps(agents_data, indent=2))
            return
        
        tree = Tree("🤖 [bold cyan]All 23 AI Agents")
        
        for category, agents in agents_data.items():
            category_branch = tree.add(f"[bold yellow]{category}")
            for agent in agents:
                category_branch.add(f"[green]• {agent}")
        
        console.print(tree)
        
        if verbose:
            console.print("\n[bold]Agent Capabilities:[/bold]")
            console.print("• [cyan]aurora[/cyan]: Product management, strategic planning, roadmaps")
            console.print("• [cyan]sage[/cyan]: Architecture design, technical strategy, scalability")
            console.print("• [cyan]felix[/cyan]: Full-stack development, best practices, clean code")
            console.print("• [cyan]mira[/cyan]: Security engineering, threat modeling, AppSec")
            console.print("• [cyan]quinn[/cyan]: QA engineering, test automation, quality gates")
    
    async def status_command(self, watch: bool = False, json_output: bool = False):
        """System status with watch mode."""
        from agents.sentinel_agent import SentinelAgent
        from performance_optimizer import get_performance_monitor
        
        try:
            sentinel = SentinelAgent()
            monitor = get_performance_monitor()
            
            if watch:
                console.print("[yellow]Watch mode - Press Ctrl+C to exit[/yellow]")
                while True:
                    health = sentinel.get_system_health_report()
                    stats = monitor.get_stats()
                    
                    table = Table(title="System Status")
                    table.add_column("Metric", style="cyan")
                    table.add_column("Value", style="green")
                    
                    table.add_row("Health Score", f"{health.health_score:.1f}%")
                    table.add_row("CPU Usage", f"{health.metrics['cpu_percent']:.1f}%")
                    table.add_row("Memory Usage", f"{health.metrics['memory_percent']:.1f}%")
                    table.add_row("Disk Usage", f"{health.metrics['disk_percent']:.1f}%")
                    table.add_row("Cache Hits", str(stats['cache_hits']))
                    table.add_row("Cache Misses", str(stats['cache_misses']))
                    
                    console.clear()
                    console.print(table)
                    await asyncio.sleep(2)
            else:
                health = sentinel.get_system_health_report()
                
                if json_output:
                    print(json.dumps({
                        'health_score': health.health_score,
                        'metrics': health.metrics,
                        'alerts': [str(a) for a in health.alerts]
                    }, indent=2))
                else:
                    console.print(Panel(
                        sentinel.format_health_report(health),
                        title="System Health",
                        border_style="green"
                    ))
        
        except Exception as e:
            console.print(f"[red]✗ Error:[/red] {str(e)}")
    
    def config_command(self, key: Optional[str] = None, value: Optional[str] = None, 
                      list_config: bool = False):
        """Configuration management."""
        if list_config:
            table = Table(title="Configuration")
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="green")
            
            for k, v in self.config.items():
                table.add_row(k, str(v))
            
            console.print(table)
        
        elif key and value:
            self.config[key] = value
            self.save_config()
            console.print(f"[green]✓[/green] Set {key} = {value}")
        
        elif key:
            value = self.config.get(key, "Not set")
            console.print(f"[cyan]{key}[/cyan] = [green]{value}[/green]")
        
        else:
            console.print("[yellow]Usage:[/yellow] codeforge config [--list] [--set KEY=VALUE]")
    
    def history_command(self, limit: int = 10, json_output: bool = False):
        """Show command history."""
        recent = self.history[-limit:]
        
        if json_output:
            print(json.dumps(recent, indent=2))
        else:
            table = Table(title=f"Recent Commands (last {limit})")
            table.add_column("Time", style="cyan")
            table.add_column("Command", style="white")
            table.add_column("Status", style="green")
            
            for entry in recent:
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                status = "✓" if entry['success'] else "✗"
                table.add_row(timestamp, entry['command'], status)
            
            console.print(table)
    
    async def chat_command(self, agent: str, message: str):
        """Direct chat with an agent."""
        from agents.universal_agent_interface import UniversalAgent
        
        try:
            agent_obj = UniversalAgent(agent)
            response = agent_obj(message)
            
            console.print(Panel(response, title=f"💬 {agent}", border_style="blue"))
            self.save_history(f"chat {agent}: {message}", response)
            return response
        
        except Exception as e:
            console.print(f"[red]✗ Error:[/red] {str(e)}")
            return None
    
    def version_command(self):
        """Show version information."""
        console.print(f"[bold cyan]AI CodeForge CLI v{self.VERSION}[/bold cyan]")
        console.print("23 specialized agents • Enterprise-grade • Production-ready")
        console.print("https://github.com/MrNova420/ai-codeforge")


async def main():
    """Main CLI entry point with argument parsing."""
    cli = CodeForgeAdvancedCLI()
    
    parser = argparse.ArgumentParser(
        description="CodeForge Advanced CLI - AAA Production Development Team",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Code command
    code_parser = subparsers.add_parser('code', help='Generate code')
    code_parser.add_argument('task', help='Task description')
    code_parser.add_argument('--language', '-l', help='Programming language')
    code_parser.add_argument('--output', '-o', help='Output file')
    code_parser.add_argument('--agent', '-a', help='Specific agent to use')
    
    # Team command
    team_parser = subparsers.add_parser('team', help='Team collaboration')
    team_parser.add_argument('task', help='Task description')
    team_parser.add_argument('--mode', '-m', choices=['parallel', 'sequential', 'collaborative', 'autonomous'],
                           default='sequential', help='Work mode')
    team_parser.add_argument('--agents', '-a', nargs='+', help='Specific agents')
    
    # Security command
    security_parser = subparsers.add_parser('security', help='Security audit')
    security_parser.add_argument('path', help='Path to audit')
    security_parser.add_argument('--report', '-r', action='store_true', help='Generate full report')
    security_parser.add_argument('--output', '-o', help='Save report to file')
    
    # Agents command
    agents_parser = subparsers.add_parser('agents', help='List all agents')
    agents_parser.add_argument('--json', action='store_true', help='JSON output')
    agents_parser.add_argument('--verbose', '-v', action='store_true', help='Show details')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='System status')
    status_parser.add_argument('--watch', '-w', action='store_true', help='Watch mode')
    status_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configuration')
    config_parser.add_argument('--list', '-l', action='store_true', help='List all config')
    config_parser.add_argument('--set', '-s', help='Set config KEY=VALUE')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Command history')
    history_parser.add_argument('--limit', '-n', type=int, default=10, help='Number of entries')
    history_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Chat with agent')
    chat_parser.add_argument('agent', help='Agent name')
    chat_parser.add_argument('message', help='Message to agent')
    
    # Version command
    subparsers.add_parser('version', help='Show version')
    
    # Parse arguments
    if len(sys.argv) == 1:
        cli.print_banner()
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    # Execute commands
    if args.command == 'code':
        await cli.code_command(args.task, args.language, args.output, args.agent)
    
    elif args.command == 'team':
        await cli.team_command(args.task, args.mode, args.agents)
    
    elif args.command == 'security':
        await cli.security_command(args.path, args.report, args.output)
    
    elif args.command == 'agents':
        cli.agents_command(args.json, args.verbose)
    
    elif args.command == 'status':
        await cli.status_command(args.watch, args.json)
    
    elif args.command == 'config':
        if args.set:
            key, value = args.set.split('=', 1)
            cli.config_command(key, value)
        else:
            cli.config_command(list_config=args.list)
    
    elif args.command == 'history':
        cli.history_command(args.limit, args.json)
    
    elif args.command == 'chat':
        await cli.chat_command(args.agent, args.message)
    
    elif args.command == 'version':
        cli.version_command()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]✗ Fatal error:[/red] {str(e)}")
        sys.exit(1)
