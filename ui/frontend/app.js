// AI CodeForge Web Application
// Main JavaScript for the War Room UI

// WebSocket connection
let ws = null;
let reconnectInterval = null;

// App State
const appState = {
    agents: [],
    tasks: [],
    activities: [],
    config: {}
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    populateAgents();
    populateActivityFeed();
    populateTeamStatus();
    connectWebSocket();
    loadConfiguration();
});

// Navigation
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const viewName = item.dataset.view;
            switchView(viewName);
            
            // Update active state
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            // Update page title
            document.getElementById('page-title').textContent = 
                item.textContent.trim();
        });
    });
}

function switchView(viewName) {
    const views = document.querySelectorAll('.view');
    views.forEach(view => view.classList.remove('active'));
    document.getElementById(`${viewName}-view`).classList.add('active');
}

// WebSocket Connection
function connectWebSocket() {
    try {
        ws = new WebSocket('ws://localhost:8000/ws');
        
        ws.onopen = () => {
            console.log('✅ Connected to AI CodeForge');
            updateConnectionStatus(true);
        };
        
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            handleWebSocketMessage(message);
        };
        
        ws.onclose = () => {
            console.log('❌ Disconnected from server');
            updateConnectionStatus(false);
            attemptReconnect();
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    } catch (error) {
        console.error('Failed to connect:', error);
        updateConnectionStatus(false);
    }
}

function attemptReconnect() {
    if (!reconnectInterval) {
        reconnectInterval = setInterval(() => {
            console.log('Attempting to reconnect...');
            connectWebSocket();
        }, 5000);
    }
}

function updateConnectionStatus(isConnected) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-indicator span:last-child');
    
    if (isConnected) {
        statusDot.classList.add('online');
        statusText.textContent = 'System Online';
        if (reconnectInterval) {
            clearInterval(reconnectInterval);
            reconnectInterval = null;
        }
    } else {
        statusDot.classList.remove('online');
        statusText.textContent = 'Reconnecting...';
    }
}

function handleWebSocketMessage(message) {
    console.log('Message:', message);
    
    switch (message.type) {
        case 'agent_event':
            handleAgentEvent(message);
            break;
        case 'task_update':
            handleTaskUpdate(message);
            break;
        case 'system_alert':
            handleSystemAlert(message);
            break;
        case 'system_status':
            updateSystemStatus(message.data);
            break;
    }
}

// Agent Management
function populateAgents() {
    const agents = [
        { name: 'Aurora', role: 'Product Manager', icon: '👔', category: 'planner' },
        { name: 'Sage', role: 'Lead Architect', icon: '🏗️', category: 'planner' },
        { name: 'Felix', role: 'Senior Developer', icon: '💻', category: 'planner' },
        { name: 'Ember', role: 'Creative Director', icon: '💡', category: 'planner' },
        { name: 'Orion', role: 'Code Reviewer', icon: '👀', category: 'critic' },
        { name: 'Atlas', role: 'Performance Specialist', icon: '⚡', category: 'critic' },
        { name: 'Mira', role: 'Security Engineer', icon: '🔒', category: 'critic' },
        { name: 'Vex', role: 'Critical Analyst', icon: '🤔', category: 'critic' },
        { name: 'Sol', role: 'Backend Specialist', icon: '🔧', category: 'specialist' },
        { name: 'Echo', role: 'Frontend Developer', icon: '🎨', category: 'specialist' },
        { name: 'Nova', role: 'DevOps Engineer', icon: '🚀', category: 'specialist' },
        { name: 'Quinn', role: 'QA Lead', icon: '🧪', category: 'specialist' },
        { name: 'Blaze', role: 'Mobile Developer', icon: '📱', category: 'specialist' },
        { name: 'Ivy', role: 'Data Engineer', icon: '📊', category: 'specialist' },
        { name: 'Zephyr', role: 'Cloud Architect', icon: '☁️', category: 'specialist' },
        { name: 'Pixel', role: 'UX Designer', icon: '🎭', category: 'assistant' },
        { name: 'Script', role: 'Tech Writer', icon: '📚', category: 'assistant' },
        { name: 'Turbo', role: 'Performance Engineer', icon: '⚡', category: 'assistant' },
        { name: 'Sentinel', role: 'SRE Lead', icon: '👁️', category: 'assistant' },
        { name: 'Helix', role: 'Research Lead', icon: '🔬', category: 'special' },
        { name: 'Patch', role: 'Bug Hunter', icon: '🐛', category: 'special' },
        { name: 'Pulse', role: 'Integration Specialist', icon: '🔌', category: 'special' },
        { name: 'Link', role: 'Collaboration Lead', icon: '🔗', category: 'special' }
    ];
    
    appState.agents = agents;
    
    // Populate agents grid
    const agentsGrid = document.getElementById('agents-grid');
    if (agentsGrid) {
        agentsGrid.innerHTML = agents.map(agent => `
            <div class="agent-card">
                <div class="icon">${agent.icon}</div>
                <div class="name">${agent.name}</div>
                <div class="role">${agent.role}</div>
            </div>
        `).join('');
    }
}

