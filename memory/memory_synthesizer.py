#!/usr/bin/env python3
"""
Memory Synthesizer - Extract key learnings from completed tasks
Part of AGENT_ENHANCEMENT_STRATEGY.md implementation
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskInsight:
    """Key insight from a completed task."""
    task_description: str
    solution_summary: str
    agents_involved: List[str]
    success: bool
    key_learnings: List[str]
    code_snippets: List[str]
    errors_overcome: List[Dict[str, str]]
    timestamp: str


class MemorySynthesizer:
    """
    Synthesize key learnings from completed tasks and store in vector memory.
    
    This is a critical component for creating a learning system that improves over time.
    After each task, this synthesizer extracts:
    - Key learnings and patterns
    - Successful solutions
    - Errors that were overcome
    - Important code snippets
    
    These are then stored in the vector memory for future recall.
    """
    
    def __init__(self, vector_store, llm_agent=None):
        """
        Initialize synthesizer.
        
        Args:
            vector_store: VectorMemoryStore instance
            llm_agent: Optional LLM for generating summaries
        """
        self.vector_store = vector_store
        self.llm_agent = llm_agent
    
    def synthesize_task(
        self,
        task: str,
        result: Dict[str, Any],
        agents_used: List[str]
    ) -> TaskInsight:
        """
        Extract key learnings from a completed task.
        
        Args:
            task: Original task description
            result: Task result with success, output, errors, etc.
            agents_used: List of agents that worked on the task
            
        Returns:
            TaskInsight with synthesized information
        """
        # Extract success status
        success = result.get('success', False)
        
        # Generate summary
        summary = self._generate_summary(task, result)
        
        # Extract key learnings
        learnings = self._extract_learnings(task, result, agents_used)
        
        # Extract code snippets
        code_snippets = self._extract_code(result)
        
        # Extract errors that were overcome
        errors_overcome = self._extract_errors(result)
        
        insight = TaskInsight(
            task_description=task,
            solution_summary=summary,
            agents_involved=agents_used,
            success=success,
            key_learnings=learnings,
            code_snippets=code_snippets,
            errors_overcome=errors_overcome,
            timestamp=datetime.now().isoformat()
        )
        
        # Store in vector memory
        self._store_insight(insight)
        
        return insight
    
    def _generate_summary(self, task: str, result: Dict) -> str:
        """Generate a concise summary of what was accomplished."""
        if self.llm_agent:
            # Use LLM to generate summary
            prompt = f"""Summarize this completed task in 2-3 sentences:

Task: {task}
Result: {result.get('summary', 'Completed')}

