#!/usr/bin/env python3
"""
AI Dev Team - Configuration Settings
Adjust these for your needs and hardware
"""

# ============================================================================
# COLLABORATION MODE SETTINGS
# ============================================================================

# Use enhanced collaboration with multi-agent coordination
# True: Full multi-agent with progress bars and task tracking
# False: Simple mode - overseer only
ENHANCED_COLLABORATION = True

# Timeout for collaboration tasks (seconds)
# Realistic: Complex multi-agent tasks can take 5-10 minutes
# Simple tasks: 2-3 minutes, Complex: 5-10 minutes
COLLABORATION_TIMEOUT = 300  # 5 minutes (realistic for multi-agent)

# Maximum number of agents to use simultaneously
# Lower = faster but less specialized, Higher = slower but more thorough
MAX_CONCURRENT_AGENTS = 5

# ============================================================================
# AGENT RESPONSE SETTINGS
# ============================================================================

# Default timeout for single agent responses (seconds)
# Realistic: codellama:7b at 4-5 tok/s needs time for quality responses
AGENT_TIMEOUT = 180  # 3 minutes (allows 750+ tokens)

# Maximum tokens per response
# Lower = faster responses, Higher = more detailed responses
MAX_RESPONSE_TOKENS = 500

# Temperature for responses (0.0 = deterministic, 1.0 = creative)
RESPONSE_TEMPERATURE = 0.7

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# Enable streaming responses in solo mode
ENABLE_STREAMING = True

# Enable response caching (speeds up repeated questions)
ENABLE_CACHING = False  # Not implemented yet

# Show detailed timing information
SHOW_TIMING_INFO = True

# ============================================================================
# UI SETTINGS
# ============================================================================

# Show agent status updates
SHOW_AGENT_STATUS = True

# Show progress bars for long tasks
SHOW_PROGRESS_BARS = True

# Truncate long responses (characters)
MAX_DISPLAY_LENGTH = 1000

# Rich UI theme
UI_THEME = "default"  # default, minimal, detailed

# ============================================================================
# WORKSPACE SETTINGS
# ============================================================================

# Workspace directory for generated code
WORKSPACE_DIR = "workspace"

# Storage directory for conversations and memory
STORAGE_DIR = "storage"

# Auto-save generated code
AUTO_SAVE_CODE = True

# Keep conversation history (sessions)
CONVERSATION_HISTORY_LIMIT = 50

# ============================================================================
# LOGGING & DEBUGGING
# ============================================================================

# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"

# Save logs to file
SAVE_LOGS = True
LOG_FILE = "ai_dev_team.log"

# Debug mode (verbose output)
DEBUG_MODE = False

# ============================================================================
# MODEL SETTINGS
# ============================================================================

# These are defaults - can be overridden in config.yaml

# Ollama settings
OLLAMA_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "codellama:7b"

# OpenAI settings
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"

# Gemini settings  
DEFAULT_GEMINI_MODEL = "gemini-pro"

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Retry failed requests
MAX_RETRIES = 2
RETRY_DELAY = 5  # seconds

# Rate limiting (requests per minute)
RATE_LIMIT = 60

# Memory management
MAX_MEMORY_SIZE_MB = 100
MEMORY_CLEANUP_INTERVAL = 3600  # 1 hour

# File operations
MAX_FILE_SIZE_MB = 10
ALLOWED_FILE_TYPES = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.md', '.txt', '.json', '.yaml', '.yml']

# Code execution
ENABLE_CODE_EXECUTION = True
CODE_EXECUTION_TIMEOUT = 30  # seconds
SANDBOX_ENABLED = True

# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================

