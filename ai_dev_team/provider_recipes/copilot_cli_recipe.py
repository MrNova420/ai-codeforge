import shutil
import subprocess
import questionary
import sys

from .base_recipe import BaseRecipe

# --- Utility Functions ---
def print_info(message):
    print(f"\033[94m[INFO]\033[0m {message}")

def print_error(message):
    print(f"\033[91m[ERROR]\033[0m {message}", file=sys.stderr)

class CopilotCliRecipe(BaseRecipe):
    def get_name(self) -> str:
        return "GitHub Copilot CLI"

    def is_installed(self) -> bool:
        return shutil.which("gh") is not None

    def install(self):
        print_error("Automatic installation of the GitHub CLI ('gh') is not supported.")
        print_info("Please install it by following the instructions at: https://cli.github.com/")
        sys.exit(1)

    def is_authenticated(self) -> bool:
        try:
            subprocess.run(
                "gh auth status", 
                shell=True, check=True, capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def authenticate(self):
        print_info("Handing over to the official GitHub CLI login process...")
        try:
            return_code = subprocess.run("gh auth login", shell=True).returncode
            if return_code != 0:
                print_error("GitHub login failed. Please try again.")
                sys.exit(1)
        except Exception as e:
            print_error(f"An error occurred during authentication: {e}")
            sys.exit(1)

    def get_config(self) -> dict:
        """Asks for Copilot-specific configuration."""
        print_info("Configuring GitHub Copilot provider...")
        
        provider_name = questionary.text(
            "Enter a unique name for this provider:",
            default="copilot_cli_provider"
        ).ask()

        # This is the configuration that will be saved
        provider_config = {
            'name': provider_name,
            'type': 'copilot', # The provider type to load at runtime
            'command': 'gh copilot suggest -t shell' # The executable to call
        }
        return provider_config