Focus on WHAT was done and HOW it was accomplished."""
            
            try:
                summary = self.llm_agent.generate(prompt)
                return summary[:500]  # Limit length
            except Exception:
                # LLM may not be available, use fallback
                pass
        
        # Fallback: Simple summary
        if result.get('success'):
            return f"Successfully completed: {task}"
        else:
            return f"Attempted but failed: {task}. Error: {result.get('error', 'Unknown')}"
    
    def _extract_learnings(
        self,
        task: str,
        result: Dict,
        agents: List[str]
    ) -> List[str]:
        """Extract key learnings from the task."""
        learnings = []
        
        # Learning: Which agents were most effective
        if result.get('success'):
            learnings.append(f"Task type '{self._classify_task(task)}' successfully handled by {', '.join(agents)}")
        
        # Learning: Common patterns
        if 'patterns' in result:
            for pattern in result['patterns']:
                learnings.append(f"Applied pattern: {pattern}")
        
        # Learning: Time taken
        if 'duration' in result:
            learnings.append(f"Task completed in {result['duration']}s with {len(agents)} agents")
        
        # Learning: Tools used
        if 'tools_used' in result:
            learnings.append(f"Key tools: {', '.join(result['tools_used'])}")
        
        return learnings[:5]  # Top 5 learnings
    
    def _extract_code(self, result: Dict) -> List[str]:
        """Extract important code snippets."""
        code_snippets = []
        
        # Look for code in results
        if 'code' in result:
            code = result['code']
            if isinstance(code, str) and len(code) > 20:
                code_snippets.append(code)
        
        # Look for code in agent outputs
        if 'results' in result:
            for agent_name, agent_result in result['results'].items():
                if isinstance(agent_result, str):
                    # Simple heuristic: if it contains code keywords
                    if any(kw in agent_result for kw in ['def ', 'class ', 'function ', 'import ']):
                        code_snippets.append(agent_result[:1000])
        
        return code_snippets[:3]  # Max 3 snippets
    
    def _extract_errors(self, result: Dict) -> List[Dict[str, str]]:
        """Extract errors that were encountered and overcome."""
        errors = []
        
        # Check task history for errors
        if 'history' in result:
            for attempt in result['history']:
                if attempt.get('error') and attempt.get('fixed'):
                    errors.append({
                        'type': attempt.get('error_type', 'Unknown'),
                        'message': attempt['error'][:200],
                        'fix': attempt.get('fix', 'Retried and succeeded')
                    })
        
        # Check for explicit error list
        if 'errors_overcome' in result:
            errors.extend(result['errors_overcome'])
        
        return errors[:5]  # Max 5 errors
    
    def _classify_task(self, task: str) -> str:
        """Classify task type for categorization."""
        task_lower = task.lower()
        
        if any(kw in task_lower for kw in ['create', 'build', 'implement', 'add']):
            return 'creation'
        elif any(kw in task_lower for kw in ['fix', 'debug', 'resolve', 'error']):
            return 'debugging'
        elif any(kw in task_lower for kw in ['test', 'verify', 'check']):
            return 'testing'
        elif any(kw in task_lower for kw in ['refactor', 'improve', 'optimize']):
            return 'optimization'
        elif any(kw in task_lower for kw in ['research', 'find', 'investigate']):
            return 'research'
        else:
            return 'general'
    
    def _store_insight(self, insight: TaskInsight) -> None:
        """Store the synthesized insight in vector memory."""
        if not self.vector_store:
            return
        
        # Store task summary
        self.vector_store.store_task_summary(
            task=insight.task_description,
            solution=insight.solution_summary,
            agents_involved=insight.agents_involved,
            success=insight.success
        )
        
        # Store code snippets
        for i, code in enumerate(insight.code_snippets):
            # Detect language from code patterns
            language = self._detect_language(code)
            
            self.vector_store.store_code_snippet(
                code=code,
                description=f"From task: {insight.task_description[:100]}",
                language=language,
                tags=['synthesized', insight.task_description[:50]]
            )
        
        # Store error resolutions
        for error in insight.errors_overcome:
            self.vector_store.store_error_resolution(
                error_type=error['type'],
                error_message=error['message'],
                solution=error['fix'],
                context=insight.task_description
            )
    
    def recall_similar_tasks(self, task: str, n_results: int = 3) -> List[Dict]:
        """
        Recall similar past tasks for context injection.
        
        Args:
            task: New task to find similar past tasks for
            n_results: Number of similar tasks to return
            
        Returns:
            List of similar task memories
        """
        if not self.vector_store:
            return []
        
        # Query vector memory for similar tasks
        memories = self.vector_store.recall_memories(
            query=task,
            memory_type='task_summaries',
            n_results=n_results
        )
        
        return memories
    
    def _detect_language(self, code: str) -> str:
        """Detect programming language from code patterns."""
        code_lower = code.lower()
        
        # Python indicators
        if any(kw in code for kw in ['def ', 'import ', 'from ', 'class ']):
            return 'python'
        
        # JavaScript/TypeScript indicators
        if any(kw in code for kw in ['function ', 'const ', 'let ', 'var ', '=>']):
            if 'interface ' in code or ': string' in code or ': number' in code:
                return 'typescript'
            return 'javascript'
        
        # Java indicators
        if any(kw in code for kw in ['public class', 'private ', 'protected ']):
            return 'java'
        
        # Go indicators  
        if 'func ' in code and 'package ' in code:
            return 'go'
        
        # Default
        return 'python'
    
    def get_synthesis_stats(self) -> Dict[str, int]:
        """Get statistics about synthesized memories."""
        if not self.vector_store:
            return {'total': 0}
        
        return self.vector_store.get_memory_stats()
