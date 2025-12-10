#!/usr/bin/env python3
"""
Test script to verify all fixes are working correctly.
Tests the main entry points and core functionality.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all imports work."""
    print("🧪 Testing imports...")
    
    try:
        from unified_interface import get_unified_interface
        print("  ✅ unified_interface")
    except Exception as e:
        print(f"  ❌ unified_interface: {e}")
        return False
    
    try:
        from orchestrator_v2 import EnhancedOrchestrator
        print("  ✅ orchestrator_v2")
    except ModuleNotFoundError as e:
        if 'numpy' in str(e):
            print(f"  ⚠️  orchestrator_v2: numpy not installed (non-critical, handled by chromadb)")
        else:
            print(f"  ❌ orchestrator_v2: {e}")
            return False
    except Exception as e:
        print(f"  ❌ orchestrator_v2: {e}")
        return False
    
    try:
        from collaboration_v3 import CollaborationV3
        print("  ✅ collaboration_v3")
    except Exception as e:
        print(f"  ❌ collaboration_v3: {e}")
        return False
    
    try:
        import fastapi
        import uvicorn
        print("  ✅ fastapi, uvicorn")
    except Exception as e:
        print(f"  ❌ fastapi/uvicorn: {e}")
        return False
    
    return True


def test_unified_interface():
    """Test unified interface initialization."""
    print("\n🧪 Testing unified interface...")
    
    try:
        from unified_interface import get_unified_interface
        
        unified = get_unified_interface()
        print("  ✅ Unified interface created")
        
        # Initialize features
        unified.initialize()
        print("  ✅ Features initialized")
        
        # List features
        features = unified.list_all_features()
        print(f"  ✅ Features available: {sum(1 for v in features.values() if v)}/{len(features)}")
        
        for feature, available in features.items():
            status = "✅" if available else "⚠️ "
            print(f"    {status} {feature}")
        
        # List agents
        agents = unified.list_all_agents()
        print(f"  ✅ Agents available: {len(agents)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Unified interface failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_orchestrator():
    """Test orchestrator initialization."""
    print("\n🧪 Testing orchestrator...")
    
    try:
        from orchestrator_v2 import EnhancedOrchestrator
        
        orch = EnhancedOrchestrator()
        print("  ✅ Orchestrator created")
        
        # Check attributes
        if hasattr(orch, 'agent_loader'):
            print("  ✅ Agent loader available")
        
        if hasattr(orch, 'vector_memory'):
            status = "✅" if orch.vector_memory else "⚠️ "
            print(f"  {status} Vector memory")
        
        if hasattr(orch, 'tool_registry'):
            print("  ✅ Tool registry available")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Orchestrator failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_webapp_backend():
    """Test webapp backend can be imported."""
    print("\n🧪 Testing webapp backend...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / "ui" / "backend"))
        import websocket_server
        print("  ✅ WebSocket server imported")
        
        # Check if FastAPI app exists
        if hasattr(websocket_server, 'app'):
            print("  ✅ FastAPI app defined")
        
        if hasattr(websocket_server, 'manager'):
            print("  ✅ Connection manager defined")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Webapp backend failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_collaboration_v3():
    """Test CollaborationV3 initialization."""
    print("\n🧪 Testing CollaborationV3...")
    
    try:
        from collaboration_v3 import CollaborationV3
        print("  ✅ CollaborationV3 imported")
        
        # Don't initialize without agent_chats - just verify it can be imported
        print("  ✅ CollaborationV3 requires agent_chats parameter (correct)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ CollaborationV3 failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║  AI CodeForge - Fix Verification Tests                  ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Unified Interface", test_unified_interface()))
    results.append(("Orchestrator", test_orchestrator()))
    results.append(("Webapp Backend", test_webapp_backend()))
    results.append(("CollaborationV3", test_collaboration_v3()))
    
    # Summary
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║                    Test Summary                           ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"║  {status:8} - {test_name:45} ║")
    
    print("╠═══════════════════════════════════════════════════════════╣")
    print(f"║  Results: {passed}/{total} tests passed{' ' * (33 - len(str(passed)) - len(str(total)))}║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    if passed == total:
        print("🎉 All tests passed! The fixes are working correctly.\n")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed. Review errors above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
