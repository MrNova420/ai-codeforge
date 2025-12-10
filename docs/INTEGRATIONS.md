# Integration Guide

How to integrate AI Dev Team into your workflow.

## Git Integration

### Basic Setup
```bash
cd ~/ai-dev-team/workspace
git init
git add .
git commit -m "Initial commit"
```

### Workflow
```bash
# 1. Start AI Dev Team
./run

# 2. Build feature with agents
"Create login system with JWT"

# 3. Review generated code
cd workspace/
ls -la

# 4. Commit
git add auth.py
git commit -m "Add JWT authentication"
git push
```

### Git Hooks
Create `.git/hooks/pre-commit` to auto-review:
```bash
#!/bin/bash
# Ask Orion to review before commit
echo "🤖 Running AI code review..."
# Integration code here
```

## IDE Integration

### VS Code
```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "AI Dev Team",
      "type": "shell",
      "command": "${workspaceFolder}/../run",
      "problemMatcher": []
    }
  ]
}
```

Then: `Ctrl+Shift+P` → "Run Task" → "AI Dev Team"

### Terminal in IDE
Most IDEs support integrated terminal:
```bash
# In IDE terminal
cd ../ai-dev-team
./run
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Ollama
        run: curl https://ollama.ai/install.sh | sh
      - name: AI Review
        run: |
          cd ai-dev-team
          ./run # Auto review mode
```

### GitLab CI
```yaml
# .gitlab-ci.yml
ai_review:
  script:
    - cd ai-dev-team
    - ./quick_test.py
    - ./run # automated mode
```

## API Integration

### REST API Wrapper
Create `api_server.py`:
```python
#!/usr/bin/env python3
"""
REST API wrapper for AI Dev Team
"""
from flask import Flask, request, jsonify
from agent_chat_enhanced import EnhancedAgentChat
from orchestrator import Config, AgentLoader

app = Flask(__name__)
config = Config()
loader = AgentLoader()

@app.route('/api/chat/<agent>', methods=['POST'])
def chat(agent):
    """Chat with specific agent."""
    data = request.json
    message = data.get('message')
    
    agent_profile = loader.get_agent(agent)
    chat = EnhancedAgentChat(agent_profile, config)
    response = chat.send_message(message)
    
    return jsonify({'response': response})

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List available agents."""
    return jsonify({'agents': loader.list_agents()})

if __name__ == '__main__':
    app.run(port=8080)
```

Usage:
```bash
# Start server
python3 api_server.py

# Use from anywhere
curl -X POST http://localhost:8080/api/chat/nova \
  -H "Content-Type: application/json" \
  -d '{"message":"Write a hello world function"}'
```

## Docker Integration

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh

# Copy AI Dev Team
COPY ai-dev-team /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Pull model
RUN ollama serve & sleep 5 && ollama pull codellama:7b

# Run
CMD ["./run"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  ai-dev-team:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./workspace:/app/workspace
```

## Slack Integration

```python
# slack_bot.py
from slack_bolt import App
from agent_chat_enhanced import EnhancedAgentChat

app = App(token="xoxb-your-token")

@app.message("!ai")
def ai_command(message, say):
    """Trigger AI agent."""
    text = message['text'].replace('!ai', '').strip()
    
    # Get AI response
    agent = get_agent('nova')
    response = agent.send_message(text)
    
    say(f"🤖 {response}")

app.start(port=3000)
```

## Database Integration

### Save Generated Code
```python
# db_integration.py
import sqlite3

def save_code(filename, content, agent, timestamp):
    """Save generated code to database."""
    conn = sqlite3.connect('ai_history.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS generated_code (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            content TEXT,
            agent TEXT,
            timestamp TEXT
        )
    ''')
    
    c.execute(
        'INSERT INTO generated_code VALUES (NULL, ?, ?, ?, ?)',
        (filename, content, agent, timestamp)
    )
    
    conn.commit()
    conn.close()
```

## Web Dashboard

```python
# dashboard.py
from flask import Flask, render_template, request
from agent_chat_enhanced import EnhancedAgentChat

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    prompt = request.json['prompt']
    agent_name = request.json.get('agent', 'nova')
    
    # Generate code
    response = get_agent_response(agent_name, prompt)
    
    return {'code': response}

if __name__ == '__main__':
    app.run(debug=True)
```

## External Tools

### Jira Integration
```python
# Create ticket from AI output
from jira import JIRA

jira = JIRA('https://your-domain.atlassian.net', 
            basic_auth=('email', 'token'))

# Create ticket from AI analysis
issue = jira.create_issue(
    project='DEV',
    summary='Implement feature from AI',
    description=ai_response,
    issuetype={'name': 'Task'}
)
```

### Notion Integration
```python
# Save to Notion
from notion_client import Client

notion = Client(auth="your_token")

notion.pages.create(
    parent={"database_id": "your_db_id"},
    properties={
        "Name": {"title": [{"text": {"content": "AI Generated Code"}}]},
        "Content": {"rich_text": [{"text": {"content": code}}]}
    }
)
```

## Custom Workflows

### Auto-Documentation
```bash
#!/bin/bash
# auto_document.sh

# Generate code
./run --auto "Create user authentication"

# Generate docs with AI
./run --solo pixel "Document the auth.py file"

# Commit both
git add workspace/auth.py workspace/README.md
git commit -m "Add auth with docs"
```

### Testing Pipeline
```bash
#!/bin/bash
# test_pipeline.sh

# 1. Generate code
./run --solo nova "Create calculator.py"

# 2. Generate tests
./run --solo sentinel "Write tests for calculator.py"

# 3. Run tests
cd workspace/
pytest test_calculator.py
```

## Environment Variables

```bash
# .env file
AI_DEV_TEAM_MODEL=codellama:7b
AI_DEV_TEAM_TIMEOUT=120
AI_DEV_TEAM_WORKSPACE=/custom/path
AI_DEV_TEAM_MODE=api  # or local

# Load in scripts
source .env
./run
```

## Production Considerations

### Security
- Don't expose API without authentication
- Validate all inputs
- Sandbo code execution
- Rate limit requests

### Performance
- Use API models in production
- Cache common responses
- Implement queue system for long tasks
- Monitor resource usage

### Scaling
- Run multiple instances
- Load balance requests
- Use message queue (Redis, RabbitMQ)
- Separate model serving from API

## Examples

See `examples/` directory for:
- GitHub Actions workflow
- Docker setup
- API server
- Slack bot
- Web dashboard

## Next Steps

1. Pick integration that fits your workflow
2. Start with simple API wrapper
3. Add authentication and logging
4. Scale as needed
5. Share your integration! 🚀
