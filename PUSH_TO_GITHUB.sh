#!/bin/bash
# AI CodeForge - GitHub Push Script

echo "🚀 AI CodeForge - GitHub Setup"
echo "================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "📝 Adding files..."
    git add .
    
    echo ""
    echo "💾 Creating commit..."
    git commit -m "Initial commit: AI CodeForge v0.1.0

- Multi-agent collaboration system (23+ agents)
- Self-learning vector memory (ChromaDB)
- Deep code understanding (AST graph)
- Self-correction capabilities
- Web research agent
- Background code indexing
- Impact analysis
- Tool registry system"
    
    echo "✅ Commit created"
fi

echo ""
echo "================================"
echo "🎯 NEXT STEPS:"
echo "================================"
echo ""
echo "1. Authenticate with GitHub:"
echo "   gh auth login"
echo "   (Follow the prompts - choose 'Login with browser')"
echo ""
echo "2. Create and push repository:"
echo "   gh repo create ai-codeforge --public --source=. --push"
echo ""
echo "3. Add repository description:"
echo "   gh repo edit --description 'Autonomous multi-agent AI development system with 23+ specialized agents'"
echo ""
echo "4. Add topics:"
echo "   gh repo edit --add-topic artificial-intelligence,multi-agent-system,autonomous-agents,llm,python"
echo ""
echo "5. Create first release:"
echo "   gh release create v0.1.0 --title 'AI CodeForge v0.1.0' --notes 'First release with core features'"
echo ""
echo "================================"
echo "📚 Or use the web interface:"
echo "================================"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: ai-codeforge"
echo "3. Make it PUBLIC"
echo "4. Don't initialize with README (we have one)"
echo "5. Click 'Create repository'"
echo ""
echo "Then run:"
echo "  git remote add origin https://github.com/YOUR_USERNAME/ai-codeforge.git"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""
echo "================================"

