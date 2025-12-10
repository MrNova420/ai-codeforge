#!/usr/bin/env python3
"""
Configuration Manager - Centralized settings for entire project
Manages all configuration, preferences, and state for AI CodeForge

Features:
- User preferences and settings
- Project-specific configurations
- Agent customization
- Performance tuning
- Interface preferences (simple/advanced)
- Persistent state management
- Environment variables
- API keys and credentials (secure)
- Workspace management
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import yaml


@dataclass
class AgentConfig:
    """Configuration for individual agent."""
    name: str
    temperature: float = 0.7
    max_tokens: int = 2000
    personality: str = "professional"
    enabled: bool = True
    custom_instructions: Optional[str] = None


@dataclass
class InterfaceConfig:
    """UI/Interface preferences."""
    mode: str = "simple"  # simple, advanced, expert
    theme: str = "dark"  # dark, light, custom
    show_progress: bool = True
    show_thinking: bool = False
    verbose: bool = False
    output_format: str = "text"  # text, json, yaml, markdown
    auto_save: bool = True
    show_tips: bool = True


@dataclass
class PerformanceConfig:
    """Performance tuning."""
    enable_caching: bool = True
    cache_ttl: int = 3600  # seconds
    max_concurrent_agents: int = 5
    enable_parallel: bool = True
    fast_startup: bool = True
    preload_models: bool = True
    memory_limit_mb: int = 512


@dataclass
class SecurityConfig:
    """Security settings."""
    enable_docker_sandbox: bool = True
    network_isolation: bool = True
    read_only_filesystem: bool = True
    max_execution_time: int = 300  # seconds
    allowed_domains: List[str] = None
    scan_code: bool = True
    
    def __post_init__(self):
        if self.allowed_domains is None:
            self.allowed_domains = []


@dataclass
class WorkspaceConfig:
    """Workspace and project settings."""
    workspace_dir: str = "workspace"
    output_dir: str = "output"
    temp_dir: str = "temp"
    logs_dir: str = "logs"
    auto_create_dirs: bool = True
    git_enabled: bool = True
    default_branch: str = "main"


@dataclass
class ProjectConfig:
    """Complete project configuration."""
    version: str = "2.0.0"
    interface: InterfaceConfig = None
    performance: PerformanceConfig = None
    security: SecurityConfig = None
    workspace: WorkspaceConfig = None
    agents: Dict[str, AgentConfig] = None
    custom_settings: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.interface is None:
            self.interface = InterfaceConfig()
        if self.performance is None:
            self.performance = PerformanceConfig()
        if self.security is None:
            self.security = SecurityConfig()
        if self.workspace is None:
            self.workspace = WorkspaceConfig()
        if self.agents is None:
            self.agents = {}
        if self.custom_settings is None:
            self.custom_settings = {}


class ConfigurationManager:
    """Centralized configuration management for entire project."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration manager."""
        self.config_dir = config_dir or Path.home() / ".codeforge"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "config.json"
        self.agents_file = self.config_dir / "agents.json"
        self.state_file = self.config_dir / "state.json"
        self.env_file = self.config_dir / ".env"
        
        self.config = self.load_config()
        self.state = self.load_state()
    
    def load_config(self) -> ProjectConfig:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    data = json.load(f)
                
                # Reconstruct nested dataclasses
                config = ProjectConfig(
                    version=data.get('version', '2.0.0'),
                    interface=InterfaceConfig(**data.get('interface', {})),
                    performance=PerformanceConfig(**data.get('performance', {})),
                    security=SecurityConfig(**data.get('security', {})),
                    workspace=WorkspaceConfig(**data.get('workspace', {})),
                    agents={k: AgentConfig(**v) for k, v in data.get('agents', {}).items()},
                    custom_settings=data.get('custom_settings', {})
                )
                return config
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
        
        # Return default config
        return ProjectConfig()
    
    def save_config(self):
        """Save configuration to file."""
        try:
            # Convert to dict
            config_dict = {
                'version': self.config.version,
                'interface': asdict(self.config.interface),
                'performance': asdict(self.config.performance),
                'security': asdict(self.config.security),
                'workspace': asdict(self.config.workspace),
                'agents': {k: asdict(v) for k, v in self.config.agents.items()},
                'custom_settings': self.config.custom_settings,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_state(self) -> Dict[str, Any]:
        """Load application state."""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'last_used_agent': 'felix',
            'last_used_mode': 'sequential',
            'workspace_path': None,
            'recent_projects': [],
            'favorites': [],
            'statistics': {
                'total_tasks': 0,
                'successful_tasks': 0,
                'failed_tasks': 0,
                'agents_used': {}
            }
        }
    
    def save_state(self):
        """Save application state."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving state: {e}")
            return False
    
    # Interface Settings
    def set_interface_mode(self, mode: str):
        """Set interface mode (simple, advanced, expert)."""
        if mode in ['simple', 'advanced', 'expert']:
            self.config.interface.mode = mode
            self.save_config()
            return True
        return False
    
    def set_theme(self, theme: str):
        """Set UI theme."""
        self.config.interface.theme = theme
        self.save_config()
    
    def set_output_format(self, format: str):
        """Set output format (text, json, yaml, markdown)."""
        if format in ['text', 'json', 'yaml', 'markdown']:
            self.config.interface.output_format = format
            self.save_config()
            return True
        return False
    
    def toggle_verbose(self, enabled: Optional[bool] = None):
        """Toggle verbose mode."""
        if enabled is None:
            self.config.interface.verbose = not self.config.interface.verbose
        else:
            self.config.interface.verbose = enabled
        self.save_config()
    
    # Agent Configuration
    def configure_agent(self, agent_name: str, **kwargs):
        """Configure individual agent."""
        if agent_name not in self.config.agents:
            self.config.agents[agent_name] = AgentConfig(name=agent_name)
        
        agent = self.config.agents[agent_name]
        for key, value in kwargs.items():
            if hasattr(agent, key):
                setattr(agent, key, value)
        
        self.save_config()
    
    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """Get agent configuration."""
        if agent_name not in self.config.agents:
            self.config.agents[agent_name] = AgentConfig(name=agent_name)
        return self.config.agents[agent_name]
    
    def list_agents(self) -> List[str]:
        """List all configured agents."""
        return list(self.config.agents.keys())
    
    # Performance Settings
    def set_caching(self, enabled: bool):
        """Enable/disable caching."""
        self.config.performance.enable_caching = enabled
        self.save_config()
    
    def set_cache_ttl(self, seconds: int):
        """Set cache TTL."""
        self.config.performance.cache_ttl = seconds
        self.save_config()
    
    def set_max_concurrent(self, count: int):
        """Set max concurrent agents."""
        self.config.performance.max_concurrent_agents = count
        self.save_config()
    
    def toggle_fast_startup(self, enabled: Optional[bool] = None):
        """Toggle fast startup."""
        if enabled is None:
            self.config.performance.fast_startup = not self.config.performance.fast_startup
        else:
            self.config.performance.fast_startup = enabled
        self.save_config()
    
    # Security Settings
    def set_docker_sandbox(self, enabled: bool):
        """Enable/disable Docker sandboxing."""
        self.config.security.enable_docker_sandbox = enabled
        self.save_config()
    
    def set_network_isolation(self, enabled: bool):
        """Enable/disable network isolation."""
        self.config.security.network_isolation = enabled
        self.save_config()
    
    def set_max_execution_time(self, seconds: int):
        """Set max execution time."""
        self.config.security.max_execution_time = seconds
        self.save_config()
    
    def add_allowed_domain(self, domain: str):
        """Add allowed domain."""
        if domain not in self.config.security.allowed_domains:
            self.config.security.allowed_domains.append(domain)
            self.save_config()
    
    # Workspace Settings
    def set_workspace_dir(self, path: str):
        """Set workspace directory."""
        self.config.workspace.workspace_dir = path
        self.save_config()
    
    def set_output_dir(self, path: str):
        """Set output directory."""
        self.config.workspace.output_dir = path
        self.save_config()
    
    def create_workspace_dirs(self):
        """Create workspace directories."""
        if self.config.workspace.auto_create_dirs:
            for dir_attr in ['workspace_dir', 'output_dir', 'temp_dir', 'logs_dir']:
                dir_path = Path(getattr(self.config.workspace, dir_attr))
                dir_path.mkdir(parents=True, exist_ok=True)
    
    # Custom Settings
    def set_custom(self, key: str, value: Any):
        """Set custom setting."""
        self.config.custom_settings[key] = value
        self.save_config()
    
    def get_custom(self, key: str, default: Any = None) -> Any:
        """Get custom setting."""
        return self.config.custom_settings.get(key, default)
    
    # State Management
    def update_statistics(self, task_success: bool, agent_name: str):
        """Update usage statistics."""
        self.state['statistics']['total_tasks'] += 1
        
        if task_success:
            self.state['statistics']['successful_tasks'] += 1
        else:
            self.state['statistics']['failed_tasks'] += 1
        
        agents_used = self.state['statistics']['agents_used']
        agents_used[agent_name] = agents_used.get(agent_name, 0) + 1
        
        self.save_state()
    
    def add_recent_project(self, project_path: str):
        """Add to recent projects."""
        recent = self.state['recent_projects']
        if project_path in recent:
            recent.remove(project_path)
        recent.insert(0, project_path)
        self.state['recent_projects'] = recent[:10]  # Keep last 10
        self.save_state()
    
    def add_favorite(self, item: str):
        """Add to favorites."""
        if item not in self.state['favorites']:
            self.state['favorites'].append(item)
            self.save_state()
    
    # Export/Import
    def export_config(self, output_path: str, format: str = 'json'):
        """Export configuration."""
        config_dict = {
            'version': self.config.version,
            'interface': asdict(self.config.interface),
            'performance': asdict(self.config.performance),
            'security': asdict(self.config.security),
            'workspace': asdict(self.config.workspace),
            'agents': {k: asdict(v) for k, v in self.config.agents.items()},
            'custom_settings': self.config.custom_settings
        }
        
        output_file = Path(output_path)
        
        if format == 'yaml':
            with open(output_file, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False)
        else:  # json
            with open(output_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
        
        return True
    
    def import_config(self, input_path: str):
        """Import configuration."""
        input_file = Path(input_path)
        
        try:
            if input_file.suffix == '.yaml' or input_file.suffix == '.yml':
                with open(input_file) as f:
                    data = yaml.safe_load(f)
            else:  # json
                with open(input_file) as f:
                    data = json.load(f)
            
            # Reconstruct config
            self.config = ProjectConfig(
                version=data.get('version', '2.0.0'),
                interface=InterfaceConfig(**data.get('interface', {})),
                performance=PerformanceConfig(**data.get('performance', {})),
                security=SecurityConfig(**data.get('security', {})),
                workspace=WorkspaceConfig(**data.get('workspace', {})),
                agents={k: AgentConfig(**v) for k, v in data.get('agents', {}).items()},
                custom_settings=data.get('custom_settings', {})
            )
            
            self.save_config()
            return True
        
        except Exception as e:
            print(f"Error importing config: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.config = ProjectConfig()
        self.save_config()
        return True
    
    def get_summary(self) -> Dict[str, Any]:
        """Get configuration summary."""
        return {
            'version': self.config.version,
            'interface_mode': self.config.interface.mode,
            'theme': self.config.interface.theme,
            'caching_enabled': self.config.performance.enable_caching,
            'docker_sandbox': self.config.security.enable_docker_sandbox,
            'workspace': self.config.workspace.workspace_dir,
            'configured_agents': len(self.config.agents),
            'total_tasks': self.state['statistics']['total_tasks'],
            'success_rate': (
                self.state['statistics']['successful_tasks'] / 
                max(1, self.state['statistics']['total_tasks']) * 100
            )
        }


# Global instance
_config_manager = None


def get_config_manager() -> ConfigurationManager:
    """Get global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigurationManager()
    return _config_manager


