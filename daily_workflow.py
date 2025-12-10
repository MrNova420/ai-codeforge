#!/usr/bin/env python3
"""
Daily Workflow System - Streamlined for production daily use
Quick access to common development tasks

Usage:
    from daily_workflow import DailyWorkflow
    
    workflow = DailyWorkflow()
    workflow.quick_code("Create REST API for users")
    workflow.quick_test("tests/test_api.py")
    workflow.quick_review("src/api.py")
"""

from typing import Dict, List, Optional, Any
from agents.universal_agent_interface import UniversalAgent, ask_agent
from performance_optimizer import get_performance_monitor
from datetime import datetime


class DailyWorkflow:
    """
    Streamlined workflows for daily development.
    
    Everything you need for daily coding:
    - Quick code generation
    - Instant testing
    - Fast reviews
    - Architecture planning
    - Bug fixing
    - Documentation
    """
    
    def __init__(self, use_cache: bool = True):
        """Initialize daily workflow."""
        self.use_cache = use_cache
        self.session_log: List[Dict] = []
        
        # Initialize commonly used agents
        self.coder = UniversalAgent("felix")  # Fast coder
        self.tester = UniversalAgent("quinn")  # QA expert
        self.reviewer = UniversalAgent("orion")  # Code reviewer
        self.architect = UniversalAgent("aurora")  # System designer
        self.fixer = UniversalAgent("patch")  # Bug fixer
        self.writer = UniversalAgent("pixel")  # Documentation
    
    def quick_code(self, task: str, language: str = "python") -> str:
        """
        Quick code generation.
        
        Args:
            task: What to code
            language: Programming language
            
        Returns:
            Generated code
        """
        prompt = f"Language: {language}\nTask: {task}\n\nProvide clean, production-ready code."
        
        with get_performance_monitor().track_operation("quick_code"):
            response = self.coder(prompt)
        
        self._log_activity("code_generation", task, str(response))
        return str(response)
    
    def quick_test(self, code_or_file: str, test_type: str = "unit") -> str:
        """
        Quick test generation.
        
        Args:
            code_or_file: Code to test or file path
            test_type: Type of tests (unit, integration, e2e)
            
        Returns:
            Test code
        """
        prompt = f"Generate {test_type} tests for:\n\n{code_or_file}"
        
        with get_performance_monitor().track_operation("quick_test"):
            response = self.tester(prompt)
        
        self._log_activity("test_generation", code_or_file[:50], str(response))
        return str(response)
    
    def quick_review(self, code_or_file: str) -> Dict[str, Any]:
        """
        Quick code review.
        
        Args:
            code_or_file: Code or file to review
            
        Returns:
            Review with suggestions
        """
        prompt = f"Review this code for quality, bugs, and improvements:\n\n{code_or_file}"
        
        with get_performance_monitor().track_operation("quick_review"):
            response = self.reviewer(prompt)
        
        self._log_activity("code_review", code_or_file[:50], str(response))
        
        return {
            'review': str(response),
            'timestamp': datetime.now().isoformat()
        }
    
    def quick_fix(self, bug_description: str, code: Optional[str] = None) -> str:
        """
        Quick bug fix.
        
        Args:
            bug_description: Description of the bug
            code: Optional code with the bug
            
        Returns:
            Fixed code or fix instructions
        """
        if code:
            prompt = f"Bug: {bug_description}\n\nCode with bug:\n{code}\n\nProvide fixed version."
        else:
            prompt = f"Bug: {bug_description}\n\nProvide fix instructions."
        
        with get_performance_monitor().track_operation("quick_fix"):
            response = self.fixer(prompt)
        
        self._log_activity("bug_fix", bug_description, str(response))
        return str(response)
    
    def quick_design(self, requirements: str) -> Dict[str, Any]:
        """
        Quick architecture design.
        
        Args:
            requirements: System requirements
            
        Returns:
            Architecture design
        """
        prompt = f"Design system architecture for:\n\n{requirements}\n\nInclude: components, data flow, tech stack"
        
        with get_performance_monitor().track_operation("quick_design"):
            response = self.architect(prompt)
        
        self._log_activity("architecture_design", requirements[:50], str(response))
        
        return {
            'design': str(response),
            'timestamp': datetime.now().isoformat()
        }
    
    def quick_docs(self, code_or_function: str) -> str:
        """
        Quick documentation generation.
        
        Args:
            code_or_function: Code to document
            
        Returns:
            Documentation
        """
        prompt = f"Write clear, comprehensive documentation for:\n\n{code_or_function}"
        
        with get_performance_monitor().track_operation("quick_docs"):
            response = self.writer(prompt)
        
        self._log_activity("documentation", code_or_function[:50], str(response))
        return str(response)
    
    def full_feature(self, feature_description: str) -> Dict[str, Any]:
        """
        Complete feature implementation workflow.
        
        Full cycle: design -> code -> tests -> docs
        
        Args:
            feature_description: Feature to implement
            
        Returns:
            Complete feature package
        """
        print(f"🚀 Implementing: {feature_description}")
        
        # Step 1: Design
        print("  1/4 Designing architecture...")
        design = self.quick_design(feature_description)
        
        # Step 2: Code
        print("  2/4 Generating code...")
        code = self.quick_code(feature_description)
        
        # Step 3: Tests
        print("  3/4 Creating tests...")
        tests = self.quick_test(code)
        
        # Step 4: Documentation
        print("  4/4 Writing documentation...")
        docs = self.quick_docs(code)
        
        print("✅ Feature complete!")
        
        result = {
            'feature': feature_description,
            'design': design,
            'code': code,
            'tests': tests,
            'documentation': docs,
            'timestamp': datetime.now().isoformat()
        }
        
        self._log_activity("full_feature", feature_description, result)
        return result
    
    def debug_session(self, error_message: str, code: str) -> Dict[str, Any]:
        """
        Complete debugging session.
        
        Args:
            error_message: Error encountered
            code: Code with the error
            
        Returns:
            Debug analysis and fix
        """
        print(f"🐛 Debugging: {error_message[:50]}...")
        
        # Step 1: Analyze
        print("  1/3 Analyzing error...")
        analysis = self.fixer(f"Analyze this error:\n\nError: {error_message}\n\nCode:\n{code}")
        
        # Step 2: Fix
        print("  2/3 Generating fix...")
        fix = self.quick_fix(error_message, code)
        
        # Step 3: Test
        print("  3/3 Creating verification tests...")
        tests = self.quick_test(fix, test_type="unit")
        
        print("✅ Debug complete!")
        
        return {
            'error': error_message,
            'analysis': str(analysis),
            'fix': fix,
            'tests': tests,
            'timestamp': datetime.now().isoformat()
        }
    
    def code_improvement_cycle(self, code: str) -> Dict[str, Any]:
        """
        Complete code improvement cycle.
        
        Review -> Refactor -> Test -> Document
        
        Args:
            code: Code to improve
            
        Returns:
            Improved code package
        """
        print("🔧 Starting improvement cycle...")
        
        # Step 1: Review
        print("  1/4 Reviewing code...")
        review = self.quick_review(code)
        
        # Step 2: Refactor based on review
        print("  2/4 Refactoring...")
        refactor_prompt = f"Refactor this code based on review:\n\nReview: {review['review']}\n\nCode:\n{code}"
        refactored = self.coder(refactor_prompt)
        
        # Step 3: Tests for refactored code
        print("  3/4 Updating tests...")
        tests = self.quick_test(str(refactored))
        
        # Step 4: Documentation
        print("  4/4 Updating docs...")
        docs = self.quick_docs(str(refactored))
        
        print("✅ Improvement cycle complete!")
        
        return {
            'original_code': code,
            'review': review,
            'refactored_code': str(refactored),
            'tests': tests,
            'documentation': docs,
            'timestamp': datetime.now().isoformat()
        }
    
    def _log_activity(self, activity_type: str, input_summary: str, output: Any) -> None:
        """Log workflow activity."""
        self.session_log.append({
            'type': activity_type,
            'input': input_summary,
            'timestamp': datetime.now().isoformat(),
            'output_length': len(str(output))
        })
    
    def get_session_summary(self) -> str:
        """Get summary of current session."""
        if not self.session_log:
            return "No activities in this session yet."
        
        summary = "Session Summary\n" + "=" * 50 + "\n"
        summary += f"Total Activities: {len(self.session_log)}\n\n"
        
        # Count by type
        type_counts = {}
        for activity in self.session_log:
            activity_type = activity['type']
            type_counts[activity_type] = type_counts.get(activity_type, 0) + 1
        
        summary += "Activities by type:\n"
        for activity_type, count in sorted(type_counts.items()):
            summary += f"  {activity_type}: {count}\n"
        
        summary += f"\nRecent activities:\n"
        for activity in self.session_log[-5:]:
            summary += f"  [{activity['timestamp']}] {activity['type']}: {activity['input'][:40]}...\n"
        
        return summary


