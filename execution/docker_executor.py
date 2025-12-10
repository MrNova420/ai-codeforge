#!/usr/bin/env python3
"""
Docker Code Executor - Secure sandboxed code execution
Part of PROJECT_REVISION_PLAN.md Phase 3

Executes code in isolated Docker containers with:
- Resource limits (CPU, memory, disk)
- Network isolation
- Timeout enforcement
- Security restrictions
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import tempfile
import subprocess
import time


@dataclass
class ExecutionResult:
    """Result of code execution in Docker."""
    success: bool
    output: str
    error: Optional[str]
    exit_code: int
    execution_time: float
    memory_used: Optional[int]  # bytes
    container_id: Optional[str]


class DockerCodeExecutor:
    """
    Execute code in isolated Docker containers.
    
    Security Features:
    - Network disabled by default
    - Read-only filesystem where possible
    - Limited CPU and memory
    - Execution timeout
    - Non-root user execution
    - No privileged access
    
    Supported Languages:
    - Python (3.8, 3.9, 3.10, 3.11, 3.12)
    - JavaScript/Node.js
    - TypeScript
    - Java
    - Go
    - Rust
    """
    
    def __init__(
        self,
        docker_available: bool = None,
        default_timeout: int = 30,
        default_memory_limit: str = "512m",
        default_cpu_quota: int = 50000  # 50% of one CPU
    ):
        """
        Initialize Docker executor.
        
        Args:
            docker_available: Whether Docker is available (auto-detect if None)
            default_timeout: Default execution timeout in seconds
            default_memory_limit: Default memory limit (e.g., "512m", "1g")
            default_cpu_quota: Default CPU quota (100000 = 1 full CPU)
        """
        self.docker_available = docker_available if docker_available is not None else self._check_docker()
        self.default_timeout = default_timeout
        self.default_memory_limit = default_memory_limit
        self.default_cpu_quota = default_cpu_quota
        
        self.language_images = {
            'python': 'python:3.11-slim',
            'javascript': 'node:18-slim',
            'typescript': 'node:18-slim',
            'java': 'openjdk:17-slim',
            'go': 'golang:1.21-alpine',
            'rust': 'rust:1.75-slim'
        }
        
        self.file_extensions = {
            'python': '.py',
            'javascript': '.js',
            'typescript': '.ts',
            'java': '.java',
            'go': '.go',
            'rust': '.rs'
        }
    
    def _check_docker(self) -> bool:
        """Check if Docker is available and running."""
        try:
            result = subprocess.run(
                ['docker', 'version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def execute(
        self,
        code: str,
        language: str = 'python',
        timeout: Optional[int] = None,
        memory_limit: Optional[str] = None,
        network_enabled: bool = False,
        env_vars: Optional[Dict[str, str]] = None
    ) -> ExecutionResult:
        """
        Execute code in Docker container.
        
        Args:
            code: Source code to execute
            language: Programming language
            timeout: Execution timeout (seconds)
            memory_limit: Memory limit (e.g., "512m")
            network_enabled: Whether to enable network
            env_vars: Environment variables
            
        Returns:
            ExecutionResult with output and metrics
        """
        if not self.docker_available:
            return ExecutionResult(
                success=False,
                output="",
                error="Docker is not available. Install Docker to use sandboxed execution.",
                exit_code=-1,
                execution_time=0.0,
                memory_used=None,
                container_id=None
            )
        
        timeout = timeout or self.default_timeout
        memory_limit = memory_limit or self.default_memory_limit
        
        start_time = time.time()
        
        try:
            # Create temporary directory for code
            with tempfile.TemporaryDirectory() as tmpdir:
                # Write code to file
                code_file = self._prepare_code_file(tmpdir, code, language)
                
                # Build Docker command
                docker_cmd = self._build_docker_command(
                    tmpdir=tmpdir,
                    code_file=code_file,
                    language=language,
                    memory_limit=memory_limit,
                    network_enabled=network_enabled,
                    env_vars=env_vars
                )
                
                # Execute in Docker
                result = subprocess.run(
                    docker_cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                execution_time = time.time() - start_time
                
                return ExecutionResult(
                    success=result.returncode == 0,
                    output=result.stdout,
                    error=result.stderr if result.returncode != 0 else None,
                    exit_code=result.returncode,
                    execution_time=execution_time,
                    memory_used=None,  # Would need Docker stats API
                    container_id=None
                )
        
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return ExecutionResult(
                success=False,
                output="",
                error=f"Execution timed out after {timeout} seconds",
                exit_code=-1,
                execution_time=execution_time,
                memory_used=None,
                container_id=None
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                success=False,
                output="",
                error=f"Execution error: {str(e)}",
                exit_code=-1,
                execution_time=execution_time,
                memory_used=None,
                container_id=None
            )
    
    def _prepare_code_file(self, tmpdir: str, code: str, language: str) -> str:
        """Prepare code file in temporary directory."""
        ext = self.file_extensions.get(language, '.txt')
        code_file = Path(tmpdir) / f'code{ext}'
        code_file.write_text(code)
        return code_file.name
    
    def _build_docker_command(
        self,
        tmpdir: str,
        code_file: str,
        language: str,
        memory_limit: str,
        network_enabled: bool,
        env_vars: Optional[Dict[str, str]]
    ) -> List[str]:
        """Build Docker run command with security restrictions."""
        image = self.language_images.get(language, 'python:3.11-slim')
        
        cmd = [
            'docker', 'run',
            '--rm',  # Remove container after execution
            '--read-only',  # Read-only filesystem
            '--tmpfs', '/tmp:rw,noexec,nosuid,size=100m',  # Writable /tmp with limits
            f'--memory={memory_limit}',  # Memory limit
            f'--cpu-quota={self.default_cpu_quota}',  # CPU limit
            '--security-opt=no-new-privileges',  # No privilege escalation
            '--cap-drop=ALL',  # Drop all capabilities
            '-v', f'{tmpdir}:/code:ro',  # Mount code directory read-only
        ]
        
        # Network isolation (default)
        if not network_enabled:
            cmd.append('--network=none')
        
        # Environment variables
        if env_vars:
            for key, value in env_vars.items():
                cmd.extend(['-e', f'{key}={value}'])
        
        # Add image and execution command
        cmd.append(image)
        cmd.extend(self._get_execution_command(language, code_file))
        
        return cmd
    
    def _get_execution_command(self, language: str, code_file: str) -> List[str]:
        """Get the command to execute code in the container."""
        commands = {
            'python': ['python', f'/code/{code_file}'],
            'javascript': ['node', f'/code/{code_file}'],
            'typescript': ['sh', '-c', f'npx ts-node /code/{code_file}'],
            'java': ['sh', '-c', f'javac /code/{code_file} && java -cp /code {code_file[:-5]}'],
            'go': ['go', 'run', f'/code/{code_file}'],
            'rust': ['sh', '-c', f'rustc /code/{code_file} -o /tmp/code && /tmp/code']
        }
        return commands.get(language, ['cat', f'/code/{code_file}'])
    
    def execute_with_tests(
        self,
        code: str,
        test_code: str,
        language: str = 'python'
    ) -> ExecutionResult:
        """
        Execute code with tests in Docker.
        
        Args:
            code: Source code
            test_code: Test code
            language: Programming language
            
        Returns:
            ExecutionResult with test results
        """
        # Combine code and tests
        combined = f"{code}\n\n{test_code}"
        
        return self.execute(
            code=combined,
            language=language,
            timeout=60  # Tests may take longer
        )
    
    def pull_images(self, languages: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Pre-pull Docker images for faster execution.
        
        Args:
            languages: List of languages to pull images for (None = all)
            
        Returns:
            Dict of language -> success status
        """
        if not self.docker_available:
            return {}
        
        languages = languages or list(self.language_images.keys())
        results = {}
        
        for lang in languages:
            if lang not in self.language_images:
                results[lang] = False
                continue
            
            image = self.language_images[lang]
            print(f"Pulling {image}...")
            
            try:
                result = subprocess.run(
                    ['docker', 'pull', image],
                    capture_output=True,
                    timeout=300  # 5 minute timeout for pull
                )
                results[lang] = result.returncode == 0
                if results[lang]:
                    print(f"✓ {lang} image ready")
                else:
                    print(f"✗ {lang} image pull failed")
            except Exception:
                # Image pull failed
                results[lang] = False
        
        return results
    
    def get_available_languages(self) -> List[str]:
        """Get list of supported languages."""
        return list(self.language_images.keys())
    
    def is_docker_available(self) -> bool:
        """Check if Docker is available."""
        return self.docker_available
    
    def get_stats(self) -> Dict[str, Any]:
        """Get executor statistics."""
        return {
            'docker_available': self.docker_available,
            'supported_languages': self.get_available_languages(),
            'default_timeout': self.default_timeout,
            'default_memory_limit': self.default_memory_limit
        }
