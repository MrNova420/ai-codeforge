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

class GeminiCliRecipe(BaseRecipe):
    def get_name(self) -> str:
        return "Gemini CLI (Official)"

    def is_installed(self) -> bool:
        # The gemini cli is installed as part of gcloud
        return shutil.which("gcloud") is not None

    def install(self):
        print_error("Automatic installation of the Google Cloud SDK is not supported.")
        print_info("Please install it by following the instructions at: https://cloud.google.com/sdk/docs/install")
        sys.exit(1)

    def is_authenticated(self) -> bool:
        try:
            # A simple way to check is to try printing the token
            # If it fails, the user is likely not logged in.
            subprocess.run(
                "gcloud auth application-default print-access-token", 
                shell=True, check=True, capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def authenticate(self):
        print_info("Handing over to the official Google Cloud login process...")
        try:
            # Use os.system to give the process full control of the terminal
            return_code = subprocess.run("gcloud auth application-default login", shell=True).returncode
            if return_code != 0:
                print_error("Google Cloud login failed. Please try again.")
                sys.exit(1)
        except Exception as e:
            print_error(f"An error occurred during authentication: {e}")
            sys.exit(1)

    def get_config(self) -> dict:
        """Asks for Gemini-specific configuration."""
        print_info("Configuring Gemini CLI provider...")
        
        provider_name = questionary.text(
            "Enter a unique name for this provider:",
            default="gemini_cli_provider"
        ).ask()
        
        model = questionary.text(
            "Which Gemini model do you want to use?",
            default="gemini-pro"
        ).ask()

        # This is the configuration that will be saved
        provider_config = {
            'name': provider_name,
            'type': 'gemini', # The provider type to load at runtime
            'command': 'gemini', # The executable to call
            'model': model
        }
        return provider_config

