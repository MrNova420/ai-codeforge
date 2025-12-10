#!/usr/bin/env python3
"""
Query Engine - Semantic code queries on the codebase graph
Enables natural language questions about code structure
"""

from typing import List, Dict, Any, Optional
from .graph_manager import CodebaseGraphManager, CodeNode


class QueryEngine:
    """
    High-level query interface for the codebase graph.
    
    Provides semantic queries that agents can use to understand code.
    """
    
    def __init__(self, graph: CodebaseGraphManager):
        """
        Initialize query engine.
        
        Args:
            graph: Codebase graph to query
        """
        self.graph = graph
    
    def find_function(self, name: str) -> List[CodeNode]:
        """Find all functions with a given name."""
        return self.graph.find_nodes(name=name, node_type='function')
    
    def find_class(self, name: str) -> List[CodeNode]:
        """Find all classes with a given name."""
        return self.graph.find_nodes(name=name, node_type='class')
    
    def what_calls(self, function_name: str) -> Dict[str, Any]:
        """
        Answer: "What calls this function?"
        
        Args:
            function_name: Function to find callers for
            
        Returns:
            Dict with caller information
        """
        callers = self.graph.find_callers(function_name)
        
        return {
            'function': function_name,
            'caller_count': len(callers),
            'callers': [
                {
                    'name': caller.name,
                    'type': caller.node_type,
                    'file': caller.file_path,
                    'line': caller.line_number
                }
                for caller in callers
            ]
        }
    
    def what_does_it_call(self, function_name: str) -> Dict[str, Any]:
        """
        Answer: "What does this function call?"
        
        Args:
            function_name: Function to analyze
            
        Returns:
            Dict with called functions
        """
        # Find the function
        functions = self.find_function(function_name)
        if not functions:
            return {'error': f'Function {function_name} not found'}
        
        func_node = functions[0]
        
        # Get what it calls
        calls = self.graph.get_relationships(
            source_id=func_node.node_id,
            rel_type='calls'
        )
        
        called_functions = []
        for call_rel in calls:
            target = self.graph.get_node(call_rel.target_id)
            if target:
                called_functions.append({
                    'name': target.name,
                    'type': target.node_type,
                    'file': target.file_path
                })
        
        return {
            'function': function_name,
            'calls_count': len(called_functions),
            'calls': called_functions
        }
    
    def what_imports(self, module_name: str) -> Dict[str, Any]:
        """
        Answer: "What files import this module?"
        
        Args:
            module_name: Module to find importers for
            
        Returns:
            Dict with importing files
        """
        import_rels = self.graph.get_relationships(rel_type='imports')
        
        importers = []
        for rel in import_rels:
            target = self.graph.get_node(rel.target_id)
            if target and module_name in target.name:
                source = self.graph.get_node(rel.source_id)
                if source:
                    importers.append({
                        'file': source.file_path,
                        'import': target.name,
                        'line': target.line_number
                    })
        
        return {
            'module': module_name,
            'imported_by': len(importers),
            'importers': importers
        }
    
    def what_inherits_from(self, class_name: str) -> Dict[str, Any]:
        """
        Answer: "What classes inherit from this class?"
        
        Args:
            class_name: Base class name
            
        Returns:
            Dict with child classes
        """
        # Find child classes
        inherit_rels = self.graph.get_relationships(rel_type='inherits')
        
        children = []
        for rel in inherit_rels:
            target = self.graph.get_node(rel.target_id)
            if target and class_name in target.name:
                source = self.graph.get_node(rel.source_id)
                if source:
                    children.append({
                        'name': source.name,
                        'file': source.file_path,
                        'line': source.line_number
                    })
        
        return {
            'base_class': class_name,
            'child_count': len(children),
            'children': children
        }
    
    def impact_of_changing(self, item_name: str) -> Dict[str, Any]:
        """
        Answer: "What will break if I change this?"
        
        Critical for large codebases!
        
        Args:
            item_name: Function, class, etc. to analyze
            
        Returns:
            Impact analysis
        """
        # Find the item
        candidates = (
            self.find_function(item_name) or
            self.find_class(item_name) or
            self.graph.find_nodes(name=item_name)
        )
        
        if not candidates:
            return {'error': f'{item_name} not found in codebase'}
        
        item_node = candidates[0]
        
        # Use graph's impact analysis
        return self.graph.impact_analysis(item_node.node_id)
    
    def where_is_defined(self, item_name: str) -> Dict[str, Any]:
        """
        Answer: "Where is this defined?"
        
        Args:
            item_name: Item to locate
            
        Returns:
            Location information
        """
        nodes = self.graph.find_nodes(name=item_name)
        
        if not nodes:
            return {'error': f'{item_name} not found'}
        
        locations = [
            {
                'type': node.node_type,
                'file': node.file_path,
                'line': node.line_number,
                'source': node.source_code[:200] if node.source_code else None
            }
            for node in nodes
        ]
        
        return {
            'item': item_name,
            'found': len(locations),
            'locations': locations
        }
    
    def list_all_functions(self) -> List[str]:
        """Get all function names in the codebase."""
        functions = self.graph.find_nodes(node_type='function')
        return [f.name for f in functions]
    
    def list_all_classes(self) -> List[str]:
        """Get all class names in the codebase."""
        classes = self.graph.find_nodes(node_type='class')
        return [c.name for c in classes]
    
    def get_file_overview(self, file_path: str) -> Dict[str, Any]:
        """
        Get an overview of a file's contents.
        
        Args:
            file_path: File to analyze
            
        Returns:
            Overview with classes, functions, imports
        """
        nodes = self.graph.find_nodes(file_path=file_path)
        
        overview = {
            'file': file_path,
            'classes': [],
            'functions': [],
            'imports': []
        }
        
        for node in nodes:
            if node.node_type == 'class':
                overview['classes'].append(node.name)
            elif node.node_type == 'function':
                overview['functions'].append(node.name)
            elif node.node_type == 'import':
                overview['imports'].append(node.name)
        
        return overview
    
    def search_by_pattern(self, pattern: str) -> List[CodeNode]:
        """
        Search for nodes matching a pattern.
        
        Args:
            pattern: Pattern to search for (simple substring match)
            
        Returns:
            List of matching nodes
        """
        pattern_lower = pattern.lower()
        matches = []
        
        for node in self.graph.nodes.values():
            if (pattern_lower in node.name.lower() or
                (node.source_code and pattern_lower in node.source_code.lower())):
                matches.append(node)
        
        return matches