function populateTeamStatus() {
    const teamStatus = document.getElementById('team-status');
    if (teamStatus) {
        const featuredAgents = appState.agents.slice(0, 8);
        teamStatus.innerHTML = featuredAgents.map(agent => `
            <div class="agent-status">
                <div class="icon">${agent.icon}</div>
                <div class="name">${agent.name}</div>
                <div class="status">Ready</div>
            </div>
        `).join('');
    }
}

function populateActivityFeed() {
    const activities = [
        { icon: '🚀', title: 'System initialized', meta: 'Just now', type: 'system' },
        { icon: '🤖', title: 'All 23 agents ready', meta: '1 min ago', type: 'info' },
        { icon: '⚡', title: 'Performance optimization active', meta: '2 min ago', type: 'success' }
    ];
    
    appState.activities = activities;
    
    const activityFeed = document.getElementById('activity-feed');
    if (activityFeed) {
        activityFeed.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-icon">${activity.icon}</div>
                <div class="activity-content">
                    <div class="activity-title">${activity.title}</div>
                    <div class="activity-meta">${activity.meta}</div>
                </div>
            </div>
        `).join('');
    }
}

function addActivity(icon, title, meta) {
    const activity = { icon, title, meta, type: 'info' };
    appState.activities.unshift(activity);
    
    if (appState.activities.length > 20) {
        appState.activities.pop();
    }
    
    populateActivityFeed();
}

// Quick Actions
function generateCode() {
    addActivity('💻', 'Code generation started', 'Just now');
    switchView('code');
    document.getElementById('code-prompt').focus();
}

function runTests() {
    addActivity('🧪', 'Running test suite', 'Just now');
    alert('Test runner would start here. This connects to the backend agents.');
}

function codeReview() {
    addActivity('🔍', 'Code review initiated', 'Just now');
    alert('Code review would start here with Orion agent.');
}

function securityScan() {
    addActivity('🔒', 'Security scan started', 'Just now');
    switchView('security');
}

function deploy() {
    addActivity('🚀', 'Deployment pipeline started', 'Just now');
    alert('Deployment would start here with Nova and Zephyr agents.');
}

function research() {
    addActivity('🔬', 'Research lab opened', 'Just now');
    switchView('research');
}

// Code Editor Functions
function generateCodeFromPrompt() {
    const prompt = document.getElementById('code-prompt').value;
    if (!prompt.trim()) {
        alert('Please enter a task description');
        return;
    }
    
    const editor = document.getElementById('code-editor');
    editor.value = '// Generating code...\n// This would connect to Felix agent via WebSocket\n// Task: ' + prompt;
    
    addActivity('💻', `Generating: ${prompt}`, 'Just now');
    
    // In real implementation, send via WebSocket
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'generate_code',
            data: { prompt: prompt }
        }));
    }
}

function copyCode() {
    const editor = document.getElementById('code-editor');
    editor.select();
    document.execCommand('copy');
    alert('Code copied to clipboard!');
}

function saveCode() {
    const code = document.getElementById('code-editor').value;
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'generated_code.txt';
    a.click();
    addActivity('💾', 'Code saved', 'Just now');
}

function executeCode() {
    addActivity('⚡', 'Executing code in Docker sandbox', 'Just now');
    alert('Code would execute in secure Docker container via backend.');
}

// Security Functions
function runSecurityScan() {
    const results = document.getElementById('security-results');
    results.innerHTML = `
        <div style="padding: 2rem;">
            <h4>🔍 Scanning for vulnerabilities...</h4>
            <p>This would connect to Mira (Security Engineer) to scan the codebase.</p>
            <ul style="margin-top: 1rem; line-height: 2;">
                <li>✅ OWASP Top 10 scan</li>
                <li>✅ Dependency vulnerabilities</li>
                <li>✅ Code security patterns</li>
                <li>✅ Configuration review</li>
            </ul>
        </div>
    `;
    addActivity('🔒', 'Security scan in progress', 'Just now');
}

// Research Functions
function startResearch() {
    const query = document.getElementById('research-query').value;
    if (!query.trim()) {
        alert('Please enter a research query');
        return;
    }
    
    const results = document.getElementById('research-results');
    results.innerHTML = `
        <div style="padding: 2rem;">
            <h4>🔬 Researching: ${query}</h4>
            <p>Helix (Research Lead) would analyze this topic and provide insights.</p>
        </div>
    `;
    
    addActivity('🔬', `Researching: ${query}`, 'Just now');
}

// Design Functions
function uxDesign() {
    addActivity('🎨', 'UX design started', 'Just now');
    alert('Pixel (UX Designer) would create user flows and wireframes.');
}

function uiComponents() {
    addActivity('🎨', 'UI component generation started', 'Just now');
    alert('Generating UI component library with Pixel.');
}

function accessibilityAudit() {
    addActivity('♿', 'Accessibility audit started', 'Just now');
    alert('Running WCAG compliance check with Pixel.');
}

function designSystem() {
    addActivity('🎨', 'Design system generation started', 'Just now');
    alert('Creating comprehensive design system with Pixel.');
}

// Configuration
function loadConfiguration() {
    // Load from localStorage or defaults
    const config = {
        interfaceMode: localStorage.getItem('interfaceMode') || 'advanced',
        defaultAgent: localStorage.getItem('defaultAgent') || 'felix',
        enableCache: localStorage.getItem('enableCache') !== 'false',
        fastStartup: localStorage.getItem('fastStartup') !== 'false',
        dockerSandbox: localStorage.getItem('dockerSandbox') !== 'false',
        networkIsolation: localStorage.getItem('networkIsolation') !== 'false'
    };
    
    appState.config = config;
    
    // Apply to UI
    if (document.getElementById('interface-mode')) {
        document.getElementById('interface-mode').value = config.interfaceMode;
        document.getElementById('default-agent').value = config.defaultAgent;
        document.getElementById('enable-cache').checked = config.enableCache;
        document.getElementById('fast-startup').checked = config.fastStartup;
        document.getElementById('docker-sandbox').checked = config.dockerSandbox;
        document.getElementById('network-isolation').checked = config.networkIsolation;
    }
}

function saveConfiguration() {
    const config = {
        interfaceMode: document.getElementById('interface-mode').value,
        defaultAgent: document.getElementById('default-agent').value,
        enableCache: document.getElementById('enable-cache').checked,
        fastStartup: document.getElementById('fast-startup').checked,
        dockerSandbox: document.getElementById('docker-sandbox').checked,
        networkIsolation: document.getElementById('network-isolation').checked
    };
    
    // Save to localStorage
    Object.keys(config).forEach(key => {
        localStorage.setItem(key, config[key]);
    });
    
    appState.config = config;
    addActivity('⚙️', 'Configuration saved', 'Just now');
    alert('Configuration saved successfully!');
}

// Tasks
function showNewTaskModal() {
    document.getElementById('task-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('task-modal').classList.remove('active');
}

function createTask() {
    const description = document.getElementById('task-description').value;
    const mode = document.getElementById('task-mode').value;
    
    if (!description.trim()) {
        alert('Please enter a task description');
        return;
    }
    
    const task = {
        id: Date.now(),
        description,
        mode,
        status: 'running',
        created: new Date().toLocaleString()
    };
    
    appState.tasks.push(task);
    addActivity('📋', `New task: ${description}`, 'Just now');
    
    // Send to backend
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'create_task',
            data: task
        }));
    }
    
    closeModal();
    switchView('tasks');
    populateTasks();
}

function populateTasks() {
    const tasksList = document.getElementById('tasks-list');
    if (!tasksList) return;
    
    if (appState.tasks.length === 0) {
        tasksList.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📋</span>
                <p>No tasks yet</p>
                <button class="btn-secondary" onclick="showNewTaskModal()">Create First Task</button>
            </div>
        `;
    } else {
        tasksList.innerHTML = appState.tasks.map(task => `
            <div class="task-item">
                <div class="task-info">
                    <h4>${task.description}</h4>
                    <div class="task-meta">
                        Mode: ${task.mode} | Created: ${task.created}
                    </div>
                </div>
                <div class="task-status ${task.status}">${task.status}</div>
            </div>
        `).join('');
    }
}

// Handle updates from WebSocket
function handleAgentEvent(message) {
    addActivity(
        '🤖',
        `${message.agent}: ${message.event_type}`,
        'Just now'
    );
}

function handleTaskUpdate(message) {
    const task = appState.tasks.find(t => t.id === message.task_id);
    if (task) {
        task.status = message.status;
        populateTasks();
    }
    
    addActivity(
        '📋',
        `Task ${message.status}: ${message.task_id}`,
        'Just now'
    );
}

function handleSystemAlert(message) {
    addActivity(
        message.severity === 'error' ? '❌' : '⚠️',
        message.message,
        'Just now'
    );
}

function updateSystemStatus(status) {
    if (status.running_tasks !== undefined) {
        document.getElementById('tasks-running').textContent = status.running_tasks;
    }
    if (status.completed_tasks !== undefined) {
        document.getElementById('tasks-completed').textContent = status.completed_tasks;
    }
}

// Update stats periodically
setInterval(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'get_status' }));
    }
}, 5000);
