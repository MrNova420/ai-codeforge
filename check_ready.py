#!/usr/bin/env python3
"""
Check if AI CodeForge is ready to use
"""

import sys
from pathlib import Path

def check_system():
    """Check system readiness."""
    print("🔍 Checking AI CodeForge v1.0.0 Status...\n")
    
    checks = []
    
    # Check version files
    checks.append(("VERSION file", Path("VERSION").exists()))
    checks.append(("__version__.py", Path("__version__.py").exists()))
    
    # Check interfaces
    checks.append(("Natural language (./talk)", Path("talk").exists()))
    checks.append(("Web app (webapp.py)", Path("webapp.py").exists()))
    checks.append(("CLI (codeforge)", Path("codeforge").exists()))
    checks.append(("Advanced CLI (codeforge_advanced)", Path("codeforge_advanced").exists()))
    
    # Check core files
    checks.append(("Natural interface", Path("natural_interface.py").exists()))
    checks.append(("Configuration", Path("config_manager.py").exists()))
    checks.append(("Startup", Path("startup.py").exists()))
    
    # Check documentation
    checks.append(("README.md", Path("README.md").exists()))
    checks.append(("QUICKSTART.md", Path("QUICKSTART.md").exists()))
    checks.append(("NATURAL_LANGUAGE_GUIDE.md", Path("NATURAL_LANGUAGE_GUIDE.md").exists()))
    checks.append(("WEBAPP_GUIDE.md", Path("WEBAPP_GUIDE.md").exists()))
    
    # Check directories
    checks.append(("agents/", Path("agents").is_dir()))
    checks.append(("ui/", Path("ui").is_dir()))
    checks.append(("teams/", Path("teams").is_dir()))
    
    # Display results
    all_pass = True
    for name, status in checks:
        symbol = "✅" if status else "❌"
        print(f"{symbol} {name}")
        if not status:
            all_pass = False
    
    print()
    if all_pass:
        print("✅ System Status: READY TO USE!")
        print("\n🚀 Quick Start:")
        print("   ./talk                    # Natural language")
        print("   python3 webapp.py         # Web interface")
        print("   ./codeforge help          # CLI help")
        return 0
    else:
        print("❌ System Status: Some files missing")
        print("Run: ./setup.sh")
        return 1

if __name__ == "__main__":
    sys.exit(check_system())
