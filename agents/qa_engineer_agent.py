#!/usr/bin/env python3
"""
QA Engineer Agent - Test generation and quality assurance
Part of AGENT_ENHANCEMENT_STRATEGY.md implementation

This agent specializes in:
- Generating comprehensive unit tests
- Writing integration tests
- Analyzing code coverage
- Identifying edge cases
- Test execution and reporting
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import subprocess
import tempfile
from pathlib import Path
import json


@dataclass
class TestSuite:
    """Collection of generated tests."""
    test_code: str
    language: str
    framework: str
    test_count: int
    categories: List[str]  # happy_path, edge_cases, error_handling
    

@dataclass
class CoverageReport:
    """Code coverage analysis report."""
    overall_coverage: float
    line_coverage: float
    branch_coverage: float
    uncovered_lines: List[int]
    covered_files: Dict[str, float]


class QAEngineerAgent:
    """
    QA Engineer - The team's quality assurance specialist.
    
    This agent ensures code quality by:
    1. Generating comprehensive tests
    2. Identifying edge cases
    3. Analyzing code coverage
    4. Running tests and reporting results
    
    Philosophy: "If it's not tested, it's broken."
    """
    
    def __init__(self, llm_agent=None):
        """
        Initialize QA Engineer.
        
        Args:
            llm_agent: Base LLM agent for test generation
        """
        self.llm_agent = llm_agent
        self.test_frameworks = {
            'python': 'pytest',
            'javascript': 'jest',
            'typescript': 'jest',
            'java': 'junit',
            'go': 'testing'
        }
    
    def generate_tests(
        self,
        code: str,
        language: str = 'python',
        include_integration: bool = False
    ) -> TestSuite:
        """
        Generate comprehensive unit tests for given code.
        
        Args:
            code: Source code to test
            language: Programming language
            include_integration: Whether to include integration tests
            
        Returns:
            TestSuite with generated tests
        """
        framework = self.test_frameworks.get(language, 'pytest')
        
        # Generate test prompt
        prompt = self._create_test_generation_prompt(code, language, framework, include_integration)
        
        # Generate tests using LLM
        if self.llm_agent:
            test_code = self._generate_with_llm(prompt)
        else:
            test_code = self._generate_fallback_tests(code, language)
        
        # Analyze generated tests
        categories = self._analyze_test_categories(test_code)
        test_count = self._count_tests(test_code, language)
        
        return TestSuite(
            test_code=test_code,
            language=language,
            framework=framework,
            test_count=test_count,
            categories=categories
        )
    
    def _create_test_generation_prompt(
        self,
        code: str,
        language: str,
        framework: str,
        include_integration: bool
    ) -> str:
        """Create detailed prompt for test generation."""
        prompt = f"""You are an expert QA Engineer. Generate comprehensive {framework} tests for this {language} code.

CODE TO TEST:
```{language}
{code}
```

REQUIREMENTS:
1. **Happy Path Tests**: Test normal, expected usage
2. **Edge Cases**: Test boundary conditions, empty inputs, maximum values
3. **Error Handling**: Test invalid inputs, exceptions, error conditions
4. **Input Validation**: Test type checking, range validation
5. **State Changes**: Test that functions modify state correctly
"""
        
        if include_integration:
            prompt += "\n6. **Integration Tests**: Test interactions between components\n"
        
        prompt += f"""
BEST PRACTICES:
- Use descriptive test names (test_should_return_empty_list_when_input_is_none)
- One assertion per test when possible
- Setup and teardown properly
- Use {framework} features (fixtures, parametrize, mocking)
- Include docstrings explaining what each test validates

Generate ONLY the test code, properly formatted for {framework}.
"""
        return prompt
    
    def _generate_with_llm(self, prompt: str) -> str:
        """Generate tests using LLM."""
        try:
            if hasattr(self.llm_agent, 'generate'):
                return self.llm_agent.generate(prompt)
            elif hasattr(self.llm_agent, 'send_message'):
                return self.llm_agent.send_message(prompt)
            else:
                return """# ERROR: LLM agent not properly initialized
