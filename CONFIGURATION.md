# AI CodeForge Configuration Guide

Complete guide to configuring and customizing AI CodeForge for your needs.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Configuration Files](#configuration-files)
3. [Interface Modes](#interface-modes)
4. [Agent Configuration](#agent-configuration)
5. [Performance Tuning](#performance-tuning)
6. [Security Settings](#security-settings)
7. [Workspace Management](#workspace-management)
8. [Environment Variables](#environment-variables)
9. [Advanced Settings](#advanced-settings)
10. [CLI Configuration](#cli-configuration)

---

## Quick Start

### First Time Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run setup
./setup.sh

# Initialize system
python3 startup.py --mode auto

# Configure (optional)
python3 config_manager.py
```

### Basic Configuration

```bash
# Set interface mode
python3 config_manager.py set interface_mode advanced

# Set default agent
python3 config_manager.py set default_agent felix

# Enable caching
python3 config_manager.py set enable_caching true
```

---

## Configuration Files

All configuration is stored in `~/.codeforge/`:

```
~/.codeforge/
├── config.json          # Main configuration
├── agents.json          # Agent-specific settings
├── state.json           # Application state
├── history.json         # Command history
└── .env                 # Environment variables
```

### config.json Structure

```json
{
  "version": "2.0.0",
  "interface": {
    "mode": "simple",
    "theme": "dark",
    "show_progress": true,
    "verbose": false,
    "output_format": "text"
  },
  "performance": {
    "enable_caching": true,
    "cache_ttl": 3600,
    "max_concurrent_agents": 5,
    "fast_startup": true
  },
  "security": {
    "enable_docker_sandbox": true,
    "network_isolation": true,
    "max_execution_time": 300
  },
  "workspace": {
    "workspace_dir": "workspace",
    "output_dir": "output",
    "logs_dir": "logs"
  }
}
```

---

## Interface Modes

AI CodeForge supports three interface modes:

### 1. Simple Mode (Default)

Best for: Beginners, quick tasks

```bash
# Use simple CLI
./codeforge code "create API"
./codeforge test "api.py"
```

**Features:**
- Easy commands
- Interactive mode
- Minimal options
- Clear output

### 2. Advanced Mode

Best for: Power users, complex projects

```bash
# Use advanced CLI with full options
./codeforge_advanced code "task" --language python --output file.py --agent felix
./codeforge_advanced team "task" --mode parallel
./codeforge_advanced status --watch
```

**Features:**
- Argument parsing
- Configuration management
- History tracking
- JSON output
- Watch mode

### 3. Expert Mode

Best for: Automation, scripting, CI/CD

```bash
# Set expert mode
python3 config_manager.py set interface_mode expert

# Use with full control
./codeforge_advanced code "task" --json --no-cache --timeout 600
```

**Features:**
- All advanced features
- No prompts/confirmations
- Scriptable output
- Fine-grained control

**Setting Interface Mode:**

```python
from config_manager import get_config_manager

config = get_config_manager()
config.set_interface_mode('advanced')  # simple, advanced, expert
```

---

## Agent Configuration

### Default Agent

```bash
# Set default agent for code generation
python3 config_manager.py set default_agent felix
```

### Agent-Specific Settings

```python
from config_manager import get_config_manager

config = get_config_manager()

# Configure felix
config.configure_agent('felix',
    temperature=0.8,
    max_tokens=3000,
    personality='creative',
    custom_instructions='Always include type hints'
)

# Configure mira (security)
config.configure_agent('mira',
    temperature=0.3,
    max_tokens=2000,
    personality='cautious'
)
```

### Available Agents

**Planners:**
- `aurora` - Product Manager
- `sage` - Lead Architect  
- `felix` - Senior Developer
- `ember` - Creative Director

**Critics:**
- `orion` - Code Reviewer
- `atlas` - Performance Specialist
- `mira` - Security Engineer
- `vex` - Critical Analyst

**Specialists:**
- `sol` - Backend API
- `echo` - Frontend/UI
- `nova` - DevOps
- `quinn` - QA Engineer
- `blaze` - Mobile Dev
- `ivy` - Data Engineer
- `zephyr` - Cloud Architect

**Assistants:**
- `pixel` - UX Designer
- `script` - Technical Writer
- `turbo` - Performance Engineer
- `sentinel` - Monitoring/SRE

**Special:**
- `helix` - Research Lead
- `patch` - Bug Hunter
- `pulse` - Integration Specialist
- `link` - Communication Lead

---

## Performance Tuning

### Caching

```python
# Enable/disable caching
config.set_caching(True)

# Set cache TTL (seconds)
config.set_cache_ttl(3600)  # 1 hour

# Expected speedup: 100-300x for repeated queries
```

### Concurrency

```python
# Set max concurrent agents
config.set_max_concurrent(5)

# More concurrent = faster but more resources
# Recommended: 3-10 depending on your system
```

### Fast Startup

```python
# Enable fast startup (< 5 seconds)
config.toggle_fast_startup(True)

# Preload models in background
config.performance.preload_models = True
```

### Memory Limits

```python
# Set memory limit (MB)
config.performance.memory_limit_mb = 512

# Lower = more constrained but safer
# Higher = more capable but uses more RAM
```

---

## Security Settings

### Docker Sandboxing

```python
# Enable Docker sandbox for code execution
config.set_docker_sandbox(True)

# Network isolation
config.set_network_isolation(True)

# Read-only filesystem
config.security.read_only_filesystem = True
```

### Execution Limits

```python
# Max execution time (seconds)
config.set_max_execution_time(300)  # 5 minutes

# For longer-running tasks, increase this
```

### Allowed Domains

```python
# Add domains for web access
config.add_allowed_domain('api.github.com')
config.add_allowed_domain('stackoverflow.com')
```

### Code Scanning

```python
# Enable automatic code scanning
config.security.scan_code = True

# Scans for vulnerabilities before execution
```

---

## Workspace Management

### Directory Structure

```python
# Set workspace directory
config.set_workspace_dir('~/projects/myapp')

# Set output directory
config.set_output_dir('~/projects/myapp/output')

# Auto-create directories
config.workspace.auto_create_dirs = True
config.create_workspace_dirs()
```

### Git Integration

```python
# Enable Git integration
config.workspace.git_enabled = True

# Set default branch
config.workspace.default_branch = 'main'
```

---

## Environment Variables

Create `~/.codeforge/.env`:

```bash
# API Keys (if using external services)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Optional: Custom endpoints
LLM_ENDPOINT=http://localhost:8000
LLM_MODEL=custom-model

# Database
DATABASE_URL=postgresql://localhost/codeforge

# Docker
DOCKER_HOST=unix:///var/run/docker.sock

# Logging
LOG_LEVEL=INFO
LOG_FILE=~/.codeforge/logs/app.log
```

---

## Advanced Settings

### Custom Settings

```python
# Set any custom setting
config.set_custom('my_setting', 'my_value')

# Get custom setting
value = config.get_custom('my_setting', default='default_value')
```

### Export/Import Configuration

```bash
# Export to file
python3 config_manager.py export my_config.json

# Export to YAML
python3 config_manager.py export my_config.yaml

# Import from file
python3 config_manager.py import my_config.json
```

```python
from config_manager import get_config_manager

config = get_config_manager()

# Export
config.export_config('backup.json', format='json')
config.export_config('backup.yaml', format='yaml')

# Import
config.import_config('backup.json')
```

### Reset to Defaults

```bash
# Reset all settings
python3 config_manager.py reset
```

```python
config.reset_to_defaults()
```

---

## CLI Configuration

### Simple CLI (`codeforge`)

No configuration needed. Just use it!

```bash
./codeforge
./codeforge code "task"
./codeforge help
```

### Advanced CLI (`codeforge_advanced`)

#### Command History

```bash
# View history
./codeforge_advanced history

# View last 20 commands
./codeforge_advanced history --limit 20

# Export history as JSON
./codeforge_advanced history --json > history.json
```

#### Configuration Commands

```bash
# List all config
./codeforge_advanced config --list

# Set config value
./codeforge_advanced config --set default_agent=nova

# Get specific config
./codeforge_advanced config default_agent
```

#### Output Formats

```bash
# Text output (default)
./codeforge_advanced agents

# JSON output
./codeforge_advanced agents --json

# Verbose output
./codeforge_advanced agents --verbose
```

#### Watch Mode

```bash
# Monitor system in real-time
./codeforge_advanced status --watch

# Press Ctrl+C to exit
```

---

## Configuration Examples

### Example 1: Development Setup

```python
from config_manager import get_config_manager

config = get_config_manager()

# Interface
config.set_interface_mode('advanced')
config.set_theme('dark')
config.toggle_verbose(True)

# Performance
config.set_caching(True)
config.set_max_concurrent(5)
config.toggle_fast_startup(True)

# Security (relaxed for development)
config.set_docker_sandbox(False)
config.set_network_isolation(False)

# Workspace
config.set_workspace_dir('./dev')
config.create_workspace_dirs()
```

### Example 2: Production Setup

```python
config = get_config_manager()

# Interface
config.set_interface_mode('expert')
config.set_output_format('json')

# Performance
config.set_caching(True)
config.set_cache_ttl(7200)  # 2 hours
config.set_max_concurrent(10)

# Security (strict for production)
config.set_docker_sandbox(True)
config.set_network_isolation(True)
config.set_max_execution_time(600)
config.security.scan_code = True

# Workspace
config.set_workspace_dir('/opt/codeforge/workspace')
```

### Example 3: Team Setup

```python
config = get_config_manager()

# Configure all agents for consistency
for agent_name in ['felix', 'quinn', 'mira', 'orion']:
    config.configure_agent(agent_name,
        temperature=0.7,
        max_tokens=2500
    )

# Set team defaults
config.set_custom('default_team_mode', 'collaborative')
config.set_custom('team_size', 4)

# Export for team
config.export_config('team_config.json')
```

---

## Troubleshooting

### Configuration Not Loading

```bash
# Check config file
ls -la ~/.codeforge/

# Reset to defaults
python3 config_manager.py reset

# Manually delete and recreate
rm -rf ~/.codeforge/
python3 startup.py
```

### Performance Issues

```python
# Check current settings
from config_manager import get_config_manager
config = get_config_manager()
print(config.get_summary())

# Optimize
config.set_caching(True)
config.toggle_fast_startup(True)
config.set_max_concurrent(3)  # Reduce if system is slow
```

### Permission Issues

```bash
# Fix permissions
chmod 755 ~/.codeforge
chmod 644 ~/.codeforge/*.json

# Or recreate
rm -rf ~/.codeforge/
python3 startup.py
```

---

## Summary

**Configuration Locations:**
- Global: `~/.codeforge/config.json`
- Project: `./codeforge.json` (optional)
- Environment: `~/.codeforge/.env`

**Key Commands:**
```bash
# View config
python3 config_manager.py

# Set value
python3 config_manager.py set key value

# Export/import
python3 config_manager.py export file.json
python3 config_manager.py import file.json

# Reset
python3 config_manager.py reset

# Initialize
python3 startup.py
```

**Programmatic Access:**
```python
from config_manager import get_config_manager

config = get_config_manager()
# Use config methods...
```

---

For more information, see:
- `README.md` - General usage
- `CONTRIBUTING.md` - Development setup
- `FINAL_COMPLETE_SUMMARY.md` - Feature overview
