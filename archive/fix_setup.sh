#!/bin/bash
# Fix setup issues and install properly

cd "$(dirname "$0")"

echo "🔧 Fixing AI Dev Team Setup..."
echo ""

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install -q --upgrade pip

# Install all dependencies
echo "📦 Installing all dependencies..."
pip install -q rich pyyaml openai google-generativeai requests prompt-toolkit questionary

echo ""
echo "✅ Setup complete!"
echo ""
echo "Now you can run:"
echo "  ./start_v2.sh  (for V2 with all features)"
echo "  ./start.sh     (for V1 simple)"
echo ""
