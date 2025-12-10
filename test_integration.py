#!/usr/bin/env python3
"""
Simple integration test to verify core components work together
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_unified_interface():
    """Test that unified interface can be imported and initialized."""
    print("Testing unified_interface...")
    try:
        from unified_interface import get_unified_interface, UnifiedInterface
        
        # Get instance
        unified = get_unified_interface()
        assert unified is not None, "Unified interface is None"
        assert isinstance(unified, UnifiedInterface), "Not a UnifiedInterface instance"
        
        # Test basic methods exist
        assert hasattr(unified, 'list_all_agents'), "Missing list_all_agents method"
        assert hasattr(unified, 'list_all_features'), "Missing list_all_features method"
        assert hasattr(unified, 'get_agent_info'), "Missing get_agent_info method"
        assert hasattr(unified, 'execute_task'), "Missing execute_task method"
        
        print("✅ unified_interface working")
        return True
    except Exception as e:
        print(f"❌ unified_interface failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_code_executor():
    """Test that code executor can be imported and initialized."""
    print("\nTesting code_executor...")
    try:
        from code_executor import CodeExecutor, ExecutionResult
        from pathlib import Path
        
        # Create workspace
        workspace = Path("/tmp/test_workspace")
        workspace.mkdir(exist_ok=True)
        
        # Initialize executor
        executor = CodeExecutor(workspace_dir=workspace)
        assert executor is not None, "Executor is None"
        
        # Test simple Python code
        result = executor.execute_python("print('Hello, World!')")
        assert hasattr(result, 'success'), "Result missing success attribute"
        assert hasattr(result, 'output'), "Result missing output attribute"
        
        print(f"✅ code_executor working (output: {result.output.strip()})")
        return True
    except Exception as e:
        print(f"❌ code_executor failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test that required files exist."""
    print("\nTesting file structure...")
    try:
        required_files = [
            "ui/frontend/index.html",
            "ui/frontend/app.js",
            "ui/frontend/styles.css",
            "ui/backend/websocket_server.py",
            "unified_interface.py",
            "code_executor.py",
        ]
        
        for file_path in required_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"Missing file: {file_path}"
        
        print("✅ All required files exist")
        return True
    except Exception as e:
        print(f"❌ File structure test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("AI CodeForge Integration Test")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("File Structure", test_file_structure()))
    results.append(("Unified Interface", test_unified_interface()))
    results.append(("Code Executor", test_code_executor()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Integration working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
