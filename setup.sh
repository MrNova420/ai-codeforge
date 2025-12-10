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

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

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
echo "🚀 Quick Start:"
echo ""
echo "   ./codeforge              # Start interactive mode"
echo "   ./codeforge help         # Show all commands"
echo "   ./codeforge agents       # List all 23 agents"
echo ""
echo "Or if global command installed:"
echo ""
echo "   codeforge               # From anywhere!"
echo ""
echo "📚 Documentation: README.md"
echo "🤝 Support: https://github.com/MrNova420/ai-codeforge"
echo ""
