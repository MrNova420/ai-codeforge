#!/usr/bin/env python3
"""
File Manager - Handles safe file operations for agents
"""

import os
from pathlib import Path
from typing import List, Optional, Dict
import shutil
from datetime import datetime


class FileManager:
    """Manages file operations with safety checks."""
    
    def __init__(self, workspace_dir: Path, allowed_extensions: List[str] = None):
        self.workspace_dir = workspace_dir
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Default allowed extensions for code files
        self.allowed_extensions = allowed_extensions or [
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.go', '.rs', '.rb', '.php', '.cs', '.swift', '.kt', '.scala',
            '.html', '.css', '.scss', '.sass', '.less',
            '.json', '.yaml', '.yml', '.toml', '.xml',
            '.md', '.txt', '.sh', '.bash', '.sql'
        ]
        
        # Track file operations for audit
        self.operations_log = []
    
    def _is_safe_path(self, path: Path) -> bool:
        """Check if path is within workspace."""
        try:
            resolved = path.resolve()
            workspace = self.workspace_dir.resolve()
            return str(resolved).startswith(str(workspace))
        except Exception:
            return False
    
    def _is_allowed_extension(self, path: Path) -> bool:
        """Check if file extension is allowed."""
        return path.suffix.lower() in self.allowed_extensions
    
    def _log_operation(self, operation: str, path: str, success: bool, error: str = None):
        """Log file operation."""
        self.operations_log.append({
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'path': path,
            'success': success,
            'error': error
        })
    
    def read_file(self, file_path: str) -> Optional[str]:
        """Read a file safely."""
        path = self.workspace_dir / file_path
        
        if not self._is_safe_path(path):
            self._log_operation('read', file_path, False, 'Path outside workspace')
            return None
        
        if not path.exists():
            self._log_operation('read', file_path, False, 'File not found')
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self._log_operation('read', file_path, True)
            return content
        except Exception as e:
            self._log_operation('read', file_path, False, str(e))
            return None
    
    def write_file(self, file_path: str, content: str) -> bool:
        """Write to a file safely."""
        path = self.workspace_dir / file_path
        
        if not self._is_safe_path(path):
            self._log_operation('write', file_path, False, 'Path outside workspace')
            return False
        
        if not self._is_allowed_extension(path):
            self._log_operation('write', file_path, False, 'File type not allowed')
            return False
        
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            self._log_operation('write', file_path, True)
            return True
        except Exception as e:
            self._log_operation('write', file_path, False, str(e))
            return False
    
    def append_file(self, file_path: str, content: str) -> bool:
        """Append to a file safely."""
        path = self.workspace_dir / file_path
        
        if not self._is_safe_path(path):
            self._log_operation('append', file_path, False, 'Path outside workspace')
            return False
        
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content)
            self._log_operation('append', file_path, True)
            return True
        except Exception as e:
            self._log_operation('append', file_path, False, str(e))
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file safely."""
        path = self.workspace_dir / file_path
        
        if not self._is_safe_path(path):
            self._log_operation('delete', file_path, False, 'Path outside workspace')
            return False
        
        if not path.exists():
            self._log_operation('delete', file_path, False, 'File not found')
            return False
        
        try:
            path.unlink()
            self._log_operation('delete', file_path, True)
            return True
        except Exception as e:
            self._log_operation('delete', file_path, False, str(e))
            return False
    
    def list_files(self, directory: str = "", pattern: str = "*") -> List[str]:
        """List files in directory."""
        path = self.workspace_dir / directory
        
        if not self._is_safe_path(path):
            return []
        
        if not path.exists() or not path.is_dir():
            return []
        
        try:
            files = []
            for item in path.glob(pattern):
                if item.is_file():
                    rel_path = item.relative_to(self.workspace_dir)
                    files.append(str(rel_path))
            return sorted(files)
        except Exception:
            return []
    
    def create_directory(self, dir_path: str) -> bool:
        """Create a directory safely."""
        path = self.workspace_dir / dir_path
        
        if not self._is_safe_path(path):
            self._log_operation('mkdir', dir_path, False, 'Path outside workspace')
            return False
        
        try:
            path.mkdir(parents=True, exist_ok=True)
            self._log_operation('mkdir', dir_path, True)
            return True
        except Exception as e:
            self._log_operation('mkdir', dir_path, False, str(e))
            return False
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists."""
        path = self.workspace_dir / file_path
        return self._is_safe_path(path) and path.exists()
    
    def get_file_info(self, file_path: str) -> Optional[Dict]:
        """Get file information."""
        path = self.workspace_dir / file_path
        
        if not self._is_safe_path(path) or not path.exists():
            return None
        
        try:
            stats = path.stat()
            return {
                'name': path.name,
                'path': str(path.relative_to(self.workspace_dir)),
                'size': stats.st_size,
                'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
                'is_file': path.is_file(),
                'extension': path.suffix
            }
        except Exception:
            return None
    
    def search_in_files(self, search_text: str, pattern: str = "*.py") -> List[Dict]:
        """Search for text in files."""
        results = []
        
        try:
            for file_path in self.workspace_dir.rglob(pattern):
                if not file_path.is_file() or not self._is_safe_path(file_path):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if search_text in line:
                                results.append({
                                    'file': str(file_path.relative_to(self.workspace_dir)),
                                    'line': line_num,
                                    'content': line.strip()
                                })
                except Exception:
                    continue
        except Exception:
            pass
        
        return results
    
    def get_operations_log(self, limit: int = 50) -> List[Dict]:
        """Get recent file operations."""
        return self.operations_log[-limit:]
