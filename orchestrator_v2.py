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

# Import new components
from collaboration_simple import SimpleCollaboration
from collaboration_enhanced import EnhancedCollaboration
from collaboration_v3 import CollaborationV3  # NEW: V3 with JSON and threading
from agent_chat_enhanced import EnhancedAgentChat
from memory_manager import MemoryManager
from file_manager import FileManager
from code_executor import CodeExecutor
import settings

console = Console()

PROJECT_ROOT = Path(__file__).parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
STORAGE_DIR = PROJECT_ROOT / "storage"


class EnhancedOrchestrator:
    """Enhanced orchestrator with full collaboration features."""
    
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
    
    def show_welcome(self):
        """Display welcome screen."""
        console.print(Panel.fit(
            "[bold cyan]Ultimate AI Dev Team Orchestrator V2[/bold cyan]\n"
            "✨ Enhanced with Multi-Agent Collaboration\n"
            "📁 File Operations | 🔧 Code Execution | 💾 Persistent Memory",
            border_style="cyan"
        ))
    
    def show_features(self):
        """Show new features."""
        features = Table(title="✨ New Features", show_header=False)
        features.add_column("Feature", style="cyan")
        features.add_column("Description", style="white")
        
        features.add_row("🤝 Real Collaboration", "Agents actually work together on tasks")
        features.add_row("💾 Memory", "Conversations saved across sessions")
        features.add_row("📁 File Operations", "Agents can read/write code files")
        features.add_row("🔧 Code Execution", "Safe sandbox for running code")
        features.add_row("⚡ Streaming", "See responses in real-time")
        features.add_row("📊 Progress Tracking", "Visual dashboard of team activity")
        
        console.print(features)
    
    def main_menu(self):
        """Enhanced main menu."""
        while True:
            console.print("\n[bold]Main Menu:[/bold]")
            console.print("1. 🤝 Team Collaboration Mode (Real multi-agent)")
            console.print("2. 💬 Solo Agent Chat")
            console.print("3. 👥 View All Agents")
            console.print("4. 💾 Memory & History")
            console.print("5. 📁 Workspace Files")
            console.print("6. ⚙️  Configuration")
            console.print("7. ✨ About New Features")
            console.print("8. 🚪 Exit")
            
            choice = Prompt.ask("Select option", choices=["1","2","3","4","5","6","7","8"])
            
            if choice == "1":
                self.launch_team_collaboration()
            elif choice == "2":
                self.launch_solo_mode()
            elif choice == "3":
                self.show_agents()
            elif choice == "4":
                self.manage_memory()
            elif choice == "5":
                self.browse_workspace()
            elif choice == "6":
                self.configure_settings()
            elif choice == "7":
                self.show_features()
            elif choice == "8":
                console.print("[yellow]Goodbye![/yellow]")
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
        """Initialize agents for collaboration."""
        if self.agent_chats:
            return  # Already initialized
        
        # Create enhanced agent chats
        file_manager = FileManager(WORKSPACE_DIR)
        code_executor = CodeExecutor(WORKSPACE_DIR)
        
        for name, agent in self.agent_loader.agents.items():
            agent_chat = EnhancedAgentChat(
                agent,
                self.config,
                file_manager=file_manager,
                code_executor=code_executor
            )
            self.agent_chats[name] = agent_chat
        
        # Initialize collaboration engine - USE V3!
        # V3 has JSON parsing, threading via AgentManager, and parallel execution
        self.collab_engine = CollaborationV3(self.agent_chats)
        
        # Keep old option for fallback
        self.use_legacy = False  # Set to True to use old enhanced mode
    
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
    
    def manage_memory(self):
        """Manage conversation memory."""
        console.print("\n[bold cyan]Memory & History[/bold cyan]")
        
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
