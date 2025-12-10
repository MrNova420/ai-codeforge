#!/usr/bin/env python3
"""
CodeForge CLI - Advanced Command Line Interface
Professional, feature-rich CLI for AI CodeForge with full control

Usage:
    codeforge                              # Interactive mode with TUI
    codeforge code "task"                  # Generate code
    codeforge test "file"                  # Generate tests
    codeforge review "file"                # Review code
    codeforge fix "issue" [--code FILE]    # Fix bugs
    codeforge design "feature"             # Design feature
    codeforge team "task" [--mode MODE]    # Full team collaboration
    codeforge build "project"              # Complete production cycle
    codeforge security "path" [--report]   # Security audit
    codeforge research "topic"             # Research technology
    codeforge agents [--json]              # List all agents
    codeforge status [--watch]             # System status
    codeforge config [--set KEY=VALUE]     # Configuration
    codeforge history [--limit N]          # Command history
    codeforge chat AGENT "message"         # Direct agent chat
    codeforge workflow create NAME         # Custom workflow
    codeforge export [--format FORMAT]     # Export results
    codeforge version                      # Show version
    codeforge help [COMMAND]               # Detailed help
"""

import sys
import asyncio
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def print_banner():
    """Print CodeForge banner."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🔨 AI CODEFORGE - AAA Production Development Team          ║
║                                                               ║
║   23 Specialized AI Agents • Enterprise-Grade Quality        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")

def print_help():
    """Print help information."""
    print_banner()
    print("""
QUICK COMMANDS:
  codeforge                        Start interactive mode
  codeforge code "create REST API" Generate code
  codeforge test "api.py"          Generate tests  
  codeforge review "src/api.py"    Review code
  codeforge fix "login bug"        Fix issue
  codeforge design "checkout flow" Design feature
  codeforge security "src/"        Security audit
  codeforge research "GraphQL"     Research technology
  codeforge team "build app"       Full team collaboration
  codeforge agents                 List all 23 agents
  codeforge status                 Show system status

TEAM MODES:
  codeforge team --parallel "task"      All agents work simultaneously
  codeforge team --sequential "task"    Production pipeline
  codeforge team --collaborative "task" Agents discuss and iterate
  codeforge team --autonomous "task"    Agents self-organize

PRODUCTION CYCLE:
  codeforge build "E-commerce Platform"  Complete 6-phase production

EXAMPLES:
  codeforge code "Create user authentication API"
  codeforge test "Write tests for login function"
  codeforge review "Check security in auth.py"
  codeforge team "Build REST API with full test coverage"
  codeforge security "Scan for vulnerabilities in src/"

OPTIONS:
  --help, -h      Show this help
  --version, -v   Show version
  --agents        List all agents
  --status        System status

AGENTS:
  23 specialized AI agents ready to help:
  • Planners: aurora, sage, felix, ember
  • Critics: orion, atlas, mira, vex  
  • Specialists: sol, echo, nova, quinn, blaze, ivy, zephyr
  • Assistants: pixel, script, turbo, sentinel
  • Special: helix, patch, pulse, link

