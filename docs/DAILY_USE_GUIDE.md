# Daily Use Guide - AI Dev Team

Realistic guide for using AI Dev Team in your daily workflow.

## Reality Check: Local Model Performance

### What To Expect (codellama:7b on CPU)

**Single Agent Tasks:**
- Simple (100 tokens): 30-60 seconds
- Medium (500 tokens): 2-3 minutes  
- Complex (1000+ tokens): 4-6 minutes

**Multi-Agent Collaboration:**
- 2-3 agents: 5-8 minutes
- 4-5 agents: 8-12 minutes
- 6+ agents: 12-20 minutes

**These times are NORMAL for local models. If you need faster:**
- Use API models (GPT-3.5/4) → 10-50x faster
- Upgrade hardware (GPU) → 3-5x faster
- Use smaller, faster models

## Recommended Settings (Updated Dec 10)

### Default: "Realistic" Preset

```python
Mode: Enhanced Collaboration
Collaboration Timeout: 8 minutes
Agent Timeout: 4 minutes per agent
Max Tokens: 1000 per response
```

**Why these numbers?**
- Most real tasks need thoughtful, complete responses
- Rushing agents produces incomplete/poor code
- Better to wait 5-10 min for quality than restart repeatedly

### When to Use Other Presets

**Fast** (2-4 min total):
- Quick questions
- Code snippets
- Simple fixes
- Already know what you want

**Balanced** (5-7 min):
- Medium features
- Standard tasks
- Good default if "realistic" too slow

**Thorough** (10-15 min):
- Complex architecture
- Full applications
- Learning projects
- Maximum quality

## Daily Workflow Patterns

### Pattern 1: Morning Planning (10-15 min)

```bash
./run

# Solo Mode → Aurora (Architect)
"Plan today's features: [describe project]"
(Takes 3-4 min, worth it for solid plan)

# Save the plan
Copy output to notes

# Use plan throughout day
```

### Pattern 2: Feature Development (15-30 min)

```bash
# Step 1: Design (3-4 min)
Solo → Aurora: "Design schema for [feature]"

# Step 2: Implement (4-6 min)
Solo → Nova: "Implement [feature] using schema above"

# Step 3: Test (3-4 min)
Solo → Sentinel: "Write tests for [feature]"

# Step 4: Review (2-3 min)
Solo → Orion: "Review the code above"

Total: ~15-20 min for complete feature
```

### Pattern 3: Quick Iterations (2-5 min)

```bash
# For simple changes, use Fast preset
Settings → Switch to 'fast'

# Quick tasks
Solo → any dev agent: "Add validation to login()"
(Takes 1-2 min)

# Switch back to realistic when done
```

### Pattern 4: Learning Mode (20-30 min)

```bash
# Use thorough preset for learning
Settings → 'thorough'

# Ask for detailed explanations
"Explain microservices architecture with examples"
(Takes 5-7 min, very detailed)

# Follow-up questions
"Show implementation in Python"
(Takes 4-5 min)
```

## Time Management Tips

### 1. Batch Similar Tasks

Instead of:
```
Task 1 (5 min wait)
Task 2 (5 min wait)
Task 3 (5 min wait)
= 15 minutes of waiting
```

Do:
```
Queue all tasks mentally
Task 1 (5 min) → review while next runs
Task 2 (5 min) → work on Task 1 code
Task 3 (5 min) → integrate previous
= 15 minutes of productive work
```

### 2. Multi-Task While Waiting

**During 5-minute agent response:**
- Review previous output
- Write tests
- Update documentation
- Check other code
- Make coffee ☕

**Never just sit and watch spinner!**

### 3. Use the Right Tool

**Need it NOW:**
- Use fast preset or API models
- Solo mode, specific agent
- Very specific prompts

**Need it GOOD:**
- Use realistic/thorough preset
- Team collaboration mode
- Detailed prompts

**Need it PERFECT:**
- Multiple passes
- Different agents review
- Iterate on output

## Handling Long Wait Times

### 5+ Minute Waits

**✅ Do This:**
- Work on something else
- Review previous code
- Plan next steps
- Read documentation
- Stretch/take break

**❌ Don't Do This:**
- Stare at screen
- Get frustrated
- Cancel and restart
- Spam refresh
- Give up

### Timeouts (>10 minutes)

If task times out:

**Option 1: Break It Down**
```
Instead of:
"Build complete authentication system"

Do:
1. "Design auth database schema"
2. "Implement user registration"
3. "Implement login with JWT"
4. "Add password reset"
5. "Write auth tests"
```

**Option 2: Increase Timeout**
```python
# In settings.py
AGENT_TIMEOUT = 360  # 6 minutes
COLLABORATION_TIMEOUT = 720  # 12 minutes
```

**Option 3: Switch to API**
```bash
./setup_proper.py
# Choose OpenAI/Gemini
# Much faster, costs money
```

## Agent Selection for Daily Tasks

### Quick Reference

| Task Type | Best Agent | Expected Time |
|-----------|-----------|---------------|
| Architecture | Aurora | 3-5 min |
| Backend API | Nova | 4-6 min |
| Frontend UI | Echo | 4-6 min |
| UI Design | Felix | 2-4 min |
| Code Review | Orion | 2-3 min |
| Security | Mira | 3-4 min |
| Testing | Sentinel | 3-5 min |
| Docs | Pixel | 2-3 min |
| Debugging | Patch | 3-5 min |
| DevOps | Blaze | 3-4 min |

### When to Use Team Mode

**Use Team Mode When:**
- Building complete feature (10-15 min)
- Need multiple perspectives
- Learning how components fit
- Want automatic testing/review

