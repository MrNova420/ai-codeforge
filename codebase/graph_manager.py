#!/usr/bin/env python3
"""
Codebase Graph Manager - The system's architectural brain
Implements the core Codebase Graph from SCALING_TO_LARGE_PROJECTS.md

This is a persistent, queryable knowledge graph of the entire codebase.
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
import json
from datetime import datetime


@dataclass
class CodeNode:
    """Represents a node in the codebase graph."""
    node_id: str  # Unique identifier
    node_type: str  # file, class, function, variable, etc.
    name: str
    file_path: str
    line_number: Optional[int] = None
    source_code: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    

@dataclass
class CodeRelationship:
    """Represents an edge in the codebase graph."""
    source_id: str
    target_id: str
    rel_type: str  # imports, calls, inherits, implements, references, returns
    metadata: Dict[str, Any] = field(default_factory=dict)


class CodebaseGraphManager:
    """
    Manages the codebase knowledge graph.
    
    This is the "brain" that gives AI agents deep understanding
    of code structure and relationships.
    
    Features:
    - Stores code nodes (files, classes, functions)
    - Tracks relationships (imports, calls, inheritance)
    - Enables semantic queries
    - Supports impact analysis
    """
    
    def __init__(self, project_root: str, storage_dir: str = "./storage/codebase_graph"):
        """
        Initialize graph manager.
        
        Args:
            project_root: Root directory of the codebase to analyze
            storage_dir: Where to persist the graph
        """
        self.project_root = Path(project_root)
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory graph storage
        self.nodes: Dict[str, CodeNode] = {}  # node_id -> CodeNode
        self.relationships: List[CodeRelationship] = []
        
        # Indexes for fast lookups
        self.file_nodes: Dict[str, List[str]] = {}  # file_path -> [node_ids]
        self.type_index: Dict[str, Set[str]] = {}  # node_type -> {node_ids}
        self.name_index: Dict[str, Set[str]] = {}  # name -> {node_ids}
        
        # Load existing graph if available
        self._load_graph()
    
    def add_node(self, node: CodeNode) -> str:
        """
        Add a node to the graph.
        
        Args:
            node: CodeNode to add
            
        Returns:
            Node ID
        """
        # Store node
        self.nodes[node.node_id] = node
        
        # Update indexes
        if node.file_path not in self.file_nodes:
            self.file_nodes[node.file_path] = []
        self.file_nodes[node.file_path].append(node.node_id)
        
        if node.node_type not in self.type_index:
            self.type_index[node.node_type] = set()
        self.type_index[node.node_type].add(node.node_id)
        
        if node.name not in self.name_index:
            self.name_index[node.name] = set()
        self.name_index[node.name].add(node.node_id)
        
        return node.node_id
    
    def add_relationship(self, relationship: CodeRelationship) -> None:
        """Add a relationship between nodes."""
        # Verify nodes exist
        if relationship.source_id not in self.nodes:
            raise ValueError(f"Source node {relationship.source_id} not found")
        if relationship.target_id not in self.nodes:
            raise ValueError(f"Target node {relationship.target_id} not found")
        
        self.relationships.append(relationship)
    
    def get_node(self, node_id: str) -> Optional[CodeNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def find_nodes(
        self,
        name: Optional[str] = None,
        node_type: Optional[str] = None,
        file_path: Optional[str] = None
    ) -> List[CodeNode]:
        """
        Find nodes matching criteria.
        
        Args:
            name: Node name to match
            node_type: Type of node (class, function, etc.)
            file_path: File path to search in
            
        Returns:
            List of matching nodes
        """
        candidates = None
        
        # Use indexes for efficient lookup
        if name:
            candidates = self.name_index.get(name, set())
        if node_type:
            type_nodes = self.type_index.get(node_type, set())
            candidates = type_nodes if candidates is None else candidates & type_nodes
        if file_path:
            file_node_ids = set(self.file_nodes.get(file_path, []))
            candidates = file_node_ids if candidates is None else candidates & file_node_ids
        
        # Get all nodes if no filters
        if candidates is None:
            candidates = set(self.nodes.keys())
        
        return [self.nodes[nid] for nid in candidates if nid in self.nodes]
    
    def get_relationships(
        self,
        source_id: Optional[str] = None,
        target_id: Optional[str] = None,
        rel_type: Optional[str] = None
    ) -> List[CodeRelationship]:
        """
        Get relationships matching criteria.
        
        Args:
            source_id: Filter by source node
            target_id: Filter by target node
            rel_type: Filter by relationship type
            
        Returns:
            List of matching relationships
        """
        results = self.relationships
        
        if source_id:
            results = [r for r in results if r.source_id == source_id]
        if target_id:
            results = [r for r in results if r.target_id == target_id]
        if rel_type:
            results = [r for r in results if r.rel_type == rel_type]
        
        return results
    
    def find_callers(self, function_name: str) -> List[CodeNode]:
        """
        Find all functions that call a given function.
        
        This is a key feature from the strategic plan!
        
        Args:
            function_name: Name of function to find callers for
            
        Returns:
            List of nodes that call this function
        """
        # Find the function node(s)
        function_nodes = self.find_nodes(name=function_name, node_type='function')
        if not function_nodes:
            return []
        
        callers = []
        for func_node in function_nodes:
            # Find relationships where this function is the target of a 'calls' relationship
            calling_rels = self.get_relationships(target_id=func_node.node_id, rel_type='calls')
            for rel in calling_rels:
                caller_node = self.get_node(rel.source_id)
                if caller_node:
                    callers.append(caller_node)
        
        return callers
    
    def find_dependencies(self, node_id: str) -> List[CodeNode]:
        """
        Find all nodes that a given node depends on.
        
        Follows imports, calls, and references.
        
        Args:
            node_id: Node to find dependencies for
            
        Returns:
            List of nodes this node depends on
        """
        dependency_types = ['imports', 'calls', 'references']
        deps = []
        
        for dep_type in dependency_types:
            rels = self.get_relationships(source_id=node_id, rel_type=dep_type)
            for rel in rels:
                target_node = self.get_node(rel.target_id)
                if target_node:
                    deps.append(target_node)
        
        return deps
    
    def impact_analysis(self, node_id: str, max_depth: int = 3) -> Dict[str, Any]:
        """
        Analyze the impact of changing a node.
        
        This is critical for large codebases!
        
        Args:
            node_id: Node to analyze
            max_depth: How deep to traverse relationships
            
        Returns:
            Dict with impact analysis results
        """
        node = self.get_node(node_id)
        if not node:
            return {'error': 'Node not found'}
        
        # Find all nodes that depend on this one
        affected_nodes = []
        visited = set()
        
        def traverse(current_id, depth):
            if depth > max_depth or current_id in visited:
                return
            visited.add(current_id)
            
            # Find all nodes that reference/call/import this node
            incoming = self.get_relationships(target_id=current_id)
            for rel in incoming:
                if rel.source_id not in visited:
                    source_node = self.get_node(rel.source_id)
                    if source_node:
                        affected_nodes.append({
                            'node': source_node,
                            'relationship': rel.rel_type,
                            'depth': depth
                        })
                        traverse(rel.source_id, depth + 1)
        
        traverse(node_id, 1)
        
        # Organize by file
        files_affected = {}
        for item in affected_nodes:
            file_path = item['node'].file_path
            if file_path not in files_affected:
                files_affected[file_path] = []
            files_affected[file_path].append(item)
        
        return {
            'target_node': node,
            'total_affected': len(affected_nodes),
            'files_affected': len(files_affected),
            'affected_nodes': affected_nodes[:20],  # Limit for display
            'files': list(files_affected.keys())
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the graph."""
        type_counts = {
            node_type: len(nodes)
            for node_type, nodes in self.type_index.items()
        }
        
        rel_counts = {}
        for rel in self.relationships:
            rel_counts[rel.rel_type] = rel_counts.get(rel.rel_type, 0) + 1
        
        return {
            'total_nodes': len(self.nodes),
            'total_relationships': len(self.relationships),
            'node_types': type_counts,
            'relationship_types': rel_counts,
            'files_indexed': len(self.file_nodes)
        }
    
    def _save_graph(self) -> None:
        """Persist graph to disk."""
        graph_file = self.storage_dir / "graph.json"
        
        data = {
            'nodes': [
                {
                    'node_id': node.node_id,
                    'node_type': node.node_type,
                    'name': node.name,
                    'file_path': node.file_path,
                    'line_number': node.line_number,
                    'metadata': node.metadata
                    # Don't save source_code to keep size manageable
                }
                for node in self.nodes.values()
            ],
            'relationships': [
                {
                    'source_id': rel.source_id,
                    'target_id': rel.target_id,
                    'rel_type': rel.rel_type,
                    'metadata': rel.metadata
                }
                for rel in self.relationships
            ],
            'metadata': {
                'project_root': str(self.project_root),
                'last_updated': datetime.now().isoformat(),
                'stats': self.get_stats()
            }
        }
        
        with open(graph_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_graph(self) -> None:
        """Load graph from disk."""
        graph_file = self.storage_dir / "graph.json"
        
        if not graph_file.exists():
            return
        
        try:
            with open(graph_file) as f:
                data = json.load(f)
            
            # Load nodes
            for node_data in data.get('nodes', []):
                node = CodeNode(**node_data)
                self.add_node(node)
            
            # Load relationships
            for rel_data in data.get('relationships', []):
                rel = CodeRelationship(**rel_data)
                try:
                    self.add_relationship(rel)
                except ValueError:
                    # Skip relationships with missing nodes
                    pass
                    
        except Exception as e:
            print(f"Warning: Could not load graph: {e}")
    
    def persist(self) -> None:
        """Save graph to disk."""
        self._save_graph()
    
    def clear(self) -> None:
        """Clear all graph data."""
        self.nodes.clear()
        self.relationships.clear()
        self.file_nodes.clear()
        self.type_index.clear()
        self.name_index.clear()
