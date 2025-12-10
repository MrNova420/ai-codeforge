# Getting Started with Your Ultimate AI Dev Team

Welcome! You now have a production-ready AI development team orchestrator with 17 unique agents ready to help you build high-quality software.

## 🎯 What You Have

A complete, working system that includes:
- **17 specialized AI agents** with unique personalities
- **Team Mode**: All agents collaborate under Helix (Overseer)
- **Solo Mode**: Work with individual agents
- **Multi-model support**: OpenAI GPT-4 and Gemini Pro
- **Rich terminal interface**: Beautiful, organized chat UI
- **Easy configuration**: YAML-based setup
- **Full documentation**: README, Quick Start, and guides

## 🚀 Quick Start (5 Minutes)

### Step 1: Install API Packages (Optional but Recommended)

```bash
cd /home/mrnova420/ai-dev-team
pip install -r requirements.txt
```

This installs:
- OpenAI SDK (for GPT-4)
- Google Generative AI (for Gemini)
- Rich (for beautiful terminal UI)
- PyYAML (for configuration)

### Step 2: Test Installation

```bash
python3 test_install.py
```

This verifies everything is properly installed.

### Step 3: Launch Your Team

```bash
python3 orchestrator.py
```

Or use the convenience launcher:
```bash
./start.sh
```

### Step 4: Configure API Keys or Local Models

