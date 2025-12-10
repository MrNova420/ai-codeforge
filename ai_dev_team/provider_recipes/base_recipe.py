from abc import ABC, abstractmethod

class BaseRecipe(ABC):
    """
    Abstract base class for all Provider Recipes.
    A recipe knows how to install, configure, and authenticate a specific tool.
    """

    @abstractmethod
    def get_name(self) -> str:
        """Return the user-friendly name of the tool."""
        pass

    @abstractmethod
    def is_installed(self) -> bool:
        """Return True if the underlying CLI tool is installed."""
        pass

    @abstractmethod
    def install(self):
        """Run the installation process for the tool."""
        pass

    @abstractmethod
    def is_authenticated(self) -> bool:
        """Return True if the tool is already authenticated."""
        pass
    
    @abstractmethod
    def authenticate(self):
        """Run the authentication process for the tool."""
        pass

    @abstractmethod
    def get_config(self) -> dict:
        """
        Ask any tool-specific questions and return the configuration dictionary
        to be saved in the final .teamshell/config.yml file.
        """
        pass
