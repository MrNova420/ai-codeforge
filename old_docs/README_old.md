# Ultimate AI Dev Team

A professional, production-ready orchestrator for managing an elite team of AI agents for high-end software development.

## Features

- 🤖 **17 Unique AI Agents** with distinct personalities and specializations
- 👥 **Team Mode**: All agents collaborate under Helix (Overseer) supervision
- 🎯 **Solo Mode**: Work with individual agents for focused tasks
- 🔌 **Multi-Model Support**: OpenAI, Gemini, or local models
- 💬 **Rich Chat Interface**: Beautiful terminal UI with live updates
- ⚙️ **Easy Configuration**: Simple YAML-based setup
- 📦 **Portable**: Share with your team or use across projects

## Quick Start

### 1. Installation

```bash
cd ai-dev-team
pip install -r requirements.txt
```

### 2. First-Time Setup

Run the orchestrator for the first time:

```bash
python3 orchestrator.py
```

You'll be prompted to enter your API keys:
- OpenAI API key (for GPT-4)
- Gemini API key (for Gemini Pro)

You can skip either if you prefer using only one provider.

### 3. Launch Your Team

**Team Mode** (recommended for complex projects):
```bash
python3 orchestrator.py
# Select option 1: Team Mode
```

**Solo Agent Mode** (for focused work):
```bash
python3 orchestrator.py
# Select option 2: Solo Agent Mode
# Then choose your agent
```

## Your AI Dev Team

### Planners/Designers (5 agents)
- **Aurora**: Visionary Strategist - Big-picture planning and roadmaps
- **Felix**: Detail Architect - Thorough blueprints and documentation
- **Sage**: Research Maven - Deep research and best practices
- **Ember**: Creative Designer - UI/UX and visual design
- **Orion**: Systems Planner - Architecture and process optimization

### Critics/Judges (5 agents)
- **Atlas**: The Perfectionist - Uncompromising quality standards
- **Mira**: Constructive Analyst - Balanced, practical feedback
- **Vex**: The Challenger - Questions assumptions and pushes boundaries
- **Sol**: The Veteran - Industry best practices and wisdom
- **Echo**: Data-Driven Judge - Metrics and quantifiable feedback

### Developers (5 agents)
- **Nova**: Lead Engineer - System architecture and leadership
- **Quinn**: Code Artisan - Clean, beautiful code
- **Blaze**: Performance Guru - Optimization and speed
- **Ivy**: Security Specialist - Security and compliance
- **Zephyr**: Integration Expert - APIs and automation

### Developer Assistants (5 agents)
- **Pixel**: Nova's Assistant
- **Script**: Quinn's Assistant
- **Turbo**: Blaze's Assistant
- **Sentinel**: Ivy's Assistant
- **Link**: Zephyr's Assistant

### Specialists
- **Patch**: The Fixer - Bug hunting and troubleshooting
- **Pulse**: The Tester - Comprehensive testing and QA

### Overseer
- **Helix**: The Overseer - Team management and coordination

## Configuration

### Editing config.yaml

```yaml
# API Keys
openai_api_key: "your-key-here"
gemini_api_key: "your-key-here"

# Model assignment per agent
agent_models:
  aurora: openai     # Use OpenAI for Aurora
  sage: gemini       # Use Gemini for Sage
  helix: openai      # Use OpenAI for Helix
  # ... customize for each agent
```

### Model Options
- `openai` - Uses GPT-4 (requires OpenAI API key)
- `gemini` - Uses Gemini Pro (requires Gemini API key)
- `local` - Uses local models via Ollama (free, private, offline)

**See [LOCAL_MODELS_GUIDE.md](LOCAL_MODELS_GUIDE.md) for complete local setup instructions.**

## Usage Examples

### Team Mode - Complex Project
```
You: "I need to build a REST API for a social media platform with authentication, posts, and comments"

Helix: "I'll coordinate the team for this project. Let me break this down:
- Aurora and Felix will design the architecture
- Sage will research best practices for auth
- Nova and Ivy will implement the backend
- Patch and Pulse will handle testing
I'll oversee everything and keep you updated."
```

### Solo Mode - Code Review
```
python3 orchestrator.py
# Select Solo Mode
# Choose Atlas (The Perfectionist)

You: "Review this Python function: [paste code]"

Atlas: "This code has several issues that must be addressed:
1. No input validation
2. Poor error handling
3. Not following PEP 8
Here's how to fix it..."
```

## Advanced Features

### Switching Models
Edit `config.yaml` to assign different models to different agents:
```yaml
agent_models:
  helix: openai      # Helix uses GPT-4
  aurora: gemini     # Aurora uses Gemini
  nova: openai       # Nova uses GPT-4
```

### Team Collaboration
In Team Mode, Helix coordinates all agents. You can:
- Type `agents` to see active team members
- Type `status` to get project status
- Give high-level instructions and let Helix delegate

### Custom Agent Personalities
Edit the `.md` files in the project root to customize agent personalities:
- `planner_designer_agents.md`
- `critic_judge_agents.md`
- `developer_agents.md`
- etc.

## Troubleshooting

### "API key not configured"
Run the orchestrator and select option 4 (Configure Settings) to add your API keys.

### "openai package not installed"
```bash
pip install -r requirements.txt
```

### Agent not responding
Check your API keys in `config.yaml` and ensure you have internet connectivity.

## Project Structure

```
ai-dev-team/
├── orchestrator.py              # Main entry point
├── agent_chat.py                # Chat interface and API integration
├── config.yaml                  # Your configuration (auto-created)
├── config_template.yaml         # Template for new setups
├── requirements.txt             # Python dependencies
├── planner_designer_agents.md   # Agent profiles
├── critic_judge_agents.md
├── developer_agents.md
├── developer_assistant_agents.md
├── debugger_fixer_agent.md
├── tester_agent.md
└── overseer_agent.md
```

## For Sharing

To share this project with others:
1. Delete `config.yaml` (contains your API keys)
2. Share the entire directory
3. Recipients run `python3 orchestrator.py` to set up their own keys

## Roadmap

- [x] Multi-agent personalities
- [x] OpenAI and Gemini support
- [x] Team and Solo modes
- [x] Rich terminal UI
- [x] Local model support (Ollama)
- [ ] Agent memory and persistence
- [ ] Multi-user collaboration
- [ ] Web UI
- [ ] Plugin system

## License

MIT License - Use freely for personal or commercial projects

## Support

For issues or questions, check the agent profiles in the `.md` files or edit `config.yaml` to customize behavior.