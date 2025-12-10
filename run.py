#!/usr/bin/env python3
"""
ONE SIMPLE COMMAND TO RUN EVERYTHING
Auto-detects configuration and starts agents
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

def check_and_setup():
    """Check if setup is needed, prompt if not configured."""
    config_path = PROJECT_ROOT / "config.yaml"
    
    # Check if system is configured
    if not config_path.exists():
        print("\n⚠️  First time setup needed")
        print("   Run: ./setup_proper.py\n")
        sys.exit(0)
    
    # Check if config is valid
    try:
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            agent_models = config.get('agent_models', {})
            if len(agent_models) < 23:
                print("\n⚠️  Configuration incomplete")
                print("   Run: ./setup_proper.py\n")
                sys.exit(0)
    except:
        print("\n⚠️  Configuration invalid")
        print("   Run: ./setup_proper.py\n")
        sys.exit(0)
    
    print("🤖 Starting up...")
    
    # Check for venv (optional - will use system Python if not present)
    venv_path = PROJECT_ROOT / "venv"
    if venv_path.exists():
        print("✅ Using virtual environment")
        return venv_path
    else:
        print("✅ Using system Python")
        return None

def main():
    """Main entry"""
    try:
        # Check setup
        venv_path = check_and_setup()
        
        # Determine Python executable
        if venv_path:
            python_exe = venv_path / "bin" / "python3"
            if not python_exe.exists():
                python_exe = venv_path / "Scripts" / "python.exe"  # Windows
        else:
            python_exe = sys.executable  # Use current Python
        
        orchestrator = PROJECT_ROOT / "orchestrator_v2.py"
        
        print("🚀 Launching AI CodeForge...\n")
        subprocess.run([str(python_exe), str(orchestrator)])
        
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Try: python3 orchestrator_v2.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