PRESETS = {
    'fast': {
        'ENHANCED_COLLABORATION': False,
        'COLLABORATION_TIMEOUT': 120,  # 2 min
        'AGENT_TIMEOUT': 90,
        'MAX_RESPONSE_TOKENS': 300,
        'MAX_CONCURRENT_AGENTS': 3
    },
    'balanced': {
        'ENHANCED_COLLABORATION': True,
        'COLLABORATION_TIMEOUT': 300,  # 5 min - REALISTIC
        'AGENT_TIMEOUT': 180,  # 3 min - REALISTIC
        'MAX_RESPONSE_TOKENS': 750,  # More complete responses
        'MAX_CONCURRENT_AGENTS': 5
    },
    'thorough': {
        'ENHANCED_COLLABORATION': True,
        'COLLABORATION_TIMEOUT': 600,  # 10 min for complex projects
        'AGENT_TIMEOUT': 300,  # 5 min per agent
        'MAX_RESPONSE_TOKENS': 1500,
        'MAX_CONCURRENT_AGENTS': 8
    },
    'minimal': {
        'ENHANCED_COLLABORATION': False,
        'COLLABORATION_TIMEOUT': 60,
        'AGENT_TIMEOUT': 60,
        'MAX_RESPONSE_TOKENS': 200,
        'SHOW_PROGRESS_BARS': False,
        'SHOW_AGENT_STATUS': False
    },
    'realistic': {
        # For daily real-world use
        'ENHANCED_COLLABORATION': True,
        'COLLABORATION_TIMEOUT': 480,  # 8 min - very realistic
        'AGENT_TIMEOUT': 240,  # 4 min per agent
        'MAX_RESPONSE_TOKENS': 1000,
        'MAX_CONCURRENT_AGENTS': 6,
        'SHOW_TIMING_INFO': True
    }
}

# Active preset (or None for custom settings above)
# 'realistic' is recommended for daily use with local models
ACTIVE_PRESET = 'realistic'  # None, 'fast', 'balanced', 'thorough', 'minimal', 'realistic'

# ============================================================================
# APPLY PRESET
# ============================================================================

def apply_preset(preset_name: str = None):
    """Apply a preset configuration."""
    if preset_name is None:
        preset_name = ACTIVE_PRESET
    
    if preset_name and preset_name in PRESETS:
        globals().update(PRESETS[preset_name])
        return True
    return False

# Auto-apply preset on import
if ACTIVE_PRESET:
    apply_preset(ACTIVE_PRESET)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_setting(key: str, default=None):
    """Get a setting value."""
    return globals().get(key, default)

def set_setting(key: str, value):
    """Set a setting value."""
    globals()[key] = value

def list_presets():
    """List available presets."""
    return list(PRESETS.keys())

def get_current_config():
    """Get current configuration as dict."""
    return {
        'ENHANCED_COLLABORATION': ENHANCED_COLLABORATION,
        'COLLABORATION_TIMEOUT': COLLABORATION_TIMEOUT,
        'AGENT_TIMEOUT': AGENT_TIMEOUT,
        'MAX_RESPONSE_TOKENS': MAX_RESPONSE_TOKENS,
        'RESPONSE_TEMPERATURE': RESPONSE_TEMPERATURE,
        'MAX_CONCURRENT_AGENTS': MAX_CONCURRENT_AGENTS,
        'ENABLE_STREAMING': ENABLE_STREAMING,
        'SHOW_PROGRESS_BARS': SHOW_PROGRESS_BARS,
        'ACTIVE_PRESET': ACTIVE_PRESET
    }

def print_config():
    """Print current configuration."""
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    config = get_current_config()
    
    table = Table(title="AI Dev Team Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in config.items():
        table.add_row(key, str(value))
    
    console.print(table)

# ============================================================================
# NOTES
# ============================================================================

"""
QUICK TIPS:

1. For faster responses:
   - Use 'fast' preset
   - Disable enhanced collaboration
   - Reduce timeouts

2. For better quality:
   - Use 'thorough' preset
   - Enable enhanced collaboration
   - Increase timeouts and token limits

3. For low-end hardware:
   - Use 'minimal' preset
   - Disable progress bars
   - Use smaller token limits

4. To change settings:
   - Edit this file directly, OR
   - Use set_setting() in code, OR
   - Choose a different ACTIVE_PRESET

5. Custom configuration:
   - Set ACTIVE_PRESET = None
   - Adjust individual settings above
"""
