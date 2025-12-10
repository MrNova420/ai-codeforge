#!/bin/bash
# AI CodeForge - Virtual Environment Activation Helper
# Run with: source activate.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please run ./setup.sh first"
    return 1 2>/dev/null || exit 1
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

echo "✅ Virtual environment activated!"
echo ""
echo "🚀 You can now run:"
echo "   python3 webapp.py        # Start web application"
echo "   ./codeforge              # Start CLI"
echo ""
echo "💡 To deactivate: deactivate"
