#!/usr/bin/env python3
"""
Base Tool - Standard interface for all agent tools
Implements the Tool-Use framework from AGENT_ENHANCEMENT_STRATEGY.md
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime


@dataclass
class ToolResult:
    """Result from tool execution."""
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class BaseTool(ABC):
    """
    Abstract base class for all agent tools.
    
    Every tool must implement:
    - name: Unique identifier
    - description: What the tool does
    - parameters: Expected input schema
    - execute: The actual tool logic
    """
    
    def __init__(self):
        self.call_count = 0
        self.success_count = 0
        self.error_count = 0
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name (e.g., 'web_search', 'read_file')."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what this tool does."""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON Schema describing the tool's parameters."""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters."""
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate parameters against schema."""
        schema = self.parameters
        required = schema.get('required', [])
        
        # Check required parameters
        for param in required:
            if param not in params:
                return False
        
        return True
    
    def __call__(self, **kwargs) -> ToolResult:
        """Callable interface with validation and stats."""
        self.call_count += 1
        
        if not self.validate_params(kwargs):
            self.error_count += 1
            return ToolResult(
                success=False,
                data=None,
                error=f"Invalid parameters for tool '{self.name}'"
            )
        
        try:
            result = self.execute(**kwargs)
            if result.success:
                self.success_count += 1
            else:
                self.error_count += 1
            return result
        except Exception as e:
            self.error_count += 1
            return ToolResult(
                success=False,
                data=None,
                error=f"Tool execution error: {str(e)}"
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tool usage statistics."""
        return {
            'total_calls': self.call_count,
            'successes': self.success_count,
            'errors': self.error_count,
            'success_rate': self.success_count / self.call_count if self.call_count > 0 else 0
        }
    
    def to_json_schema(self) -> Dict[str, Any]:
        """Export tool as JSON schema for LLM function calling."""
        return {
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters
        }
