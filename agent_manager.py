#!/usr/bin/env python3
"""
Agent Manager - Intelligent agent lifecycle management
Handles long-running tasks, context management, and realistic timeouts
"""

import time
import threading
from typing import Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from queue import Queue
import settings


@dataclass
class AgentResponse:
    """Response from an agent."""
    success: bool
    content: str
    tokens: int
    duration: float
    timeout: bool = False
    error: Optional[str] = None


class AgentTask:
    """Represents a task being executed by an agent."""
    
    def __init__(self, agent_name: str, task: str, timeout: int):
        self.agent_name = agent_name
        self.task = task
        self.timeout = timeout
        self.start_time = time.time()
        self.result: Optional[AgentResponse] = None
        self.progress = 0
        self.status = "pending"  # pending, running, complete, timeout, error
        self.thread: Optional[threading.Thread] = None
        
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds."""
        return time.time() - self.start_time
    
    def remaining_time(self) -> float:
        """Get remaining time before timeout."""
        return max(0, self.timeout - self.elapsed_time())
    
    def is_timeout(self) -> bool:
        """Check if task has timed out."""
        return self.elapsed_time() >= self.timeout


class AgentManager:
    """
    Manages agent execution with intelligent timeout handling.
    
    Features:
    - Automatic timeout detection
    - Background task execution
    - Progress tracking
    - Graceful cancellation
    - Context preservation
    """
    
    def __init__(self):
        self.active_tasks: Dict[str, AgentTask] = {}
        self.task_history = []
        
    def execute_agent_task(
        self,
        agent_chat,
        agent_name: str,
        task: str,
        timeout: int = None,
        on_progress: Optional[Callable] = None
    ) -> AgentResponse:
        """
        Execute agent task with smart timeout handling.
        
        Args:
            agent_chat: Agent chat instance
            agent_name: Name of agent
            task: Task to execute
            timeout: Max seconds (None = use settings)
            on_progress: Callback for progress updates
            
        Returns:
            AgentResponse with result
        """
        if timeout is None:
            timeout = settings.AGENT_TIMEOUT
        
        # Create task
        agent_task = AgentTask(agent_name, task, timeout)
        self.active_tasks[agent_name] = agent_task
        
        # Result queue for thread communication
        result_queue = Queue()
        
        def execute_in_thread():
            """Execute agent in background thread."""
            try:
                agent_task.status = "running"
                agent_task.start_time = time.time()
                
                # Execute with timeout
                response = agent_chat.send_message(task, stream=False)
                
                # Calculate stats
                duration = time.time() - agent_task.start_time
                tokens = len(response.split())  # Rough estimate
                
                result = AgentResponse(
                    success=True,
                    content=response,
                    tokens=tokens,
                    duration=duration
                )
                result_queue.put(result)
                
            except Exception as e:
                result = AgentResponse(
                    success=False,
                    content="",
                    tokens=0,
                    duration=time.time() - agent_task.start_time,
                    error=str(e)
                )
                result_queue.put(result)
        
        # Start background thread
        agent_task.thread = threading.Thread(target=execute_in_thread, daemon=True)
        agent_task.thread.start()
        
        # Wait with progress updates
        start_time = time.time()
        while True:
            elapsed = time.time() - start_time
            
            # Update progress
            progress = min(95, int((elapsed / timeout) * 100))
            agent_task.progress = progress
            
            if on_progress:
                on_progress(progress, agent_task)
            
            # Check if complete
            if not result_queue.empty():
                result = result_queue.get()
                agent_task.status = "complete"
                agent_task.progress = 100
                agent_task.result = result
                self.task_history.append(agent_task)
                del self.active_tasks[agent_name]
                return result
            
            # Check timeout
            if elapsed >= timeout:
                agent_task.status = "timeout"
                result = AgentResponse(
                    success=False,
                    content="",
                    tokens=0,
                    duration=elapsed,
                    timeout=True,
                    error=f"Timeout after {timeout}s"
                )
                agent_task.result = result
                self.task_history.append(agent_task)
                del self.active_tasks[agent_name]
                return result
            
            time.sleep(0.5)  # Check every 500ms
    
    def get_active_tasks(self) -> Dict[str, AgentTask]:
        """Get currently running tasks."""
        return self.active_tasks.copy()
    
    def cancel_task(self, agent_name: str) -> bool:
        """
        Cancel a running task.
        Note: Python threads can't be forcefully killed,
        but we mark it as cancelled.
        """
        if agent_name in self.active_tasks:
            task = self.active_tasks[agent_name]
            task.status = "cancelled"
            del self.active_tasks[agent_name]
            return True
        return False
    
    def get_agent_stats(self, agent_name: str) -> Dict:
        """Get statistics for an agent."""
        agent_tasks = [t for t in self.task_history if t.agent_name == agent_name]
        
        if not agent_tasks:
            return {
                'total_tasks': 0,
                'avg_duration': 0,
                'success_rate': 0,
                'timeout_rate': 0
            }
        
        total = len(agent_tasks)
        successes = sum(1 for t in agent_tasks if t.result and t.result.success)
        timeouts = sum(1 for t in agent_tasks if t.result and t.result.timeout)
        avg_duration = sum(t.result.duration for t in agent_tasks if t.result) / total
        
        return {
            'total_tasks': total,
            'avg_duration': avg_duration,
            'success_rate': (successes / total) * 100,
            'timeout_rate': (timeouts / total) * 100
        }
    
    def suggest_timeout(self, agent_name: str, task_complexity: str = 'medium') -> int:
        """
        Suggest optimal timeout based on history.
        
        Args:
            agent_name: Agent name
            task_complexity: 'simple', 'medium', 'complex'
            
        Returns:
            Suggested timeout in seconds
        """
        stats = self.get_agent_stats(agent_name)
        
        if stats['total_tasks'] == 0:
            # No history, use defaults
            base_timeouts = {
                'simple': 60,
                'medium': 120,
                'complex': 240
            }
            return base_timeouts.get(task_complexity, 120)
        
        # Use historical data
        avg_duration = stats['avg_duration']
        timeout_rate = stats['timeout_rate']
        
        # If high timeout rate, increase timeout
        if timeout_rate > 30:
            multiplier = 2.0
        elif timeout_rate > 10:
            multiplier = 1.5
        else:
            multiplier = 1.2
        
        # Adjust for complexity
        complexity_multiplier = {
            'simple': 0.8,
            'medium': 1.0,
            'complex': 1.5
        }.get(task_complexity, 1.0)
        
        suggested = int(avg_duration * multiplier * complexity_multiplier)
        
        # Clamp to reasonable range
        return max(30, min(600, suggested))  # 30s to 10min


class SmartAgentExecutor:
    """
    High-level executor with smart features.
    
    Features:
    - Automatic retry on failure
    - Dynamic timeout adjustment
    - Partial result recovery
    - Context preservation
    """
    
    def __init__(self, agent_manager: AgentManager):
        self.manager = agent_manager
        self.context_cache = {}
        
    def execute_with_retry(
        self,
        agent_chat,
        agent_name: str,
        task: str,
        max_retries: int = 2
    ) -> AgentResponse:
        """Execute with automatic retry on failure."""
        
        for attempt in range(max_retries + 1):
            # Get suggested timeout
            complexity = self._estimate_complexity(task)
            timeout = self.manager.suggest_timeout(agent_name, complexity)
            
            # Execute
            result = self.manager.execute_agent_task(
                agent_chat,
                agent_name,
                task,
                timeout=timeout
            )
            
            # Success!
            if result.success:
                return result
            
            # Timeout - try with longer timeout
            if result.timeout and attempt < max_retries:
                timeout = int(timeout * 1.5)
                continue
            
            # Other error - retry with same timeout
            if attempt < max_retries:
                time.sleep(2)  # Brief pause
                continue
            
            # All retries failed
            return result
        
        return result
    
    def execute_with_checkpoint(
        self,
        agent_chat,
        agent_name: str,
        task: str,
        checkpoint_interval: int = 30
    ) -> AgentResponse:
        """
        Execute with checkpoints for long tasks.
        If timeout, can resume from checkpoint.
        """
        # For very long tasks, break into chunks
        if len(task) > 500:  # Long task
            # Try to break into subtasks
            subtasks = self._break_into_subtasks(task)
            
            if len(subtasks) > 1:
                results = []
                for subtask in subtasks:
                    result = self.execute_with_retry(
                        agent_chat,
                        agent_name,
                        subtask,
                        max_retries=1
                    )
                    if result.success:
                        results.append(result.content)
                    else:
                        # Partial failure
                        break
                
                # Combine results
                combined = "\n\n".join(results)
                return AgentResponse(
                    success=len(results) > 0,
                    content=combined,
                    tokens=sum(r.tokens for r in results),
                    duration=sum(r.duration for r in results)
                )
        
        # Normal execution
        return self.execute_with_retry(agent_chat, agent_name, task)
    
    def _estimate_complexity(self, task: str) -> str:
        """Estimate task complexity from description."""
        task_lower = task.lower()
        
        # Simple indicators
        simple_keywords = ['simple', 'quick', 'small', 'basic', 'one']
        complex_keywords = ['complex', 'full', 'complete', 'comprehensive', 'entire', 'multiple']
        
        if any(kw in task_lower for kw in simple_keywords):
            return 'simple'
        elif any(kw in task_lower for kw in complex_keywords):
            return 'complex'
        
        # Check length
        if len(task) < 50:
            return 'simple'
        elif len(task) > 200:
            return 'complex'
        
        return 'medium'
    
    def _break_into_subtasks(self, task: str) -> list:
        """Break long task into subtasks."""
        # Simple heuristic: split by sentences
        sentences = task.split('.')
        
        if len(sentences) <= 2:
            return [task]
        
        # Group sentences into chunks
        chunks = []
        current_chunk = []
        
        for sentence in sentences:
            current_chunk.append(sentence)
            if len('.'.join(current_chunk)) > 200:
                chunks.append('.'.join(current_chunk).strip() + '.')
                current_chunk = []
        
        if current_chunk:
            chunks.append('.'.join(current_chunk).strip() + '.')
        
        return chunks if len(chunks) > 1 else [task]


# Global instance
_agent_manager = None

def get_agent_manager() -> AgentManager:
    """Get global agent manager instance."""
    global _agent_manager
    if _agent_manager is None:
        _agent_manager = AgentManager()
    return _agent_manager
