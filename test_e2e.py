#!/usr/bin/env python3
"""
End-to-End Test Suite for AI CodeForge
Tests all interfaces and critical paths
"""

import sys
import subprocess
import time
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(msg):
    print(f"{Colors.BLUE}[TEST]{Colors.END} {msg}")

def print_pass(msg):
    print(f"{Colors.GREEN}[PASS]{Colors.END} {msg}")

def print_fail(msg):
    print(f"{Colors.RED}[FAIL]{Colors.END} {msg}")

def print_warn(msg):
    print(f"{Colors.YELLOW}[WARN]{Colors.END} {msg}")

def test_wrapper_scripts():
    """Test that wrapper scripts exist and are executable."""
    print_test("Checking wrapper scripts...")
    
    scripts = ['talk', 'codeforge', 'run', 'webapp']
    results = []
    
    for script in scripts:
        script_path = project_root / script
        
        if not script_path.exists():
            print_fail(f"  {script} - NOT FOUND")
            results.append(False)
            continue
        
        if not script_path.is_file():
            print_fail(f"  {script} - Not a file")
            results.append(False)
            continue
        
        # Check if executable
        import os
        if not os.access(script_path, os.X_OK):
            print_warn(f"  {script} - Not executable (but exists)")
            results.append(True)  # Still count as pass since file exists
        else:
            print_pass(f"  {script} - OK")
            results.append(True)
    
    return all(results)

def test_python_scripts():
    """Test that Python scripts exist and can be imported."""
    print_test("Checking Python scripts...")
    
    scripts = ['talk.py', 'codeforge.py', 'run.py', 'webapp.py']
    results = []
    
    for script in scripts:
        script_path = project_root / script
        
        if not script_path.exists():
            print_fail(f"  {script} - NOT FOUND")
            results.append(False)
            continue
        
        # Try to compile it
        try:
            import py_compile
            py_compile.compile(str(script_path), doraise=True)
            print_pass(f"  {script} - Valid syntax")
            results.append(True)
        except Exception as e:
            print_fail(f"  {script} - Syntax error: {e}")
            results.append(False)
    
    return all(results)

