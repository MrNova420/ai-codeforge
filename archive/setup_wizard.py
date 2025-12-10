#!/usr/bin/env python3
"""
Ultimate AI Dev Team - Interactive Setup Wizard
Makes setup so easy anyone can do it!
"""

import os
import sys
import yaml
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress

console = Console()

# Available models with details
MODELS = {
    # OpenAI Models (Paid)
    "gpt-4-turbo": {
        "provider": "openai",
        "quality": "⭐⭐⭐⭐⭐",
        "speed": "⭐⭐⭐⭐",
        "cost": "💰💰💰",
        "best_for": "All tasks, highest quality",
        "paid": True
    },
    "gpt-4": {
        "provider": "openai",
        "quality": "⭐⭐⭐⭐⭐",
        "speed": "⭐⭐⭐",
        "cost": "💰💰💰",
        "best_for": "Complex reasoning, code",
        "paid": True
    },
    "gpt-3.5-turbo": {
        "provider": "openai",
        "quality": "⭐⭐⭐⭐",
        "speed": "⭐⭐⭐⭐⭐",
        "cost": "💰",
        "best_for": "Fast responses, simple tasks",
        "paid": True
    },
    
    # Gemini Models (Free tier available)
    "gemini-pro": {
        "provider": "gemini",
        "quality": "⭐⭐⭐⭐",
        "speed": "⭐⭐⭐⭐",
        "cost": "💰 (Free tier)",
        "best_for": "General tasks, good quality",
        "paid": False
    },
    "gemini-ultra": {
        "provider": "gemini",
        "quality": "⭐⭐⭐⭐⭐",
        "speed": "⭐⭐⭐",
        "cost": "💰💰",
        "best_for": "Highest quality from Gemini",
        "paid": True
    },
    
    # Local Models (Free)
    "codellama:34b": {
        "provider": "local",
        "quality": "⭐⭐⭐⭐",
        "speed": "⭐⭐",
        "cost": "🆓",
        "best_for": "Coding, large context",
        "paid": False,
        "ram": "32GB+"
    },
    "codellama:13b": {
        "provider": "local",
        "quality": "⭐⭐⭐⭐",
        "speed": "⭐⭐⭐",
        "cost": "🆓",
        "best_for": "Coding, good balance",
        "paid": False,
        "ram": "16GB"
    },
    "codellama:7b": {
        "provider": "local",
        "quality": "⭐⭐⭐",
        "speed": "⭐⭐⭐⭐",
        "cost": "🆓",
        "best_for": "Coding, fast",
        "paid": False,
        "ram": "8GB"
    },
    "llama2:70b": {
        "provider": "local",
        "quality": "⭐⭐⭐⭐⭐",
        "speed": "⭐⭐",
        "cost": "🆓",
        "best_for": "Best local quality",
        "paid": False,
        "ram": "64GB+"
    },
    "llama2:13b": {
        "provider": "local",
        "quality": "⭐⭐⭐⭐",
        "speed": "⭐⭐⭐",
        "cost": "🆓",
        "best_for": "General, good balance",
        "paid": False,
        "ram": "16GB"
    },
    "llama2:7b": {
        "provider": "local",
        "quality": "⭐⭐⭐",
        "speed": "⭐⭐⭐⭐",
        "cost": "🆓",
        "best_for": "General, fast",
        "paid": False,
        "ram": "8GB"
    },
    "mistral:7b": {
        "provider": "local",
        "quality": "⭐⭐⭐",
        "speed": "⭐⭐⭐⭐⭐",
        "cost": "🆓",
        "best_for": "Very fast responses",
        "paid": False,
        "ram": "8GB"
    },
    "mixtral:8x7b": {
        "provider": "local",
        "quality": "⭐⭐⭐⭐",
        "speed": "⭐⭐⭐",
        "cost": "🆓",
        "best_for": "High quality, local",
        "paid": False,
        "ram": "32GB"
    },
    "deepseek-coder:33b": {
        "provider": "local",
        "quality": "⭐⭐⭐⭐⭐",
        "speed": "⭐⭐",
        "cost": "🆓",
        "best_for": "Advanced coding",
        "paid": False,
        "ram": "32GB"
    },
    "deepseek-coder:6.7b": {
        "provider": "local",
        "quality": "⭐⭐⭐",
        "speed": "⭐⭐⭐⭐",
        "cost": "🆓",
        "best_for": "Coding, efficient",
        "paid": False,
        "ram": "8GB"
    },
    "phind-codellama:34b": {
        "provider": "local",
        "quality": "⭐⭐⭐⭐",
        "speed": "⭐⭐",
        "cost": "🆓",
        "best_for": "Coding with reasoning",
        "paid": False,
        "ram": "32GB"
    },
    "wizardcoder:34b": {
        "provider": "local",
        "quality": "⭐⭐⭐⭐",
        "speed": "⭐⭐",
        "cost": "🆓",
        "best_for": "Python, coding",
        "paid": False,
        "ram": "32GB"
    },
    "starling-lm:7b": {
        "provider": "local",
        "quality": "⭐⭐⭐⭐",
        "speed": "⭐⭐⭐⭐",
        "cost": "🆓",
        "best_for": "Chat, helpful responses",
        "paid": False,
        "ram": "8GB"
    },
    "neural-chat:7b": {
        "provider": "local",
        "quality": "⭐⭐⭐",
        "speed": "⭐⭐⭐⭐",
        "cost": "🆓",
        "best_for": "Conversation",
        "paid": False,
        "ram": "8GB"
    },
    "openchat:7b": {
        "provider": "local",
        "quality": "⭐⭐⭐⭐",
        "speed": "⭐⭐⭐⭐",
        "cost": "🆓",
        "best_for": "Fast, quality chat",
        "paid": False,
        "ram": "8GB"
    },
    "zephyr:7b": {
        "provider": "local",
        "quality": "⭐⭐⭐",
        "speed": "⭐⭐⭐⭐⭐",
        "cost": "🆓",
        "best_for": "Fast, efficient",
        "paid": False,
        "ram": "8GB"
    },
}

