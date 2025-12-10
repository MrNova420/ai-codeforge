#!/usr/bin/env python3
"""
Ultimate AI Dev Team Orchestrator V2
Enhanced with multi-agent collaboration, memory, file ops, and code execution
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.layout import Layout
from rich.text import Text

# Import existing components
from orchestrator import AgentProfile, AgentLoader, Config

# Import new components - ALL V3 Features
from collaboration_simple import SimpleCollaboration
from collaboration_enhanced import EnhancedCollaboration
from collaboration_v3 import CollaborationV3  # V3 with JSON and threading
from agent_chat_enhanced import EnhancedAgentChat
from memory_manager import MemoryManager
from file_manager import FileManager
from code_executor import CodeExecutor
import settings

# Import V3 Advanced Features
from researcher_agent import ResearcherAgent
from tools.registry import get_registry
try:
    from memory.vector_store import VectorMemoryStore
except (ImportError, ModuleNotFoundError):
    VectorMemoryStore = None  # Optional dependency
from codebase.graph_manager import CodebaseGraphManager
from codebase.query_engine import QueryEngine
from agents.specialized.self_correcting_agent import SelfCorrectingAgent

console = Console()

PROJECT_ROOT = Path(__file__).parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
STORAGE_DIR = PROJECT_ROOT / "storage"


class EnhancedOrchestrator:
    """Enhanced orchestrator with FULL V3 features - All advanced systems integrated."""
    
    def __init__(self):
        self.config = Config()
        self.agent_loader = AgentLoader()
        
        # Create workspace and storage
        WORKSPACE_DIR.mkdir(exist_ok=True)
        STORAGE_DIR.mkdir(exist_ok=True)
        
        # Store agent chats
        self.agent_chats = {}
        
        # Collaboration engine (initialized after agents loaded)
        self.collab_engine = None
        self.use_enhanced = settings.ENHANCED_COLLABORATION
        
        # V3 Advanced Features - Initialize once
        console.print("[dim]🔧 Initializing V3 Advanced Features...[/dim]")
        
        # Tool Registry
        self.tool_registry = get_registry()
        console.print("[dim]  ✓ Tool Registry[/dim]")
        
        # Vector Memory Store for long-term learning
        if VectorMemoryStore:
            try:
                self.vector_memory = VectorMemoryStore(persist_dir=str(STORAGE_DIR / "memory"))
                console.print("[dim]  ✓ Vector Memory (ChromaDB)[/dim]")
            except Exception as e:
                console.print(f"[dim]  ⚠ Vector Memory unavailable: {e}[/dim]")
                self.vector_memory = None
        else:
            console.print("[dim]  ⚠ Vector Memory unavailable (install chromadb)[/dim]")
            self.vector_memory = None
        
        # Codebase Graph for code analysis
        self.codebase_graph = None  # Initialized per-project
        
        # Researcher Agent for web search
        self.researcher = None  # Initialized when needed
        console.print("[dim]  ✓ Advanced features ready[/dim]\n")
    
    def show_welcome(self):
        """Display welcome screen with V3 features."""
        console.print(Panel.fit(
            "[bold cyan]🤖 AI CodeForge - V3 Full Stack[/bold cyan]\n\n"
            "✨ [bold]V3 Advanced Features Active:[/bold]\n"
            "  🤝 Collaboration V3 - JSON-based multi-agent\n"
            "  🧠 Vector Memory - ChromaDB learning system\n"
            "  🔍 Researcher Agent - Web search & synthesis\n"
            "  🛠️  Tool Registry - Extensible tool system\n"
            "  📊 Codebase Graph - AST-based code analysis\n"
            "  🔄 Self-Correction - Agents debug themselves\n"
            "  📁 File Operations - Smart file management\n"
            "  🔧 Code Execution - Safe sandbox\n"
            "  💾 Persistent Memory - Cross-session learning",
            border_style="cyan"
        ))
    
    def show_features(self):
        """Show all V3 features with details."""
        features = Table(title="✨ AI CodeForge V3 Features", show_header=True)
        features.add_column("Feature", style="cyan", width=25)
        features.add_column("Status", style="green", width=10)
        features.add_column("Description", style="white")
        
        # Core features
        features.add_row("🤝 Collaboration V3", "✅ Active", "JSON-based task delegation with parallel execution")
        features.add_row("🧠 Vector Memory", "✅ Active" if self.vector_memory else "⚠️  Install chromadb", "Persistent learning across sessions")
        features.add_row("🔍 Researcher Agent", "✅ Active", "Web search and knowledge synthesis")
        features.add_row("🛠️  Tool Registry", "✅ Active", f"{len(self.tool_registry.list_tools())} tools registered")
        features.add_row("📊 Codebase Graph", "⏳ On-demand", "AST-based code analysis (per-project)")
        features.add_row("🔄 Self-Correction", "✅ Active", "Agents debug and fix their own code")
        features.add_row("📁 File Operations", "✅ Active", "Smart file management in workspace")
        features.add_row("🔧 Code Execution", "✅ Active", "Safe sandbox for running code")
        features.add_row("💾 Memory Manager", "✅ Active", "Conversation persistence")
        features.add_row("👥 23 Agents", "✅ Active", "Specialized AI agents with unique skills")
        
        console.print(features)
        
        # Memory stats
        if self.vector_memory:
            console.print("\n[bold cyan]📊 Memory Statistics:[/bold cyan]")
            stats = self.vector_memory.get_memory_stats()
            for key, count in stats.items():
                if key != 'total':
                    console.print(f"  • {key}: {count} memories")
            console.print(f"  [bold]Total: {stats.get('total', 0)} memories[/bold]")
    
    def main_menu(self):
        """V3 Complete Main Menu - All Features Accessible."""
        while True:
            console.print("\n[bold cyan]═══ AI CodeForge V3 - Main Menu ═══[/bold cyan]")
            console.print("\n[bold]🤖 Agent Modes:[/bold]")
            console.print("  1. 🤝 Team Collaboration (Multi-agent with V3)")
            console.print("  2. 💬 Solo Agent Chat (Direct 1-on-1)")
            console.print("  3. 🔍 Research Mode (Web search & synthesis)")
            
            console.print("\n[bold]📊 Analysis & Tools:[/bold]")
            console.print("  4. 📈 Codebase Analysis (AST graph & queries)")
            console.print("  5. 🛠️  Tool Management (View/manage tools)")
            console.print("  6. 👥 View All Agents (23 specialists)")
            
            console.print("\n[bold]💾 Data & Config:[/bold]")
            console.print("  7. 🧠 Memory & Learning (Vector memory stats)")
            console.print("  8. 📁 Workspace Files (File browser)")
            console.print("  9. ⚙️  Configuration (Settings & presets)")
            
            console.print("\n[bold]ℹ️  Info:[/bold]")
            console.print("  10. ✨ V3 Features (Show all capabilities)")
            console.print("  11. 🚪 Exit")
            
            choice = Prompt.ask("Select option", choices=["1","2","3","4","5","6","7","8","9","10","11"])
            
            if choice == "1":
                self.launch_team_collaboration()
            elif choice == "2":
                self.launch_solo_mode()
            elif choice == "3":
                self.launch_research_mode()
            elif choice == "4":
                self.analyze_codebase()
            elif choice == "5":
                self.manage_tools()
            elif choice == "6":
                self.show_agents()
            elif choice == "7":
                self.manage_memory()
            elif choice == "8":
                self.browse_workspace()
            elif choice == "9":
                self.configure_settings()
            elif choice == "10":
                self.show_features()
            elif choice == "11":
                console.print("[yellow]✨ Goodbye from AI CodeForge V3![/yellow]")
                break
    
    def launch_team_collaboration(self):
        """Launch real multi-agent collaboration."""
        console.clear()
        console.print(Panel(
            "[bold cyan]Team Collaboration Mode[/bold cyan]\n"
            "Helix will analyze your request and delegate to the team",
            border_style="cyan"
        ))
        
        # Initialize agents for collaboration
        self._init_collaboration_agents()
        
        # Show team status
        self._show_team_status()
        
        console.print("\n[dim]Commands: 'agents', 'files', 'exit'[/dim]\n")
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]Your Request[/bold green]")
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    break
                
                if user_input.lower() == 'agents':
                    self.show_agents()
                    continue
                
                if user_input.lower() == 'files':
                    self._show_workspace_files()
                    continue
                
                if not user_input.strip():
                    continue
                
                # Get response from collaboration engine (V3 with JSON and threading!)
                response = self.collab_engine.handle_request(
                    user_input, 
                    timeout=settings.COLLABORATION_TIMEOUT
                )
                self.collab_engine.render_results(response)
            
            except KeyboardInterrupt:
                console.print("\n[yellow]Exiting collaboration mode...[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]")
    
    def _init_collaboration_agents(self):
        """Initialize agents for collaboration with ALL V3 features."""
        if self.agent_chats:
            return  # Already initialized
        
        console.print("[dim]🚀 Initializing agent team with V3 capabilities...[/dim]")
        
        # Create enhanced agent chats with V3 features
        file_manager = FileManager(WORKSPACE_DIR)
        code_executor = CodeExecutor(WORKSPACE_DIR)
        
        for name, agent in self.agent_loader.agents.items():
            agent_chat = EnhancedAgentChat(
                agent,
                self.config,
                file_manager=file_manager,
                code_executor=code_executor
            )
            
            # Wrap with self-correction if memory available
            if self.vector_memory:
                agent_chat = SelfCorrectingAgent(
                    agent_chat,
                    memory=self.vector_memory,
                    max_attempts=3
                )
            
            self.agent_chats[name] = agent_chat
        
        # Initialize Researcher Agent
        if 'helix' in self.agent_chats:
            self.researcher = ResearcherAgent(llm_agent=self.agent_chats['helix'])
            console.print("[dim]  ✓ Researcher Agent ready[/dim]")
        
        # Initialize collaboration engine - V3 with ALL features!
        # V3 has: JSON parsing, threading via AgentManager, parallel execution
        self.collab_engine = CollaborationV3(self.agent_chats)
        
        console.print("[dim]  ✓ Team collaboration V3 ready[/dim]")
        console.print("[green]✅ All V3 features active![/green]\n")
    
    def _show_team_status(self):
        """Show simple team status."""
        table = Table(title="Team Status")
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Current Task", style="yellow")
        
        for name in self.agent_chats.keys():
            table.add_row(name.capitalize(), "idle", "-")
        
        console.print(table)
    
    def launch_solo_mode(self):
        """Launch solo agent with streaming."""
        console.print("\n[bold cyan]Solo Agent Mode[/bold cyan]")
        
        agents = self.agent_loader.list_agents()
        console.print("\nAvailable agents:")
        for i, name in enumerate(agents, 1):
            console.print(f"{i}. {name.capitalize()}")
        
        choice = Prompt.ask("Select agent", default="1")
        try:
            agent_name = agents[int(choice) - 1]
        except (ValueError, IndexError):
            console.print("[red]Invalid selection[/red]")
            return
        
        agent = self.agent_loader.get_agent(agent_name)
        
        # Use enhanced chat with streaming
        enable_stream = Confirm.ask("Enable streaming responses?", default=True)
        enable_tools = Confirm.ask("Enable file/code tools?", default=True)
        
        # Create file and code managers if needed
        file_manager = FileManager(WORKSPACE_DIR) if enable_tools else None
        code_executor = CodeExecutor(WORKSPACE_DIR) if enable_tools else None
        
        agent_chat = EnhancedAgentChat(
            agent,
            self.config,
            file_manager=file_manager,
            code_executor=code_executor
        )
        
        console.clear()
        console.print(Panel(
            f"[bold cyan]{agent.name.capitalize()}[/bold cyan] - {agent.role}\n"
            f"[dim]{agent.personality}[/dim]\n\n"
            f"Streaming: {'✓' if enable_stream else '✗'} | Tools: {'✓' if enable_tools else '✗'}",
            border_style="cyan"
        ))
        
        console.print("\n[dim]Type 'exit' to end conversation[/dim]\n")
        
        while True:
            try:
                user_input = Prompt.ask(f"[bold green]You[/bold green]")
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    break
                
                if not user_input.strip():
                    continue
                
                # Show thinking or stream response
                console.print(f"\n[bold cyan]{agent.name.capitalize()}[/bold cyan]:")
                
                if enable_stream:
                    # Stream response
                    response_text = Text()
                    
                    def on_token(token: str):
                        response_text.append(token)
                        console.print(token, end="")
                    
                    response = agent_chat.send_message(user_input, stream=True, on_token=on_token)
                    console.print("\n")
                else:
                    # Non-streaming
                    with console.status(f"[cyan]{agent.name.capitalize()} thinking...[/cyan]"):
                        response = agent_chat.send_message(user_input, stream=False)
                    console.print(Panel(response, border_style="cyan"))
                
                console.print()
            
            except KeyboardInterrupt:
                console.print("\n[yellow]Ending conversation...[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]\n")
    
    def launch_research_mode(self):
        """Launch Research Mode - Web search and synthesis."""
        console.clear()
        console.print(Panel(
            "[bold cyan]🔍 Research Mode[/bold cyan]\n"
            "Ask anything - I'll search the web and synthesize findings",
            border_style="cyan"
        ))
        
        # Initialize researcher if not done
        if not self.researcher:
            self._init_collaboration_agents()
        
        if not self.researcher:
            console.print("[red]❌ Researcher not available[/red]")
            input("\nPress Enter to continue...")
            return
        
        console.print("\n[dim]Commands: 'exit' to return to main menu[/dim]\n")
        
        while True:
            try:
                query = Prompt.ask("\n[bold green]Research Query[/bold green]")
                
                if query.lower() in ['exit', 'quit', 'q']:
                    break
                
                if not query.strip():
                    continue
                
                # Perform research
                console.print("\n[cyan]🔍 Researching...[/cyan]")
                report = self.researcher.research(query, depth='normal')
                
                # Display formatted report
                console.print(Panel(
                    self.researcher.format_report_markdown(report),
                    title="[cyan]Research Report[/cyan]",
                    border_style="cyan"
                ))
                
                # Save to memory if available
                if self.vector_memory:
                    self.vector_memory.store_memory(
                        'task_summaries',
                        f"Research: {query}\n\nFindings: {report.summary}",
                        metadata={'type': 'research', 'query': query}
                    )
                    console.print("[dim]💾 Saved to memory[/dim]")
            
            except KeyboardInterrupt:
                console.print("\n[yellow]Exiting research mode...[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]")
    
    def analyze_codebase(self):
        """Analyze codebase with AST graph."""
        console.clear()
        console.print(Panel(
            "[bold cyan]📊 Codebase Analysis[/bold cyan]\n"
            "AST-based code analysis and queries",
            border_style="cyan"
        ))
        
        # Get project path
        project_path = Prompt.ask(
            "\n[bold]Project path to analyze[/bold]",
            default=str(WORKSPACE_DIR)
        )
        
        if not Path(project_path).exists():
            console.print(f"[red]❌ Path not found: {project_path}[/red]")
            input("\nPress Enter to continue...")
            return
        
        # Initialize codebase graph
        console.print("\n[cyan]🔄 Analyzing codebase...[/cyan]")
        try:
            self.codebase_graph = CodebaseGraphManager(project_root=project_path)
            query_engine = QueryEngine(self.codebase_graph)
            
            console.print("[green]✅ Analysis complete![/green]\n")
            
            # Show stats
            stats = Table(title="Codebase Statistics")
            stats.add_column("Metric", style="cyan")
            stats.add_column("Count", style="green")
            
            graph = self.codebase_graph.graph
            stats.add_row("Total Files", str(len([n for n in graph.nodes if graph.nodes[n].get('type') == 'file'])))
            stats.add_row("Classes", str(len([n for n in graph.nodes if graph.nodes[n].get('type') == 'class'])))
            stats.add_row("Functions", str(len([n for n in graph.nodes if graph.nodes[n].get('type') == 'function'])))
            
            console.print(stats)
            
            # Interactive queries
            console.print("\n[dim]Available queries: 'find CLASS', 'calls FUNC', 'impact CLASS', 'exit'[/dim]\n")
            
            while True:
                query = Prompt.ask("\n[bold green]Query[/bold green]")
                
                if query.lower() in ['exit', 'quit', 'q']:
                    break
                
                if query.lower().startswith('find '):
                    name = query[5:].strip()
                    results = query_engine.find_definition(name)
                    if results:
                        console.print(f"[green]Found: {results}[/green]")
                    else:
                        console.print(f"[yellow]Not found: {name}[/yellow]")
                
                elif query.lower().startswith('calls '):
                    func = query[6:].strip()
                    callers = query_engine.find_callers(func)
                    if callers:
                        console.print(f"[green]Called by: {', '.join(callers)}[/green]")
                    else:
                        console.print(f"[yellow]No callers found[/yellow]")
                
                elif query.lower().startswith('impact '):
                    name = query[7:].strip()
                    impact = query_engine.impact_of_changing(name)
                    console.print(f"[cyan]Impact: {len(impact)} items affected[/cyan]")
                    for item in impact[:10]:
                        console.print(f"  • {item}")
                
        except Exception as e:
            console.print(f"[red]❌ Analysis failed: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def manage_tools(self):
        """Manage and view available tools."""
        console.clear()
        console.print(Panel(
            "[bold cyan]🛠️  Tool Management[/bold cyan]\n"
            "View and manage available tools",
            border_style="cyan"
        ))
        
        # Show all tools
        tools = self.tool_registry.list_tools()
        
        table = Table(title=f"Available Tools ({len(tools)})")
        table.add_column("Tool Name", style="cyan")
        table.add_column("Type", style="yellow")
        table.add_column("Uses", style="green")
        
        for tool_name in tools:
            tool = self.tool_registry.get_tool(tool_name)
            if tool:
                stats = tool.get_stats()
                table.add_row(
                    tool_name,
                    tool.__class__.__name__,
                    str(stats.get('total_uses', 0))
                )
        
        console.print(table)
        
        # Show agent-tool assignments
        console.print("\n[bold cyan]Agent Tool Access:[/bold cyan]")
        console.print("[dim]Tools granted to specific agents:[/dim]\n")
        
        # This would show which agents have which tools
        # For now just show available
        console.print("[dim]All agents have access to file and execution tools[/dim]")
        
        input("\nPress Enter to continue...")
    
    def manage_memory(self):
        """Manage memory - both conversation history and vector memory."""
        console.clear()
        console.print(Panel(
            "[bold cyan]🧠 Memory & Learning System[/bold cyan]\n"
            "Conversation history and vector memory",
            border_style="cyan"
        ))
        
        # Show vector memory stats if available
        if self.vector_memory:
            console.print("\n[bold cyan]📊 Vector Memory Statistics:[/bold cyan]")
            stats = self.vector_memory.get_memory_stats()
            
            mem_table = Table(show_header=True)
            mem_table.add_column("Memory Type", style="cyan")
            mem_table.add_column("Count", style="green")
            
            for key, count in stats.items():
                if key != 'total':
                    mem_table.add_row(key.replace('_', ' ').title(), str(count))
            mem_table.add_row("[bold]Total Memories[/bold]", f"[bold]{stats.get('total', 0)}[/bold]")
            
            console.print(mem_table)
        else:
            console.print("\n[yellow]⚠️  Vector memory not available (install chromadb)[/yellow]")
        
        # Conversation sessions
        console.print("\n[bold cyan]💬 Conversation Sessions:[/bold cyan]")
        
        if not self.collab_engine:
            console.print("[dim]No sessions yet (start a collaboration first)[/dim]")
            input("\nPress Enter to continue...")
            return
        
        sessions = self.collab_engine.memory_manager.list_sessions()
        
        if not sessions:
            console.print("[yellow]No saved conversations yet.[/yellow]")
            input("\nPress Enter to continue...")
            return
        
        table = Table(title="Saved Conversations")
        table.add_column("#", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Messages", style="yellow")
        table.add_column("Last Updated", style="green")
        
        for i, session in enumerate(sessions[:20], 1):
            table.add_row(
                str(i),
                session['title'][:40],
                str(session['message_count']),
                session['updated_at'][:19]
            )
        
        console.print(table)
        
        choice = Prompt.ask("\nEnter # to view, 'delete' to remove, or Enter to go back", default="")
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(sessions):
                self._view_session(sessions[idx]['session_id'])
        elif choice.lower() == 'delete':
            del_choice = Prompt.ask("Enter # to delete")
            if del_choice.isdigit():
                idx = int(del_choice) - 1
                if 0 <= idx < len(sessions):
                    session_id = sessions[idx]['session_id']
                    if Confirm.ask(f"Delete conversation '{sessions[idx]['title']}'?"):
                        self.collab_engine.memory_manager.delete_session(session_id)
                        console.print("[green]Deleted![/green]")
    
    def _view_session(self, session_id: str):
        """View a conversation session."""
        session = self.collab_engine.memory_manager.load_session(session_id)
        if not session:
            console.print("[red]Session not found[/red]")
            return
        
        console.print(f"\n[bold]{session.title}[/bold]")
        console.print(f"[dim]{session.created_at}[/dim]\n")
        
        for msg in session.messages[-20:]:  # Show last 20 messages
            if msg.role == 'user':
                console.print(f"[bold green]You:[/bold green] {msg.content}")
            elif msg.role == 'assistant':
                agent_name = msg.agent_name or "Agent"
                console.print(f"\n[bold cyan]{agent_name.capitalize()}:[/bold cyan]")
                console.print(Panel(msg.content[:300] + ("..." if len(msg.content) > 300 else ""), 
                                  border_style="cyan"))
        
        input("\nPress Enter to continue...")
    
    def browse_workspace(self):
        """Browse workspace files."""
        console.print("\n[bold cyan]Workspace Files[/bold cyan]")
        console.print(f"Location: {WORKSPACE_DIR}\n")
        
        files = self.collab_engine.file_manager.list_files()
        
        if not files:
            console.print("[yellow]Workspace is empty.[/yellow]")
            
            if Confirm.ask("Create example project?"):
                self._create_example_project()
                files = self.collab_engine.file_manager.list_files()
        
        if files:
            for i, file_path in enumerate(files[:30], 1):
                console.print(f"{i}. {file_path}")
            
            choice = Prompt.ask("\nEnter # to view file, or Enter to go back", default="")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(files):
                    self._view_file(files[idx])
        
        input("\nPress Enter to continue...")
    
    def _view_file(self, file_path: str):
        """View a file."""
        content = self.collab_engine.file_manager.read_file(file_path)
        if content:
            console.print(f"\n[bold]{file_path}[/bold]")
            console.print(Panel(content, border_style="cyan"))
        else:
            console.print("[red]Could not read file[/red]")
    
    def _show_workspace_files(self):
        """Show workspace files inline."""
        files = self.collab_engine.file_manager.list_files()
        if files:
            console.print(f"\n[cyan]Workspace files:[/cyan] {', '.join(files[:10])}")
            if len(files) > 10:
                console.print(f"[dim]...and {len(files) - 10} more[/dim]")
        else:
            console.print("[yellow]Workspace is empty[/yellow]")
    
    def _create_example_project(self):
        """Create example project structure."""
        self.collab_engine.file_manager.write_file("example.py", """# Example Python file
