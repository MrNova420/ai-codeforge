#!/usr/bin/env python3
"""
Code Executor - Safe sandbox for executing code
"""

import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Optional, List
import time
import signal


class ExecutionResult:
    """Result of code execution."""
    
    def __init__(self, success: bool, output: str, error: str, 
                 exit_code: int, execution_time: float):
        self.success = success
        self.output = output
        self.error = error
        self.exit_code = exit_code
        self.execution_time = execution_time
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'output': self.output,
            'error': self.error,
            'exit_code': self.exit_code,
            'execution_time': self.execution_time
        }


class CodeExecutor:
    """Executes code in a safe environment."""
    
    def __init__(self, workspace_dir: Path, timeout: int = 30):
        self.workspace_dir = workspace_dir
        self.timeout = timeout
        self.allowed_interpreters = {
            'python': ['python3', '-u'],
            'javascript': ['node'],
            'bash': ['bash'],
            'shell': ['sh']
        }
    
    def execute_python(self, code: str, timeout: Optional[int] = None) -> ExecutionResult:
        """Execute Python code."""
        return self._execute_code(code, 'python', timeout)
    
    def execute_javascript(self, code: str, timeout: Optional[int] = None) -> ExecutionResult:
        """Execute JavaScript code."""
        return self._execute_code(code, 'javascript', timeout)
    
    def execute_bash(self, code: str, timeout: Optional[int] = None) -> ExecutionResult:
        """Execute Bash script."""
        return self._execute_code(code, 'bash', timeout)
    
    def _execute_code(self, code: str, language: str, timeout: Optional[int] = None) -> ExecutionResult:
        """Execute code in specified language."""
        if language not in self.allowed_interpreters:
            return ExecutionResult(False, "", f"Language '{language}' not supported", -1, 0)
        
        timeout = timeout or self.timeout
        
        # Create temporary file
        extensions = {
            'python': '.py',
            'javascript': '.js',
            'bash': '.sh',
            'shell': '.sh'
        }
        
        try:
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix=extensions.get(language, '.txt'),
                dir=self.workspace_dir,
                delete=False
            ) as f:
                f.write(code)
                temp_file = f.name
            
            # Make executable for scripts
            if language in ['bash', 'shell']:
                os.chmod(temp_file, 0o755)
            
            # Execute code
            start_time = time.time()
            interpreter = self.allowed_interpreters[language]
            
            try:
                result = subprocess.run(
                    interpreter + [temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=self.workspace_dir
                )
                
                execution_time = time.time() - start_time
                
                return ExecutionResult(
                    success=result.returncode == 0,
                    output=result.stdout,
                    error=result.stderr,
                    exit_code=result.returncode,
                    execution_time=execution_time
                )
            
            except subprocess.TimeoutExpired:
                execution_time = time.time() - start_time
                return ExecutionResult(
                    False,
                    "",
                    f"Execution timed out after {timeout} seconds",
                    -1,
                    execution_time
                )
            
            except Exception as e:
                execution_time = time.time() - start_time
                return ExecutionResult(False, "", str(e), -1, execution_time)
        
        finally:
            # Clean up temp file
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception:
                pass
    
    def execute_file(self, file_path: str, language: str, timeout: Optional[int] = None) -> ExecutionResult:
        """Execute a file in the workspace."""
        full_path = self.workspace_dir / file_path
        
        if not full_path.exists():
            return ExecutionResult(False, "", f"File not found: {file_path}", -1, 0)
        
        if language not in self.allowed_interpreters:
            return ExecutionResult(False, "", f"Language '{language}' not supported", -1, 0)
        
        timeout = timeout or self.timeout
        
        try:
            start_time = time.time()
            interpreter = self.allowed_interpreters[language]
            
            result = subprocess.run(
                interpreter + [str(full_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.workspace_dir
            )
            
            execution_time = time.time() - start_time
            
            return ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                exit_code=result.returncode,
                execution_time=execution_time
            )
        
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return ExecutionResult(
                False,
                "",
                f"Execution timed out after {timeout} seconds",
                -1,
                execution_time
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(False, "", str(e), -1, execution_time)
    
    def run_tests(self, test_command: str, timeout: Optional[int] = None) -> ExecutionResult:
        """Run test command."""
        timeout = timeout or self.timeout * 2  # Tests may take longer
        
        try:
            start_time = time.time()
            
            result = subprocess.run(
                test_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.workspace_dir
            )
            
            execution_time = time.time() - start_time
            
            return ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                exit_code=result.returncode,
                execution_time=execution_time
            )
        
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return ExecutionResult(
                False,
                "",
                f"Tests timed out after {timeout} seconds",
                -1,
                execution_time
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(False, "", str(e), -1, execution_time)
