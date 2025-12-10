
# AI Dev Team: UI/UX Interaction Model

**Document Purpose:** This document outlines the design and philosophy for the user interface (UI) and user experience (UX) of the AI Dev Team. The goal is to move beyond a simple chat prompt and create a "Virtual War Room"—an intuitive, powerful command center for directing and collaborating with a team of AI agents in real time.

---

## 1. Core Principles: The Virtual War Room

The UI will be designed around a central metaphor: the user is not just a client, but the **Team Lead** or **Project Director**. The interface is their project room, giving them full visibility and control.

- **Radical Transparency:** The user should always be able to see who is doing what, what they are thinking, and what they have accomplished. No black boxes.
- **Directability & Intervention:** The user has ultimate authority. They can pause the entire team, redirect a single agent, approve plans, or take over a task themselves at any moment.
- **Context is King:** The interface should dynamically present information relevant to the task at hand, whether it's a file, a test result, or a research summary.
- **Asynchronous & Non-Blocking:** The UI must remain fluid and responsive. The user can browse files, review past conversations, or queue up new commands while the agents are working.

---

## 2. The Anatomy of the UI: A Multi-Panel Dashboard

To achieve our principles, a multi-panel layout is essential. This provides dedicated spaces for different streams of information, preventing clutter and cognitive overload.

![Conceptual UI Layout](https://i.imgur.com/8aZ2XyY.png)
*(This is a conceptual sketch. The final design would be refined.)*

### Panel 1: The "Team Roster" (Left Sidebar)
This panel gives you an at-a-glance overview of your entire team.

- **Components:**
    - A list of all active agents for the project (`Architect`, `SoftwareEngineer`, `QAEngineer`, `Researcher`, etc.).
    - **Live Status Indicator:** A colored dot and a short status label next to each agent's name.
        - 🟢 **Idle:** Awaiting instructions.
        - 🔵 **Thinking/Planning:** Analyzing a problem or generating a plan.
        - 🟡 **Executing:** Actively working (e.g., `Coding`, `Researching`, `Running Tests`).
        - 🔴 **Error:** Encountered an issue and requires attention.
        - ⚫ **Paused:** Manually paused by the user.
- **Interaction:**
    - **Hover/Click:** Clicking on an agent reveals a tooltip or a small pop-over with a one-sentence summary of their current task: *"Refactoring `auth.py` to add a caching layer."*

### Panel 2: The "Workspace Explorer" (Far Left Sidebar)
A familiar, powerful file-tree view of the project.

- **Components:**
    - A standard hierarchical tree of files and folders in the project workspace.
- **Unique Features:**
    - **Agent Activity Glow:** Files being actively read or written to by an agent will have a subtle, colored glow corresponding to the agent working on it. This provides instant, passive information about where work is happening.
    - **Right-Click Menu:** Right-click a file to issue context-aware commands: *"@QAEngineer, write tests for this file,"* or *"@Architect, is this file in the right place?"*

### Panel 3: "Mission Control" (Center Panel)
This is the main hub for communication and high-level command.

- **Components:**
    - A super-powered chat interface. It is the primary channel for giving instructions and receiving high-level updates from the `ProjectManager` and `Architect`.
- **Unique Features:**
    - **Task-Based Threading:** When you give a new high-level goal (e.g., "Add Google OAuth"), it creates a new collapsible "mission thread." All high-level communication about that goal is contained within it, preventing the main chat from becoming an endless scroll.
    - **Plan Approval Workflow:** When the `ProjectManager` proposes a plan, it appears as a structured checklist within the chat. You can review, comment on, and finally approve or reject it with a single click.
    - **Agent Mentions:** Use `@` to talk directly to agents (`@Researcher, find the best library for PDF generation in Python`) or to the whole team (`@all, what is our current progress?`).

### Panel 4: The "Workbench" (Right Panel)
This is the largest and most dynamic area, where the tangible work of the agents is made visible. It's an evolution of the "Artifacts" concept.

- **Content-Aware Views:** This panel changes based on the context.
    - **Code View:** When an agent writes code, it appears here with syntax highlighting and a diff view comparing it to the previous version.
    - **Test Results View:** Displays `pytest` or other test runner output, clearly showing passes, fails, and error logs.
    - **Research Summary View:** Renders markdown reports from the `Researcher` agent, with clickable links.
    - **Terminal View:** Shows the live output of any shell commands being run by an agent in its secure sandbox.
    - **Diagram View:** Can render Mermaid.js or PlantUML diagrams generated by the `Architect` agent to explain a new design.
- **Interactivity:** The user can copy code, open files from this view, and in the future, even provide direct line-by-line feedback on code.

---

## 3. The Interaction Model: Leading the Team

### The Core Loop
1.  **Directive:** User issues a high-level goal in **Mission Control**.
2.  **Clarification & Planning:** The `ProductManager` or `ProjectManager` may ask clarifying questions. It then presents a structured plan for approval.
3.  **Execution:** Upon approval, agents in the **Team Roster** light up as they begin working. Their results (code, tests, etc.) appear dynamically in the **Workbench**. High-level progress is reported in the mission thread.
4.  **Review:** The user reviews the artifacts in the Workbench.
5.  **Completion:** Once the goal is met, the mission thread is marked as complete.

### Interrupts and Redirection: The "Pause" Button
- A global **PAUSE** button in the UI header immediately stops all agents from starting new actions.
- While paused, the UI enters a "Director Mode." The user can then click on any task or agent to issue new, overriding commands:
    - *"@SoftwareEngineer, stop what you are doing. Refactor the database connection logic first."*
    - Drag-and-drop a task in the plan to change its priority.

### Technology & Implementation Sketch
- **Frontend:** A modern framework like **React, Vue, or Svelte** is required to build this component-based, dynamic interface.
- **State Management:** A robust state management library (like Redux Toolkit, Zustand, or Pinia) will be essential.
- **Backend Communication:** **WebSockets** are non-negotiable. The Python backend will push a constant stream of events (e.g., `AGENT_STATUS_CHANGED`, `NEW_ARTIFACT_CREATED`, `LOG_MESSAGE_RECEIVED`) to the frontend, allowing the UI to update in real time without polling.