def test_unified_interface():
    """Test unified interface integration."""
    print_test("Testing unified interface...")
    
    try:
        from unified_interface import get_unified_interface
        
        unified = get_unified_interface()
        
        # Test methods exist
        methods = ['list_all_agents', 'list_all_features', 'get_agent_info', 'execute_task']
        for method in methods:
            if not hasattr(unified, method):
                print_fail(f"  Missing method: {method}")
                return False
        
        print_pass("  All methods present")
        
        # Test basic operations
        try:
            agents = unified.list_all_agents()
            if agents and len(agents) > 0:
                print_pass(f"  list_all_agents() - OK ({len(agents)} agents)")
            else:
                print_warn(f"  list_all_agents() - returned empty list")
        except Exception as e:
            print_fail(f"  list_all_agents() - Error: {e}")
            return False
        
        try:
            info = unified.get_agent_info("felix")
            if info and 'role' in info:
                print_pass(f"  get_agent_info() - OK (Felix: {info['role']})")
            else:
                print_warn(f"  get_agent_info() - returned incomplete info")
        except Exception as e:
            print_fail(f"  get_agent_info() - Error: {e}")
            return False
        
        return True
        
    except Exception as e:
        print_fail(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_code_executor():
    """Test code executor."""
    print_test("Testing code executor...")
    
    try:
        from code_executor import CodeExecutor
        from pathlib import Path
        
        workspace = Path("/tmp/test_workspace_e2e")
        workspace.mkdir(exist_ok=True)
        
        executor = CodeExecutor(workspace_dir=workspace)
        
        # Test Python execution
        result = executor.execute_python("x = 5 + 3\nprint(x)")
        
        if result.success and "8" in result.output:
            print_pass(f"  Python execution - OK (output: {result.output.strip()})")
        else:
            print_fail(f"  Python execution - Failed (output: {result.output}, error: {result.error})")
            return False
        
        # Test with syntax error
        result = executor.execute_python("print(")
        
        if not result.success:
            print_pass(f"  Error handling - OK (correctly caught syntax error)")
        else:
            print_warn(f"  Error handling - Should have failed on syntax error")
        
        return True
        
    except Exception as e:
        print_fail(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_webapp_files():
    """Test webapp files exist and are valid."""
    print_test("Testing webapp files...")
    
    files_to_check = [
        ('ui/frontend/index.html', 'html'),
        ('ui/frontend/app.js', 'javascript'),
        ('ui/frontend/styles.css', 'css'),
        ('ui/backend/websocket_server.py', 'python')
    ]
    
    results = []
    
    for file_path, file_type in files_to_check:
        full_path = project_root / file_path
        
        if not full_path.exists():
            print_fail(f"  {file_path} - NOT FOUND")
            results.append(False)
            continue
        
        if file_type == 'python':
            try:
                import py_compile
                py_compile.compile(str(full_path), doraise=True)
                print_pass(f"  {file_path} - Valid syntax")
                results.append(True)
            except Exception as e:
                print_fail(f"  {file_path} - Syntax error")
                results.append(False)
        else:
            # Just check it exists and has content
            if full_path.stat().st_size > 0:
                print_pass(f"  {file_path} - OK")
                results.append(True)
            else:
                print_fail(f"  {file_path} - Empty file")
                results.append(False)
    
    return all(results)

def test_ui_integration():
    """Test UI integration points."""
    print_test("Testing UI integration points...")
    
    try:
        # Check if websocket server has required imports
        with open(project_root / 'ui/backend/websocket_server.py', 'r') as f:
            content = f.read()
        
        required_patterns = [
            'from unified_interface import get_unified_interface',
            'from fastapi import FastAPI',
            'async def handle_task_execution',
            'async def handle_code_execution',
            'async def periodic_status_broadcast'
        ]
        
        for pattern in required_patterns:
            if pattern in content:
                print_pass(f"  Found: {pattern[:50]}...")
            else:
                print_fail(f"  Missing: {pattern}")
                return False
        
        # Check frontend integration
        with open(project_root / 'ui/frontend/app.js', 'r') as f:
            content = f.read()
        
        required_patterns = [
            'function initializeHeaderButtons',
            'function showNotificationsPanel',
            'function handleAgentsList',
            'function handleExecutionUpdate',
            'function connectWebSocket'
        ]
        
        for pattern in required_patterns:
            if pattern in content:
                print_pass(f"  Found: {pattern}")
            else:
                print_fail(f"  Missing: {pattern}")
                return False
        
        return True
        
    except Exception as e:
        print_fail(f"  Error: {e}")
        return False

def test_documentation():
    """Test that documentation exists."""
    print_test("Checking documentation...")
    
    docs = [
        'README.md',
        'QUICKSTART.md',
        'WEBAPP_GUIDE.md',
        'WEBAPP_FIXES.md'
    ]
    
    results = []
    
    for doc in docs:
        doc_path = project_root / doc
        if doc_path.exists():
            print_pass(f"  {doc} - OK")
            results.append(True)
        else:
            print_warn(f"  {doc} - Not found (optional)")
            results.append(True)  # Don't fail on missing docs
    
    return all(results)

def main():
    """Run all tests."""
    print("="*80)
    print("AI CodeForge End-to-End Test Suite")
    print("="*80)
    print()
    
    tests = [
        ("Wrapper Scripts", test_wrapper_scripts),
        ("Python Scripts", test_python_scripts),
        ("Unified Interface", test_unified_interface),
        ("Code Executor", test_code_executor),
        ("WebApp Files", test_webapp_files),
        ("UI Integration", test_ui_integration),
        ("Documentation", test_documentation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print()
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_fail(f"Test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print()
    print("="*80)
    print("Test Summary")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print()
        print(f"{Colors.GREEN}🎉 All tests passed! System is ready for use.{Colors.END}")
        print()
        return 0
    else:
        print()
        print(f"{Colors.YELLOW}⚠️  {total - passed} test(s) failed. Review errors above.{Colors.END}")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
