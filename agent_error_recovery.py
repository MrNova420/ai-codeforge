#!/usr/bin/env python3
"""
Agent Error Recovery System - Handles agent failures gracefully
Provides automatic retry, fallback agents, and error logging
"""

import time
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ErrorSeverity(Enum):
    """Severity levels for errors."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AgentError:
    """Represents an agent error."""
    agent_name: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    timestamp: str
    task_description: str
    retry_count: int = 0
    resolved: bool = False
    resolution_method: Optional[str] = None


class AgentErrorRecovery:
    """
    Handles agent errors with automatic recovery strategies.
    
    Features:
    - Automatic retry with exponential backoff
    - Fallback to alternative agents
    - Error logging and reporting
    - Recovery statistics
    """
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        """
        Initialize error recovery system.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay for exponential backoff (seconds)
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.error_log: List[AgentError] = []
        self.recovery_stats = {
            'total_errors': 0,
            'recovered': 0,
            'failed': 0,
            'retries': 0,
            'fallbacks': 0
        }
        
        # Fallback agents for each specialty
        self.fallback_map = {
            'backend': ['felix', 'sol', 'nova'],
            'frontend': ['aurora', 'echo', 'pixel'],
            'testing': ['quinn', 'orion'],
            'security': ['mira', 'vex'],
            'design': ['pixel', 'aurora', 'ember'],
            'data': ['ivy', 'atlas'],
            'devops': ['nova', 'zephyr'],
            'documentation': ['script', 'echo']
        }
    
    async def execute_with_recovery(
        self,
        agent_chat,
        agent_name: str,
        task: str,
        specialty: Optional[str] = None,
        fallback_agents: Optional[List] = None
    ) -> Dict[str, Any]:
        """
        Execute agent task with automatic error recovery.
        
        Args:
            agent_chat: Agent chat instance
            agent_name: Name of the agent
            task: Task to execute
            specialty: Agent specialty for fallback selection
            fallback_agents: Optional list of fallback agent objects
        
        Returns:
            Dict with result and recovery info
        """
        last_error = None
        
        # Try primary agent with retries
        for attempt in range(self.max_retries):
            try:
                # Log attempt
                if attempt > 0:
                    self.recovery_stats['retries'] += 1
                
                # Execute
                result = agent_chat.send_message(task, stream=False)
                
                # Success!
                if attempt > 0:
                    # Mark previous error as resolved
                    self._mark_error_resolved(agent_name, 'retry_succeeded')
                    self.recovery_stats['recovered'] += 1
                
                return {
                    'success': True,
                    'result': result,
                    'agent': agent_name,
                    'attempts': attempt + 1,
                    'recovery_used': attempt > 0
                }
            
            except Exception as e:
                last_error = e
                self.recovery_stats['total_errors'] += 1
                
                # Log error
                error = AgentError(
                    agent_name=agent_name,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    severity=self._classify_error(e),
                    timestamp=datetime.now().isoformat(),
                    task_description=task[:100],
                    retry_count=attempt + 1
                )
                self.error_log.append(error)
                
                # Check if should retry
                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    delay = self.base_delay * (2 ** attempt)
                    await self._async_sleep(delay)
                    continue
                else:
                    # Max retries reached, try fallback
                    break
        
        # Try fallback agents
        if fallback_agents or specialty:
            fallback_list = fallback_agents or self._get_fallback_agents(
                agent_name, specialty
            )
            
            for fallback in fallback_list:
                if fallback == agent_name:
                    continue  # Skip the failed agent
                
                try:
                    self.recovery_stats['fallbacks'] += 1
                    
                    # Try fallback agent
                    result = fallback.send_message(task, stream=False)
                    
                    # Success with fallback!
                    self._mark_error_resolved(agent_name, f'fallback_to_{fallback.agent.name}')
                    self.recovery_stats['recovered'] += 1
                    
                    return {
                        'success': True,
                        'result': result,
                        'agent': fallback.agent.name,
                        'original_agent': agent_name,
                        'recovery_method': 'fallback',
                        'attempts': self.max_retries + 1
                    }
                
                except Exception as e:
                    # Fallback also failed, try next
                    self.recovery_stats['total_errors'] += 1
                    continue
        
        # All recovery attempts failed
        self.recovery_stats['failed'] += 1
        
        return {
            'success': False,
            'error': str(last_error),
            'agent': agent_name,
            'recovery_attempted': True,
            'attempts': self.max_retries + len(fallback_list if fallback_agents or specialty else [])
        }
    
    def _classify_error(self, error: Exception) -> ErrorSeverity:
        """Classify error severity."""
        error_str = str(error).lower()
        
        if any(word in error_str for word in ['timeout', 'connection', 'network']):
            return ErrorSeverity.MEDIUM
        elif any(word in error_str for word in ['api key', 'authentication', 'permission']):
            return ErrorSeverity.HIGH
        elif any(word in error_str for word in ['crash', 'fatal', 'critical']):
            return ErrorSeverity.CRITICAL
        else:
            return ErrorSeverity.LOW
    
    def _get_fallback_agents(
        self, 
        failed_agent: str, 
        specialty: Optional[str]
    ) -> List[str]:
        """Get fallback agent names for a specialty."""
        if specialty and specialty in self.fallback_map:
            agents = self.fallback_map[specialty].copy()
            # Remove failed agent from list
            if failed_agent in agents:
                agents.remove(failed_agent)
            return agents
        return []
    
    def _mark_error_resolved(self, agent_name: str, resolution_method: str):
        """Mark the most recent error for an agent as resolved."""
        for error in reversed(self.error_log):
            if error.agent_name == agent_name and not error.resolved:
                error.resolved = True
                error.resolution_method = resolution_method
                break
    
    async def _async_sleep(self, seconds: float):
        """Async sleep helper."""
        import asyncio
        await asyncio.sleep(seconds)
    
    def get_error_report(self) -> Dict[str, Any]:
        """Get comprehensive error report."""
        recent_errors = self.error_log[-20:]  # Last 20 errors
        
        return {
            'statistics': self.recovery_stats,
            'recent_errors': [
                {
                    'agent': e.agent_name,
                    'type': e.error_type,
                    'message': e.error_message,
                    'severity': e.severity.value,
                    'timestamp': e.timestamp,
                    'resolved': e.resolved,
                    'resolution': e.resolution_method,
                    'retry_count': e.retry_count
                }
                for e in recent_errors
            ],
            'unresolved_errors': [
                {
                    'agent': e.agent_name,
                    'type': e.error_type,
                    'severity': e.severity.value,
                    'timestamp': e.timestamp
                }
                for e in self.error_log
                if not e.resolved
            ]
        }
    
    def get_recovery_rate(self) -> float:
        """Calculate recovery success rate."""
        total = self.recovery_stats['total_errors']
        if total == 0:
            return 1.0
        return self.recovery_stats['recovered'] / total
    
    def clear_old_errors(self, hours: int = 24):
        """Clear errors older than specified hours."""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(hours=hours)
        self.error_log = [
            error for error in self.error_log
            if datetime.fromisoformat(error.timestamp) > cutoff
        ]


# Global instance
_recovery_instance = None


def get_error_recovery() -> AgentErrorRecovery:
    """Get or create error recovery instance."""
    global _recovery_instance
    if _recovery_instance is None:
        _recovery_instance = AgentErrorRecovery()
    return _recovery_instance
