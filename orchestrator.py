#!/usr/bin/env python3
"""
Ultimate AI Dev Team Orchestrator
Main entry point for managing and interacting with your AI development team.
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
from rich.markdown import Markdown
from prompts_utils import build_agent_system_prompt

# Import will be done dynamically to avoid circular imports
# from agent_chat import ChatInterface, TeamChat

# Initialize Rich console
console = Console()

# Paths
PROJECT_ROOT = Path(__file__).parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
CONFIG_TEMPLATE = PROJECT_ROOT / "config_template.yaml"
# Agent files are in archive/old_docs
AGENTS_DIR = PROJECT_ROOT / "archive" / "old_docs"

# Agent profile files
AGENT_FILES = {
    "planners": "planner_designer_agents.md",
    "critics": "critic_judge_agents.md",
    "developers": "developer_agents.md",
    "assistants": "developer_assistant_agents.md",
    "debugger": "debugger_fixer_agent.md",
    "tester": "tester_agent.md",
    "overseer": "overseer_agent.md",
}


class AgentProfile:
    """Represents an individual agent with their personality and capabilities."""
    
    def __init__(self, name: str, role: str, personality: str, strengths: str, approach: str, model: str = "openai"):
        self.name = name
        self.role = role
        self.personality = personality
        self.strengths = strengths
        self.approach = approach
        self.model = model
    
    def get_system_prompt(self) -> str:
        """Generate system prompt for this agent using shared utility."""
        return build_agent_system_prompt(
            agent_name=self.name,
            role=self.role,
            personality=self.personality,
            strengths=self.strengths,
            approach=self.approach
        )


class Config:
    """Handles configuration loading and management."""
    
    def __init__(self):
        self.data = {}
        self.load()
    
    def load(self):
        """Load config from file or create from template."""
        if not CONFIG_PATH.exists():
            if not CONFIG_TEMPLATE.exists():
                console.print("[red]Error: config_template.yaml not found![/red]")
                sys.exit(1)
            
            console.print("[yellow]No config.yaml found. Creating from template...[/yellow]")
            self._create_from_template()
        
        with open(CONFIG_PATH) as f:
            self.data = yaml.safe_load(f)
    
    def _create_from_template(self):
        """Interactive setup from template."""
        import shutil
        shutil.copy(CONFIG_TEMPLATE, CONFIG_PATH)
        
        console.print(Panel.fit("[bold]First-Time Setup[/bold]\nLet's configure your AI Dev Team!", 
                               border_style="green"))
        
        # Get API keys
        openai_key = Prompt.ask("Enter your OpenAI API key (or press Enter to skip)")
        gemini_key = Prompt.ask("Enter your Gemini API key (or press Enter to skip)")
        
        # Update config
        with open(CONFIG_PATH) as f:
            config = yaml.safe_load(f)
        
        if openai_key:
            config['openai_api_key'] = openai_key
        if gemini_key:
            config['gemini_api_key'] = gemini_key
        
        with open(CONFIG_PATH, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        console.print("[green]✓ Configuration saved![/green]")
    
    def get(self, key: str, default=None):
        """Get config value."""
        return self.data.get(key, default)
    
    def get_agent_model(self, agent_name: str) -> str:
        """Get model assignment for an agent."""
        agent_models = self.get('agent_models', {})
        return agent_models.get(agent_name, 'openai')


class AgentLoader:
    """Loads agent profiles from markdown files."""
    
    def __init__(self):
        self.agents: Dict[str, AgentProfile] = {}
        self.load_all_agents()
    
    def load_all_agents(self):
        """Load all agent profiles from markdown files."""
        for category, filename in AGENT_FILES.items():
            filepath = AGENTS_DIR / filename
            if filepath.exists():
                self._parse_agent_file(filepath, category)
    
    def _parse_agent_file(self, filepath: Path, category: str):
        """Parse markdown file and extract agent profiles."""
        with open(filepath) as f:
            content = f.read()
        
        # Simple parsing: split by ## headers
        sections = content.split('\n## ')
        for section in sections[1:]:  # Skip first (title)
            lines = section.strip().split('\n')
            if not lines:
                continue
            
            # Extract agent name from first line
            name_line = lines[0].strip()
            if '(' in name_line:
                name = name_line.split('(')[0].strip().split()[-1].lower()
                role = name_line.split('(')[1].split(')')[0]
            else:
                continue
            
            # Extract personality, strengths, approach
            personality = ""
            strengths = ""
            approach = ""
            
            for line in lines[1:]:
                if line.startswith('- **Personality:**'):
                    personality = line.replace('- **Personality:**', '').strip()
                elif line.startswith('- **Strengths:**'):
                    strengths = line.replace('- **Strengths:**', '').strip()
                elif line.startswith('- **Approach:**'):
                    approach = line.replace('- **Approach:**', '').strip()
            
            if name and personality:
                self.agents[name] = AgentProfile(name, role, personality, strengths, approach)
    
    def get_agent(self, name: str) -> Optional[AgentProfile]:
        """Get agent by name."""
        return self.agents.get(name.lower())
    
    def list_agents(self) -> List[str]:
        """Get list of all agent names."""
        return list(self.agents.keys())


class Orchestrator:
    """Main orchestrator for managing the AI dev team."""
    
    def __init__(self):
        self.config = Config()
        self.agent_loader = AgentLoader()
    
    def show_welcome(self):
        """Display welcome message."""
        console.print(Panel.fit(
            "[bold cyan]Ultimate AI Dev Team Orchestrator[/bold cyan]\n"
            "Manage your elite team of AI agents for high-end development",
            border_style="cyan"
        ))
    
    def show_agents(self):
        """Display all available agents."""
        table = Table(title="Available Agents", show_header=True, header_style="bold magenta")
        table.add_column("Name", style="cyan")
        table.add_column("Role", style="green")
        table.add_column("Personality", style="yellow")
        table.add_column("Model", style="blue")
        
        for name, agent in self.agent_loader.agents.items():
            model = self.config.get_agent_model(name)
            table.add_row(
                name.capitalize(),
                agent.role,
                agent.personality[:50] + "..." if len(agent.personality) > 50 else agent.personality,
                model
            )
        
        console.print(table)
    
    def main_menu(self):
        """Display main menu and handle user choice."""
        while True:
            console.print("\n[bold]Main Menu:[/bold]")
            console.print("1. Team Mode (Launch Helix Overseer)")
            console.print("2. Solo Agent Mode")
            console.print("3. View All Agents")
            console.print("4. Configure Settings")
            console.print("5. Exit")
            
            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                self.launch_team_mode()
            elif choice == "2":
                self.launch_solo_mode()
            elif choice == "3":
                self.show_agents()
            elif choice == "4":
                self.configure_settings()
            elif choice == "5":
                console.print("[yellow]Goodbye![/yellow]")
                break
    
    def launch_team_mode(self):
        """Launch team mode with Helix overseer."""
        
        console.print("\n[bold cyan]Team Mode[/bold cyan]")
        console.print("[yellow]Launching Helix (Overseer)...[/yellow]")
        
        helix = self.agent_loader.get_agent("helix")
        if not helix:
            console.print("[red]Error: Helix agent not found![/red]")
            return
        
        # Load all agents for team mode
        all_agents = [agent for agent in self.agent_loader.agents.values() if agent.name != "helix"]
        
        # Launch team chat
        team_chat = TeamChat(all_agents, self.config, helix)
        team_chat.run()
    
    def launch_solo_mode(self):
        """Launch individual agent."""
        
        console.print("\n[bold cyan]Solo Agent Mode[/bold cyan]")
        
        agents = self.agent_loader.list_agents()
        console.print("\nAvailable agents:")
        for i, name in enumerate(agents, 1):
            console.print(f"{i}. {name.capitalize()}")
        
        choice = Prompt.ask("Select agent number", default="1")
        try:
            agent_name = agents[int(choice) - 1]
        except (ValueError, IndexError):
            console.print("[red]Invalid selection[/red]")
            return
        
        agent = self.agent_loader.get_agent(agent_name)
        console.print(f"\n[green]Launching {agent.name.capitalize()}...[/green]")
        console.print(f"Model: {self.config.get_agent_model(agent.name)}")
        
        # Launch chat interface
        chat = ChatInterface(agent, self.config)
        chat.run()
    
    def configure_settings(self):
        """Configure settings interactively."""
        console.print("\n[bold cyan]Configuration[/bold cyan]")
        console.print(f"Config file: {CONFIG_PATH}")
        
        if Confirm.ask("Edit API keys?"):
            openai_key = Prompt.ask("OpenAI API key (press Enter to skip)")
            gemini_key = Prompt.ask("Gemini API key (press Enter to skip)")
            
            if openai_key:
                self.config.data['openai_api_key'] = openai_key
            if gemini_key:
                self.config.data['gemini_api_key'] = gemini_key
            
            with open(CONFIG_PATH, 'w') as f:
                yaml.dump(self.config.data, f, default_flow_style=False)
            
            console.print("[green]✓ Configuration updated![/green]")
        
        console.print("\nPress Enter to return to main menu")
        input()
    
    def run(self):
        """Main entry point."""
        self.show_welcome()
        self.main_menu()


def main():
    """Entry point for the orchestrator."""
    try:
        orchestrator = Orchestrator()
        orchestrator.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted. Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
