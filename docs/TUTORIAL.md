# Step-by-Step Tutorial

Complete walkthrough from installation to building your first project.

## Part 1: Setup (5 minutes)

### Step 1: Install Ollama
```bash
# Install Ollama (free local AI)
curl https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve
```

### Step 2: Setup AI Dev Team
```bash
cd ~/ai-dev-team
./setup_proper.py
```

Follow the prompts:
- Model choice: Choose "Local (Ollama)" for free
- Model selection: codellama:7b recommended
- Wait for download: ~3.8GB

### Step 3: Verify Installation
```bash
./quick_test.py
```

Should see: "✅ All tests passed!"

## Part 2: First Interaction (2 minutes)

### Step 1: Launch System
```bash
./run
```

### Step 2: Choose Solo Mode
Press `2` for Solo Agent Chat

### Step 3: Select Nova
Press `11` for Nova (Backend Developer)

### Step 4: Ask Simple Question
```
You: Write a Python function that reverses a string
```

Wait ~15 seconds. You'll see code generated!

### Step 5: Exit
Type `exit` and press Enter

## Part 3: Build Something Real (10 minutes)

Let's build a **Task Manager CLI app**!

### Step 1: Launch Team Mode
```bash
./run
# Press 1 for Team Collaboration
```

### Step 2: Request the Project
```
You: Create a command-line task manager in Python with these features:
- Add tasks
- List all tasks
- Mark tasks as complete
- Delete tasks
- Save/load from JSON file
- Simple and clean code
```

### Step 3: Wait for Team
The team will:
1. Helix analyzes request
2. Agents coordinate
3. Code generated in workspace/

This takes 2-3 minutes with local model.

### Step 4: Check Results
```bash
ls workspace/
cat workspace/task_manager.py
```

### Step 5: Test It!
```bash
cd workspace/
python3 task_manager.py
```

### Step 6: Improve It
Back in AI Dev Team:
```
You: Add a feature to set task priorities (high, medium, low)
```

Team updates the code!

## Part 4: Understanding Agents (5 minutes)

### View All Agents
```bash
./run
# Press 3 for View All Agents
```

You'll see 23 specialized agents.

### Try Different Agents

**For UI/UX:**
```bash
# Solo mode → Felix (UI/UX Designer)
You: Design a dashboard layout for the task manager
```

**For Testing:**
```bash
# Solo mode → Sentinel (Testing Expert)
You: Write unit tests for task_manager.py
```

**For Documentation:**
```bash
# Solo mode → Pixel (Documentation Writer)
You: Write a README for the task manager
```

## Part 5: Real Project Workflow (15 minutes)

Let's build a **Blog API**!

### Step 1: Plan Architecture
```bash
# Solo mode → Aurora (System Architect)

You: Design a REST API architecture for a blog with:
- Users can create accounts
- Users can write posts
- Users can comment on posts
- Posts have tags
- Use SQLite database
```

Aurora will provide a complete architecture design.

### Step 2: Create Database Schema
```bash
# Solo mode → Ivy (Data Engineer)

You: Based on Aurora's design, create SQL schema for the blog database
```

### Step 3: Build the API
```bash
# Team Collaboration Mode

You: Create a Flask REST API implementing the blog system:
- User authentication with JWT
- CRUD operations for posts
- CRUD operations for comments
- Tag system
- Use SQLite as designed
```

Wait ~5 minutes for completion.

### Step 4: Add Tests
```bash
# Solo mode → Sentinel

You: Write comprehensive tests for the blog API in workspace/blog_api.py
```

### Step 5: Review Code
```bash
# Solo mode → Orion (Code Reviewer)

You: Review the blog_api.py file and suggest improvements
```

### Step 6: Document It
```bash
# Solo mode → Pixel

You: Create complete API documentation for blog_api.py with:
- Installation instructions
- API endpoints
- Example requests
- Response formats
```

