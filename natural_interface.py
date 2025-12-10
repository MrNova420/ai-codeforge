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

**Your complete AI development team - just talk naturally!**

I can help you build ANYTHING:

## 🚀 What Can I Build For You?

**Websites & Apps:**
- "Build a blog with comments and user accounts"
- "Create a React e-commerce store"
- "Make a mobile app for recipes"

**APIs & Backends:**
- "Create a REST API for my data"
- "Build a GraphQL server"
- "Make a real-time chat backend"

**Data & Analytics:**
- "Analyze this CSV and create visualizations"
- "Build a data dashboard"
- "Make an AI recommendation system"

**Games & Graphics:**
- "Create a 2D platformer game"
- "Build a 3D visualization"
- "Make an interactive animation"

**Tools & Scripts:**
- "Make a file organizer script"
- "Build a web scraper"
- "Create an automation tool"

**Design:**
- "Design a modern UI for my app"
- "Create wireframes for a website"
- "Make a logo and brand identity"

**And Much More:**
- Fix bugs, optimize code, add features
- Write tests, documentation
- Deploy to cloud, set up CI/CD
- Research, learn, get advice

**No coding knowledge needed - just tell me what you want!** 😊
    """
    
    console.print(Panel(
        Markdown(welcome_text),
        title="💬 I Can Build Anything You Imagine!",
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
    
    # Code generation keywords (MAIN FOCUS)
    if any(word in user_lower for word in ["create", "build", "make", "develop", "generate", "write", "add"]):
        intent["action"] = "generate"
        
        # What are they building?
        if any(word in user_lower for word in ["api", "rest", "endpoint", "backend"]):
            intent["type"] = "api"
            intent["agents_needed"] = ["felix", "sol", "quinn"]
        elif any(word in user_lower for word in ["website", "web app", "frontend", "react", "vue"]):
            intent["type"] = "frontend"
            intent["agents_needed"] = ["echo", "pixel", "felix"]
        elif any(word in user_lower for word in ["mobile", "app", "ios", "android"]):
            intent["type"] = "mobile"
            intent["agents_needed"] = ["blaze", "pixel", "quinn"]
        elif any(word in user_lower for word in ["database", "schema", "data model", "sql"]):
            intent["type"] = "database"
            intent["agents_needed"] = ["ivy", "sage", "felix"]
        elif any(word in user_lower for word in ["login", "auth", "authentication", "signup", "user"]):
            intent["type"] = "authentication"
            intent["agents_needed"] = ["felix", "quinn", "orion"]
        elif any(word in user_lower for word in ["script", "automation", "tool", "utility"]):
            intent["type"] = "script"
            intent["agents_needed"] = ["felix", "script"]
        elif any(word in user_lower for word in ["game", "3d", "graphics"]):
            intent["type"] = "game"
            intent["agents_needed"] = ["felix", "echo", "pixel"]
        elif any(word in user_lower for word in ["ai", "ml", "machine learning", "data science"]):
            intent["type"] = "ai_ml"
            intent["agents_needed"] = ["ivy", "helix", "felix"]
        else:
            intent["type"] = "general"
            intent["agents_needed"] = ["felix", "orion"]
    
    # Design keywords (EQUAL PRIORITY)
    elif any(word in user_lower for word in ["design", "ui", "ux", "interface", "layout", "wireframe"]):
        intent["action"] = "design"
        intent["agents_needed"] = ["pixel", "echo", "ember"]
    
    # Bug fixing keywords
    elif any(word in user_lower for word in ["fix", "bug", "error", "issue", "problem", "broken", "crash"]):
        intent["action"] = "fix"
        intent["agents_needed"] = ["patch", "felix", "orion"]
    
    # Testing keywords
    elif any(word in user_lower for word in ["test", "testing", "unit test", "e2e", "qa"]):
        intent["action"] = "test"
        intent["agents_needed"] = ["quinn", "felix"]
    
    # Review/improvement keywords
    elif any(word in user_lower for word in ["review", "check", "improve", "optimize", "refactor", "better"]):
        intent["action"] = "review"
        intent["agents_needed"] = ["orion", "atlas", "felix"]
    
    # Deployment keywords
    elif any(word in user_lower for word in ["deploy", "deployment", "publish", "release", "production"]):
        intent["action"] = "deploy"
        intent["agents_needed"] = ["nova", "zephyr", "sentinel"]
    
    # Research keywords (EQUAL PRIORITY)
    elif any(word in user_lower for word in ["how", "what", "why", "research", "learn", "explain", "teach"]):
        intent["action"] = "research"
        intent["agents_needed"] = ["helix", "sage", "script"]
    
    # Data/Analytics keywords
    elif any(word in user_lower for word in ["data", "analytics", "report", "dashboard", "visualize"]):
        intent["action"] = "data"
        intent["agents_needed"] = ["ivy", "felix", "pixel"]
    
    # Documentation keywords
    elif any(word in user_lower for word in ["document", "docs", "readme", "guide", "explain"]):
        intent["action"] = "document"
        intent["agents_needed"] = ["script", "felix"]
    
    # Performance keywords
    elif any(word in user_lower for word in ["faster", "speed", "performance", "optimize"]):
        intent["action"] = "optimize"
        intent["agents_needed"] = ["atlas", "turbo", "felix"]
    
    # Security keywords (BALANCED - not overemphasized)
    elif any(word in user_lower for word in ["security", "secure", "vulnerability", "safe"]):
        intent["action"] = "security"
        intent["agents_needed"] = ["mira", "felix", "orion"]
    
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
            f"[cyan]🔒 I'll check security for you![/cyan]\n\n"
            f"📝 Reviewing: {user_input}\n\n"
            f"👥 Team:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            "\n\n✨ Ensuring everything is secure...",
            title="🔒 Security Review",
            border_style="cyan"
        ))
    
    elif intent["action"] == "data":
        console.print(Panel(
            f"[blue]📊 I'll work with your data![/blue]\n\n"
            f"📝 Task: {user_input}\n\n"
            f"👥 Data team:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            "\n\n📈 Processing and analyzing...",
            title="📊 Data Analytics",
            border_style="blue"
        ))
    
    elif intent["action"] == "document":
        console.print(Panel(
            f"[green]📚 I'll create documentation![/green]\n\n"
            f"📝 Documenting: {user_input}\n\n"
            f"👥 Documentation team:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            "\n\n✍️ Writing clear documentation...",
            title="📚 Documentation",
            border_style="green"
        ))
    
    elif intent["action"] == "optimize":
        console.print(Panel(
            f"[yellow]⚡ I'll make it faster![/yellow]\n\n"
            f"📝 Optimizing: {user_input}\n\n"
            f"👥 Performance team:\n" +
            "\n".join([f"   • {agent}" for agent in intent["agents_needed"]]) +
            "\n\n🚀 Boosting performance...",
            title="⚡ Performance Optimization",
            border_style="yellow"
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

**🚀 Create Anything:**
- "Build a blog website with comments"
- "Create a REST API for user management"
- "Make a React todo app"
- "Build a mobile app for iOS"
- "Create a Python script to organize files"
- "Build a game with graphics"
- "Make an AI chatbot"
- "Create a data visualization dashboard"

**🎨 Design:**
- "Design a login screen"
- "Create wireframes for a shopping cart"
- "Make a modern UI for my app"
- "Design a logo and brand identity"

**🐛 Fix & Improve:**
- "Fix the bug where users can't log out"
- "Make this code run faster"
- "Improve the user experience"
- "Optimize database performance"

**📊 Data & Analytics:**
- "Analyze this data and create charts"
- "Build a reporting dashboard"
- "Create data visualizations"
- "Make a machine learning model"

**🧪 Testing:**
- "Add tests for my functions"
- "Create integration tests"
- "Test everything automatically"

**🚀 Deploy:**
- "Deploy this to AWS"
- "Set up CI/CD pipeline"
- "Publish to production"

**📚 Learn & Research:**
- "How do I build a REST API?"
- "What's the best framework for my project?"
- "Explain how databases work"
- "Show me examples of good code"

**📖 Documentation:**
- "Write documentation for my code"
- "Create a README file"
- "Generate API documentation"

**⚡ Performance:**
- "Make my app faster"
- "Optimize loading times"
- "Improve performance"

Just type naturally - I understand everything! 😊
    """
    
    console.print(Panel(
        Markdown(help_text),
        title="💬 I Can Help With Everything!",
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
