#!/usr/bin/env python3
"""
Vector Memory Store - Persistent vector database for agent memory
Implements long-term memory from AGENT_ENHANCEMENT_STRATEGY.md using ChromaDB
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path
import json


class VectorMemoryStore:
    """
    Persistent vector database for storing agent memories.
    
    Uses ChromaDB for efficient vector similarity search.
    Memories can be:
    - Task summaries
    - Error resolutions
    - Code snippets
    - User feedback
    """
    
    def __init__(self, persist_dir: str = "./storage/memory"):
        """
        Initialize vector store.
        
        Args:
            persist_dir: Directory to persist the database
        """
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            import chromadb
        except ImportError:
            raise ImportError(
                "chromadb not installed. Run: pip install chromadb"
            )
        
        # Initialize ChromaDB client (new API)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        
        # Create/get collections for different memory types
        self.collections = {
            'task_summaries': self.client.get_or_create_collection('task_summaries'),
            'error_resolutions': self.client.get_or_create_collection('error_resolutions'),
            'code_snippets': self.client.get_or_create_collection('code_snippets'),
            'user_feedback': self.client.get_or_create_collection('user_feedback'),
        }
    
    def store_memory(
        self,
        memory_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None
    ) -> str:
        """
        Store a memory in the vector database.
        
        Args:
            memory_type: Type of memory ('task_summaries', 'error_resolutions', etc.)
            content: The memory content (text)
            metadata: Additional metadata (tags, timestamps, etc.)
            embedding: Optional pre-computed embedding (if None, ChromaDB will generate)
            
        Returns:
            Memory ID (for later retrieval/updates)
        """
        if memory_type not in self.collections:
            raise ValueError(f"Unknown memory type: {memory_type}")
        
        collection = self.collections[memory_type]
        
        # Generate ID
        memory_id = f"{memory_type}_{datetime.now().timestamp()}"
        
        # Prepare metadata
        if metadata is None:
            metadata = {}
        metadata['timestamp'] = datetime.now().isoformat()
        metadata['type'] = memory_type
        
        # Store in collection
        if embedding:
            collection.add(
                ids=[memory_id],
                documents=[content],
                embeddings=[embedding],
                metadatas=[metadata]
            )
        else:
            collection.add(
                ids=[memory_id],
                documents=[content],
                metadatas=[metadata]
            )
        
        return memory_id
    
    def recall_memories(
        self,
        query: str,
        memory_type: Optional[str] = None,
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Recall relevant memories based on a query.
        
        Args:
            query: The query text to search for relevant memories
            memory_type: Optional filter by memory type
            n_results: Number of results to return
            where: Optional metadata filter
            
        Returns:
            List of relevant memories with content, metadata, and similarity
        """
        results = []
        
        # Search in specified collection(s)
        collections_to_search = (
            [self.collections[memory_type]] if memory_type 
            else list(self.collections.values())
        )
        
        for collection in collections_to_search:
            try:
                search_results = collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    where=where
                )
                
                # Format results
                if search_results['ids'][0]:  # Check if results exist
                    for i, doc_id in enumerate(search_results['ids'][0]):
                        results.append({
                            'id': doc_id,
                            'content': search_results['documents'][0][i],
                            'metadata': search_results['metadatas'][0][i],
                            'distance': search_results['distances'][0][i] if 'distances' in search_results else None
                        })
            except Exception as e:
                print(f"Error searching collection: {e}")
                continue
        
        # Sort by distance (most similar first)
        if results and results[0].get('distance') is not None:
            results.sort(key=lambda x: x['distance'])
        
        return results[:n_results]
    
    def store_task_summary(
        self,
        task: str,
        solution: str,
        agents_involved: List[str],
        success: bool = True
    ) -> str:
        """
        Store a task summary memory.
        
        Args:
            task: Description of the task
            solution: How it was solved
            agents_involved: Which agents worked on it
            success: Whether the task succeeded
            
        Returns:
            Memory ID
        """
        content = f"Task: {task}\nSolution: {solution}"
        metadata = {
            'task': task,
            'agents': ','.join(agents_involved),
            'success': success
        }
        return self.store_memory('task_summaries', content, metadata)
    
    def store_error_resolution(
        self,
        error_type: str,
        error_message: str,
        solution: str,
        context: Optional[str] = None
    ) -> str:
        """
        Store an error resolution memory.
        
        Args:
            error_type: Type of error (e.g., 'TypeError', 'ImportError')
            error_message: The error message
            solution: How it was fixed
            context: Optional context about when/where it occurred
            
        Returns:
            Memory ID
        """
        content = f"Error: {error_type}: {error_message}\nSolution: {solution}"
        if context:
            content += f"\nContext: {context}"
        
        metadata = {
            'error_type': error_type,
            'has_solution': True
        }
        return self.store_memory('error_resolutions', content, metadata)
    
    def store_code_snippet(
        self,
        code: str,
        description: str,
        language: str,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Store a code snippet memory.
        
        Args:
            code: The code snippet
            description: What the code does
            language: Programming language
            tags: Optional tags for categorization
            
        Returns:
            Memory ID
        """
        content = f"Description: {description}\nLanguage: {language}\n\nCode:\n{code}"
        metadata = {
            'language': language,
            'tags': ','.join(tags) if tags else '',
        }
        return self.store_memory('code_snippets', content, metadata)
    
    def get_memory_stats(self) -> Dict[str, int]:
        """Get statistics about stored memories."""
        stats = {}
        for name, collection in self.collections.items():
            stats[name] = collection.count()
        stats['total'] = sum(stats.values())
        return stats
    
    def persist(self):
        """Persist all changes to disk."""
        self.client.persist()
    
    def clear_collection(self, memory_type: str):
        """Clear all memories of a specific type."""
        if memory_type in self.collections:
            # Delete and recreate collection
            try:
                self.client.delete_collection(memory_type)
                self.collections[memory_type] = self.client.create_collection(memory_type)
            except Exception as e:
                print(f"Error clearing collection: {e}")