def hello(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(hello("World"))
""")
        
        self.collab_engine.file_manager.write_file("README.md", """# Example Project

This is an example project created by the AI Dev Team.
""")
        
        console.print("[green]Created example project![/green]")
    
    def show_agents(self):
        """Show all agents."""
        table = Table(title="AI Development Team", show_header=True)
        table.add_column("Name", style="cyan")
        table.add_column("Role", style="green")
        table.add_column("Personality", style="yellow")
        table.add_column("Model", style="blue")
        
        for name, agent in self.agent_loader.agents.items():
            model = self.config.get_agent_model(name)
            table.add_row(
                name.capitalize(),
                agent.role,
                agent.personality[:40] + "..." if len(agent.personality) > 40 else agent.personality,
                model
            )
        
        console.print(table)
    
    def configure_settings(self):
        """Configure settings."""
        console.print("\n[bold cyan]⚙️  Configuration[/bold cyan]\n")
        
        # Show current configuration
        settings.print_config()
        
        console.print("\n[bold]Options:[/bold]")
        console.print("1. Switch preset (fast/balanced/thorough/minimal)")
        console.print("2. Toggle enhanced collaboration")
        console.print("3. Adjust timeouts")
        console.print("4. Run setup wizard")
        console.print("5. Back to main menu")
        
        choice = Prompt.ask("Select option", choices=["1","2","3","4","5"])
        
        if choice == "1":
            presets = settings.list_presets()
            console.print("\nAvailable presets:")
            for i, preset in enumerate(presets, 1):
                console.print(f"{i}. {preset}")
            
            preset_choice = Prompt.ask("Select preset", choices=[str(i) for i in range(1, len(presets)+1)])
            preset_name = presets[int(preset_choice)-1]
            settings.apply_preset(preset_name)
            self.use_enhanced = settings.ENHANCED_COLLABORATION
            console.print(f"\n✅ Applied '{preset_name}' preset!")
            
        elif choice == "2":
            settings.ENHANCED_COLLABORATION = not settings.ENHANCED_COLLABORATION
            self.use_enhanced = settings.ENHANCED_COLLABORATION
            mode = "Enhanced" if settings.ENHANCED_COLLABORATION else "Simple"
            console.print(f"\n✅ Collaboration mode: {mode}")
            
        elif choice == "3":
            console.print(f"\nCurrent timeouts:")
            console.print(f"  Collaboration: {settings.COLLABORATION_TIMEOUT}s")
            console.print(f"  Agent: {settings.AGENT_TIMEOUT}s")
            
            new_collab = Prompt.ask("New collaboration timeout (seconds)", 
                                   default=str(settings.COLLABORATION_TIMEOUT))
            new_agent = Prompt.ask("New agent timeout (seconds)", 
                                  default=str(settings.AGENT_TIMEOUT))
            
            settings.COLLABORATION_TIMEOUT = int(new_collab)
            settings.AGENT_TIMEOUT = int(new_agent)
            console.print("\n✅ Timeouts updated!")
            
        elif choice == "4":
            import subprocess
            subprocess.run([sys.executable, str(PROJECT_ROOT / "setup_proper.py")])
            self.config.load()  # Reload config
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main entry point."""
        self.show_welcome()
        self.main_menu()


def main():
    """Entry point."""
    try:
        orchestrator = EnhancedOrchestrator()
        orchestrator.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
