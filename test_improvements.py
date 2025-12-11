#!/usr/bin/env python3
"""
Comprehensive Integration Tests - Validates all improvements
Tests collaboration, activity logging, error recovery, and performance monitoring
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class TestResults:
    """Track test results."""
    
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
    
    def add_pass(self, test_name: str, message: str = ""):
        self.passed.append({'name': test_name, 'message': message})
        console.print(f"✅ [green]{test_name}[/green] {message}")
    
    def add_fail(self, test_name: str, error: str):
        self.failed.append({'name': test_name, 'error': error})
        console.print(f"❌ [red]{test_name}[/red]: {error}")
    
    def add_warning(self, test_name: str, message: str):
        self.warnings.append({'name': test_name, 'message': message})
        console.print(f"⚠️  [yellow]{test_name}[/yellow]: {message}")
    
    def print_summary(self):
        """Print test summary."""
        total = len(self.passed) + len(self.failed) + len(self.warnings)
        
        table = Table(title="Test Summary")
        table.add_column("Status", style="bold")
        table.add_column("Count", justify="right")
        table.add_column("Percentage", justify="right")
        
        table.add_row("✅ Passed", str(len(self.passed)), f"{len(self.passed)/total*100:.1f}%")
        table.add_row("❌ Failed", str(len(self.failed)), f"{len(self.failed)/total*100:.1f}%")
        table.add_row("⚠️  Warnings", str(len(self.warnings)), f"{len(self.warnings)/total*100:.1f}%")
        table.add_row("📊 Total", str(total), "100%")
        
        console.print("\n")
        console.print(table)
        
        return len(self.failed) == 0


async def test_prompt_utilities():
    """Test centralized prompt utilities."""
    console.print("\n[bold cyan]Testing Prompt Utilities...[/bold cyan]")
    results = TestResults()
    
    try:
        from prompts_utils import (
            build_actionable_task_prompt,
            build_enhanced_task_prompt,
            build_delegation_prompt,
            build_agent_system_prompt,
            CONTEXT_SUMMARY_LENGTH,
            SCROLL_HINT_THRESHOLD
        )
        
        # Test actionable prompt
        prompt = build_actionable_task_prompt("Test task", "Backend Dev", "high")
        if "ACTUALLY IMPLEMENT" in prompt and "Test task" in prompt:
            results.add_pass("build_actionable_task_prompt", "Contains action instructions")
        else:
            results.add_fail("build_actionable_task_prompt", "Missing action instructions")
        
        # Test enhanced prompt
        prompt = build_enhanced_task_prompt("Test task")
        if "CRITICAL INSTRUCTIONS" in prompt:
            results.add_pass("build_enhanced_task_prompt", "Contains critical instructions")
        else:
            results.add_fail("build_enhanced_task_prompt", "Missing instructions")
        
        # Test delegation prompt
        prompt = build_delegation_prompt("Build API", ["felix", "aurora"])
        if "AGENTS NEEDED" in prompt and "felix" in prompt:
            results.add_pass("build_delegation_prompt", "Contains agent list")
        else:
            results.add_fail("build_delegation_prompt", "Missing agent information")
        
        # Test agent system prompt
        prompt = build_agent_system_prompt("Felix", "Developer", "Friendly", "Coding", "Methodical")
        if "IMPLEMENTER" in prompt and "Felix" in prompt:
            results.add_pass("build_agent_system_prompt", "Contains implementation emphasis")
        else:
            results.add_fail("build_agent_system_prompt", "Missing implementation focus")
        
        # Test constants
        if CONTEXT_SUMMARY_LENGTH == 200:
            results.add_pass("CONTEXT_SUMMARY_LENGTH", "Correct value (200)")
        else:
            results.add_fail("CONTEXT_SUMMARY_LENGTH", f"Unexpected value: {CONTEXT_SUMMARY_LENGTH}")
        
        if SCROLL_HINT_THRESHOLD == 2000:
            results.add_pass("SCROLL_HINT_THRESHOLD", "Correct value (2000)")
        else:
            results.add_fail("SCROLL_HINT_THRESHOLD", f"Unexpected value: {SCROLL_HINT_THRESHOLD}")
    
    except Exception as e:
        results.add_fail("prompt_utilities", str(e))
    
    return results


async def test_collaboration_v3():
    """Test CollaborationV3 features."""
    console.print("\n[bold cyan]Testing CollaborationV3...[/bold cyan]")
    results = TestResults()
    
    try:
        from collaboration_v3 import CollaborationV3
        
        # Create mock agent chats
        mock_agents = {
            'helix': type('Agent', (), {'send_message': lambda self, *args, **kwargs: "Mock response"})(),
            'felix': type('Agent', (), {'send_message': lambda self, *args, **kwargs: "Mock code"})(),
        }
        
        collab = CollaborationV3(mock_agents)
        
        # Test activity logging
        if hasattr(collab, 'activity_log'):
            results.add_pass("activity_log", "Activity logging initialized")
        else:
            results.add_fail("activity_log", "Missing activity log")
        
        # Test task history
        if hasattr(collab, 'task_history'):
            results.add_pass("task_history", "Task history initialized")
        else:
            results.add_fail("task_history", "Missing task history")
        
        # Test error recovery
        if hasattr(collab, 'error_recovery'):
            results.add_pass("error_recovery", "Error recovery system integrated")
        else:
            results.add_fail("error_recovery", "Missing error recovery")
        
        # Test agent statuses
        if hasattr(collab, 'agent_statuses') and 'felix' in collab.agent_statuses:
            status = collab.agent_statuses['felix']
            if 'errors' in status and 'recovered' in status:
                results.add_pass("agent_statuses", "Enhanced with error tracking")
            else:
                results.add_warning("agent_statuses", "Missing error tracking fields")
        else:
            results.add_fail("agent_statuses", "Missing agent statuses")
        
        # Test error report
        if hasattr(collab, 'get_error_report'):
            report = collab.get_error_report()
            if 'recovery_system' in report and 'agent_errors' in report:
                results.add_pass("get_error_report", "Returns comprehensive report")
            else:
                results.add_warning("get_error_report", "Incomplete report")
        else:
            results.add_fail("get_error_report", "Missing error report method")
    
    except Exception as e:
        results.add_fail("collaboration_v3", str(e))
    
    return results


async def test_error_recovery():
    """Test error recovery system."""
    console.print("\n[bold cyan]Testing Error Recovery...[/bold cyan]")
    results = TestResults()
    
    try:
        from agent_error_recovery import (
            AgentErrorRecovery,
            ErrorSeverity,
            get_error_recovery
        )
        
        # Test singleton
        recovery1 = get_error_recovery()
        recovery2 = get_error_recovery()
        if recovery1 is recovery2:
            results.add_pass("singleton", "Single instance maintained")
        else:
            results.add_fail("singleton", "Multiple instances created")
        
        # Test initialization
        recovery = AgentErrorRecovery(max_retries=3, base_delay=1.0)
        if recovery.max_retries == 3 and recovery.base_delay == 1.0:
            results.add_pass("initialization", "Parameters set correctly")
        else:
            results.add_fail("initialization", "Parameters incorrect")
        
        # Test fallback map
        if recovery.fallback_map:
            if 'backend' in recovery.fallback_map and 'felix' in recovery.fallback_map['backend']:
                results.add_pass("fallback_map", "Contains backend fallbacks")
            else:
                results.add_warning("fallback_map", "Missing some fallbacks")
        else:
            results.add_fail("fallback_map", "No fallback map")
        
        # Test error classification
        test_error = Exception("Connection timeout")
        severity = recovery._classify_error(test_error)
        if severity in [ErrorSeverity.LOW, ErrorSeverity.MEDIUM, ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            results.add_pass("error_classification", f"Classified as {severity.value}")
        else:
            results.add_fail("error_classification", "Invalid severity")
        
        # Test statistics
        stats = recovery.recovery_stats
        if all(k in stats for k in ['total_errors', 'recovered', 'failed', 'retries', 'fallbacks']):
            results.add_pass("recovery_stats", "All stats tracked")
        else:
            results.add_fail("recovery_stats", "Missing stats")
    
    except Exception as e:
        results.add_fail("error_recovery", str(e))
    
    return results


async def test_performance_monitor():
    """Test performance monitoring."""
    console.print("\n[bold cyan]Testing Performance Monitor...[/bold cyan]")
    results = TestResults()
    
    try:
        from performance_monitor import (
            PerformanceMonitor,
            get_performance_monitor
        )
        
        # Test singleton
        monitor1 = get_performance_monitor()
        monitor2 = get_performance_monitor()
        if monitor1 is monitor2:
            results.add_pass("singleton", "Single instance maintained")
        else:
            results.add_fail("singleton", "Multiple instances created")
        
        # Test initialization
        monitor = PerformanceMonitor(history_size=1000)
        if monitor.metrics_history.maxlen == 1000:
            results.add_pass("initialization", "History size set correctly")
        else:
            results.add_fail("initialization", "History size incorrect")
        
        # Test thresholds
        if all(k in monitor.thresholds for k in ['task_duration_slow', 'memory_warning', 'cpu_warning']):
            results.add_pass("thresholds", "All thresholds defined")
        else:
            results.add_fail("thresholds", "Missing thresholds")
        
        # Test metric recording
        monitor.record_metric("test_metric", 42.0, "units", agent="test_agent")
        if len(monitor.metrics_history) > 0:
            results.add_pass("record_metric", "Metric recorded successfully")
        else:
            results.add_fail("record_metric", "Metric not recorded")
        
        # Test task timing
        monitor.start_task_timer("task1", "felix")
        if 'felix' in monitor.agent_metrics:
            results.add_pass("start_task_timer", "Timer started")
        else:
            results.add_fail("start_task_timer", "Timer not started")
        
        # Test system stats
        stats = monitor.get_system_stats()
        if 'uptime_seconds' in stats and 'total_tasks' in stats:
            results.add_pass("get_system_stats", "Returns system statistics")
        else:
            results.add_fail("get_system_stats", "Incomplete statistics")
    
    except Exception as e:
        results.add_fail("performance_monitor", str(e))
    
    return results


async def test_webapp_adapter():
    """Test webapp adapter integration."""
    console.print("\n[bold cyan]Testing Webapp Adapter...[/bold cyan]")
    results = TestResults()
    
    try:
        from webapp_adapter import WebappAdapter, get_webapp_adapter
        
        # Test singleton
        adapter1 = get_webapp_adapter()
        adapter2 = get_webapp_adapter()
        if adapter1 is adapter2:
            results.add_pass("singleton", "Single instance maintained")
        else:
            results.add_fail("singleton", "Multiple instances created")
        
        # Test initialization
        adapter = WebappAdapter()
        if hasattr(adapter, 'active_tasks') and hasattr(adapter, 'event_callbacks'):
            results.add_pass("initialization", "Properties initialized")
        else:
            results.add_fail("initialization", "Missing properties")
        
        # Test callback registration
        test_callback = lambda event: None
        adapter.register_callback(test_callback)
        if test_callback in adapter.event_callbacks:
            results.add_pass("register_callback", "Callback registered")
        else:
            results.add_fail("register_callback", "Callback not registered")
        
        # Test methods exist
        methods = ['execute_task_with_streaming', 'get_activity_feed', 'get_task_history', 
                  'get_agent_stats', 'get_agent_status', 'get_all_agent_statuses']
        for method in methods:
            if hasattr(adapter, method):
                results.add_pass(f"method_{method}", "Method exists")
            else:
                results.add_fail(f"method_{method}", "Method missing")
    
    except Exception as e:
        results.add_fail("webapp_adapter", str(e))
    
    return results


async def main():
    """Run all tests."""
    console.print(Panel(
        "[bold cyan]AI CodeForge - Comprehensive Integration Tests[/bold cyan]\n"
        "Testing all improvements and new features",
        border_style="cyan"
    ))
    
    all_results = []
    
    # Run all test suites
    all_results.append(await test_prompt_utilities())
    all_results.append(await test_collaboration_v3())
    all_results.append(await test_error_recovery())
    all_results.append(await test_performance_monitor())
    all_results.append(await test_webapp_adapter())
    
    # Print final summary
    console.print("\n" + "="*60)
    console.print("[bold]FINAL TEST SUMMARY[/bold]")
    console.print("="*60 + "\n")
    
    total_passed = sum(len(r.passed) for r in all_results)
    total_failed = sum(len(r.failed) for r in all_results)
    total_warnings = sum(len(r.warnings) for r in all_results)
    total = total_passed + total_failed + total_warnings
    
    console.print(f"✅ Passed:   {total_passed}/{total} ({total_passed/total*100:.1f}%)")
    console.print(f"❌ Failed:   {total_failed}/{total} ({total_failed/total*100:.1f}%)")
    console.print(f"⚠️  Warnings: {total_warnings}/{total} ({total_warnings/total*100:.1f}%)")
    
    if total_failed == 0:
        console.print("\n[bold green]🎉 ALL TESTS PASSED! 🎉[/bold green]")
        return 0
    else:
        console.print(f"\n[bold red]❌ {total_failed} TESTS FAILED[/bold red]")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
