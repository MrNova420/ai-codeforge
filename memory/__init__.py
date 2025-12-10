"""
Memory System - Persistent learning for AI agents
Implements vector-based long-term memory from AGENT_ENHANCEMENT_STRATEGY.md
"""

from .vector_store import VectorMemoryStore
from .embedding_service import EmbeddingService

__all__ = ['VectorMemoryStore', 'EmbeddingService']
