#!/bin/bash
# AI CodeForge Setup Script
# Easy installation and setup

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║   🔨 AI CODEFORGE - Setup Script                            ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Setup virtual environment
echo ""
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment."
        echo "   Try: sudo apt install python3-venv python3-full"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r requirements.txt

# Make scripts executable
echo ""
echo "🔧 Setting up CLI tools..."
chmod +x codeforge
chmod +x run
chmod +x start.py

# Create symlink to /usr/local/bin if possible
if [ -w /usr/local/bin ]; then
    ln -sf "$(pwd)/codeforge" /usr/local/bin/codeforge
    echo "✅ Created global 'codeforge' command"
else
    echo "⚠️  Could not create global command (need sudo)"
    echo "   Run: sudo ln -sf $(pwd)/codeforge /usr/local/bin/codeforge"
fi

# Setup complete
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║   ✅ SETUP COMPLETE!                                         ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Quick Start - No activation needed!"
echo ""
echo "   Choose your interface (all automatically use the venv):"
echo ""
echo "   ./run                    # Full orchestrator - All 23 agents + V3 features"
echo "   ./talk \"build an API\"   # Natural language - Just describe what you want"
echo "   ./codeforge              # CLI commands (code, test, review, agents, etc.)"
echo "   ./webapp                 # Web UI - Visual dashboard in your browser"
echo ""
echo ""
echo "💡 First time? Try the easiest interface:"
echo "   ./talk \"create a hello world function\""
echo ""
echo "📖 New User Guide: cat GETTING_STARTED.md"
echo "📚 Full Documentation: README.md"
echo "🤝 Support: https://github.com/MrNova420/ai-codeforge"
echo ""
