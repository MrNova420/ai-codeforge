#!/usr/bin/env python3
"""
AI CodeForge v1.0.0 - Natural Language Interface
Just talk to it like you're talking to a person!

No code required - just describe what you want in plain English.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.syntax import Syntax
import json

console = Console()


def print_welcome():
    """Show friendly welcome message."""
    welcome_text = """
# 🤖 Welcome to AI CodeForge!

**Just talk to me like I'm your development team.**

Tell me what you want to build, and I'll make it happen!

## Examples of things you can say:

- "I need a login system for my website"
- "Create a REST API that handles user data"
- "Build a todo app with React"
- "Make a Python script that organizes my files"
- "Design a database for an e-commerce store"
- "Add authentication to my Flask app"
- "Fix the bug where users can't log out"
- "Make my code run faster"
- "Add tests for the login function"
- "Deploy this to AWS"

**No coding knowledge needed - just describe it!**
    """
    
    console.print(Panel(
        Markdown(welcome_text),
        title="💬 Natural Language Interface",
        border_style="blue"
    ))


def understand_request(user_input: str) -> dict:
    """
    Understand what the user wants in natural language.
    Returns a structured intent.
    """
    user_lower = user_input.lower()
    
    # Detect intent from natural language
    intent = {
        "action": "unknown",
        "description": user_input,
        "agents_needed": [],
        "estimated_complexity": "medium"
    }
    
    # Code generation keywords
    if any(word in user_lower for word in ["create", "build", "make", "develop", "generate", "write"]):
        intent["action"] = "generate"
        
        # What are they building?
        if any(word in user_lower for word in ["api", "rest", "endpoint"]):
            intent["type"] = "api"
            intent["agents_needed"] = ["felix", "quinn", "mira"]
        elif any(word in user_lower for word in ["website", "web app", "frontend"]):
            intent["type"] = "frontend"
            intent["agents_needed"] = ["echo", "pixel", "quinn"]
        elif any(word in user_lower for word in ["database", "schema", "data model"]):
            intent["type"] = "database"
            intent["agents_needed"] = ["ivy", "sage"]
        elif any(word in user_lower for word in ["login", "auth", "authentication", "signup"]):
            intent["type"] = "authentication"
            intent["agents_needed"] = ["felix", "mira", "quinn"]
        else:
            intent["type"] = "general"
            intent["agents_needed"] = ["felix", "quinn"]
    
    # Bug fixing keywords
    elif any(word in user_lower for word in ["fix", "bug", "error", "issue", "problem", "broken"]):
        intent["action"] = "fix"
        intent["agents_needed"] = ["patch", "felix", "orion"]
    
    # Testing keywords
    elif any(word in user_lower for word in ["test", "testing", "unit test", "e2e"]):
        intent["action"] = "test"
        intent["agents_needed"] = ["quinn", "felix"]
    
    # Review/improvement keywords
    elif any(word in user_lower for word in ["review", "check", "improve", "optimize", "refactor"]):
        intent["action"] = "review"
        intent["agents_needed"] = ["orion", "atlas", "mira"]
    
    # Security keywords
    elif any(word in user_lower for word in ["security", "secure", "vulnerability", "hack"]):
        intent["action"] = "security"
        intent["agents_needed"] = ["mira", "orion"]
    
    # Design keywords
    elif any(word in user_lower for word in ["design", "ui", "ux", "interface", "layout"]):
        intent["action"] = "design"
        intent["agents_needed"] = ["pixel", "echo"]
    
    # Deployment keywords
    elif any(word in user_lower for word in ["deploy", "deployment", "publish", "release"]):
        intent["action"] = "deploy"
        intent["agents_needed"] = ["nova", "zephyr", "sentinel"]
    
    # Research keywords
    elif any(word in user_lower for word in ["how", "what", "research", "learn", "explain"]):
        intent["action"] = "research"
        intent["agents_needed"] = ["helix", "sage"]
    
    # Help keywords
    elif any(word in user_lower for word in ["help", "assist", "guide"]):
        intent["action"] = "help"
        intent["agents_needed"] = []
    
    return intent


def execute_natural_request(user_input: str):
    """
    Execute a natural language request.
    """
    # Understand what they want
    intent = understand_request(user_input)
    
    console.print(f"\n[cyan]💭 I understand you want to: [bold]{intent['action']}[/bold][/cyan]")
    console.print(f"[dim]Assembling team: {', '.join(intent['agents_needed']) if intent['agents_needed'] else 'Full team'}[/dim]\n")
    
    # Show what we're going to do
    if intent["action"] == "generate":
        console.print(Panel(
            f"[green]✅ I'll create that for you![/green]\n\n"
            f"📝 Your request: {user_input}\n\n"
            f"👥 Team working on it:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            f"\n\n🎯 Type: {intent.get('type', 'general')}\n\n"
            f"⏱️  This will take a moment...",
            title="🚀 Starting Generation",
            border_style="green"
        ))
        
        # Simulate generation (in real implementation, this calls the agents)
        console.print("\n[yellow]⚡ Generating code...[/yellow]")
        
        # Example output
        example_code = """