# Agent roles
AGENTS = [
    ("helix", "Overseer", "Team Manager"),
    ("aurora", "Planner", "Visionary Strategist"),
    ("felix", "Planner", "Detail Architect"),
    ("sage", "Planner", "Research Maven"),
    ("ember", "Designer", "Creative Designer"),
    ("orion", "Planner", "Systems Planner"),
    ("atlas", "Critic", "The Perfectionist"),
    ("mira", "Critic", "Constructive Analyst"),
    ("vex", "Critic", "The Challenger"),
    ("sol", "Critic", "The Veteran"),
    ("echo", "Critic", "Data-Driven Judge"),
    ("nova", "Developer", "Lead Engineer"),
    ("quinn", "Developer", "Code Artisan"),
    ("blaze", "Developer", "Performance Guru"),
    ("ivy", "Developer", "Security Specialist"),
    ("zephyr", "Developer", "Integration Expert"),
    ("pixel", "Assistant", "Nova's Assistant"),
    ("script", "Assistant", "Quinn's Assistant"),
    ("turbo", "Assistant", "Blaze's Assistant"),
    ("sentinel", "Assistant", "Ivy's Assistant"),
    ("link", "Assistant", "Zephyr's Assistant"),
    ("patch", "Specialist", "The Fixer"),
    ("pulse", "Specialist", "The Tester"),
]