# Convenience functions
def get_config() -> ProjectConfig:
    """Get current configuration."""
    return get_config_manager().config


def save_config():
    """Save current configuration."""
    return get_config_manager().save_config()


def reset_config():
    """Reset to default configuration."""
    return get_config_manager().reset_to_defaults()


if __name__ == '__main__':
    # CLI for configuration management
    import sys
    
    mgr = ConfigurationManager()
    
    if len(sys.argv) < 2:
        print("Configuration Manager - AI CodeForge")
        print("\nCurrent Configuration:")
        summary = mgr.get_summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'set':
        if len(sys.argv) < 4:
            print("Usage: config_manager.py set <key> <value>")
            sys.exit(1)
        
        key, value = sys.argv[2], sys.argv[3]
        mgr.set_custom(key, value)
        print(f"Set {key} = {value}")
    
    elif command == 'get':
        if len(sys.argv) < 3:
            print("Usage: config_manager.py get <key>")
            sys.exit(1)
        
        key = sys.argv[2]
        value = mgr.get_custom(key)
        print(f"{key} = {value}")
    
    elif command == 'reset':
        mgr.reset_to_defaults()
        print("Configuration reset to defaults")
    
    elif command == 'export':
        if len(sys.argv) < 3:
            print("Usage: config_manager.py export <file>")
            sys.exit(1)
        
        mgr.export_config(sys.argv[2])
        print(f"Configuration exported to {sys.argv[2]}")
    
    elif command == 'import':
        if len(sys.argv) < 3:
            print("Usage: config_manager.py import <file>")
            sys.exit(1)
        
        if mgr.import_config(sys.argv[2]):
            print(f"Configuration imported from {sys.argv[2]}")
        else:
            print("Failed to import configuration")
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: set, get, reset, export, import")
