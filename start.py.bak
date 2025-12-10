#!/usr/bin/env python3
"""
Simple launcher for AI CodeForge
No venv required - uses system Python directly
"""

import sys
from pathlib import Path

# Ensure we're in the right directory
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    """Direct launch - no venv needed."""
    try:
        # Check config exists
        config_path = PROJECT_ROOT / "config.yaml"
        if not config_path.exists():
            print("\n⚠️  Configuration needed!")
            print("   Run: python3 setup_proper.py\n")
            sys.exit(1)
        
        # Import and run
        print("🚀 Starting AI CodeForge...\n")
        from orchestrator_v2 import main as orchestrator_main
        orchestrator_main()
        
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("\n💡 Install dependencies:")
        print("   pip install -r requirements.txt\n")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
