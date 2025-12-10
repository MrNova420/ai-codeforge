import os
import sys
import yaml
import questionary
import importlib
import pkgutil
import subprocess

from .repl import REPL
from .providers.gemini import GeminiProvider
from .providers.copilot import CopilotProvider
from . import provider_recipes

# --- Constants ---
TEAM_DIR = ".teamshell"
CONFIG_FILE_NAME = "config.yml"
CONFIG_FILE_PATH = os.path.join(TEAM_DIR, CONFIG_FILE_NAME)

# --- Utility Functions ---
def print_info(message): print(f"\033[94m[INFO]\033[0m {message}")
def print_success(message): print(f"\033[92m[SUCCESS]\033[0m {message}")
def print_error(message): print(f"\033[91m[ERROR]\033[0m {message}", file=sys.stderr)

# --- Provider Loading ---
def load_provider(provider_config):
    provider_type = provider_config.get('type')
    if provider_type == 'gemini': return GeminiProvider(provider_config)
    if provider_type == 'copilot': return CopilotProvider(provider_config)
    
    # A simple built-in shell provider
    if provider_type == 'shell':
        from .providers.base import BaseProvider
        class ShellProvider(BaseProvider):
            def authenticate(self): pass
            def execute(self, prompt, **kwargs):
                try:
                    subprocess.run(prompt, shell=True, check=True)
                except Exception as e:
                    print_error(f"Shell command failed: {e}")
        return ShellProvider(provider_config)
        
    raise ValueError(f"Unknown provider type: {provider_type}")

# --- Core Logic ---
def handle_init():
    """Simplified init. Creates a directory and a blank config."""
    if os.path.exists(TEAM_DIR):
        print_info("TeamShell directory already exists.")
    else:
        os.makedirs(TEAM_DIR)
        print_success(f"Created directory at '{TEAM_DIR}'.")
    
    if not os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'w') as f:
            yaml.dump({'project_goal': 'A new project.', 'providers': [], 'agents': []}, f)
        print_success(f"Created blank config at '{CONFIG_FILE_PATH}'.")
    
    print_info("\nNext Step: Run 'team setup' to configure your AI Dev Team.")

def handle_setup():
    """The new interactive wizard for building the team using recipes."""
    if not os.path.exists(CONFIG_FILE_PATH):
        print_error("Directory not initialized. Run 'team init' first.")
        sys.exit(1)

    print_info("Welcome to the AI Dev Team setup wizard!")
    
    # Dynamically load all recipes from the provider_recipes package
    recipes = []
    recipe_path = os.path.dirname(provider_recipes.__file__)
    for finder, name, ispkg in pkgutil.iter_modules([recipe_path]):
        if name.endswith('_recipe'):
            module = importlib.import_module(f'.{name}', 'ai_dev_team.provider_recipes')
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                # Ensure it's a class, a subclass of BaseRecipe, and not BaseRecipe itself
                if isinstance(attribute, type) and issubclass(attribute, provider_recipes.base_recipe.BaseRecipe) and attribute is not provider_recipes.base_recipe.BaseRecipe:
                    recipes.append(attribute())
    
    if not recipes:
        print_error("No provider recipes found in 'ai_dev_team/provider_recipes/'.")
        sys.exit(1)

    # Main setup loop
    while True:
        action = questionary.select("What would you like to do?", choices=["Add a new tool", "Exit"]).ask()
        if action is None or action == "Exit": break

        if action == "Add a new tool":
            recipe_choices = sorted([r.get_name() for r in recipes])
            chosen_recipe_name = questionary.select("Which tool do you want to add?", choices=recipe_choices).ask()
            if chosen_recipe_name is None: continue
            
            recipe = next(r for r in recipes if r.get_name() == chosen_recipe_name)

            # 1. Install
            if not recipe.is_installed():
                if questionary.confirm(f"'{recipe.get_name()}' is not installed. Attempt to guide installation?").ask():
                    recipe.install()
            
            # 2. Authenticate
            if not recipe.is_authenticated():
                if questionary.confirm(f"'{recipe.get_name()}' requires authentication. Proceed with login?").ask():
                    recipe.authenticate()
                else:
                    print_info(f"Skipping authentication for '{recipe.get_name()}'.")
                    continue
            
            # 3. Configure
            provider_config = recipe.get_config()
            agent_name = questionary.text("What '@' command do you want to use for this tool?", default=provider_config['name'].split('_')[0]).ask()
            if agent_name is None: continue

            with open(CONFIG_FILE_PATH, 'r') as f:
                config = yaml.safe_load(f)
            
            # Prevent duplicate providers
            if any(p['name'] == provider_config['name'] for p in config['providers']):
                print_info(f"Provider '{provider_config['name']}' is already configured.")
            else:
                config['providers'].append(provider_config)

            config.setdefault('agents', []).append({'name': agent_name, 'provider': provider_config['name']})
            
            with open(CONFIG_FILE_PATH, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            print_success(f"Successfully configured '@{agent_name}' to use '{provider_config['name']}'.")

    print_info("Setup complete. You can now use your configured team with 'team start'.")

def handle_start():
    if not os.path.exists(CONFIG_FILE_PATH):
        print_error("TeamShell not initialized. Run 'team init' or 'team setup' first.")
        sys.exit(1)
        
    with open(CONFIG_FILE_PATH, 'r') as f:
        config = yaml.safe_load(f)

    primary_agent_name = config.get('primary_agent')
    if not primary_agent_name:
        provider_names = [p['name'] for p in config.get('providers', [])]
        if not provider_names:
            print_error("No providers configured. Please run 'team setup'.")
            sys.exit(1)
        chosen_name = questionary.select("Which tool should be the primary conversational agent?", choices=provider_names).ask()
        if not chosen_name: sys.exit(0)
        config['primary_agent'] = chosen_name
        with open(CONFIG_FILE_PATH, 'w') as f: yaml.dump(config, f)
        primary_agent_name = chosen_name

    primary_agent_config = next((p for p in config['providers'] if p['name'] == primary_agent_name), None)
    if not primary_agent_config:
        print_error(f"Primary agent '{primary_agent_name}' not defined in providers. Run 'team setup'.")
        sys.exit(1)

    try:
        primary_agent_provider = load_provider(primary_agent_config)
    except Exception as e:
        print_error(f"Failed to initialize primary agent: {e}")
        sys.exit(1)
        
    repl = REPL(config, primary_agent_provider)
    repl.start()

def main():
    if len(sys.argv) < 2:
        print_error("Usage: team <init|setup|start>")
        sys.exit(1)

    command = sys.argv[1]
    if command == 'init': handle_init()
    elif command == 'setup': handle_setup()
    elif command == 'start': handle_start()
    else: print_error(f"Unknown command: '{command}'. Use 'init', 'setup', or 'start'.")

if __name__ == "__main__":
    main()
