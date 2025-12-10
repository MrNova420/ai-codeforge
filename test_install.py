#!/usr/bin/env python3
"""
Installation Test Script
Verifies that all dependencies and components are properly installed.
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def test_imports():
    """Test if all required packages are installed."""
    results = []
    
    packages = [
        ("rich", "Rich terminal UI"),
        ("yaml", "YAML configuration"),
        ("openai", "OpenAI API"),
        ("google.generativeai", "Gemini API"),
    ]
    
    for package, description in packages:
        try:
            __import__(package)
            results.append((package, description, True, "✅"))
        except ImportError:
            results.append((package, description, False, "❌"))
    
    return results

def test_files():
    """Test if all required files exist."""
    from pathlib import Path
    
    results = []
    files = [
        "orchestrator.py",
        "agent_chat.py",
        "config_template.yaml",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md",
        "planner_designer_agents.md",
        "critic_judge_agents.md",
        "developer_agents.md",
        "developer_assistant_agents.md",
        "debugger_fixer_agent.md",
        "tester_agent.md",
        "overseer_agent.md",
    ]
    
    for filename in files:
        exists = Path(filename).exists()
        results.append((filename, exists, "✅" if exists else "❌"))
    
    return results

def test_agent_loading():
    """Test if agents can be loaded."""
    try:
        sys.path.insert(0, ".")
        from orchestrator import AgentLoader
        
        loader = AgentLoader()
        agents = loader.list_agents()
        
        expected_count = 17
        actual_count = len(agents)
        
        return actual_count, expected_count, actual_count >= expected_count
    except Exception as e:
        return 0, 17, False

def main():
    console.print(Panel.fit(
        "[bold cyan]Ultimate AI Dev Team - Installation Test[/bold cyan]\n"
        "Checking if everything is properly installed...",
        border_style="cyan"
    ))
    
    # Test imports
    console.print("\n[bold]1. Testing Python Packages...[/bold]")
    import_results = test_imports()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Package")
    table.add_column("Description")
    table.add_column("Status")
    
    all_imports_ok = True
    for package, desc, success, status in import_results:
        table.add_row(package, desc, status)
        if not success:
            all_imports_ok = False
    
    console.print(table)
    
    if not all_imports_ok:
        console.print("\n[yellow]⚠️  Some packages are missing. Install them with:[/yellow]")
        console.print("[cyan]pip install -r requirements.txt[/cyan]")
    
    # Test files
    console.print("\n[bold]2. Testing Project Files...[/bold]")
    file_results = test_files()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("File")
    table.add_column("Status")
    
    all_files_ok = True
    for filename, exists, status in file_results:
        table.add_row(filename, status)
        if not exists:
            all_files_ok = False
    
    console.print(table)
    
    if not all_files_ok:
        console.print("\n[red]❌ Some files are missing![/red]")
    
    # Test agent loading
    console.print("\n[bold]3. Testing Agent Loading...[/bold]")
    try:
        actual, expected, success = test_agent_loading()
        if success:
            console.print(f"[green]✅ Successfully loaded {actual} agents (expected {expected})[/green]")
        else:
            console.print(f"[yellow]⚠️  Loaded {actual} agents (expected {expected})[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error loading agents: {e}[/red]")
        success = False
    
    # Final summary
    console.print("\n" + "="*60)
    if all_imports_ok and all_files_ok and success:
        console.print(Panel.fit(
            "[bold green]✅ All Tests Passed![/bold green]\n\n"
            "Your Ultimate AI Dev Team is ready to use!\n"
            "Run: [cyan]python3 orchestrator.py[/cyan] to get started.",
            border_style="green"
        ))
        return 0
    else:
        console.print(Panel.fit(
            "[bold yellow]⚠️  Some Issues Found[/bold yellow]\n\n"
            "Please check the results above and fix any issues.\n"
            "Run: [cyan]pip install -r requirements.txt[/cyan] to install packages.",
            border_style="yellow"
        ))
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        console.print(f"[red]Error running tests: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)