### Step 7: Deploy Script
```bash
# Solo mode → Blaze (DevOps Engineer)

You: Create a deployment script for the blog API with:
- Setup virtual environment
- Install dependencies
- Initialize database
- Run migrations
- Start server
```

## Part 6: Advanced Usage (10 minutes)

### Use File Operations
```bash
# Tell agents about existing files

You: Read the config.yaml file and explain the model settings
```

### Execute Code
```bash
# Agents can run code safely

You: Create a test script and run it to verify the blog API works
```

### Iterate on Design
```bash
# Continuous improvement

You: Add rate limiting to the blog API
You: Add caching for frequently accessed posts
You: Add search functionality
```

### Combine Agents
```bash
# Team mode is powerful

You: Have Aurora redesign the database schema for better performance,
then have Nova implement the changes, and Sentinel update the tests
```

## Part 7: Best Practices (5 minutes)

### 1. Be Specific
❌ "Make a website"
✅ "Create a Flask web app with login page, dashboard, and user profile"

### 2. Break Down Big Tasks
Instead of one huge request, do:
1. Architecture design
2. Database schema
3. Core API
4. Authentication
5. Tests
6. Documentation

### 3. Use the Right Mode
- **Solo:** Quick code, specific expertise
- **Team:** Complex projects, multiple steps

### 4. Save Your Work
```bash
# Workspace is temporary - save your code!
cp -r workspace/blog_api ~/projects/
cd ~/projects/blog_api
git init
git add .
git commit -m "Initial commit"
```

### 5. Check Generated Code
Always review AI-generated code:
- Read through it
- Understand what it does
- Test it thoroughly
- Modify as needed

## Part 8: Troubleshooting (5 minutes)

### Slow Responses
```bash
# Check performance
./quick_test.py

# See optimization tips
cat docs/PERFORMANCE.md
```

### Timeouts
Make simpler requests or use API models:
```bash
./setup_proper.py
# Switch to OpenAI or Gemini
```

### Model Not Found
```bash
ollama pull codellama:7b
```

### Connection Issues
```bash
# Ensure Ollama is running
ollama serve

# Check status
curl http://localhost:11434/api/tags
```

## Part 9: Next Steps

### Explore Examples
```bash
cd examples/
cat README.md
python3 fibonacci_example.py
```

### Read Documentation
- `docs/USAGE_GUIDE.md` - Complete usage reference
- `docs/PERFORMANCE.md` - Optimization tips
- `docs/INTEGRATIONS.md` - Workflow integration

### Build Your Project
Ideas to try:
- 🌐 Personal website
- 🔐 Authentication system
- 📊 Data dashboard
- 🤖 Discord bot
- 📱 API for mobile app
- 🎮 Game logic
- 📈 Analytics tool

### Share Your Experience
- What did you build?
- What worked well?
- What could be better?

## Quick Reference Card

```
SETUP
  ./setup_proper.py         First time configuration
  ./quick_test.py           Verify installation
  ./run                     Launch system

MODES
  1. Team Collaboration     Complex projects
  2. Solo Agent Chat        Quick tasks
  3. View All Agents        See the team
  
AGENTS (SOLO MODE)
  Aurora     System architecture
  Nova       Backend/API development
  Echo       Frontend development
  Orion      Code review
  Sentinel   Testing
  Pixel      Documentation
  Helix      Team coordination

WORKSPACE
  workspace/                Generated code here
  examples/                 Example projects
  docs/                     Documentation

TIPS
  - Be specific in requests
  - Break down big projects
  - Always review generated code
  - Save your work from workspace/
  - Use quick_test.py if issues
```

## Congratulations! 🎉

You've completed the tutorial and learned:
- ✅ Setup and configuration
- ✅ Basic interaction
- ✅ Building real projects
- ✅ Using different agents
- ✅ Professional workflows
- ✅ Best practices

Now go build something amazing! 🚀
