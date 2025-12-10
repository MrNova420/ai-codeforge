# Team Collaboration Guide

Complete guide to using the multi-agent collaboration features effectively.

## Overview

AI Dev Team offers two collaboration modes:

1. **Enhanced Mode** - Full multi-agent with progress tracking (default)
2. **Simple Mode** - Fast single overseer response

## Enhanced Collaboration Mode

### What It Does

1. **Analyzes Request** - Helix breaks down your request
2. **Creates Plan** - Identifies which agents are needed
3. **Assigns Tasks** - Delegates work to specialized agents
4. **Tracks Progress** - Shows real-time progress for each agent
5. **Compiles Results** - Combines all agent outputs

### Visual Interface

```
📋 Helix's Plan
┌────────────────────────────────────────┐
│ Breaking down into 3 tasks:           │
│ - Nova: Create backend API             │
│ - Echo: Create frontend components     │
│ - Sentinel: Write tests                │
└────────────────────────────────────────┘

⚡ Executing 3 Tasks...
⠋ Nova         ████████████████████ 100%  Complete ✓
⠋ Echo         ████████████████████ 100%  Complete ✓
⠋ Sentinel     ████████████        60%   Generating...

📦 Agent Results:
┌─ Nova ─────────────────────────────────┐
│ [Generated API code here...]           │
└────────────────────────────────────────┘
```

### When To Use

**✅ Use Enhanced Mode For:**
- Complex projects with multiple components
- Tasks requiring different expertise areas
- Learning how the team works together
- Projects you want reviewed and tested
- Architecture and design work

**❌ Don't Use Enhanced Mode For:**
- Quick one-line code snippets
- Simple questions
- Tight time constraints
- Low-end hardware (use fast preset)

## Configuration Presets

### Fast Preset
```python
Enhanced: No
Timeout: 60s
Tokens: 300
Best for: Quick tasks, simple questions
```

### Balanced Preset (Default)
```python
Enhanced: Yes
Timeout: 180s (3 min)
Tokens: 500
Best for: Most projects, good balance
```

### Thorough Preset
```python
Enhanced: Yes
Timeout: 300s (5 min)
Tokens: 1000
Best for: Complex projects, high quality
```

### Minimal Preset
```python
Enhanced: No
Timeout: 30s
Tokens: 200
Best for: Very low-end hardware
```

## Changing Modes

### In The UI
```
Main Menu → 6. Configuration → 1. Switch preset
```

### In Code
```python
# Edit settings.py
ACTIVE_PRESET = 'fast'  # or 'balanced', 'thorough', 'minimal'
```

### Temporarily
```python
# In your session
import settings
settings.apply_preset('fast')
```

## Timeouts Explained

### Why 3 Minutes?

With local models (codellama:7b at ~4.5 tokens/sec):
- Simple task (200 tokens): ~45 seconds
- Medium task (500 tokens): ~110 seconds
- Complex task (1000 tokens): ~220 seconds

Multiple agents in sequence:
- 3 agents × 60s each = 180s (3 min)
- 5 agents × 40s each = 200s (3.3 min)

**3 minutes = Sweet spot for most tasks**

### Adjusting Timeouts

```python
# For faster local model or API models
settings.COLLABORATION_TIMEOUT = 120  # 2 min

# For complex multi-step tasks
settings.COLLABORATION_TIMEOUT = 300  # 5 min

# For very simple tasks
settings.COLLABORATION_TIMEOUT = 60  # 1 min
```

## Agent Selection Logic

Helix (overseer) selects agents based on:

1. **Task Type**
   - "Create API" → Nova (Backend)
   - "Design UI" → Felix (UI/UX)
   - "Write tests" → Sentinel (Testing)

2. **Complexity**
   - Simple: 1-2 agents
   - Medium: 3-4 agents
   - Complex: 5+ agents

3. **Dependencies**
   - Architecture first (Aurora)
   - Implementation second (Developers)
   - Testing last (Sentinel)
   - Review throughout (Orion)

## Example Workflows

### Workflow 1: Simple Feature
```
User: "Add user login"

Helix Plan:
- Nova: Implement authentication

Result: One agent, ~60-90s
```

### Workflow 2: Medium Feature
```
User: "Create blog post system"

Helix Plan:
- Aurora: Design database schema
- Nova: Implement backend API
- Sentinel: Write tests

Result: 3 agents, ~150-180s
```

### Workflow 3: Complex Project
```
User: "Build e-commerce checkout"

Helix Plan:
- Aurora: System architecture
- Nova: Payment processing API
- Echo: Checkout UI
- Mira: Security review
- Sentinel: Integration tests

Result: 5 agents, ~250-300s
```

## Progress Indicators

### Status Icons
- `⏳ Pending` - Waiting to start
- `⚙️  Working` - Currently generating
- `✅ Complete` - Finished successfully
- `❌ Error` - Something went wrong

