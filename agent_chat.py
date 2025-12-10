#!/usr/bin/env python3
"""
Agent Chat Interface
Handles real-time chat with AI agents using OpenAI, Gemini, or local models.
"""

import os
import sys
from typing import List, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live
from rich.table import Table

console = Console()


class Message:
    """Represents a chat message."""
    
    def __init__(self, role: str, content: str, agent_name: str = ""):
        self.role = role  # 'system', 'user', 'assistant'
        self.content = content
        self.agent_name = agent_name


class AgentChat:
    """Manages chat conversation with an AI agent."""
    
    def __init__(self, agent, config):
        self.agent = agent
        self.config = config
        self.messages: List[Message] = []
        
        # Get the actual model name (e.g., "gpt-4", "gemini-pro", "codellama:7b")
        self.model_name = config.get_agent_model(agent.name)
        
        # Determine provider type from model name
        if self.model_name.startswith("gpt-"):
            self.model_type = "openai"
        elif self.model_name.startswith("gemini-"):
            self.model_type = "gemini"
        elif ":" in self.model_name or self.model_name in ["llama2", "codellama", "mistral"]:
            self.model_type = "local"
        else:
            # Fallback for legacy config
            self.model_type = self.model_name
        
        # Initialize system prompt with agent's unique personality
        self.messages.append(Message("system", agent.get_system_prompt()))
    
    def send_message(self, content: str) -> str:
        """Send a message and get response."""
        # Add user message
        self.messages.append(Message("user", content))
        
        # Get response based on model type
        if self.model_type == "openai":
            response = self._openai_chat(content)
        elif self.model_type == "gemini":
            response = self._gemini_chat(content)
        elif self.model_type == "local":
            response = self._local_chat(content)
        else:
            response = f"Error: Unknown model type '{self.model_type}'"
        
        # Add assistant message
        self.messages.append(Message("assistant", response, self.agent.name))
        return response
    
    def _openai_chat(self, content: str) -> str:
        """Chat using OpenAI API."""
        try:
            import openai
            
            api_key = self.config.get('openai_api_key')
            if not api_key or api_key == "YOUR_OPENAI_API_KEY_HERE":
                return "Error: OpenAI API key not configured. Run setup to add your key."
            
            openai.api_key = api_key
            
            # Prepare messages for API
            api_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in self.messages
            ]
            
            # Use the specific model assigned to this agent
            model_to_use = self.model_name if self.model_name.startswith("gpt-") else "gpt-4"
            
            # Call API
            response = openai.ChatCompletion.create(
                model=model_to_use,
                messages=api_messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            return "Error: openai package not installed. Run: pip install openai"
        except Exception as e:
            return f"Error calling OpenAI API: {e}"
    
    def _gemini_chat(self, content: str) -> str:
        """Chat using Gemini API."""
        try:
            import google.generativeai as genai
            
            api_key = self.config.get('gemini_api_key')
            if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
                return "Error: Gemini API key not configured. Run setup to add your key."
            
            genai.configure(api_key=api_key)
            
            # Use the specific Gemini model assigned to this agent
            gemini_model = self.model_name if self.model_name.startswith("gemini-") else "gemini-pro"
            model = genai.GenerativeModel(gemini_model)
            
            # Build conversation context
            context = self.messages[0].content  # System prompt
            conversation = "\n\n".join([
                f"{msg.role.upper()}: {msg.content}"
                for msg in self.messages[1:]
            ])
            
            prompt = f"{context}\n\n{conversation}\n\nASSISTANT:"
            
            response = model.generate_content(prompt)
            return response.text
            
        except ImportError:
            return "Error: google-generativeai package not installed. Run: pip install google-generativeai"
        except Exception as e:
            return f"Error calling Gemini API: {e}"
    
    def _local_chat(self, content: str) -> str:
        """Chat using local model via Ollama."""
        try:
            import requests
            
            # Get Ollama configuration
            ollama_url = self.config.get('ollama_url', 'http://localhost:11434')
            
            # Use the specific local model assigned to this agent
            ollama_model = self.model_name
            
            # Build conversation context
            context = self.messages[0].content  # System prompt
            conversation = "\n\n".join([
                f"{'User' if msg.role == 'user' else 'Assistant'}: {msg.content}"
                for msg in self.messages[1:]
            ])
            
            prompt = f"{context}\n\n{conversation}\n\nAssistant:"
            
            # Call Ollama API
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": ollama_model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response from model')
            else:
                return f"Error: Ollama returned status {response.status_code}. Is Ollama running?"
                
        except requests.exceptions.ConnectionError:
            return ("❌ Cannot connect to Ollama!\n\n"
                   "To use free local models:\n"
                   "1. Install Ollama: https://ollama.ai\n"
                   "2. Start server: ollama serve\n"
                   f"3. Pull model: ollama pull {ollama_model}\n\n"
                   "Or use paid models:\n"
                   "  Run ./setup and add OpenAI or Gemini API key")
        except ImportError:
            return "Error: requests package not installed. Run: pip install requests"
        except Exception as e:
            return f"Error calling local model: {e}"
    
    def get_history(self) -> List[Message]:
        """Get chat history."""
        return self.messages[1:]  # Skip system prompt


class ChatInterface:
    """Terminal UI for chatting with agents."""
    
    def __init__(self, agent, config):
        self.agent_chat = AgentChat(agent, config)
        self.agent = agent
    
    def run(self):
        """Run the chat interface."""
        console.clear()
        
        # Display agent info
        console.print(Panel.fit(
            f"[bold cyan]{self.agent.name.capitalize()}[/bold cyan] - {self.agent.role}\n"
            f"[dim]{self.agent.personality}[/dim]",
            border_style="cyan"
        ))
        
        console.print("\n[dim]Type 'exit' or 'quit' to end the conversation[/dim]\n")
        
        # Chat loop
        while True:
            try:
                # Get user input
                user_input = Prompt.ask(f"[bold green]You[/bold green]")
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    console.print("[yellow]Ending conversation...[/yellow]")
                    break
                
                if not user_input.strip():
                    continue
                
                # Show thinking indicator
                with console.status(f"[cyan]{self.agent.name.capitalize()} is thinking...[/cyan]"):
                    response = self.agent_chat.send_message(user_input)
                
                # Display response
                console.print(f"\n[bold cyan]{self.agent.name.capitalize()}[/bold cyan]:")
                console.print(Panel(response, border_style="cyan"))
                console.print()
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Ending conversation...[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]\n")


class TeamChat:
    """Manages chat with multiple agents working together."""
    
    def __init__(self, agents: List, config, overseer):
        self.agents = {agent.name: AgentChat(agent, config) for agent in agents}
        self.overseer_chat = AgentChat(overseer, config)
        self.config = config
        self.overseer = overseer
    
    def run(self):
        """Run team chat interface."""
        console.clear()
        
        # Display team info
        console.print(Panel.fit(
            f"[bold cyan]Team Mode[/bold cyan] - {self.overseer.name.capitalize()} Overseer\n"
            f"Managing {len(self.agents)} agents",
            border_style="cyan"
        ))
        
        console.print("\n[dim]Available commands:[/dim]")
        console.print("[dim]  - 'agents' - List active agents[/dim]")
        console.print("[dim]  - 'status' - Get team status[/dim]")
        console.print("[dim]  - 'exit' or 'quit' - End session[/dim]\n")
        
        # Chat loop
        while True:
            try:
                user_input = Prompt.ask(f"[bold green]You[/bold green]")
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    console.print("[yellow]Ending team session...[/yellow]")
                    break
                
                if user_input.lower() == 'agents':
                    self._show_agents()
                    continue
                
                if user_input.lower() == 'status':
                    self._show_status()
                    continue
                
                if not user_input.strip():
                    continue
                
                # Send to overseer
                with console.status(f"[cyan]{self.overseer.name.capitalize()} is coordinating...[/cyan]"):
                    response = self.overseer_chat.send_message(user_input)
                
                # Display response
                console.print(f"\n[bold cyan]{self.overseer.name.capitalize()}[/bold cyan]:")
                console.print(Panel(response, border_style="cyan"))
                console.print()
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Ending session...[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]\n")
    
    def _show_agents(self):
        """Display active agents."""
        table = Table(title="Active Agents", show_header=True)
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="green")
        
        for name in self.agents:
            table.add_row(name.capitalize(), "Ready")
        
        console.print(table)
        console.print()
    
    def _show_status(self):
        """Show team status."""
        console.print(Panel(
            f"[green]Team Status: Active[/green]\n"
            f"Agents: {len(self.agents)}\n"
            f"Overseer: {self.overseer.name.capitalize()}",
            title="Status",
            border_style="green"
        ))
        console.print()