# Quick access functions for common tasks
def code(task: str, language: str = "python") -> str:
    """Quick code generation."""
    return ask_agent("felix", f"Language: {language}\n{task}")


def test(code: str) -> str:
    """Quick test generation."""
    return ask_agent("quinn", f"Generate tests for:\n{code}")


def review(code: str) -> str:
    """Quick code review."""
    return ask_agent("orion", f"Review this code:\n{code}")


def fix(bug: str, code: str = "") -> str:
    """Quick bug fix."""
    return ask_agent("patch", f"Bug: {bug}\n\nCode: {code}")


def design(requirements: str) -> str:
    """Quick architecture design."""
    return ask_agent("aurora", f"Design system for:\n{requirements}")


def docs(code: str) -> str:
    """Quick documentation."""
    return ask_agent("pixel", f"Document:\n{code}")


# Example usage
if __name__ == "__main__":
    # Demo daily workflow
    workflow = DailyWorkflow()
    
    print("=== AI CodeForge Daily Workflow Demo ===\n")
    
    # Quick code
    code_result = workflow.quick_code("Create a function to validate email addresses")
    print(f"Code generated: {len(code_result)} characters\n")
    
    # Quick test
    test_result = workflow.quick_test(code_result)
    print(f"Tests generated: {len(test_result)} characters\n")
    
    # Session summary
    print(workflow.get_session_summary())