# To use QA Engineer's test generation:
# 1. Ensure an LLM agent is provided when creating QAEngineerAgent
# 2. Configure API keys in config.yaml (OpenAI, Gemini) or start Ollama
# 3. Fallback: Use _generate_fallback_tests() for template-based tests
"""
        except Exception as e:
            return f"""# Error generating tests: {e}
# Check LLM configuration and connectivity
# Using fallback template tests instead
{self._generate_fallback_tests('', 'python')}
"""
    
    def _generate_fallback_tests(self, code: str, language: str) -> str:
        """Generate basic template tests when LLM not available."""
        if language == 'python':
            return f"""import pytest

# TODO: Add specific tests for your code

def test_basic_functionality():
    \"\"\"Test basic functionality.\"\"\"
    # Arrange
    # Act
    # Assert
    pass

def test_edge_cases():
    \"\"\"Test edge cases.\"\"\"
    pass

def test_error_handling():
    \"\"\"Test error handling.\"\"\"
    with pytest.raises(Exception):
        pass
"""
        return f"# Tests for {language} code\n"
    
    def _analyze_test_categories(self, test_code: str) -> List[str]:
        """Identify what test categories are covered."""
        categories = []
        
        test_lower = test_code.lower()
        
        if any(kw in test_lower for kw in ['happy', 'normal', 'valid', 'success']):
            categories.append('happy_path')
        
        if any(kw in test_lower for kw in ['edge', 'boundary', 'empty', 'null', 'zero']):
            categories.append('edge_cases')
        
        if any(kw in test_lower for kw in ['error', 'exception', 'invalid', 'raises']):
            categories.append('error_handling')
        
        if any(kw in test_lower for kw in ['mock', 'patch', 'integration']):
            categories.append('integration')
        
        return categories if categories else ['general']
    
    def _count_tests(self, test_code: str, language: str) -> int:
        """Count number of test functions in generated code."""
        if language == 'python':
            return test_code.count('def test_')
        elif language in ['javascript', 'typescript']:
            return test_code.count('test(') + test_code.count('it(')
        else:
            return test_code.count('test')
    
    def run_tests(
        self,
        test_code: str,
        source_code: Optional[str] = None,
        language: str = 'python'
    ) -> Dict[str, Any]:
        """
        Execute generated tests and return results.
        
        Args:
            test_code: Test code to run
            source_code: Optional source code to test
            language: Programming language
            
        Returns:
            Test execution results
        """
        if language == 'python':
            return self._run_python_tests(test_code, source_code)
        else:
            return {'success': False, 'error': f'Unsupported language: {language}'}
    
    def _run_python_tests(
        self,
        test_code: str,
        source_code: Optional[str]
    ) -> Dict[str, Any]:
        """Run Python tests with pytest."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                tmppath = Path(tmpdir)
                
                # Write source code if provided
                if source_code:
                    (tmppath / 'source.py').write_text(source_code)
                
                # Write test code
                test_file = tmppath / 'test_generated.py'
                test_file.write_text(test_code)
                
                # Run pytest
                result = subprocess.run(
                    ['python3', '-m', 'pytest', str(test_file), '-v', '--tb=short'],
                    capture_output=True,
                    text=True,
                    cwd=str(tmppath),
                    timeout=30
                )
                
                # Parse results
                output = result.stdout + result.stderr
                passed = output.count(' PASSED')
                failed = output.count(' FAILED')
                
                return {
                    'success': result.returncode == 0,
                    'passed': passed,
                    'failed': failed,
                    'output': output,
                    'return_code': result.returncode
                }
        
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Tests timed out after 30s'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_coverage(
        self,
        code_path: str,
        test_path: Optional[str] = None
    ) -> CoverageReport:
        """
        Analyze code coverage.
        
        Args:
            code_path: Path to source code
            test_path: Optional path to tests
            
        Returns:
            CoverageReport with coverage metrics
        """
        try:
            # Run pytest with coverage
            cmd = ['python3', '-m', 'pytest', '--cov=' + code_path]
            if test_path:
                cmd.append(test_path)
            cmd.extend(['--cov-report=json', '--cov-report=term'])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Parse coverage report
            try:
                coverage_file = Path('.coverage.json')
                if coverage_file.exists():
                    with open(coverage_file) as f:
                        cov_data = json.load(f)
                    
                    overall = cov_data.get('totals', {}).get('percent_covered', 0.0)
                    
                    return CoverageReport(
                        overall_coverage=overall,
                        line_coverage=overall,  # Simplified
                        branch_coverage=0.0,  # Would need more parsing
                        uncovered_lines=[],
                        covered_files={}
                    )
            except:
                pass
            
            # Fallback: parse terminal output
            output = result.stdout
            overall = self._extract_coverage_percentage(output)
            
            return CoverageReport(
                overall_coverage=overall,
                line_coverage=overall,
                branch_coverage=0.0,
                uncovered_lines=[],
                covered_files={}
            )
        
        except Exception as e:
            return CoverageReport(
                overall_coverage=0.0,
                line_coverage=0.0,
                branch_coverage=0.0,
                uncovered_lines=[],
                covered_files={}
            )
    
    def _extract_coverage_percentage(self, output: str) -> float:
        """Extract coverage percentage from pytest output."""
        import re
        match = re.search(r'(\d+)%', output)
        if match:
            return float(match.group(1))
        return 0.0
    
    def suggest_test_improvements(self, test_code: str, coverage: CoverageReport) -> List[str]:
        """
        Suggest improvements for test coverage.
        
        Args:
            test_code: Current test code
            coverage: Coverage report
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Coverage-based suggestions
        if coverage.overall_coverage < 80:
            suggestions.append(f"Coverage is {coverage.overall_coverage:.1f}%. Aim for 80%+ coverage.")
        
        if coverage.overall_coverage < 50:
            suggestions.append("Critical: Many code paths untested. Add tests for uncovered functions.")
        
        # Test category suggestions
        categories = self._analyze_test_categories(test_code)
        
        if 'happy_path' not in categories:
            suggestions.append("Add happy path tests for normal usage scenarios.")
        
        if 'edge_cases' not in categories:
            suggestions.append("Add edge case tests (empty inputs, boundaries, null values).")
        
        if 'error_handling' not in categories:
            suggestions.append("Add error handling tests (exceptions, invalid inputs).")
        
        # Specific improvements
        test_count = self._count_tests(test_code, 'python')
        if test_count < 5:
            suggestions.append(f"Only {test_count} tests found. Consider adding more comprehensive tests.")
        
        return suggestions
    
    def generate_test_report(
        self,
        test_suite: TestSuite,
        run_results: Optional[Dict] = None,
        coverage: Optional[CoverageReport] = None
    ) -> str:
        """
        Generate comprehensive test report.
        
        Args:
            test_suite: Generated test suite
            run_results: Optional test execution results
            coverage: Optional coverage report
            
        Returns:
            Formatted test report
        """
        report = "# QA Engineer Test Report\n\n"
        
        # Test Suite Info
        report += "## Generated Test Suite\n"
        report += f"- **Framework**: {test_suite.framework}\n"
        report += f"- **Language**: {test_suite.language}\n"
        report += f"- **Test Count**: {test_suite.test_count}\n"
        report += f"- **Categories**: {', '.join(test_suite.categories)}\n\n"
        
        # Execution Results
        if run_results:
            report += "## Test Execution Results\n"
            if run_results.get('success'):
                report += f"✅ **All tests passed** ({run_results.get('passed', 0)} passed)\n"
            else:
                report += f"❌ **Tests failed** ({run_results.get('failed', 0)} failed, {run_results.get('passed', 0)} passed)\n"
            report += "\n"
        
        # Coverage Analysis
        if coverage:
            report += "## Code Coverage\n"
            report += f"- **Overall**: {coverage.overall_coverage:.1f}%\n"
            report += f"- **Line Coverage**: {coverage.line_coverage:.1f}%\n"
            
            if coverage.overall_coverage >= 80:
                report += "\n✅ Excellent coverage!\n"
            elif coverage.overall_coverage >= 60:
                report += "\n⚠️  Good coverage, room for improvement\n"
            else:
                report += "\n❌ Low coverage, needs more tests\n"
            report += "\n"
        
        # Recommendations
        if coverage:
            suggestions = self.suggest_test_improvements(test_suite.test_code, coverage)
            if suggestions:
                report += "## Recommendations\n"
                for i, suggestion in enumerate(suggestions, 1):
                    report += f"{i}. {suggestion}\n"
        
        return report