**Option 1: Use API Keys (OpenAI/Gemini)**
On first run, you'll be prompted to enter:
- **OpenAI API key** (get from https://platform.openai.com/api-keys)
- **Gemini API key** (get from https://makersuite.google.com/app/apikey)

**Option 2: Use Local Models (Free, Private)**
1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
2. Start Ollama: `ollama serve`
3. Download a model: `ollama pull llama2` or `ollama pull codellama`
4. Edit config.yaml and set agents to use `local` model

**See [LOCAL_MODELS_GUIDE.md](LOCAL_MODELS_GUIDE.md) for complete instructions.**

### Step 5: Start Building!

Choose your mode:
1. **Team Mode** - Full team collaboration (recommended for complex projects)
2. **Solo Mode** - Individual agent (recommended for focused tasks)

## 💡 Usage Examples

### Example 1: Team Mode - Build a Web Application

```bash
$ python3 orchestrator.py
> Select: 1 (Team Mode)

You: I need to build a todo list web app with user authentication, 
     task management, and a REST API. Use Python FastAPI and React.

Helix: Excellent project! I'll coordinate the team:

- Aurora is designing the system architecture
- Felix is documenting the API specifications
- Sage is researching best practices for auth
- Nova and Zephyr are setting up the FastAPI backend
- Ember is designing the React UI
- Ivy is implementing security measures
- Patch will handle debugging
- Pulse will create tests

I'll keep you updated as we progress. Let's start with Aurora's 
architecture proposal...
```

### Example 2: Solo Mode - Code Review

```bash
$ python3 orchestrator.py
> Select: 2 (Solo Mode)
> Choose: Atlas (The Perfectionist)

You: Review this Python function:
```python
def get_user(id):
    user = db.query(id)
    return user
```

Atlas: This code has several critical issues that must be addressed:

1. **No input validation** - The id parameter could be anything
2. **SQL injection risk** - Direct query without parameterization
3. **No error handling** - What if the user doesn't exist?
4. **Poor naming** - 'id' shadows built-in function
5. **No type hints** - Makes code harder to maintain
6. **No docstring** - Purpose unclear

Here's the corrected version:
```python
def get_user(user_id: int) -> Optional[User]:
    """
    Retrieve a user from the database by ID.
    
    Args:
        user_id: The unique identifier of the user
        
    Returns:
        User object if found, None otherwise
        
    Raises:
        ValueError: If user_id is invalid
    """
    if not isinstance(user_id, int) or user_id < 1:
        raise ValueError(f"Invalid user_id: {user_id}")
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except DatabaseError as e:
        logger.error(f"Database error retrieving user {user_id}: {e}")
        raise
```

This addresses all issues and follows best practices.
```

### Example 3: Solo Mode - Architecture Design

```bash
$ python3 orchestrator.py
> Select: 2 (Solo Mode)
> Choose: Nova (Lead Engineer)

You: How should I structure a microservices architecture for 
     an e-commerce platform?

Nova: For an e-commerce microservices architecture, I recommend 
this structure:

**Core Services:**
1. **User Service** - Authentication, profiles, preferences
2. **Product Catalog Service** - Products, categories, search
3. **Shopping Cart Service** - Cart management, session handling
4. **Order Service** - Order processing, history, tracking
5. **Payment Service** - Payment processing, refunds
6. **Inventory Service** - Stock management, reservations
7. **Notification Service** - Emails, SMS, push notifications

**Architecture Pattern:**
- API Gateway (Kong or AWS API Gateway)
- Service mesh (Istio) for inter-service communication
- Event bus (Kafka) for async communication
- Separate databases per service (database per service pattern)
- Centralized logging (ELK stack)
- Distributed tracing (Jaeger)

**Communication:**
- Synchronous: REST/gRPC via API Gateway
- Asynchronous: Event-driven via Kafka

Here's the high-level diagram:
[Detailed architecture explanation continues...]
```

## 🎨 Your 17 Agents

### Planners/Designers
- **Aurora** - Visionary big-picture strategist
- **Felix** - Detail-oriented architect
- **Sage** - Research and best practices expert
- **Ember** - Creative UI/UX designer
- **Orion** - Systems and process optimizer

### Critics/Judges
- **Atlas** - Perfectionist code reviewer
- **Mira** - Constructive analyst
- **Vex** - Provocative challenger
- **Sol** - Industry veteran
- **Echo** - Data-driven evaluator

### Developers
- **Nova** - Lead engineer and architect
- **Quinn** - Code artisan (clean code)
- **Blaze** - Performance optimization guru
- **Ivy** - Security specialist
- **Zephyr** - Integration and API expert

### Developer Assistants
- **Pixel** - Assists Nova
- **Script** - Assists Quinn
- **Turbo** - Assists Blaze
- **Sentinel** - Assists Ivy
- **Link** - Assists Zephyr

### Specialists
- **Patch** - Bug fixer and debugger
- **Pulse** - Testing and QA specialist

### Overseer
- **Helix** - Team coordinator and manager

## ⚙️ Configuration

### Choosing Models for Agents

Edit `config.yaml`:

```yaml
agent_models:
  # Use GPT-4 for technical leads
  helix: openai
  nova: openai
  quinn: openai
  
  # Use Gemini for research and creative work
  aurora: gemini
  sage: gemini
  ember: gemini
  
  # Mix and match as you prefer
  atlas: openai
  patch: openai
  pulse: openai
```

### Adding/Updating API Keys

```bash
python3 orchestrator.py
> Select: 4 (Configure Settings)
> Follow prompts to update keys
```

## 📚 Documentation

- **README.md** - Complete documentation
- **QUICKSTART.md** - 5-minute quick start
- **PROJECT_STATUS.md** - What's built and working
- **GETTING_STARTED.md** - This file

## 🎯 Best Practices

### 1. Start with Team Mode for New Projects
Let Helix coordinate the team for the best results.

### 2. Use Solo Mode for Specific Tasks
- Code reviews → Atlas
- Architecture → Nova
- Performance → Blaze
- Security → Ivy
- Bug fixes → Patch

### 3. Be Specific in Your Requests
Instead of "build an app", try:
> "Build a REST API for a blog platform using FastAPI and PostgreSQL. 
> Include user authentication with JWT, CRUD operations for posts and 
> comments, and comprehensive tests."

### 4. Leverage Agent Specializations
Each agent has unique strengths - use them!

### 5. Iterate and Refine
Ask follow-up questions, request improvements, challenge ideas.

## 🔧 Troubleshooting

### "API key not configured"
Run: `python3 orchestrator.py` → Option 4 → Enter your keys

### "Package not installed"
Run: `pip install -r requirements.txt`

### Agent not responding as expected
- Check your API keys in `config.yaml`
- Try a different model (OpenAI vs Gemini)
- Be more specific in your request

### Want to customize agents?
Edit the `*_agents.md` files to change personalities and approaches.

## 🎉 You're Ready!

Your Ultimate AI Dev Team is fully built and ready to use. Start with:

```bash
python3 orchestrator.py
```

Choose Team Mode for your first project and let Helix coordinate the team!

## 📞 Next Steps

1. **Try Team Mode** with a sample project
2. **Experiment with different agents** in Solo Mode
3. **Customize configurations** to match your preferences
4. **Read the full README** for advanced features
5. **Start building** something amazing!

---

**Project Location:** `/home/mrnova420/ai-dev-team`

**Main Command:** `python3 orchestrator.py`

**Quick Launcher:** `./start.sh`

🚀 **Happy building with your Ultimate AI Dev Team!**