class SetupWizard:
    def __init__(self):
        self.config = {}
        self.config_path = Path("config.yaml")
        
    def run(self):
        """Run the complete setup wizard."""
        console.clear()
        self.show_welcome()
        
        # Step 1: Choose setup mode
        mode = self.choose_setup_mode()
        
        if mode == "quick":
            self.quick_setup()
        elif mode == "custom":
            self.custom_setup()
        elif mode == "free":
            self.free_setup()
        
        # Save configuration
        self.save_config()
        
        # Show completion
        self.show_completion()
    
    def show_welcome(self):
        """Show welcome screen."""
        console.print(Panel.fit(
            "[bold cyan]Ultimate AI Dev Team - Setup Wizard[/bold cyan]\n\n"
            "Welcome! This wizard will help you set up your AI development team.\n"
            "We'll configure 23 unique agents with the models you choose.\n\n"
            "[dim]This setup is designed to be so easy, anyone can do it![/dim]",
            border_style="cyan"
        ))
        console.print()
    
    def choose_setup_mode(self):
        """Let user choose setup mode."""
        console.print("[bold]Choose your setup mode:[/bold]\n")
        console.print("1. [green]Quick Setup[/green] - Best defaults, ready in 2 minutes")
        console.print("2. [cyan]Custom Setup[/cyan] - Choose models for each agent")
        console.print("3. [yellow]Free Setup[/yellow] - 100% free local models only")
        console.print()
        
        choice = Prompt.ask("Select mode", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            return "quick"
        elif choice == "2":
            return "custom"
        else:
            return "free"
    
    def quick_setup(self):
        """Quick setup with smart defaults."""
        console.print("\n[bold green]Quick Setup[/bold green]\n")
        
        # Ask what they have
        has_openai = Confirm.ask("Do you have an OpenAI API key?")
        has_gemini = Confirm.ask("Do you have a Gemini API key?")
        wants_local = Confirm.ask("Do you want to use free local models?")
        
        # Get API keys if they have them
        if has_openai:
            key = Prompt.ask("Enter your OpenAI API key", password=True)
            self.config['openai_api_key'] = key
            primary_model = "gpt-4"
        else:
            self.config['openai_api_key'] = ""
            
        if has_gemini:
            key = Prompt.ask("Enter your Gemini API key", password=True)
            self.config['gemini_api_key'] = key
            if not has_openai:
                primary_model = "gemini-pro"
        else:
            self.config['gemini_api_key'] = ""
        
        # Set up local if requested
        if wants_local:
            self.config['ollama_url'] = "http://localhost:11434"
            self.config['ollama_model'] = "codellama:7b"
            if not has_openai and not has_gemini:
                primary_model = "local"
        
        # Assign models to agents
        agent_models = {}
        for agent_name, role, desc in AGENTS:
            if has_openai:
                # Use GPT-4 for critical agents, GPT-3.5 for others
                if role in ["Overseer", "Developer"]:
                    agent_models[agent_name] = "gpt-4"
                else:
                    agent_models[agent_name] = "gpt-3.5-turbo"
            elif has_gemini:
                agent_models[agent_name] = "gemini-pro"
            elif wants_local:
                # Use codellama for coding, llama2 for others
                if role in ["Developer", "Specialist"]:
                    agent_models[agent_name] = "codellama:7b"
                else:
                    agent_models[agent_name] = "llama2:7b"
        
        self.config['agent_models'] = agent_models
        
        console.print("\n[green]✓ Configuration complete![/green]")
    
    def custom_setup(self):
        """Custom setup - choose model for each agent."""
        console.print("\n[bold cyan]Custom Setup[/bold cyan]\n")
        console.print("[dim]Choose models for each of your 23 agents[/dim]\n")
        
        # Get API keys first
        self.get_api_keys()
        
        # Show available models
        self.show_model_list()
        
        # Let user assign models to agents
        agent_models = {}
        
        console.print("\n[bold]Assign models to agents:[/bold]\n")
        console.print("[dim]You can assign the same model to multiple agents[/dim]\n")
        
        # Group agents by role for easier assignment
        use_groups = Confirm.ask("Assign models by role (faster)?", default=True)
        
        if use_groups:
            agent_models = self.assign_by_role()
        else:
            agent_models = self.assign_individually()
        
        self.config['agent_models'] = agent_models
        
    def free_setup(self):
        """Free setup - local models only."""
        console.print("\n[bold yellow]Free Setup - Local Models Only[/bold yellow]\n")
        console.print("[green]✓ No API keys needed![/green]")
        console.print("[green]✓ Completely free forever![/green]")
        console.print("[green]✓ 100% private![/green]\n")
        
        # Set empty API keys
        self.config['openai_api_key'] = ""
        self.config['gemini_api_key'] = ""
        self.config['ollama_url'] = "http://localhost:11434"
        
        # Show local models only
        console.print("[bold]Available FREE local models:[/bold]\n")
        
        local_models = {k: v for k, v in MODELS.items() if v['provider'] == 'local'}
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan")
        table.add_column("Model", style="green")
        table.add_column("Quality", style="yellow")
        table.add_column("Speed", style="blue")
        table.add_column("Best For", style="white")
        table.add_column("RAM", style="red")
        
        for idx, (name, details) in enumerate(local_models.items(), 1):
            table.add_row(
                str(idx),
                name,
                details['quality'],
                details['speed'],
                details['best_for'],
                details.get('ram', 'N/A')
            )
        
        console.print(table)
        console.print()
        
        # Choose default model
        console.print("\n[bold]Choose your default model:[/bold]")
        console.print("Recommendation: [cyan]codellama:7b[/cyan] (best for coding, 8GB RAM)")
        
        default_model = Prompt.ask("Enter model name", default="codellama:7b")
        self.config['ollama_model'] = default_model
        
        # Assign to all agents
        agent_models = {}
        for agent_name, role, desc in AGENTS:
            agent_models[agent_name] = default_model
        
        self.config['agent_models'] = agent_models
        
        console.print("\n[green]✓ All agents configured with free local models![/green]")
        
    def get_api_keys(self):
        """Get API keys from user."""
        console.print("[bold]API Keys (optional):[/bold]\n")
        
        if Confirm.ask("Add OpenAI API key?", default=False):
            key = Prompt.ask("OpenAI API key", password=True)
            self.config['openai_api_key'] = key
        else:
            self.config['openai_api_key'] = ""
        
        if Confirm.ask("Add Gemini API key?", default=False):
            key = Prompt.ask("Gemini API key", password=True)
            self.config['gemini_api_key'] = key
        else:
            self.config['gemini_api_key'] = ""
        
        if Confirm.ask("Use local models?", default=True):
            self.config['ollama_url'] = "http://localhost:11434"
            model = Prompt.ask("Default local model", default="codellama:7b")
            self.config['ollama_model'] = model
        
        console.print()
    
    def show_model_list(self):
        """Show all available models."""
        console.print("\n[bold]Available Models:[/bold]\n")
        
        # Paid models
        console.print("[bold red]PAID MODELS (Require API Key & Costs Money):[/bold red]")
        paid_table = Table(show_header=True)
        paid_table.add_column("#", style="cyan")
        paid_table.add_column("Model", style="green")
        paid_table.add_column("Quality", style="yellow")
        paid_table.add_column("Speed", style="blue")
        paid_table.add_column("Cost", style="red")
        paid_table.add_column("Best For", style="white")
        
        idx = 1
        for name, details in MODELS.items():
            if details['paid']:
                paid_table.add_row(
                    str(idx),
                    name,
                    details['quality'],
                    details['speed'],
                    details['cost'],
                    details['best_for']
                )
                idx += 1
        
        console.print(paid_table)
        console.print()
        
        # Free models
        console.print("[bold green]FREE MODELS (No Cost, Private, Local):[/bold green]")
        free_table = Table(show_header=True)
        free_table.add_column("#", style="cyan")
        free_table.add_column("Model", style="green")
        free_table.add_column("Quality", style="yellow")
        free_table.add_column("Speed", style="blue")
        free_table.add_column("Best For", style="white")
        free_table.add_column("RAM", style="magenta")
        
        for name, details in MODELS.items():
            if not details['paid']:
                free_table.add_row(
                    str(idx),
                    name,
                    details['quality'],
                    details['speed'],
                    details['best_for'],
                    details.get('ram', 'N/A')
                )
                idx += 1
        
        console.print(free_table)
        console.print()
    
    def assign_by_role(self):
        """Assign models by agent role."""
        agent_models = {}
        
        roles = {
            "Overseer": [],
            "Planner": [],
            "Designer": [],
            "Critic": [],
            "Developer": [],
            "Assistant": [],
            "Specialist": []
        }
        
        # Group agents by role
        for agent_name, role, desc in AGENTS:
            roles[role].append((agent_name, desc))
        
        # Assign model for each role
        for role, agents in roles.items():
            if not agents:
                continue
            
            console.print(f"\n[bold]{role}s:[/bold]")
            for agent_name, desc in agents:
                console.print(f"  • {agent_name.capitalize()} - {desc}")
            
            model = Prompt.ask(f"Model for {role}s", default="gpt-4")
            
            for agent_name, desc in agents:
                agent_models[agent_name] = model
        
        return agent_models
    
    def assign_individually(self):
        """Assign model to each agent individually."""
        agent_models = {}
        
        for agent_name, role, desc in AGENTS:
            console.print(f"\n[cyan]{agent_name.capitalize()}[/cyan] - {role} - {desc}")
            model = Prompt.ask("Model", default="gpt-4")
            agent_models[agent_name] = model
        
        return agent_models
    
    def save_config(self):
        """Save configuration to file."""
        console.print("\n[bold]Saving configuration...[/bold]")
        
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
        
        console.print("[green]✓ Configuration saved to config.yaml[/green]")
    
    def show_completion(self):
        """Show completion message."""
        console.print()
        console.print(Panel.fit(
            "[bold green]✓ Setup Complete![/bold green]\n\n"
            "Your AI Dev Team is ready to use!\n\n"
            "Next steps:\n"
            "1. Run: [cyan]python3 orchestrator.py[/cyan]\n"
            "2. Choose Team or Solo mode\n"
            "3. Start building amazing things!\n\n"
            "[dim]Your 23 agents are ready and waiting![/dim]",
            border_style="green"
        ))


def main():
    """Main entry point."""
    try:
        wizard = SetupWizard()
        wizard.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Setup cancelled.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