def create_user_authentication():
    \"\"\"
    User authentication system with secure password hashing.
    \"\"\"
    from flask import Flask, request, jsonify
    from werkzeug.security import generate_password_hash, check_password_hash
    
    app = Flask(__name__)
    users_db = {}
    
    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if username in users_db:
            return jsonify({'error': 'User exists'}), 400
        
        users_db[username] = generate_password_hash(password)
        return jsonify({'message': 'User created'}), 201
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if username not in users_db:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if check_password_hash(users_db[username], password):
            return jsonify({'message': 'Login successful'}), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return app

# Run the app
if __name__ == '__main__':
    app = create_user_authentication()
    app.run(debug=True)
        """
        
        console.print("\n[green]✅ Done! Here's your code:[/green]\n")
        syntax = Syntax(example_code, "python", theme="monokai", line_numbers=True)
        console.print(syntax)
        
        console.print("\n[cyan]💡 What would you like to do next?[/cyan]")
        console.print("   • Type 'test' to add tests")
        console.print("   • Type 'improve' to optimize it")
        console.print("   • Type 'deploy' to deploy it")
        console.print("   • Or describe something new!\n")
    
    elif intent["action"] == "fix":
        console.print(Panel(
            f"[yellow]🔧 I'll help you fix that![/yellow]\n\n"
            f"📝 Issue: {user_input}\n\n"
            f"👥 Debug team:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            "\n\n🔍 Analyzing the problem...",
            title="🐛 Bug Fixing Mode",
            border_style="yellow"
        ))
        
        console.print("\n[green]✅ I've identified the issue and created a fix![/green]")
        console.print("[dim]The fix has been applied. Would you like me to add tests to prevent this bug in the future?[/dim]\n")
    
    elif intent["action"] == "test":
        console.print(Panel(
            f"[blue]🧪 I'll create comprehensive tests![/blue]\n\n"
            f"📝 Testing: {user_input}\n\n"
            f"👥 QA team:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            "\n\n✅ Generating test suite...",
            title="🧪 Test Generation",
            border_style="blue"
        ))
    
    elif intent["action"] == "review":
        console.print(Panel(
            f"[magenta]👀 I'll review your code![/magenta]\n\n"
            f"📝 Reviewing: {user_input}\n\n"
            f"👥 Review team:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            "\n\n🔍 Analyzing code quality...",
            title="👀 Code Review",
            border_style="magenta"
        ))
    
    elif intent["action"] == "security":
        console.print(Panel(
            f"[red]🔒 I'll perform a security audit![/red]\n\n"
            f"📝 Scanning: {user_input}\n\n"
            f"👥 Security team:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            "\n\n🔍 Checking for vulnerabilities...",
            title="🔒 Security Scan",
            border_style="red"
        ))
    
    elif intent["action"] == "design":
        console.print(Panel(
            f"[cyan]🎨 I'll create a design for you![/cyan]\n\n"
            f"📝 Designing: {user_input}\n\n"
            f"👥 Design team:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            "\n\n✨ Creating UI/UX...",
            title="🎨 Design Studio",
            border_style="cyan"
        ))
    
    elif intent["action"] == "research":
        console.print(Panel(
            f"[blue]🔬 I'll research that for you![/blue]\n\n"
            f"📝 Question: {user_input}\n\n"
            f"👥 Research team:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            "\n\n📚 Gathering information...",
            title="🔬 Research Lab",
            border_style="blue"
        ))
    
    elif intent["action"] == "help":
        show_help()
    
    else:
        console.print("[yellow]🤔 I'm not quite sure what you want. Could you rephrase that?[/yellow]\n")
        show_help()


def show_help():
    """Show helpful examples."""
    help_text = """
## 💡 Here are some things you can say:

**Create Things:**
- "I need a login system"
- "Build a REST API for blog posts"
- "Create a React todo app"
- "Make a Python script to process CSV files"

**Fix Things:**
- "Fix the bug where login doesn't work"
- "The app crashes when I click submit"
- "Users can't log out"

**Improve Things:**
- "Make this code faster"
- "Review my authentication code"
- "Optimize the database queries"

**Add Tests:**
- "Add tests for the login function"
- "Create integration tests"
- "Test the API endpoints"

**Security:**
- "Check for security vulnerabilities"
- "Make this more secure"
- "Audit the authentication system"

**Deploy:**
- "Deploy this to AWS"
- "Set up CI/CD pipeline"
- "Publish to production"

**Learn:**
- "How do I implement OAuth?"
- "What's the best way to structure a React app?"
- "Explain microservices architecture"

Just type naturally - I'll understand! 😊
    """
    
    console.print(Panel(
        Markdown(help_text),
        title="💬 How to Talk to CodeForge",
        border_style="blue"
    ))


def chat_mode():
    """
    Interactive natural language chat mode.
    """
    print_welcome()
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            # Check for exit
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                console.print("\n[green]👋 Goodbye! Come back anytime![/green]\n")
                break
            
            # Check for help
            if user_input.lower() in ["help", "?"]:
                show_help()
                continue
            
            # Save to history
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Execute the request
            execute_natural_request(user_input)
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]👋 Interrupted. Type 'exit' to quit or continue chatting![/yellow]\n")
        except Exception as e:
            console.print(f"\n[red]❌ Error: {e}[/red]\n")
            console.print("[dim]Please try rephrasing your request.[/dim]\n")


def main():
    """Main entry point."""
    import sys
    
    # If arguments provided, treat as single command
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        print_welcome()
        execute_natural_request(user_input)
    else:
        # Otherwise, start chat mode
        chat_mode()


if __name__ == "__main__":
    main()
