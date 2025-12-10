"""
Codebase Graph System - Deep code understanding
Implements the "Codebase Graph" from SCALING_TO_LARGE_PROJECTS.md

This system provides:
- AST-based code parsing
- Relationship tracking (calls, imports, inherits, etc.)
- Semantic search across codebase
- Impact analysis
"""

from .graph_manager import CodebaseGraphManager
from .ast_parser import ASTParser
from .query_engine import QueryEngine

__all__ = ['CodebaseGraphManager', 'ASTParser', 'QueryEngine']