### Progress Bar
```
⠋ Nova    ████████████████████ 100%  Complete ✓
         Agent name  Progress    %     Status
```

### Timing
Each agent shows elapsed time:
- `(0.5s)` - Very fast
- `(15s)` - Normal
- `(60s)` - Slow but okay
- `(120s+)` - Very slow, consider faster model

## Handling Long Tasks

### Task Runs Over 3 Minutes

**Option 1: Wait for timeout**
- System will try for full timeout
- You'll get partial results
- Can retry with simpler prompt

**Option 2: Break it down**
Instead of:
```
"Create complete app with auth, API, frontend, tests"
```

Do step-by-step:
```
1. "Design app architecture"
2. "Create backend API"
3. "Create frontend"
4. "Add tests"
```

**Option 3: Use API models**
```bash
./setup_proper.py
# Choose OpenAI or Gemini
# 10-20x faster responses
```

## Optimization Tips

### For Speed
1. Use 'fast' preset
2. Disable enhanced mode
3. Be more specific in requests
4. Use solo mode for simple tasks
5. Switch to API models

### For Quality
1. Use 'thorough' preset
2. Enable enhanced mode
3. Break complex tasks into steps
4. Let multiple agents review
5. Use longer timeouts

### For Low-End Hardware
1. Use 'minimal' preset
2. Disable progress bars
3. Use simple mode
4. Close other applications
5. Consider smaller model

## Troubleshooting

### Agents Not Appearing
- Check if enhanced mode enabled
- Verify agents exist in config
- Look at Helix's plan - might be simple request
- Try more complex request

### Timeout Errors
- Increase timeout in settings
- Use simpler prompts
- Try fast preset
- Check system resources
- Consider API models

### Slow Performance
- Check CPU/RAM usage
- Use faster model (mistral vs codellama)
- Reduce response token limit
- Close background applications
- See docs/PERFORMANCE.md

### Wrong Agents Selected
- Be more specific in request
- Mention desired expertise
- Break task into steps
- Use solo mode for direct control

## Advanced Usage

### Force Specific Agents

Instead of relying on Helix:
```bash
# Use solo mode
Main Menu → 2. Solo Agent Chat → Select specific agent
```

### Chain Agent Work
```python
# In team mode
1. "Aurora, design the database"
2. "Nova, implement the design from Aurora"
3. "Sentinel, test Nova's implementation"
```

### Parallel Work
Currently sequential, but agents can work on independent tasks:
```
Good: "Create API (Nova) and UI (Echo) for blog"
  → Both get separate tasks
  
Better: Split into two requests
  1. "Nova: Create blog API"
  2. "Echo: Create blog UI"
```

### Review Workflow
```
1. Create code with developer agent
2. "Orion, review the code above"
3. Apply Orion's suggestions
4. "Sentinel, write tests"
```

## Best Practices

### 1. Start Simple
Test with small tasks before complex projects.

### 2. Be Specific
More details = better agent selection and results.

### 3. Use Right Mode
- Quick code: Solo mode
- Full feature: Enhanced mode
- Question: Solo mode
- Project: Enhanced mode

### 4. Watch The Progress
Learn which tasks are fast/slow for your hardware.

### 5. Adjust Settings
Find what works for your use case and hardware.

### 6. Save Good Prompts
When a prompt works well, save it for reuse.

## Configuration Reference

### settings.py Variables
```python
ENHANCED_COLLABORATION      # True/False
COLLABORATION_TIMEOUT       # Seconds (60-600)
MAX_CONCURRENT_AGENTS       # Number (1-10)
AGENT_TIMEOUT              # Seconds (30-300)
MAX_RESPONSE_TOKENS        # Number (100-2000)
SHOW_PROGRESS_BARS         # True/False
```

### Quick Changes
```python
# In Python REPL or code
import settings

# Toggle mode
settings.ENHANCED_COLLABORATION = False

# Change timeout
settings.COLLABORATION_TIMEOUT = 240  # 4 min

# Apply preset
settings.apply_preset('thorough')
```

## Performance Expectations

### With codellama:7b (CPU)
- Simple request: 60-90s
- Medium request: 120-180s
- Complex request: 180-300s

### With API models (GPT-3.5)
- Simple request: 5-10s
- Medium request: 15-30s
- Complex request: 30-60s

### Hardware Impact
- 4 cores: Multiply times by 1.5x
- 8 cores: Normal times
- 16 cores: Divide times by 0.8x
- GPU: Divide times by 0.3-0.5x

## Next Steps

1. Try enhanced mode with simple task
2. Watch agent progress
3. Try different presets
4. Adjust for your hardware
5. Build something complex!

---

**Questions?** See docs/USAGE_GUIDE.md or docs/PERFORMANCE.md