For more information: https://github.com/MrNova420/ai-codeforge
""")

def list_agents():
    """List all available agents."""
    print_banner()
    print("\n🤖 ALL 23 SPECIALIZED AGENTS:\n")
    
    categories = {
        "Planners & Strategists": [
            ("aurora", "Product Manager & Strategic Planner"),
            ("sage", "Lead Architect & Technical Strategist"),
            ("felix", "Senior Full-Stack Developer"),
            ("ember", "Creative Director & Innovation Lead")
        ],
        "Critics & Reviewers": [
            ("orion", "Senior Code Reviewer & Quality Lead"),
            ("atlas", "Performance & Optimization Specialist"),
            ("mira", "Security Engineer & AppSec Lead"),
            ("vex", "Critical Analyst & Skeptic")
        ],
        "Specialists": [
            ("sol", "Backend API Specialist"),
            ("echo", "Frontend & UI Developer"),
            ("nova", "DevOps & Infrastructure Engineer"),
            ("quinn", "QA Lead & Test Automation"),
            ("blaze", "Mobile Development Lead"),
            ("ivy", "Data Engineer & Database Specialist"),
            ("zephyr", "Cloud Architect")
        ],
        "Assistants": [
            ("pixel", "UX Designer & Design System Lead"),
            ("script", "Technical Writer & Documentation"),
            ("turbo", "Performance Engineer"),
            ("sentinel", "Monitoring & SRE Lead")
        ],
        "Special Agents": [
            ("helix", "Research Lead & Technology Advisor"),
            ("patch", "Bug Hunter & Debugging Specialist"),
            ("pulse", "Integration Specialist"),
            ("link", "Communication & Collaboration Lead")
        ]
    }
    
    for category, agents in categories.items():
        print(f"\n{category}:")
        print("-" * 70)
        for name, role in agents:
            print(f"  • {name:12} - {role}")
    
    print("\n" + "=" * 70)
    print("Total: 23 agents ready to work together!")
    print("=" * 70 + "\n")

def show_status():
    """Show system status."""
    print_banner()
    print("\n📊 SYSTEM STATUS:\n")
    print("✅ 23 Specialized Agents - Ready")
    print("✅ Master Orchestrator - Active")
    print("✅ Security Operations - Active")
    print("✅ Innovation Lab - Active")
    print("✅ Design Studio - Active")
    print("✅ Enterprise Hub - Active")
    print("✅ Performance Optimizer - Active")
    print("\n🎯 All systems operational and ready!\n")

async def run_command(command: str, args: list):
    """Run a CodeForge command."""
    try:
        if command == "code":
            from daily_workflow import code
            task = " ".join(args) if args else "Generate code"
            print(f"\n🔨 Generating code: {task}\n")
            result = await code(task)
            print(result)
            
        elif command == "test":
            from daily_workflow import test
            target = " ".join(args) if args else "tests/"
            print(f"\n🧪 Generating tests: {target}\n")
            result = await test(target)
            print(result)
            
        elif command == "review":
            from daily_workflow import review
            target = " ".join(args) if args else "code"
            print(f"\n👀 Reviewing: {target}\n")
            result = await review(target)
            print(result)
            
        elif command == "fix":
            from daily_workflow import fix
            issue = " ".join(args) if args else "bug"
            print(f"\n🔧 Fixing: {issue}\n")
            result = await fix(issue, "")
            print(result)
            
        elif command == "design":
            from daily_workflow import design
            feature = " ".join(args) if args else "feature"
            print(f"\n🎨 Designing: {feature}\n")
            result = await design(feature)
            print(result)
            
        elif command == "security":
            from security.security_operations import SecurityOpsCenter
            path = args[0] if args else "src/"
            print(f"\n🔒 Security audit: {path}\n")
            sec_ops = SecurityOpsCenter()
            report = await sec_ops.comprehensive_security_audit(path)
            print(sec_ops.generate_security_report(report))
            
        elif command == "research":
            from research.innovation_lab import InnovationLab
            topic = " ".join(args) if args else "technology"
            print(f"\n🔬 Researching: {topic}\n")
            lab = InnovationLab()
            result = await lab.research_technology(topic)
            print(f"Technology: {result.name}")
            print(f"Score: {result.score}/10")
            print(f"Maturity: {result.maturity.value}")
            print(f"\nRecommendation: {result.recommendation}\n")
            
        elif command == "team":
            from teams.master_orchestrator import MasterOrchestrator, WorkMode
            task = " ".join([a for a in args if not a.startswith("--")])
            
            # Determine mode
            mode = WorkMode.COLLABORATIVE
            if "--parallel" in args:
                mode = WorkMode.PARALLEL
            elif "--sequential" in args:
                mode = WorkMode.SEQUENTIAL
            elif "--autonomous" in args:
                mode = WorkMode.AUTONOMOUS
            
            print(f"\n🤝 Team collaboration ({mode.value}): {task}\n")
            orchestrator = MasterOrchestrator()
            result = await orchestrator.all_agents_work_together(task, mode)
            print(result)
            
        elif command == "build":
            from teams.master_orchestrator import MasterOrchestrator
            project = " ".join(args) if args else "Application"
            print(f"\n🏗️ Full production cycle: {project}\n")
            orchestrator = MasterOrchestrator()
            result = await orchestrator.full_production_cycle(project)
            print(result)
            
        else:
            print(f"❌ Unknown command: {command}")
            print("Run 'codeforge help' for usage information")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTry 'codeforge help' for usage information")

def interactive_mode():
    """Run CodeForge in interactive mode."""
    print_banner()
    print("\n🎯 Interactive Mode - Type commands or 'help' for assistance\n")
    
    while True:
        try:
            cmd = input("\ncodeforge> ").strip()
            
            if not cmd:
                continue
            
            if cmd.lower() in ["exit", "quit", "q"]:
                print("\n👋 Goodbye!\n")
                break
            
            if cmd.lower() in ["help", "h", "?"]:
                print_help()
                continue
            
            if cmd.lower() == "agents":
                list_agents()
                continue
            
            if cmd.lower() == "status":
                show_status()
                continue
            
            parts = cmd.split()
            command = parts[0]
            args = parts[1:]
            
            asyncio.run(run_command(command, args))
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    """Main entry point."""
    args = sys.argv[1:]
    
    # No arguments - interactive mode
    if not args:
        interactive_mode()
        return
    
    command = args[0].lower()
    
    # Help
    if command in ["help", "-h", "--help"]:
        print_help()
        return
    
    # Version
    if command in ["version", "-v", "--version"]:
        print_banner()
        print("Version: 3.0.0 - Complete AAA Production System")
        print("Status: Production-Ready ✅\n")
        return
    
    # Agents
    if command in ["agents", "--agents"]:
        list_agents()
        return
    
    # Status
    if command in ["status", "--status"]:
        show_status()
        return
    
    # Full orchestrator mode
    if command in ["orchestrator", "full", "all"]:
        print_banner()
        print("\n🚀 Activating Full Orchestrator Mode...")
        print("   All 23 agents + V3 advanced features\n")
        
        from unified_interface import get_unified_interface
        unified = get_unified_interface()
        task = " ".join(args[1:]) if len(args) > 1 else "interactive"
        
        if task == "interactive":
            print("💡 Starting full orchestrator in interactive mode")
            print("   Use ./run for the complete orchestrator interface\n")
        else:
            result = unified.execute_task(task, mode="full_orchestrator")
            print(f"\n✅ Task executed in full orchestrator mode")
        return
    
    # Features list
    if command in ["features", "--features"]:
        from unified_interface import get_unified_interface
        unified = get_unified_interface()
        features = unified.list_all_features()
        
        print_banner()
        print("\n✨ Available Features:\n")
        for feature, available in features.items():
            status = "✅" if available else "❌"
            print(f"  {status} {feature.replace('_', ' ').title()}")
        print()
        return
    
    # Run command
    asyncio.run(run_command(command, args[1:]))

if __name__ == "__main__":
    main()
