#!/bin/bash
# Local Models Setup Script for Ultimate AI Dev Team

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║         Ultimate AI Dev Team - Local Models Setup           ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed"
else
    echo "📦 Installing Ollama..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Please install Ollama from: https://ollama.ai/download"
        echo "Or use: brew install ollama"
        exit 1
    else
        echo "Please install Ollama from: https://ollama.ai/download"
        exit 1
    fi
    
    if [ $? -eq 0 ]; then
        echo "✅ Ollama installed successfully"
    else
        echo "❌ Failed to install Ollama"
        exit 1
    fi
fi

echo ""
echo "🚀 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!
sleep 3

echo ""
echo "📥 Downloading recommended models..."
echo ""

# Ask user which models to download
echo "Which models would you like to download?"
echo "1. llama2:7b (4GB) - General purpose, fast"
echo "2. codellama:7b (4GB) - Optimized for coding"
echo "3. mistral:7b (4GB) - Very fast, good quality"
echo "4. All of the above"
echo "5. Skip download (I'll do it manually)"
echo ""
read -p "Select (1-5): " choice

case $choice in
    1)
        echo "Downloading llama2..."
        ollama pull llama2
        SELECTED_MODEL="llama2"
        ;;
    2)
        echo "Downloading codellama..."
        ollama pull codellama
        SELECTED_MODEL="codellama"
        ;;
    3)
        echo "Downloading mistral..."
        ollama pull mistral
        SELECTED_MODEL="mistral"
        ;;
    4)
        echo "Downloading all models..."
        ollama pull llama2
        ollama pull codellama
        ollama pull mistral
        SELECTED_MODEL="codellama"
        ;;
    5)
        echo "Skipping download. Remember to run 'ollama pull <model>' later."
        SELECTED_MODEL="llama2"
        ;;
    *)
        echo "Invalid choice. Exiting."
        kill $OLLAMA_PID 2>/dev/null
        exit 1
        ;;
esac

echo ""
echo "⚙️  Configuring AI Dev Team..."

# Update config.yaml if it exists
if [ -f "config.yaml" ]; then
    # Backup original
    cp config.yaml config.yaml.backup
    
    # Update ollama settings
    if grep -q "ollama_model:" config.yaml; then
        sed -i "s/ollama_model:.*/ollama_model: \"$SELECTED_MODEL\"/" config.yaml
    else
        echo "ollama_model: \"$SELECTED_MODEL\"" >> config.yaml
    fi
    
    echo "✅ Updated config.yaml"
    echo "   (Backup saved as config.yaml.backup)"
else
    echo "ℹ️  No config.yaml found yet. It will be created on first run."
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║                    ✅ Setup Complete!                         ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 Your local AI models are ready!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit config.yaml and set agents to 'local'"
echo "   2. Run: python3 orchestrator.py"
echo "   3. Select agents and start building!"
echo ""
echo "💡 Tips:"
echo "   - Use 'codellama' for coding tasks"
echo "   - Use 'llama2' for general tasks"
echo "   - Keep 'ollama serve' running in background"
echo ""
echo "📚 For more info, see: LOCAL_MODELS_GUIDE.md"
echo ""
echo "🔧 Ollama is running in background (PID: $OLLAMA_PID)"
echo "   To stop: kill $OLLAMA_PID"
echo ""
