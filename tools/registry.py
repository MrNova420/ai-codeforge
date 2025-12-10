#!/usr/bin/env python3
"""
Tool Registry - Central tool management system
Implements tool registration and discovery from AGENT_ENHANCEMENT_STRATEGY.md
"""

from typing import Dict, List, Optional, Set
from .base_tool import BaseTool


class ToolRegistry:
    """
    Central registry for all available tools.
    
    Agents register tools they can use, and the system
    can dynamically grant/revoke tool access.
    """
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._agent_tools: Dict[str, Set[str]] = {}  # agent_name -> set of tool names
        
    def register_tool(self, tool: BaseTool) -> None:
        """Register a new tool."""
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool
        
    def unregister_tool(self, tool_name: str) -> None:
        """Unregister a tool."""
        if tool_name in self._tools:
            del self._tools[tool_name]
            # Remove from all agents
            for agent in self._agent_tools.values():
                agent.discard(tool_name)
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(tool_name)
    
    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
    
    def grant_tool_to_agent(self, agent_name: str, tool_name: str) -> bool:
        """
        Grant a tool to a specific agent.
        
        Returns True if successful, False if tool doesn't exist.
        """
        if tool_name not in self._tools:
            return False
        
        if agent_name not in self._agent_tools:
            self._agent_tools[agent_name] = set()
        
        self._agent_tools[agent_name].add(tool_name)
        return True
    
    def revoke_tool_from_agent(self, agent_name: str, tool_name: str) -> None:
        """Revoke a tool from an agent."""
        if agent_name in self._agent_tools:
            self._agent_tools[agent_name].discard(tool_name)
    
    def get_agent_tools(self, agent_name: str) -> List[BaseTool]:
        """Get all tools available to a specific agent."""
        if agent_name not in self._agent_tools:
            return []
        
        tool_names = self._agent_tools[agent_name]
        return [self._tools[name] for name in tool_names if name in self._tools]
    
    def get_agent_tool_schemas(self, agent_name: str) -> List[Dict]:
        """
        Get JSON schemas for all tools available to an agent.
        Useful for LLM function calling.
        """
        tools = self.get_agent_tools(agent_name)
        return [tool.to_json_schema() for tool in tools]
    
    def execute_tool(self, tool_name: str, agent_name: str, **kwargs):
        """
        Execute a tool on behalf of an agent.
        Checks if agent has permission.
        """
        # Check if agent has access
        if agent_name in self._agent_tools:
            if tool_name not in self._agent_tools[agent_name]:
                return {
                    'success': False,
                    'error': f"Agent '{agent_name}' does not have access to tool '{tool_name}'"
                }
        
        # Get tool
        tool = self.get_tool(tool_name)
        if not tool:
            return {
                'success': False,
                'error': f"Tool '{tool_name}' not found"
            }
        
        # Execute
        return tool(**kwargs)
    
    def get_all_stats(self) -> Dict[str, Dict]:
        """Get usage statistics for all tools."""
        return {
            name: tool.get_stats()
            for name, tool in self._tools.items()
        }
    
    def preset_agent_tools(self, agent_name: str, agent_type: str) -> None:
        """
        Grant preset tools based on agent type.
        
        Implements the "role specialization" concept from the plans.
        """
        presets = {
            'developer': [
                'read_file', 'write_file', 'list_directory',
                'execute_code', 'run_tests', 'search_codebase'
            ],
            'researcher': [
                'web_search', 'read_webpage', 'extract_code_examples'
            ],
            'qa': [
                'run_tests', 'generate_test_cases', 'code_coverage'
            ],
            'architect': [
                'analyze_dependencies', 'find_callers', 'generate_diagram'
            ],
            'devops': [
                'deploy_app', 'check_status', 'view_logs', 'scale_resources'
            ]
        }
        
        tools_to_grant = presets.get(agent_type, [])
        for tool_name in tools_to_grant:
            if tool_name in self._tools:
                self.grant_tool_to_agent(agent_name, tool_name)


# Global registry instance
_global_registry = None


def get_registry() -> ToolRegistry:
    """Get the global tool registry (singleton)."""
    global _global_registry
    if _global_registry is None:
        _global_registry = ToolRegistry()
    return _global_registry
