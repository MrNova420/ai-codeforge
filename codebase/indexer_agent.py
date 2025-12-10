#!/usr/bin/env python3
"""
AST Indexer Agent - Background agent that maintains codebase knowledge
Implements the background indexer from SCALING_TO_LARGE_PROJECTS.md

This agent:
- Watches for file changes
- Incrementally updates the graph
- Runs in background thread
- Provides status updates
"""

import threading
import time
from pathlib import Path
from typing import Optional, Callable, Dict, Any
from datetime import datetime
import hashlib

from .graph_manager import CodebaseGraphManager
from .ast_parser import ASTParser


class IndexerAgent:
    """
    Background agent that continuously maintains the codebase graph.
    
    Features:
    - Automatic file discovery
    - Incremental indexing
    - Change detection
    - Background processing
    - Status callbacks
    """
    
    def __init__(
        self,
        graph: CodebaseGraphManager,
        project_root: str,
        on_progress: Optional[Callable] = None,
        on_complete: Optional[Callable] = None
    ):
        """
        Initialize indexer agent.
        
        Args:
            graph: Codebase graph to maintain
            project_root: Root directory to index
            on_progress: Callback for progress updates (file, status)
            on_complete: Callback when indexing completes (stats)
        """
        self.graph = graph
        self.project_root = Path(project_root)
        self.parser = ASTParser(graph)
        
        self.on_progress = on_progress
        self.on_complete = on_complete
        
        # State
        self.is_running = False
        self.is_indexing = False
        self.thread: Optional[threading.Thread] = None
        
        # Track file hashes to detect changes
        self.file_hashes: Dict[str, str] = {}
        
        # Statistics
        self.stats = {
            'files_indexed': 0,
            'files_failed': 0,
            'nodes_added': 0,
            'relationships_added': 0,
            'last_index_time': None,
            'indexing_duration': 0
        }
    
    def start(self) -> None:
        """Start the indexer agent in background."""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
    
    def stop(self) -> None:
        """Stop the indexer agent."""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
    
    def index_now(self) -> Dict[str, Any]:
        """
        Trigger immediate indexing (synchronous).
        
        Returns:
            Indexing results
        """
        return self._index_codebase()
    
    def _run_loop(self) -> None:
        """Main background loop."""
        # Do initial index
        self._index_codebase()
        
        # Then watch for changes (simplified - no file watching yet)
        while self.is_running:
            time.sleep(30)  # Check every 30 seconds
            
            # Check for file changes
            if self._has_changes():
                self._index_codebase()
    
    def _index_codebase(self) -> Dict[str, Any]:
        """
        Index all Python files in the project.
        
        Returns:
            Indexing statistics
        """
        if self.is_indexing:
            return {'status': 'already_indexing'}
        
        self.is_indexing = True
        start_time = time.time()
        
        # Reset stats
        self.stats['files_indexed'] = 0
        self.stats['files_failed'] = 0
        self.stats['nodes_added'] = 0
        self.stats['relationships_added'] = 0
        
        try:
            # Find all Python files
            py_files = list(self.project_root.rglob('*.py'))
            
            # Filter out venv, __pycache__, etc.
            py_files = [
                f for f in py_files
                if not any(exclude in str(f) for exclude in ['venv', '__pycache__', '.git'])
            ]
            
            total_files = len(py_files)
            
            # Index each file
            for i, py_file in enumerate(py_files, 1):
                if not self.is_running:
                    break
                
                # Notify progress
                if self.on_progress:
                    self.on_progress(str(py_file), f"{i}/{total_files}")
                
                # Check if file changed
                file_hash = self._hash_file(py_file)
                if file_hash == self.file_hashes.get(str(py_file)):
                    continue  # Skip unchanged files
                
                # Parse file
                result = self.parser.parse_file(str(py_file))
                
                if 'error' in result:
                    self.stats['files_failed'] += 1
                else:
                    self.stats['files_indexed'] += 1
                    self.stats['nodes_added'] += result.get('nodes_added', 0)
                    self.stats['relationships_added'] += result.get('relationships_added', 0)
                    
                    # Update hash
                    self.file_hashes[str(py_file)] = file_hash
            
            # Persist graph
            self.graph.persist()
            
            # Update metadata
            duration = time.time() - start_time
            self.stats['indexing_duration'] = duration
            self.stats['last_index_time'] = datetime.now().isoformat()
            
            # Notify complete
            if self.on_complete:
                self.on_complete(self.stats)
            
            return self.stats
            
        finally:
            self.is_indexing = False
    
    def _has_changes(self) -> bool:
        """Check if any files have changed."""
        py_files = list(self.project_root.rglob('*.py'))
        py_files = [
            f for f in py_files
            if not any(exclude in str(f) for exclude in ['venv', '__pycache__'])
        ]
        
        for py_file in py_files:
            file_hash = self._hash_file(py_file)
            if file_hash != self.file_hashes.get(str(py_file)):
                return True
        
        return False
    
    def _hash_file(self, file_path: Path) -> str:
        """Calculate hash of file contents."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ''
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the indexer."""
        return {
            'is_running': self.is_running,
            'is_indexing': self.is_indexing,
            'stats': self.stats,
            'files_tracked': len(self.file_hashes)
        }


class IndexerStatus:
    """
    Simple status tracker for indexer agent.
    Can be used to monitor progress from other threads.
    """
    
    def __init__(self):
        self.current_file: Optional[str] = None
        self.progress: Optional[str] = None
        self.complete = False
        self.results: Optional[Dict] = None
    
    def on_progress(self, file_path: str, progress: str):
        """Called when a file is being indexed."""
        self.current_file = file_path
        self.progress = progress
    
    def on_complete(self, stats: Dict[str, Any]):
        """Called when indexing completes."""
        self.complete = True
        self.results = stats
    
    def reset(self):
        """Reset status."""
        self.current_file = None
        self.progress = None
        self.complete = False
        self.results = None
