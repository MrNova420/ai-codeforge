import sys
import subprocess

from .base import BaseProvider

def print_error(message):
    print(f"\033[91m[ERROR]\033[0m {message}", file=sys.stderr)

class GeminiProvider(BaseProvider):
    """
    Provider for the official Gemini CLI.
    It does not handle auth, it simply calls the 'gemini' executable.
    """
    def __init__(self, config):
        super().__init__(config)
        self.model_name = config.get('model')
        # The command can be customized if needed, but defaults to 'gemini'
        self.command = config.get('command', 'gemini')

    def authenticate(self):
        """
        This provider does not handle authentication.
        The 'gemini' CLI is expected to handle its own auth flow.
        """
        pass # Do nothing.

    def execute(self, prompt: str, **kwargs):
        """Executes the 'gemini' CLI with the given prompt."""
        cmd_args = [self.command]
        if self.model_name:
            # Note: The official CLI might use a different flag. Adjust if necessary.
            # This is an assumption based on common CLI design.
            cmd_args.extend(['--model', self.model_name])
        
        cmd_args.append(prompt)

        try:
            # We use Popen to stream the output in real-time
            process = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Stream stdout
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            # Check for errors after the process completes
            return_code = process.wait()
            if return_code != 0:
                stderr_output = process.stderr.read()
                print_error(f"'gemini' CLI failed:")
                print_error(stderr_output)

        except FileNotFoundError:
            print_error("The 'gemini' command was not found. Is the Gemini CLI installed and on your PATH?")
        except Exception as e:
            print_error(f"An error occurred while running the 'gemini' CLI: {e}")
