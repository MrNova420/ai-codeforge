# 🚀 Ultimate AI Dev Team - Simple Start

## ONE Command to Rule Them All

```bash
./run
```

That's it! Everything else is automatic.

---

## What Happens Automatically

When you run `./run`, the system automatically:

1. ✅ Checks if Ollama is installed (installs if needed)
2. ✅ Starts Ollama service (if not running)
3. ✅ Downloads AI model (mistral:7b, ~4GB)
4. ✅ Configures all 23 agents
5. ✅ Launches the system

**No setup wizard. No configuration files. No questions.**

Just works.

---

## What You Get

- **23 AI Agents** - Each with unique personality
  - 5 Planners/Designers (Aurora, Felix, Sage, Ember, Orion)
  - 5 Critics/Judges (Atlas, Mira, Vex, Sol, Echo)
  - 5 Developers (Nova, Quinn, Blaze, Ivy, Zephyr)
  - 5 Dev Assistants (Pixel, Script, Turbo, Sentinel, Link)
  - 3 Specialists (Patch, Pulse, Helix)

- **100% FREE** - No API keys needed
- **100% PRIVATE** - Runs on your computer
- **100% AUTOMATIC** - Zero configuration

---

## How to Use

### Team Mode (Recommended)
```bash
./run
# Choose option 1: Team Collaboration Mode
# Tell Helix what you want
# He coordinates the team automatically
```

**Example:**
```
Your Request: review my web-game project and give me a summary

Helix will:
- Assign Sage to analyze the project
- Assign Nova to review the code
- Assign Atlas to critique the quality
- Compile a summary for you
```

### Solo Mode
```bash
./run
# Choose option 2: Solo Agent Chat
# Pick any agent
# Chat directly with them
```

---

## First Run

The first time takes 5-10 minutes:
- Download model: ~2-5 minutes (4.4GB)
- Setup: ~1 minute

After that, starts in seconds.

---

## Requirements

- **Linux** (Ubuntu, Debian, etc.)
- **8GB RAM** minimum (16GB+ recommended)
- **Internet** (first time only, for download)

---

## Troubleshooting

### "Ollama not found"
```bash
sudo snap install ollama
./run
```

### "Cannot connect"
Open another terminal:
```bash
ollama serve
```
Then run `./run` again.

### Still not working?
```bash
./fix_setup.sh
./run
```

---

## That's All!

Seriously, that's everything you need to know.

```bash
./run
```

Enjoy your AI dev team! 🎉
