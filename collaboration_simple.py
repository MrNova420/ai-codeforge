#!/usr/bin/env python3
"""
Simple Collaboration Engine - Works, doesn't hang
Optimized for single model usage
"""

from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel

console = Console()


class SimpleCollaboration:
    """Simple collaboration without complex parsing."""
    
    def __init__(self, agent_chats: Dict):
        self.agent_chats = agent_chats
        self.overseer = agent_chats.get('helix')
    
    def handle_request(self, user_request: str, timeout: int = 30) -> str:
        """
        Handle user request - simple and direct.
        For single model setups, we keep it straightforward.
        """
        if not self.overseer:
            return "Error: Overseer (Helix) not available"
        
        # Simple prompt for overseer
        prompt = f"""User Request: {user_request}

As the overseer, provide a direct response. 

If this requires multiple agents:
- Briefly explain what needs to be done
- List which agents would handle each part
- Give a summary response

Keep it concise and helpful."""
        
        try:
            # Get overseer's response with timeout handling
            console.print("\n[cyan]Helix analyzing...[/cyan]")
            response = self.overseer.send_message(prompt, stream=False)
            return response
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def quick_delegate(self, agent_name: str, task: str) -> str:
        """Quickly delegate to a specific agent."""
        if agent_name not in self.agent_chats:
            return f"Agent {agent_name} not found"
        
        try:
            agent = self.agent_chats[agent_name]
            response = agent.send_message(task, stream=False)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
