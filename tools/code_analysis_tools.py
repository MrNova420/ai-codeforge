#!/usr/bin/env python3
"""
Code Analysis Tools - Static analysis, linting, complexity metrics
Advanced code quality tools for agents
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import subprocess
import json
from tools.base_tool import BaseTool, ToolResult


class LinterTool(BaseTool):
    """Run code linters (pylint, eslint, etc.)."""
    
    name = "linter"
    description = "Run code linter for quality checks"
    
    def __call__(
        self,
        file_path: str,
        language: str = "python",
        config: Optional[str] = None
    ) -> ToolResult:
        """Run linter on file."""
        try:
            if language == "python":
                cmd = ['pylint', file_path]
                if config:
                    cmd.extend(['--rcfile', config])
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                # Parse pylint output
                issues = self._parse_pylint_output(result.stdout)
                score = self._extract_pylint_score(result.stdout)
                
                return ToolResult(
                    success=len(issues) == 0,
                    data={
                        'language': language,
                        'file': file_path,
                        'score': score,
                        'issues': issues,
                        'raw_output': result.stdout
                    }
                )
            
            else:
                return ToolResult(
                    success=False,
                    data={},
                    error=f"Linter not implemented for {language}"
                )
        
        except FileNotFoundError:
            return ToolResult(
                success=False,
                data={},
                error=f"Linter not installed for {language}"
            )
        except Exception as e:
            return ToolResult(success=False, data={}, error=str(e))
    
    def _parse_pylint_output(self, output: str) -> List[Dict]:
        """Parse pylint output into structured issues."""
        issues = []
        for line in output.split('\n'):
            if ':' in line and any(c in line for c in ['C:', 'R:', 'W:', 'E:', 'F:']):
                parts = line.split(':', 3)
                if len(parts) >= 4:
                    issues.append({
                        'line': parts[1].strip(),
                        'column': parts[2].strip(),
                        'message': parts[3].strip()
                    })
        return issues
    
    def _extract_pylint_score(self, output: str) -> Optional[float]:
        """Extract score from pylint output."""
        for line in output.split('\n'):
            if 'Your code has been rated at' in line:
                try:
                    score = float(line.split()[6].split('/')[0])
                    return score
                except:
                    pass
        return None


class ComplexityAnalyzerTool(BaseTool):
    """Analyze code complexity (cyclomatic complexity)."""
    
    name = "complexity_analyzer"
    description = "Analyze code complexity metrics"
    
    def __call__(
        self,
        file_path: str,
        threshold: int = 10
    ) -> ToolResult:
        """Analyze code complexity."""
        try:
            # Use radon for Python complexity
            result = subprocess.run(
                ['radon', 'cc', file_path, '-j'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                try:
                    complexity_data = json.loads(result.stdout)
                    
                    # Analyze results
                    functions = []
                    high_complexity = []
                    
                    for file_data in complexity_data.values():
                        for func in file_data:
                            functions.append({
                                'name': func['name'],
                                'complexity': func['complexity'],
                                'line': func['lineno']
                            })
                            
                            if func['complexity'] > threshold:
                                high_complexity.append(func['name'])
                    
                    avg_complexity = sum(f['complexity'] for f in functions) / len(functions) if functions else 0
                    
                    return ToolResult(
                        success=len(high_complexity) == 0,
                        data={
                            'file': file_path,
                            'total_functions': len(functions),
                            'average_complexity': round(avg_complexity, 2),
                            'high_complexity_functions': high_complexity,
                            'threshold': threshold,
                            'functions': functions
                        }
                    )
                except json.JSONDecodeError:
                    pass
            
            # Fallback: simple line count analysis
            with open(file_path) as f:
                lines = f.readlines()
            
            return ToolResult(
                success=True,
                data={
                    'file': file_path,
                    'total_lines': len(lines),
                    'note': 'Install radon for detailed complexity: pip install radon'
                }
            )
        
        except Exception as e:
            return ToolResult(success=False, data={}, error=str(e))


class SecurityScannerTool(BaseTool):
    """Scan code for security vulnerabilities."""
    
    name = "security_scanner"
    description = "Scan code for security issues"
    
    def __call__(
        self,
        file_path: str,
        language: str = "python"
    ) -> ToolResult:
        """Scan for security issues."""
        try:
            if language == "python":
                # Use bandit for Python security
                result = subprocess.run(
                    ['bandit', '-f', 'json', file_path],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                try:
                    scan_results = json.loads(result.stdout)
                    issues = scan_results.get('results', [])
                    
                    # Categorize by severity
                    critical = [i for i in issues if i.get('issue_severity') == 'HIGH']
                    high = [i for i in issues if i.get('issue_severity') == 'MEDIUM']
                    low = [i for i in issues if i.get('issue_severity') == 'LOW']
                    
                    return ToolResult(
                        success=len(critical) == 0,
                        data={
                            'file': file_path,
                            'total_issues': len(issues),
                            'critical': len(critical),
                            'high': len(high),
                            'low': len(low),
                            'issues': issues[:10]  # Top 10 issues
                        },
                        error="Critical security issues found" if critical else None
                    )
                except json.JSONDecodeError:
                    pass
            
            return ToolResult(
                success=True,
                data={'note': f'Security scanner not available for {language}'}
            )
        
        except FileNotFoundError:
            return ToolResult(
                success=True,
                data={'note': 'Install bandit for Python security: pip install bandit'}
            )
        except Exception as e:
            return ToolResult(success=False, data={}, error=str(e))
