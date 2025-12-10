#!/usr/bin/env python3
"""
AST Parser - Analyzes Python code to build the codebase graph
Extracts functions, classes, imports, and their relationships
"""

import ast
from typing import List, Dict, Set, Optional
from pathlib import Path
from .graph_manager import CodeNode, CodeRelationship, CodebaseGraphManager


class ASTParser:
    """
    Parses Python files using AST to extract code structure.
    
    Extracts:
    - Functions and their parameters
    - Classes and their methods
    - Imports and dependencies
    - Function calls
    - Class inheritance
    """
    
    def __init__(self, graph_manager: CodebaseGraphManager):
        """
        Initialize parser.
        
        Args:
            graph_manager: Graph to populate with parsed data
        """
        self.graph = graph_manager
    
    def parse_file(self, file_path: str) -> Dict[str, any]:
        """
        Parse a Python file and add it to the graph.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dict with parsing results
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'error': f'File not found: {file_path}'}
        
        if not file_path.suffix == '.py':
            return {'error': 'Not a Python file'}
        
        try:
            with open(file_path) as f:
                source = f.read()
            
            # Parse AST
            tree = ast.parse(source, filename=str(file_path))
            
            # Extract components
            results = {
                'file': str(file_path),
                'nodes_added': 0,
                'relationships_added': 0
            }
            
            # Add file node
            file_node_id = f"file:{file_path}"
            file_node = CodeNode(
                node_id=file_node_id,
                node_type='file',
                name=file_path.name,
                file_path=str(file_path),
                metadata={'lines': len(source.splitlines())}
            )
            self.graph.add_node(file_node)
            results['nodes_added'] += 1
            
            # Visit all nodes in AST
            visitor = CodeVisitor(self.graph, str(file_path), source)
            visitor.visit(tree)
            
            results['nodes_added'] += visitor.nodes_added
            results['relationships_added'] += visitor.relationships_added
            
            return results
            
        except SyntaxError as e:
            return {'error': f'Syntax error: {e}'}
        except Exception as e:
            return {'error': f'Parse error: {e}'}
    
    def parse_directory(self, directory: str, recursive: bool = True) -> Dict[str, any]:
        """
        Parse all Python files in a directory.
        
        Args:
            directory: Directory to scan
            recursive: Whether to recurse into subdirectories
            
        Returns:
            Dict with overall results
        """
        directory = Path(directory)
        
        if not directory.is_dir():
            return {'error': 'Not a directory'}
        
        # Find Python files
        pattern = '**/*.py' if recursive else '*.py'
        py_files = list(directory.glob(pattern))
        
        results = {
            'files_parsed': 0,
            'files_failed': 0,
            'total_nodes': 0,
            'total_relationships': 0,
            'errors': []
        }
        
        for py_file in py_files:
            # Skip __pycache__ and venv
            if '__pycache__' in str(py_file) or 'venv' in str(py_file):
                continue
            
            file_result = self.parse_file(str(py_file))
            
            if 'error' in file_result:
                results['files_failed'] += 1
                results['errors'].append({
                    'file': str(py_file),
                    'error': file_result['error']
                })
            else:
                results['files_parsed'] += 1
                results['total_nodes'] += file_result['nodes_added']
                results['total_relationships'] += file_result['relationships_added']
        
        return results


class CodeVisitor(ast.NodeVisitor):
    """
    AST visitor that extracts code elements and relationships.
    """
    
    def __init__(self, graph: CodebaseGraphManager, file_path: str, source: str):
        self.graph = graph
        self.file_path = file_path
        self.source = source
        self.source_lines = source.splitlines()
        
        self.nodes_added = 0
        self.relationships_added = 0
        
        # Track current context
        self.current_class: Optional[str] = None
        self.current_function: Optional[str] = None
    
    def visit_Import(self, node: ast.Import):
        """Handle import statements."""
        for alias in node.names:
            module_name = alias.name
            
            # Create node for import
            import_id = f"import:{self.file_path}:{module_name}"
            import_node = CodeNode(
                node_id=import_id,
                node_type='import',
                name=module_name,
                file_path=self.file_path,
                line_number=node.lineno
            )
            self.graph.add_node(import_node)
            self.nodes_added += 1
            
            # Create relationship from file to import
            file_id = f"file:{self.file_path}"
            rel = CodeRelationship(
                source_id=file_id,
                target_id=import_id,
                rel_type='imports'
            )
            self.graph.add_relationship(rel)
            self.relationships_added += 1
        
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Handle from X import Y statements."""
        module = node.module or ''
        
        for alias in node.names:
            import_name = f"{module}.{alias.name}" if module else alias.name
            
            # Create import node
            import_id = f"import:{self.file_path}:{import_name}"
            import_node = CodeNode(
                node_id=import_id,
                node_type='import',
                name=import_name,
                file_path=self.file_path,
                line_number=node.lineno
            )
            self.graph.add_node(import_node)
            self.nodes_added += 1
            
            # Create relationship
            file_id = f"file:{self.file_path}"
            rel = CodeRelationship(
                source_id=file_id,
                target_id=import_id,
                rel_type='imports'
            )
            self.graph.add_relationship(rel)
            self.relationships_added += 1
        
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef):
        """Handle class definitions."""
        class_name = node.name
        class_id = f"class:{self.file_path}:{class_name}"
        
        # Get source code for this class
        source_lines = self.source_lines[node.lineno - 1:node.end_lineno]
        source_code = '\n'.join(source_lines) if source_lines else ''
        
        # Create class node
        class_node = CodeNode(
            node_id=class_id,
            node_type='class',
            name=class_name,
            file_path=self.file_path,
            line_number=node.lineno,
            source_code=source_code[:500],  # Limit size
            metadata={
                'bases': [self._get_name(base) for base in node.bases],
                'decorators': [self._get_name(dec) for dec in node.decorator_list]
            }
        )
        self.graph.add_node(class_node)
        self.nodes_added += 1
        
        # Create relationship from file to class
        file_id = f"file:{self.file_path}"
        rel = CodeRelationship(
            source_id=file_id,
            target_id=class_id,
            rel_type='contains'
        )
        self.graph.add_relationship(rel)
        self.relationships_added += 1
        
        # Handle inheritance
        for base in node.bases:
            base_name = self._get_name(base)
            if base_name:
                # Find or create base class node
                base_id = f"class:{base_name}"
                rel = CodeRelationship(
                    source_id=class_id,
                    target_id=base_id,
                    rel_type='inherits'
                )
                try:
                    self.graph.add_relationship(rel)
                    self.relationships_added += 1
                except ValueError:
                    # Base class not in graph yet
                    pass
        
        # Visit class body with context
        old_class = self.current_class
        self.current_class = class_id
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Handle function/method definitions."""
        func_name = node.name
        
        # Determine if this is a method or standalone function
        if self.current_class:
            func_id = f"method:{self.current_class}:{func_name}"
            node_type = 'method'
        else:
            func_id = f"function:{self.file_path}:{func_name}"
            node_type = 'function'
        
        # Get source code
        source_lines = self.source_lines[node.lineno - 1:node.end_lineno]
        source_code = '\n'.join(source_lines) if source_lines else ''
        
        # Extract parameters
        params = [arg.arg for arg in node.args.args]
        
        # Create function node
        func_node = CodeNode(
            node_id=func_id,
            node_type=node_type,
            name=func_name,
            file_path=self.file_path,
            line_number=node.lineno,
            source_code=source_code[:500],
            metadata={
                'parameters': params,
                'decorators': [self._get_name(dec) for dec in node.decorator_list]
            }
        )
        self.graph.add_node(func_node)
        self.nodes_added += 1
        
        # Create relationship to parent (file or class)
        parent_id = self.current_class if self.current_class else f"file:{self.file_path}"
        rel = CodeRelationship(
            source_id=parent_id,
            target_id=func_id,
            rel_type='contains'
        )
        self.graph.add_relationship(rel)
        self.relationships_added += 1
        
        # Visit function body with context
        old_func = self.current_function
        self.current_function = func_id
        self.generic_visit(node)
        self.current_function = old_func
    
    def visit_Call(self, node: ast.Call):
        """Handle function calls."""
        if self.current_function:
            # Get the function being called
            called_func_name = self._get_name(node.func)
            
            if called_func_name:
                # Create relationship showing this function calls another
                called_func_id = f"function:{called_func_name}"
                
                rel = CodeRelationship(
                    source_id=self.current_function,
                    target_id=called_func_id,
                    rel_type='calls'
                )
                
                try:
                    self.graph.add_relationship(rel)
                    self.relationships_added += 1
                except ValueError:
                    # Called function not in graph
                    pass
        
        self.generic_visit(node)
    
    def _get_name(self, node) -> Optional[str]:
        """Extract name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value_name = self._get_name(node.value)
            return f"{value_name}.{node.attr}" if value_name else node.attr
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return None
