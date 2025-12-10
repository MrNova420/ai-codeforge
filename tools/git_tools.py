#!/usr/bin/env python3
"""
Git Tools - Version control integration
Part of Phase 9: Advanced Tool Ecosystem

Provides Git operations for agents:
- Repository management
- Commit operations
- Branch operations
- Push/Pull operations
- Diff viewing
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import subprocess
from tools.base_tool import BaseTool, ToolResult


class GitCloneTool(BaseTool):
    """Clone a Git repository."""
    
    name = "git_clone"
    description = "Clone a Git repository to local directory"
    
    def __call__(self, url: str, destination: Optional[str] = None) -> ToolResult:
        """Clone repository."""
        try:
            cmd = ['git', 'clone', url]
            if destination:
                cmd.append(destination)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return ToolResult(
                success=result.returncode == 0,
                data={"output": result.stdout, "path": destination or url.split('/')[-1].replace('.git', '')},
                error=result.stderr if result.returncode != 0 else None
            )
        except Exception as e:
            return ToolResult(success=False, data={}, error=str(e))


class GitCommitTool(BaseTool):
    """Commit changes to Git repository."""
    
    name = "git_commit"
    description = "Commit staged changes with a message"
    
    def __call__(self, message: str, repo_path: str = ".") -> ToolResult:
        """Commit changes."""
        try:
            # Stage all changes
            subprocess.run(
                ['git', 'add', '.'],
                cwd=repo_path,
                capture_output=True,
                timeout=30
            )
            
            # Commit
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return ToolResult(
                success=result.returncode == 0,
                data={"output": result.stdout},
                error=result.stderr if result.returncode != 0 else None
            )
        except Exception as e:
            return ToolResult(success=False, data={}, error=str(e))


class GitStatusTool(BaseTool):
    """Get Git repository status."""
    
    name = "git_status"
    description = "Get current status of Git repository"
    
    def __call__(self, repo_path: str = ".") -> ToolResult:
        """Get status."""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse output
            files = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    status = line[:2]
                    filepath = line[3:]
                    files.append({"status": status, "file": filepath})
            
            return ToolResult(
                success=True,
                data={"files": files, "raw": result.stdout}
            )
        except Exception as e:
            return ToolResult(success=False, data={}, error=str(e))


class GitDiffTool(BaseTool):
    """View Git diff."""
    
    name = "git_diff"
    description = "View changes in working directory"
    
    def __call__(self, repo_path: str = ".", file_path: Optional[str] = None) -> ToolResult:
        """Get diff."""
        try:
            cmd = ['git', 'diff']
            if file_path:
                cmd.append(file_path)
            
            result = subprocess.run(
                cmd,
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return ToolResult(
                success=True,
                data={"diff": result.stdout}
            )
        except Exception as e:
            return ToolResult(success=False, data={}, error=str(e))
