#!/usr/bin/env python3
"""
Self-Correcting Agent - Agent that can debug its own code
Implements the debugging loop from AGENT_ENHANCEMENT_STRATEGY.md

This agent:
1. Writes code
2. Tests it
3. Reads errors
4. Fixes issues
5. Repeats until success
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import subprocess
import tempfile
from pathlib import Path

from memory.vector_store import VectorMemoryStore


@dataclass
class CorrectionAttempt:
    """Record of a correction attempt."""
    attempt_number: int
    code: str
    error: Optional[str]
    success: bool
    fix_applied: Optional[str] = None


class SelfCorrectingAgent:
    """
    Agent wrapper that adds self-correction capabilities.
    
    This wraps any code-generating agent and adds:
    - Automatic error detection
    - Self-debugging logic
    - Learning from failures
    - Retry with improvements
    
    Key Feature: The agent learns from past errors stored in memory!
    """
    
    def __init__(
        self,
        base_agent,  # The underlying agent (e.g., Felix)
        memory: Optional[VectorMemoryStore] = None,
        max_attempts: int = 3,
        timeout: int = 10
    ):
        """
        Initialize self-correcting wrapper.
        
        Args:
            base_agent: Agent that generates code
            memory: Memory system for learning from errors
            max_attempts: Maximum correction attempts
            timeout: Timeout for code execution
        """
        self.base_agent = base_agent
        self.memory = memory
        self.max_attempts = max_attempts
        self.timeout = timeout
        
        self.correction_history: List[CorrectionAttempt] = []
    
    def generate_and_test(
        self,
        task: str,
        test_code: Optional[str] = None,
        language: str = 'python'
    ) -> Dict[str, Any]:
        """
        Generate code with automatic self-correction.
        
        Args:
            task: What to implement
            test_code: Optional test to validate code
            language: Programming language
            
        Returns:
            Dict with final code and correction history
        """
        self.correction_history.clear()
        
        for attempt in range(1, self.max_attempts + 1):
            print(f"🔄 Attempt {attempt}/{self.max_attempts}")
            
            # Generate code
            if attempt == 1:
                # First attempt - fresh generation
                prompt = task
            else:
                # Subsequent attempts - include error feedback
                last_attempt = self.correction_history[-1]
                prompt = self._create_fix_prompt(task, last_attempt)
            
            code = self._generate_code(prompt)
            
            # Test the code
            test_result = self._test_code(code, test_code, language)
            
            # Record attempt
            attempt_record = CorrectionAttempt(
                attempt_number=attempt,
                code=code,
                error=test_result.get('error'),
                success=test_result.get('success', False),
                fix_applied=None
            )
            self.correction_history.append(attempt_record)
            
            # Success!
            if test_result.get('success'):
                print(f"✅ Success on attempt {attempt}!")
                
                # Store success in memory if we had to correct
                if attempt > 1 and self.memory:
                    self._remember_success(task, code)
                
                return {
                    'success': True,
                    'code': code,
                    'attempts': attempt,
                    'history': self.correction_history
                }
            
            # Failed - but will try again
            error_msg = test_result.get('error', 'Unknown error')
            print(f"❌ Error: {error_msg[:100]}...")
            
            # Check memory for similar errors
            if self.memory:
                similar_fixes = self._recall_similar_errors(error_msg)
                if similar_fixes:
                    print(f"💡 Found {len(similar_fixes)} similar errors in memory")
        
        # All attempts exhausted
        print(f"💀 Failed after {self.max_attempts} attempts")
        
        # Store failure for learning
        if self.memory:
            self._remember_failure(task, self.correction_history)
        
        return {
            'success': False,
            'code': self.correction_history[-1].code if self.correction_history else None,
            'attempts': self.max_attempts,
            'history': self.correction_history,
            'final_error': self.correction_history[-1].error if self.correction_history else None
        }
    
    def _generate_code(self, prompt: str) -> str:
        """
        Generate code using the base agent.
        
        Args:
            prompt: Generation prompt
            
        Returns:
            Generated code
        """
        # This would call the actual agent
        # For now, return a placeholder
        if hasattr(self.base_agent, 'generate'):
            return self.base_agent.generate(prompt)
        elif hasattr(self.base_agent, 'send_message'):
            return self.base_agent.send_message(prompt)
        else:
            # Fallback - return the prompt as code (for testing)
            return f"# Generated code for: {prompt}\n"
    
    def _test_code(
        self,
        code: str,
        test_code: Optional[str],
        language: str
    ) -> Dict[str, Any]:
        """
        Test generated code.
        
        Args:
            code: Code to test
            test_code: Optional test code
            language: Programming language
            
        Returns:
            Test results
        """
        if language == 'python':
            return self._test_python_code(code, test_code)
        else:
            return {'success': False, 'error': f'Unsupported language: {language}'}
    
    def _test_python_code(
        self,
        code: str,
        test_code: Optional[str]
    ) -> Dict[str, Any]:
        """
        Test Python code.
        
        Args:
            code: Python code to test
            test_code: Optional pytest code
            
        Returns:
            Test results
        """
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                if test_code:
                    f.write('\n\n')
                    f.write(test_code)
                temp_file = f.name
            
            # Run the code
            result = subprocess.run(
                ['python3', temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            # Clean up
            Path(temp_file).unlink()
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'output': result.stdout
                }
        
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f'Code execution timed out after {self.timeout}s'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Test execution failed: {str(e)}'
            }
    
    def _create_fix_prompt(self, original_task: str, last_attempt: CorrectionAttempt) -> str:
        """
        Create prompt for fixing code.
        
        Args:
            original_task: Original task
            last_attempt: Previous failed attempt
            
        Returns:
            Fix prompt
        """
        prompt = f"""The following code for '{original_task}' has an error:

