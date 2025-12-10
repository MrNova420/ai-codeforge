import sys
import subprocess
import shutil
import questionary

from .base import BaseProvider

# --- Utility Functions ---
def print_info(message):
    print(f"\033[94m[INFO]\033[0m {message}")

def print_error(message):
    print(f"\033[91m[ERROR]\033[0m {message}", file=sys.stderr)

class CopilotProvider(BaseProvider):
    """
    Provider for GitHub Copilot CLI.
    Handles authentication by checking and calling the `gh` CLI.
    """
    def __init__(self, config):
        super().__init__(config)
        self.command = config.get('command', 'gh copilot suggest -t shell')

    def _is_gh_installed(self):
        return shutil.which("gh") is not None

    def _is_gh_authenticated(self):
        try:
            # We check the status. If it fails, user is not logged in.
            result = subprocess.run("gh auth status", shell=True, check=True, capture_output=True, text=True)
            return "Logged in to github.com" in result.stderr
        except subprocess.CalledProcessError:
            return False

    def authenticate(self):
        """
        This provider does not handle authentication.
        The 'gh' CLI is expected to handle its own auth flow.
        """
        pass # Do nothing.

    def execute(self, prompt: str, **kwargs):
        """
        Executes the `gh copilot` command with the given prompt.
        """
        full_command = f"{self.command} \"{prompt}\""
        print_info(f"Executing Copilot: {full_command}")
        
        try:
            # We stream the output for a better user experience
            with subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1) as proc:
                for line in proc.stdout:
                    print(f"\033[36m{line.strip()}\033[0m")
                
                proc.wait()
                if proc.returncode != 0:
                    print_error(f"Copilot command failed:")
                    for line in proc.stderr:
                        print_error(line.strip())
        except Exception as e:
            print_error(f"Failed to execute Copilot command: {e}")

