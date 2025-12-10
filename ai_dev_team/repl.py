import questionary
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
import os
import subprocess
import sys

# --- Utility Functions ---
def print_info(message):
    print(f"\033[94m[INFO]\033[0m {message}")

def print_error(message):
    print(f"\033[91m[ERROR]\033[0m {message}", file=sys.stderr)

def print_success(message):
    print(f"\033[92m[SUCCESS]\033[0m {message}")

def print_agent_output(output):
    print(f"\033[36m{output}\033[0m") # Cyan for agent output

class REPL:
    def __init__(self, config, primary_agent_provider):
        self.config = config
        self.primary_agent = primary_agent_provider
        self.agents = self._load_tool_agents()
        self.session = PromptSession(history=FileHistory(os.path.join(".teamshell", ".chat_history")))

    def _load_tool_agents(self):
        """Loads, authenticates, and returns providers for all tool agents."""
        # Dynamically import the loader function to avoid circular import
        from .main import load_provider

        agents = {}
        providers_config = self.config.get('providers', [])
        tool_agents_config = self.config.get('agents', [])

        for agent_def in tool_agents_config:
            agent_name = agent_def['name']
            provider_name = agent_def['provider']
            
            provider_config = next((p for p in providers_config if p['name'] == provider_name), None)
            if not provider_config:
                print_error(f"Configuration error: Provider '{provider_name}' for agent '@{agent_name}' not found.")
                continue

            try:
                print_info(f"Initializing tool agent '@{agent_name}'...")
                provider_instance = load_provider(provider_config)
                agents[agent_name] = provider_instance
            except Exception as e:
                print_error(f"Failed to initialize agent '@{agent_name}': {e}")
        
        return agents

    def start(self):
        """Starts the main Read-Eval-Print-Loop."""
        project_goal = self.config.get('project_goal', 'No goal defined.')

        print_success("Welcome to your AI Dev Team!")
        print_info(f"Project Goal: {project_goal}")
        print_info("Type your message to chat with the planner.")
        print_info("Use '@<agent_name> <prompt>' to command an agent (e.g., '@coder create a flask app').")
        print_info("Available agents: " + ", ".join([f"@{name}" for name in self.agents.keys()]))
        print_info("Type 'exit' or 'quit' to end the session.")
        print("-" * 30)

        while True:
            try:
                user_input = self.session.prompt("(ai-team) > ")

                if user_input.lower() in ['exit', 'quit']:
                    print_info("Ending session. Goodbye!")
                    break
                
                if user_input.startswith('@'):
                    self.handle_agent_command(user_input)
                else:
                    print(f"\033[92mPlanner:\033[0m ", end="") # Print "Planner: " header
                    self.primary_agent.execute(user_input)
                
            except KeyboardInterrupt:
                print_info("\nUse 'exit' or 'quit' to end the session.")
            except EOFError:
                print_info("\nEnding session. Goodbye!")
                break

    def handle_agent_command(self, user_input):
        parts = user_input.split(' ', 1)
        agent_name = parts[0][1:]
        prompt = parts[1] if len(parts) > 1 else ""

        provider_instance = self.agents.get(agent_name)
        if not provider_instance:
            print_error(f"Agent '@{agent_name}' not found or failed to initialize.")
            return

        provider_instance.execute(prompt)
