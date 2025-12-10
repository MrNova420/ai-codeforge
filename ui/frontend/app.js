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
    config: {},
    isConnected: false
};

// State Persistence
function saveState() {
    localStorage.setItem('appState', JSON.stringify({
        tasks: appState.tasks,
        activities: appState.activities,
        config: appState.config
    }));
}

function loadState() {
    const savedState = localStorage.getItem('appState');
    if (savedState) {
        try {
            const state = JSON.parse(savedState);
            appState.tasks = state.tasks || [];
            appState.activities = state.activities || [];
            appState.config = state.config || {};
            
            // Restore UI
            populateTasks();
            populateActivityFeed();
        } catch (e) {
            console.error('Failed to load state:', e);
        }
    }
}

// Notification System
function showNotification(type, message) {
    const container = document.getElementById('notification-container') || createNotificationContainer();
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${getNotificationIcon(type)}</span>
        <span class="notification-message">${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    container.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

function createNotificationContainer() {
    const container = document.createElement('div');
    container.id = 'notification-container';
    container.className = 'notification-container';
    document.body.appendChild(container);
    return container;
}

function getNotificationIcon(type) {
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    return icons[type] || 'ℹ️';
}

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    loadState();
    initializeNavigation();
    initializeHeaderButtons();
    populateAgents();
    populateActivityFeed();
    populateTeamStatus();
    connectWebSocket();
    loadConfiguration();
    
    // Save state periodically
    setInterval(saveState, 30000); // Save every 30 seconds
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

// Header Button Handlers
function initializeHeaderButtons() {
    // Notifications button
    const notificationsBtn = document.getElementById('notifications');
    if (notificationsBtn) {
        notificationsBtn.addEventListener('click', showNotificationsPanel);
    }
    
    // Settings button
    const settingsBtn = document.getElementById('settings');
    if (settingsBtn) {
        settingsBtn.addEventListener('click', () => {
            switchView('config');
            // Update nav state
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            document.querySelector('[data-view="config"]').classList.add('active');
            document.getElementById('page-title').textContent = 'Configuration';
        });
    }
    
    // User profile
    const userProfile = document.querySelector('.user-profile');
    if (userProfile) {
        userProfile.addEventListener('click', showUserMenu);
    }
}

function showNotificationsPanel() {
    // Check if panel exists, otherwise create it
    let panel = document.getElementById('notifications-panel');
    
    if (!panel) {
        panel = document.createElement('div');
        panel.id = 'notifications-panel';
        panel.className = 'notifications-panel';
        document.body.appendChild(panel);
    }
    
    // Toggle panel visibility
    if (panel.classList.contains('active')) {
        panel.classList.remove('active');
        return;
    }
    
    // Populate with recent activities
    const notifications = appState.activities.slice(0, 10);
    
    panel.innerHTML = `
        <div class="panel-header">
            <h3>🔔 Notifications</h3>
            <button class="panel-close" onclick="closeNotificationsPanel()">&times;</button>
        </div>
        <div class="panel-body">
            ${notifications.length > 0 ? notifications.map(notif => `
                <div class="notification-item">
                    <span class="notification-icon">${notif.icon}</span>
                    <div class="notification-content">
                        <div class="notification-title">${notif.title}</div>
                        <div class="notification-time">${notif.meta}</div>
                    </div>
                </div>
            `).join('') : '<p class="empty-message">No notifications yet</p>'}
        </div>
        <div class="panel-footer">
            <button class="btn-link" onclick="clearAllNotifications()">Clear All</button>
        </div>
    `;
    
    panel.classList.add('active');
}

function closeNotificationsPanel() {
    const panel = document.getElementById('notifications-panel');
    if (panel) {
        panel.classList.remove('active');
    }
}

function clearAllNotifications() {
    appState.activities = [];
    populateActivityFeed();
    closeNotificationsPanel();
    showNotification('success', 'All notifications cleared');
}

function showUserMenu() {
    // Check if menu exists, otherwise create it
    let menu = document.getElementById('user-menu');
    
    if (!menu) {
        menu = document.createElement('div');
        menu.id = 'user-menu';
        menu.className = 'user-menu';
        document.body.appendChild(menu);
        
        // Position menu near user profile
        const userProfile = document.querySelector('.user-profile');
        const rect = userProfile.getBoundingClientRect();
        menu.style.top = `${rect.bottom + 10}px`;
        menu.style.right = `20px`;
    }
    
    // Toggle menu visibility
    if (menu.classList.contains('active')) {
        menu.classList.remove('active');
        return;
    }
    
    // Populate menu
    menu.innerHTML = `
        <div class="menu-item" onclick="showUserProfile()">
            <span>👤</span>
            <span>Profile</span>
        </div>
        <div class="menu-item" onclick="showPreferences()">
            <span>⚙️</span>
            <span>Preferences</span>
        </div>
        <div class="menu-item" onclick="showSystemInfo()">
            <span>ℹ️</span>
            <span>System Info</span>
        </div>
        <div class="menu-divider"></div>
        <div class="menu-item" onclick="exportData()">
            <span>💾</span>
            <span>Export Data</span>
        </div>
        <div class="menu-item" onclick="importData()">
            <span>📥</span>
            <span>Import Data</span>
        </div>
        <div class="menu-divider"></div>
        <div class="menu-item" onclick="showAbout()">
            <span>📖</span>
            <span>About</span>
        </div>
    `;
    
    menu.classList.add('active');
    
    // Close menu when clicking outside
    setTimeout(() => {
        document.addEventListener('click', closeUserMenuOnOutsideClick);
    }, 100);
}

function closeUserMenuOnOutsideClick(event) {
    const menu = document.getElementById('user-menu');
    const userProfile = document.querySelector('.user-profile');
    
    if (menu && !menu.contains(event.target) && !userProfile.contains(event.target)) {
        menu.classList.remove('active');
        document.removeEventListener('click', closeUserMenuOnOutsideClick);
    }
}

function showUserProfile() {
    closeUserMenu();
    showNotification('info', 'User profile feature - Coming soon!');
}

function showPreferences() {
    closeUserMenu();
    switchView('config');
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    document.querySelector('[data-view="config"]').classList.add('active');
    document.getElementById('page-title').textContent = 'Configuration';
}

function showSystemInfo() {
    closeUserMenu();
    const info = {
        version: '1.0.0',
        agents: appState.agents.length,
        tasks: appState.tasks.length,
        activities: appState.activities.length,
        connected: appState.isConnected
    };
    
    showNotification('info', `AI CodeForge v${info.version} | ${info.agents} agents | ${info.tasks} tasks | Status: ${info.connected ? 'Online' : 'Offline'}`);
}

function exportData() {
    closeUserMenu();
    const data = {
        tasks: appState.tasks,
        activities: appState.activities,
        config: appState.config,
        exportDate: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ai-codeforge-export-${Date.now()}.json`;
    a.click();
    
    showNotification('success', 'Data exported successfully!');
}

function importData() {
    closeUserMenu();
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/json';
    
    input.onchange = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        
        reader.onload = (event) => {
            try {
                const data = JSON.parse(event.target.result);
                
                if (data.tasks) appState.tasks = data.tasks;
                if (data.activities) appState.activities = data.activities;
                if (data.config) appState.config = data.config;
                
                saveState();
                populateTasks();
                populateActivityFeed();
                loadConfiguration();
                
                showNotification('success', 'Data imported successfully!');
            } catch (error) {
                showNotification('error', 'Failed to import data: Invalid format');
            }
        };
        
        reader.readAsText(file);
    };
    
    input.click();
}

function showAbout() {
    closeUserMenu();
    showNotification('info', 'AI CodeForge v1.0.0 - AAA Development Team | 23 AI Agents working together');
}

function closeUserMenu() {
    const menu = document.getElementById('user-menu');
    if (menu) {
        menu.classList.remove('active');
        document.removeEventListener('click', closeUserMenuOnOutsideClick);
    }
}


// WebSocket Connection
function connectWebSocket() {
    try {
        ws = new WebSocket('ws://localhost:8000/ws');
        
        ws.onopen = () => {
            console.log('✅ Connected to AI CodeForge');
            updateConnectionStatus(true);
            
            // Request initial data
            setTimeout(() => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ type: 'get_status' }));
                    ws.send(JSON.stringify({ type: 'list_agents' }));
                }
            }, 100);
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
    
    appState.isConnected = isConnected;
    
    if (isConnected) {
        statusDot.classList.add('online');
        statusText.textContent = 'System Online';
        showNotification('success', 'Connected to AI CodeForge');
        if (reconnectInterval) {
            clearInterval(reconnectInterval);
            reconnectInterval = null;
        }
    } else {
        statusDot.classList.remove('online');
        statusText.textContent = 'Reconnecting...';
        showNotification('warning', 'Connection lost. Reconnecting...');
    }
}

function handleWebSocketMessage(message) {
    console.log('Message:', message);
    
    switch (message.type) {
        case 'connected':
            showNotification('success', 'Connected to AI CodeForge backend');
            break;
        case 'agent_event':
            handleAgentEvent(message);
            break;
        case 'task_update':
            handleTaskUpdate(message);
            break;
        case 'task_result':
            handleTaskResult(message);
            break;
        case 'system_alert':
            handleSystemAlert(message);
            break;
        case 'system_status':
            updateSystemStatus(message.data);
            break;
        case 'agents_list':
            handleAgentsList(message);
            break;
        case 'code_generated':
            handleCodeGenerated(message);
            break;
        case 'execution_result':
            handleExecutionResult(message);
            break;
        case 'execution_update':
            handleExecutionUpdate(message);
            break;
        case 'research_result':
            handleResearchResult(message);
            break;
        case 'security_result':
            handleSecurityResult(message);
            break;
    }
    
    // Save state after each message
    saveState();
}

// Agent Management
function populateAgents() {
    // If we don't have agents yet, use default list
    if (appState.agents.length === 0) {
        const defaultAgents = [
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
        
        appState.agents = defaultAgents;
    }
    
    // Populate agents grid
    const agentsGrid = document.getElementById('agents-grid');
    if (agentsGrid) {
        agentsGrid.innerHTML = appState.agents.map(agent => `
            <div class="agent-card ${agent.status === 'busy' ? 'busy' : ''}">
                <div class="icon">${agent.icon}</div>
                <div class="name">${agent.name}</div>
                <div class="role">${agent.role}</div>
                ${agent.specialty ? `<div class="specialty">${agent.specialty}</div>` : ''}
                ${agent.status ? `<div class="agent-card-status status-${agent.status}">${agent.status}</div>` : ''}
            </div>
        `).join('');
    }
}

function populateTeamStatus() {
    const teamStatus = document.getElementById('team-status');
    if (teamStatus && appState.agents.length > 0) {
        const featuredAgents = appState.agents.slice(0, 8);
        teamStatus.innerHTML = featuredAgents.map(agent => `
            <div class="agent-status">
                <div class="icon">${agent.icon}</div>
                <div class="name">${agent.name}</div>
                <div class="status ${agent.status || 'ready'}">${agent.status || 'Ready'}</div>
            </div>
        `).join('');
    } else if (teamStatus) {
        // Fallback if no agents loaded yet
        teamStatus.innerHTML = `
            <div class="loading-message">
                <span class="loading-spinner">⏳</span>
                <p>Loading agents...</p>
            </div>
        `;
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
    
    // Send request to backend
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_task',
            data: {
                task: 'Run comprehensive test suite',
                mode: 'solo',
                agents: ['quinn']
            }
        }));
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
    }
}

function codeReview() {
    addActivity('🔍', 'Code review initiated', 'Just now');
    
    // Send request to backend
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_task',
            data: {
                task: 'Perform comprehensive code review',
                mode: 'solo',
                agents: ['orion']
            }
        }));
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
    }
}

function securityScan() {
    addActivity('🔒', 'Security scan started', 'Just now');
    switchView('security');
}

function deploy() {
    addActivity('🚀', 'Deployment pipeline started', 'Just now');
    
    // Send request to backend
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_task',
            data: {
                task: 'Deploy application to production',
                mode: 'team',
                agents: ['nova', 'zephyr']
            }
        }));
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
    }
}

function research() {
    addActivity('🔬', 'Research lab opened', 'Just now');
    switchView('research');
}

// Code Editor Functions
function generateCodeFromPrompt() {
    const prompt = document.getElementById('code-prompt').value;
    if (!prompt.trim()) {
        showNotification('warning', 'Please enter a task description');
        return;
    }
    
    const editor = document.getElementById('code-editor');
    editor.value = '// Generating code...\n// Waiting for Felix agent response...\n';
    
    addActivity('💻', `Generating: ${prompt}`, 'Just now');
    
    // Send via WebSocket to backend
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_task',
            data: {
                task: prompt,
                mode: 'solo',
                agents: ['felix']
            }
        }));
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
        editor.value = '// Error: Backend not connected\n// Please check the WebSocket connection';
    }
}

function copyCode() {
    const editor = document.getElementById('code-editor');
    editor.select();
    document.execCommand('copy');
    showNotification('success', 'Code copied to clipboard!');
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
    showNotification('success', 'Code saved successfully!');
}

function executeCode() {
    const code = document.getElementById('code-editor').value;
    if (!code.trim()) {
        showNotification('warning', 'No code to execute');
        return;
    }
    
    addActivity('⚡', 'Executing code in Docker sandbox', 'Just now');
    
    // Send code execution request to backend
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_code',
            data: { code: code }
        }));
        showNotification('info', 'Code execution started...');
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
    }
}

// Security Functions
function runSecurityScan() {
    const results = document.getElementById('security-results');
    results.innerHTML = `
        <div style="padding: 2rem;">
            <h4>🔍 Scanning for vulnerabilities...</h4>
            <p>Mira (Security Engineer) is analyzing the codebase...</p>
            <ul style="margin-top: 1rem; line-height: 2;">
                <li>⏳ OWASP Top 10 scan</li>
                <li>⏳ Dependency vulnerabilities</li>
                <li>⏳ Code security patterns</li>
                <li>⏳ Configuration review</li>
            </ul>
        </div>
    `;
    addActivity('🔒', 'Security scan in progress', 'Just now');
    
    // Send security scan request to backend
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_task',
            data: {
                task: 'Perform comprehensive security audit of the codebase',
                mode: 'solo',
                agents: ['mira']
            }
        }));
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
        results.innerHTML = `
            <div style="padding: 2rem;">
                <h4>❌ Connection Error</h4>
                <p>Cannot connect to backend. Please ensure the server is running.</p>
            </div>
        `;
    }
}

// Research Functions
function startResearch() {
    const query = document.getElementById('research-query').value;
    if (!query.trim()) {
        showNotification('warning', 'Please enter a research query');
        return;
    }
    
    const results = document.getElementById('research-results');
    results.innerHTML = `
        <div style="padding: 2rem;">
            <h4>🔬 Researching: ${query}</h4>
            <p>Helix (Research Lead) is analyzing this topic...</p>
            <div style="margin-top: 1rem;">
                <div class="loading-spinner">⏳</div>
                <p style="margin-top: 1rem;">Searching web resources...</p>
            </div>
        </div>
    `;
    
    addActivity('🔬', `Researching: ${query}`, 'Just now');
    
    // Send research request to backend
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_task',
            data: {
                task: `Research and provide comprehensive information about: ${query}`,
                mode: 'research',
                agents: ['helix']
            }
        }));
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
        results.innerHTML = `
            <div style="padding: 2rem;">
                <h4>❌ Connection Error</h4>
                <p>Cannot connect to backend. Please ensure the server is running.</p>
            </div>
        `;
    }
}

// Design Functions
function uxDesign() {
    addActivity('🎨', 'UX design started', 'Just now');
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_task',
            data: {
                task: 'Create comprehensive UX design with user flows and wireframes',
                mode: 'solo',
                agents: ['pixel']
            }
        }));
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
    }
}

function uiComponents() {
    addActivity('🎨', 'UI component generation started', 'Just now');
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_task',
            data: {
                task: 'Generate comprehensive UI component library',
                mode: 'solo',
                agents: ['pixel']
            }
        }));
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
    }
}

function accessibilityAudit() {
    addActivity('♿', 'Accessibility audit started', 'Just now');
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_task',
            data: {
                task: 'Perform WCAG compliance check and accessibility audit',
                mode: 'solo',
                agents: ['pixel']
            }
        }));
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
    }
}

function designSystem() {
    addActivity('🎨', 'Design system generation started', 'Just now');
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'execute_task',
            data: {
                task: 'Create comprehensive design system with components, tokens, and guidelines',
                mode: 'solo',
                agents: ['pixel']
            }
        }));
    } else {
        showNotification('error', 'Backend not connected. Please check connection.');
    }
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
    showNotification('success', 'Configuration saved successfully!');
    
    // Send config to backend
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'update_config',
            data: config
        }));
    }
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
    if (status.active_agents !== undefined) {
        // Update agent count in navigation if needed
        const agentsNav = document.querySelector('[data-view="agents"]');
        if (agentsNav) {
            const agentText = agentsNav.querySelector('span:last-child');
            if (agentText) {
                agentText.textContent = `Agents (${status.active_agents})`;
            }
        }
    }
    if (status.connections !== undefined) {
        console.log(`Active connections: ${status.connections}`);
    }
}

// Handle agents list from backend
function handleAgentsList(message) {
    const { data } = message;
    
    if (data.agents && data.agents.length > 0) {
        // Update appState with real agent data
        appState.agents = data.agents.map(agent => ({
            name: agent.name,
            role: agent.role,
            icon: getAgentIcon(agent.name),
            category: getAgentCategory(agent.role),
            specialty: agent.specialty,
            status: agent.status || 'ready'
        }));
        
        // Update UI
        populateAgents();
        populateTeamStatus();
        
        console.log(`✅ Loaded ${data.agents.length} agents from backend`);
    } else if (data.error) {
        console.error('Failed to load agents:', data.error);
        if (data.traceback) {
            console.error('Traceback:', data.traceback);
        }
    }
}

// Get icon for agent by name
function getAgentIcon(name) {
    const icons = {
        'aurora': '👔', 'sage': '🏗️', 'felix': '💻', 'ember': '💡',
        'orion': '👀', 'atlas': '⚡', 'mira': '🔒', 'vex': '🤔',
        'sol': '🔧', 'echo': '🎨', 'nova': '🚀', 'quinn': '🧪',
        'blaze': '📱', 'ivy': '📊', 'zephyr': '☁️',
        'pixel': '🎭', 'script': '📚', 'turbo': '⚡', 'sentinel': '👁️',
        'helix': '🔬', 'patch': '🐛', 'pulse': '🔌', 'link': '🔗'
    };
    return icons[name.toLowerCase()] || '🤖';
}

// Get category for agent by role
function getAgentCategory(role) {
    const planners = ['Product Manager', 'Lead Architect', 'Senior Developer', 'Creative Director'];
    const critics = ['Code Reviewer', 'Performance Specialist', 'Security Engineer', 'Critical Analyst'];
    const specialists = ['Backend Specialist', 'Frontend Developer', 'DevOps Engineer', 'QA Lead', 
                        'Mobile Developer', 'Data Engineer', 'Cloud Architect'];
    const assistants = ['UX Designer', 'Tech Writer', 'Performance Engineer', 'SRE Lead'];
    const special = ['Research Lead', 'Bug Hunter', 'Integration Specialist', 'Collaboration Lead'];
    
    if (planners.includes(role)) return 'planner';
    if (critics.includes(role)) return 'critic';
    if (specialists.includes(role)) return 'specialist';
    if (assistants.includes(role)) return 'assistant';
    if (special.includes(role)) return 'special';
    return 'other';
}

// Handle execution update (progress messages)
function handleExecutionUpdate(message) {
    const { data } = message;
    
    if (data.status === 'executing') {
        addActivity('⚡', data.message || 'Executing code...', 'Just now');
    }
}

// Update stats periodically
setInterval(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'get_status' }));
    }
}, 5000);

// New message handlers
function handleTaskResult(message) {
    const { data } = message;
    
    if (data.status === 'success') {
        showNotification('success', `Task completed: ${data.task}`);
        addActivity('✅', `Task completed: ${data.task}`, 'Just now');
        
        // Update task if it exists
        const task = appState.tasks.find(t => t.description === data.task);
        if (task) {
            task.status = 'completed';
            task.result = data.result;
            populateTasks();
        }
    } else {
        showNotification('error', `Task failed: ${data.error}`);
        addActivity('❌', `Task failed: ${data.task}`, 'Just now');
    }
}

function handleCodeGenerated(message) {
    const { data } = message;
    const editor = document.getElementById('code-editor');
    
    if (data.code) {
        editor.value = data.code;
        showNotification('success', 'Code generated successfully!');
        addActivity('✅', 'Code generation completed', 'Just now');
    } else {
        editor.value = '// Error generating code\n// ' + (data.error || 'Unknown error');
        showNotification('error', 'Code generation failed');
    }
}

function handleExecutionResult(message) {
    const { data } = message;
    const editor = document.getElementById('code-editor');
    
    if (data.success) {
        editor.value += '\n\n// Execution Output:\n// ' + (data.output || 'Success');
        showNotification('success', 'Code executed successfully!');
        addActivity('✅', 'Code execution completed', 'Just now');
    } else {
        editor.value += '\n\n// Execution Error:\n// ' + (data.error || 'Unknown error');
        showNotification('error', 'Code execution failed');
    }
}

function handleResearchResult(message) {
    const { data } = message;
    const results = document.getElementById('research-results');
    
    if (data.result) {
        results.innerHTML = `
            <div style="padding: 2rem;">
                <h4>🔬 Research Results</h4>
                <div style="margin-top: 1rem; white-space: pre-wrap;">${data.result}</div>
            </div>
        `;
        showNotification('success', 'Research completed!');
        addActivity('✅', 'Research completed', 'Just now');
    } else {
        results.innerHTML = `
            <div style="padding: 2rem;">
                <h4>❌ Research Failed</h4>
                <p>${data.error || 'Unknown error'}</p>
            </div>
        `;
        showNotification('error', 'Research failed');
    }
}

function handleSecurityResult(message) {
    const { data } = message;
    const results = document.getElementById('security-results');
    
    if (data.result) {
        results.innerHTML = `
            <div style="padding: 2rem;">
                <h4>🔒 Security Scan Results</h4>
                <div style="margin-top: 1rem; white-space: pre-wrap;">${data.result}</div>
            </div>
        `;
        showNotification('success', 'Security scan completed!');
        addActivity('✅', 'Security scan completed', 'Just now');
    } else {
        results.innerHTML = `
            <div style="padding: 2rem;">
                <h4>❌ Security Scan Failed</h4>
                <p>${data.error || 'Unknown error'}</p>
            </div>
        `;
        showNotification('error', 'Security scan failed');
    }
}

// Fetch agents from backend on load
function fetchAgentsFromBackend() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'list_agents' }));
    } else {
        // Fallback to fetch API
        fetch('http://localhost:8000/api/agents')
            .then(response => response.json())
            .then(data => {
                if (data.agents && data.agents.length > 0) {
                    // Update with real agent data
                    appState.agents = data.agents;
                    populateAgents();
                }
            })
            .catch(error => {
                console.error('Failed to fetch agents:', error);
            });
    }
}