```python
{last_attempt.code}
```

Error:
{last_attempt.error}

Please fix the error and provide corrected code."""

        # Add memory insights if available
        if self.memory:
            similar = self._recall_similar_errors(last_attempt.error)
            if similar:
                prompt += f"\n\nPrevious similar errors and solutions:\n"
                for memory in similar[:2]:  # Top 2
                    prompt += f"- {memory['content'][:200]}...\n"
        
        return prompt
    
    def _recall_similar_errors(self, error_message: str) -> List[Dict]:
        """
        Find similar errors from memory.
        
        Args:
            error_message: Current error
            
        Returns:
            List of similar error resolutions
        """
        if not self.memory:
            return []
        
        try:
            # Search for similar errors
            results = self.memory.recall_memories(
                query=error_message,
                memory_type='error_resolutions',
                n_results=3
            )
            return results
        except:
            return []
    
    def _remember_success(self, task: str, code: str) -> None:
        """Remember a successful correction."""
        if not self.memory:
            return
        
        # Get the errors we overcame
        errors = [
            attempt.error
            for attempt in self.correction_history[:-1]
            if attempt.error
        ]
        
        if errors:
            summary = f"Task: {task}\nErrors overcome: {'; '.join(errors[:2])}\nSolution: {code[:200]}"
            
            self.memory.store_code_snippet(
                code=code,
                description=f"Self-corrected solution for: {task}",
                language='python',
                tags=['self-corrected', 'success']
            )
    
    def _remember_failure(self, task: str, history: List[CorrectionAttempt]) -> None:
        """Remember a failure for future learning."""
        if not self.memory:
            return
        
        # Store the persistent error
        final_error = history[-1].error if history else 'Unknown'
        
        self.memory.store_error_resolution(
            error_type='SelfCorrectionFailure',
            error_message=final_error[:200],
            solution=f"Failed after {len(history)} attempts. Needs manual review.",
            context=task
        )
    
    def get_correction_stats(self) -> Dict[str, Any]:
        """Get statistics about corrections."""
        return {
            'total_attempts': len(self.correction_history),
            'successful': any(a.success for a in self.correction_history),
            'attempts_used': len(self.correction_history)
        }
