# How The AI Dev Team Works

## Simple Start

```bash
./run
```

That's it!

## What Happens (Automatic & Smart)

### First Time
1. **Detects** what you have:
   - Ollama installed? ✅/❌
   - Ollama running? ✅/❌
   - Models downloaded? Lists them

2. **Asks** what you want:
   - Use existing model or download new?
   - Which model if downloading?

3. **Does it for you** (all in same session):
   - Installs Ollama if needed (asks for sudo)
   - Starts Ollama if not running
   - Downloads model you chose
   - Configures all 23 agents

### Every Time After
- Starts instantly
- Uses your configured agents
- No setup needed

## Example First Run

```
📋 Detecting what you have...
   Ollama: ✅ Installed
   Service: ✅ Running  
   Models: ✅ 1 found (mistral:7b)

📋 Choosing model...
   You have 1 model(s):
   1. mistral:7b
   2. Download a new model
   
   Which to use? [1-2]: 1
   ✅ Using: mistral:7b

📋 Configuring 23 agents with mistral:7b...
   ✅ All set!
```

## The 23 Agents

**Planners (5)**
- Aurora - Visionary strategist
- Felix - Detail architect  
- Sage - Research expert
- Ember - Creative designer
- Orion - Systems architect

**Critics (5)**
- Atlas - The perfectionist
- Mira - Balanced analyst
- Vex - The challenger
- Sol - Industry veteran
- Echo - Data-driven judge

**Developers (5)**
- Nova - Lead engineer
- Quinn - Code artisan
- Blaze - Performance guru
- Ivy - Security specialist
- Zephyr - Integration expert

**Assistants (5)**
- Pixel, Script, Turbo, Sentinel, Link

**Specialists (3)**
- Patch - Bug hunter
- Pulse - QA tester
- Helix - Team overseer

## Using Them

### Team Mode (Recommended)
Tell Helix what you need, he coordinates everyone:

```
Your Request: review my web-game project

Helix will:
→ Assign Sage to analyze
→ Assign Nova to review code  
→ Assign Atlas to critique
→ Give you a summary
```

### Solo Mode
Chat with any agent directly:
- Need code review? → Quinn
- Performance issues? → Blaze
- Security audit? → Ivy
- Planning? → Aurora

## That's All!

No complex setup. No config files to edit. No documentation to read.

Just `./run` and go! 🚀