**Use Solo Mode When:**
- Fixing specific bug (3-5 min)
- Writing one component (4-6 min)
- Quick questions (1-2 min)
- Know exactly what you need

## Productivity Hacks

### 1. Template Prompts

Save prompts that work well:

```python
# In a text file: prompts.txt

BACKEND_API = """
Create a {name} API endpoint:
- Method: {method}
- Route: {route}
- Input: {input_schema}
- Output: {output_schema}
- Validation: {validation_rules}
- Error handling
- Tests
"""

REVIEW = """
Review this code:
[paste code]

Check for:
- Bugs and edge cases
- Security issues
- Performance problems
- Code quality
"""
```

### 2. Chain Commands

Use output from one as input to next:

```
1. Aurora: "Design feature X"
   (Take 4 min)

2. Nova: "Implement this design:
   [paste Aurora's output]"
   (Takes 5 min)

3. Sentinel: "Test this code:
   [paste Nova's output]"
   (Takes 3 min)
```

### 3. Parallel Sessions

Run multiple terminals:

```bash
# Terminal 1
./run  # Working on feature A

# Terminal 2
./run  # Getting design for feature B

# Terminal 3  
./run  # Asking questions

# Work on different things while each runs
```

### 4. Save Context

Keep conversation history:

```bash
# Option 1: Copy output to files
mkdir project-context
echo "[output]" > project-context/feature-plan.md

# Option 2: Use memory feature
Menu → Memory & History

# Option 3: Export to notes
# Just copy-paste important outputs
```

## When Something Takes Too Long

### Investigation Steps

1. **Check System Resources**
```bash
top  # CPU usage
free -h  # RAM usage
```

2. **Check Ollama**
```bash
curl http://localhost:11434/api/tags
# Should respond quickly
```

3. **Test Simple Query**
```bash
# Solo mode → any agent
"Say hello"
# Should take <30 seconds
```

4. **Check Model**
```bash
# Try different model
ollama pull mistral:7b
# Update config.yaml
```

### Common Issues

**CPU at 100%**
- Normal during generation
- Close other applications
- Consider GPU

**RAM Full**
- Restart Ollama
- Use smaller model
- Close browser tabs

**Very Slow (>10 min for simple task)**
- Check model size (7b not 13b/34b)
- Verify GPU not being used for other tasks
- Restart computer

**Frequent Timeouts**
- Increase timeout in settings
- Use simpler prompts
- Break into smaller tasks

## Optimization for Daily Use

### Morning Setup (5 min)

```bash
# 1. Start Ollama
ollama serve &

# 2. Test system
cd ~/ai-dev-team
./quick_test.py

# 3. Set daily preset
./run
→ Settings → realistic preset

# 4. Ready to work!
```

### End of Day (2 min)

```bash
# Save any important outputs
cp workspace/* ~/projects/today/

# Check what worked well
# Adjust timeouts if needed

# Stop Ollama if not using overnight
pkill ollama
```

### Weekly Optimization

```bash
# Check agent stats
python3 -c "
from agent_manager import get_agent_manager
mgr = get_agent_manager()
for agent in ['aurora', 'nova', 'orion']:
    print(f'{agent}: {mgr.get_agent_stats(agent)}')
"

# Adjust timeouts based on your usage
# Update settings.py if needed
```

## Real Project Example

### Building a Blog API (30-40 min total)

**Phase 1: Planning (5 min)**
```
Aurora: "Design REST API for blog with posts, comments, tags"
→ Review and adjust plan
```

**Phase 2: Implementation (15-20 min)**
```
Nova: "Implement blog post CRUD"
(6 min)

Nova: "Implement comments system"  
(5 min)

Nova: "Implement tags and search"
(4 min)
```

**Phase 3: Testing (8-10 min)**
```
Sentinel: "Unit tests for posts"
(3 min)

Sentinel: "Integration tests for API"
(4 min)

Sentinel: "Test edge cases and errors"
(3 min)
```

**Phase 4: Review & Polish (5-8 min)**
```
Orion: "Review all code, suggest improvements"
(3 min)

Apply improvements
(2 min)

Pixel: "Write API documentation"
(3 min)
```

**Total: 33-43 minutes for production-ready API**

Compare to:
- Writing manually: 2-4 hours
- Using fast AI: 10-15 min but lower quality
- Senior developer: 1-2 hours

## Summary

### Key Takeaways

1. **Local models are slow - this is normal**
   - 4-6 min per thoughtful response is realistic
   - Quality takes time
   - Don't fight it, work with it

2. **Use time wisely**
   - Multi-task during waits
   - Batch similar requests
   - Work on previous output

3. **Right tool for job**
   - Quick: fast preset, solo mode
   - Quality: realistic/thorough, team mode
   - Perfect: multiple iterations

4. **Be patient**
   - Good code takes time
   - Rushing = poor results
   - 30 min with AI beats 3 hours manual

5. **Optimize your workflow**
   - Save good prompts
   - Chain tasks
   - Use right agents
   - Adjust settings to your needs

### Realistic Expectations

**What AI Dev Team IS Good For:**
- Generating boilerplate
- Implementing designs
- Writing tests
- Code review
- Learning
- Prototyping

**What Takes Realistic Time:**
- Quality responses (3-6 min)
- Complete features (15-30 min)
- Full applications (1-2 hours)

**What It's NOT:**
- Instant magic
- Replacement for thinking
- Always perfect first try

### Your Daily Reality

With local models:
- Morning planning: 10-15 min
- Feature development: 15-30 min each
- Code review: 5-10 min
- Questions/help: 2-5 min

**Total daily: 1-2 hours with AI = 4-8 hours of manual work**

Worth it? Absolutely! ✅

---

Now go build something awesome! Just remember to grab coffee while agents think ☕😊
