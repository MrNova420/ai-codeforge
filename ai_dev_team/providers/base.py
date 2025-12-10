from abc import ABC, abstractmethod

class BaseProvider(ABC):
    """
    Abstract base class for all providers.
    A provider is a backend service like an AI model or a shell executor.
    """
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def authenticate(self):
        """
        Handles the authentication for the provider.
        This method should be idempotent.
        If authentication is missing, it should guide the user through setup.
        """
        pass

    @abstractmethod
    def execute(self, prompt: str, **kwargs):
        """
        Executes a command or sends a prompt to the provider.
        """
        pass
