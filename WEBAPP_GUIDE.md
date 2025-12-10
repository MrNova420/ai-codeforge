# 🌐 AI CodeForge Web Application

**Beautiful, user-friendly web interface for your AAA development team!**

## ✨ Features

### Dashboard
- **Real-time stats** - Active agents, running tasks, performance metrics
- **Quick actions** - One-click access to common operations
- **Activity feed** - Live updates from all agents
- **Team status** - Visual overview of all 23 agents

### All 23 Agents
- Browse and interact with all specialized agents
- View agent roles, specialties, and current status
- Click to start chat or assign tasks

### Task Management
- **Create tasks** with natural language descriptions
- **Choose work mode**: Parallel, Sequential, Collaborative, or Autonomous
- **Track progress** in real-time
- **View history** of completed tasks

### Code Editor
- Generate code with AI assistance
- Built-in Monaco-style editor
- Copy, save, and execute code
- Connects to Docker sandbox for secure execution

### Security Operations
- Run comprehensive security scans
- OWASP Top 10 vulnerability detection
- Threat modeling and compliance checks
- Real-time security alerts

### Research Lab
- Ask research questions
- Get technology evaluations
- Market analysis and best practices
- POC development assistance

### Design Studio
- UX design tools
- UI component generation
- Accessibility audits (WCAG)
- Complete design system creation

### Configuration
- **Interface modes**: Simple, Advanced, Expert
- **Agent settings**: Choose default agents
- **Performance**: Enable caching, fast startup
- **Security**: Docker sandbox, network isolation

## 🚀 Quick Start

### Option 1: Simple Launch (Recommended)
```bash
python3 webapp.py
```

Then open your browser to: **http://localhost:3000**

### Option 2: Manual Launch

**Terminal 1 - Backend:**
```bash
cd ui/backend
python3 websocket_server.py
```

**Terminal 2 - Frontend:**
```bash
cd ui/frontend
python3 -m http.server 3000
```

Then open: **http://localhost:3000**

## 📊 Interface Overview

### Sidebar Navigation
- 📊 **Dashboard** - Overview and quick actions
- 🤖 **Agents** - View all 23 specialized agents
- 📋 **Tasks** - Create and manage tasks
- 💻 **Code Editor** - Generate and edit code
- 🔒 **Security** - Security operations center
- 🔬 **Research Lab** - Innovation and research
- 🎨 **Design Studio** - UX/UI design tools
- ⚙️ **Configuration** - System settings

### Quick Actions
One-click access to common operations:
- 💻 Generate Code
- 🧪 Run Tests
- 🔍 Code Review
- 🔒 Security Scan
- 🚀 Deploy
- 🔬 Research

## 🎯 Common Workflows

### Generate Code
1. Click **Dashboard** → **Generate Code**
2. Or go to **Code Editor**
3. Enter task description (e.g., "Create REST API for user authentication")
4. Click **Generate Code**
5. Code appears in editor
6. Copy, save, or execute

### Run Security Scan
1. Go to **Security** view
2. Click **Run Security Scan**
3. View results in real-time
4. Get actionable recommendations

### Create Complex Task
1. Go to **Tasks** view
2. Click **New Task**
3. Describe your task
4. Choose work mode:
   - **Parallel**: All agents work simultaneously
   - **Sequential**: Production pipeline order
   - **Collaborative**: Agents discuss and iterate
   - **Autonomous**: Agents self-organize
5. Click **Create Task**
6. Watch progress in real-time

### Research Technology
1. Go to **Research Lab**
2. Enter question (e.g., "GraphQL vs REST API")
3. Click **Research**
4. Get comprehensive analysis

## 🔄 Real-Time Features

### WebSocket Connection
- Automatic connection to backend
- Real-time updates from all agents
- Live task progress
- Instant notifications
- Auto-reconnect if disconnected

### Activity Feed
- See everything happening in real-time
- Agent actions
- Task updates
- System events
- Security alerts

### Status Indicators
- Connection status (top bar)
- Agent availability
- Task progress
- System health

## ⚙️ Configuration

### Save Your Preferences
1. Go to **Configuration** view
2. Set your preferences:
   - Interface mode (Simple/Advanced/Expert)
   - Default agent (Felix, Quinn, Mira, etc.)
   - Performance options (caching, fast startup)
   - Security settings (Docker, network isolation)
3. Click **Save Configuration**

Settings are saved in your browser's localStorage.

## 🎨 Customization

### Theme
The UI uses a modern, professional design with:
- Dark sidebar for focus
- Light content area for readability
- Smooth animations
- Responsive layout (works on mobile!)

### Layout
- Flexible grid system
- Responsive cards
- Collapsible sidebar on mobile
- Full-screen code editor

## 🔒 Security

### Secure by Default
- All code execution in Docker sandbox
- Network isolation optional
- WebSocket connections can be secured with WSS
- No sensitive data stored in browser

### Production Deployment
For production use:
1. Enable HTTPS/WSS
2. Configure CORS appropriately
3. Add authentication
4. Use reverse proxy (nginx)

## 📱 Mobile Support

The UI is fully responsive:
- Sidebar collapses to icons
- Touch-friendly buttons
- Optimized layouts
- All features accessible

## 🐛 Troubleshooting

### Can't connect to backend
- Check if backend is running: `http://localhost:8000/health`
- Verify port 8000 is not in use
- Check firewall settings

### WebSocket won't connect
- Backend must be running first
- Check browser console for errors
- Try refreshing the page

### Frontend won't load
- Check if port 3000 is available
- Navigate to correct URL: `http://localhost:3000`
- Try different port: `python3 -m http.server 8080`

## 🎯 Two Interfaces

AI CodeForge now offers **TWO ways to work**:

### 1. Command Line (CLI)
**Best for:** Developers, automation, scripts
```bash
./codeforge code "create API"
./codeforge_advanced status --watch
```

### 2. Web Application
**Best for:** Visual workflow, team collaboration, beginners
```bash
python3 webapp.py
# Open http://localhost:3000
```

**Use both!** The web app and CLI work together seamlessly.

## 🚀 Next Steps

1. **Try the quick actions** - Generate code, run tests
2. **Create a task** - Experience the full team workflow
3. **Explore agents** - See all 23 specialized agents
4. **Configure** - Customize to your preferences
5. **Build something** - Put the AAA team to work!

## 📊 System Requirements

- Python 3.8+
- FastAPI and uvicorn (for backend)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 4GB RAM minimum (for full system)
- Network access for WebSocket connection

## 🎉 Features Summary

✅ Beautiful, modern UI
✅ Real-time WebSocket connection
✅ All 23 agents accessible
✅ Task creation and management
✅ Code editor with generation
✅ Security operations center
✅ Research and innovation lab
✅ Design studio
✅ Complete configuration
✅ Activity feed and monitoring
✅ Mobile responsive
✅ Fast and performant

---

**Enjoy your AI CodeForge Web Application!** 🚀

For CLI documentation, see: `./codeforge help` or `./codeforge_advanced --help`

For full system documentation, see: `FINAL_COMPLETE_SUMMARY.md`
