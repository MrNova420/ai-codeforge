# AI Dev Team: Project Revision and Development Plan

**Document Purpose:** This document provides a comprehensive analysis of the current AI Dev Team project, identifies critical weaknesses, and presents a detailed, strategic plan for its redesign and future development.

--- 

## 1. Current State Analysis

The "AI Dev Team" project is an ambitious multi-agent system designed to automate software development tasks using a team of specialized AI agents. The user interacts with the system via a Terminal User Interface (TUI) to select modes of operation (e.g., solo agent vs. team collaboration).

### 1.1. Existing Architecture

- **Entry Point:** The application is launched via the `./run` script, which executes `orchestrator_v2.py`.
- **Orchestration:** `orchestrator_v2.py` serves as the central hub, managing the UI and high-level workflow. It inherits base classes from `orchestrator.py` for loading agent profiles and configurations.
- **Agent Interaction:** All LLM communication is handled by `agent_chat_enhanced.py`, which makes direct API calls to services like OpenAI, Gemini, or a local server.
- **Team Collaboration:** The multi-agent "team" mode is managed by `collaboration_enhanced.py`. It uses an "Overseer" agent to break down a user's request into a series of tasks.
- **Code Execution:** Agent-generated code is executed via `code_executor.py`, which uses the `subprocess` module with a timeout.

### 1.2. Identified Critical Weaknesses

The current implementation suffers from several architectural flaws that are the primary source of its instability and brittleness.

1.  **Blocking API Calls (Primary Source of Instability):**
    - **Problem:** In `agent_chat_enhanced.py`, all network calls to LLM APIs are **synchronous and blocking**. If the API is slow to respond or experiences an outage, the entire application freezes, leading to a frustrating and unreliable user experience.
    - **Impact:** This is the single largest contributor to the application's "unstable" feel.

2.  **Unused Resiliency Module (A Missed Opportunity):**
    - **Discovery:** The codebase contains a sophisticated but **completely unused** module: `agent_manager.py`.
    - **Functionality:** This module provides a robust, threaded, and resilient framework for executing agent tasks with configurable timeouts and retries. It was clearly designed to solve the blocking API call problem but was never integrated into the main application loop.
    - **Impact:** The application is reinventing a less reliable version of a problem already solved within its own codebase.

3.  **Brittle Task Parsing in Team Mode:**
    - **Problem:** The `collaboration_enhanced.py` module relies on parsing the natural language output of the "Overseer" LLM to generate a task list. This "prompt parsing" is notoriously unreliable and can easily break if the model changes its phrasing or output format even slightly.
    - **Impact:** This makes the team collaboration mode fragile and unpredictable.

4.  **Sequential Task Execution:**
    - **Problem:** The collaboration mode executes the parsed tasks one by one (sequentially).
    - **Impact:** This is inefficient and does not leverage the potential for parallel work that a multi-agent system should provide.

5.  **Inadequate Sandboxing:**
    - **Problem:** `code_executor.py` executes code directly on the host machine using `subprocess`. While it has a timeout, it lacks true isolation.
    - **Impact:** This is a major security risk. A malicious or buggy agent could generate code that damages the user's system, accesses sensitive files, or installs malware.

--- 

## 2. The New Vision: A Resilient & Scalable Architecture

To address these weaknesses, I propose a significant architectural refactor centered on five core principles:

- **Stability:** The application must never freeze, regardless of network conditions.
- **Modularity:** Components should be decoupled and independently manageable.
- **Asynchronicity:** All long-running tasks (especially I/O) must be non-blocking.
- **Structured Communication:** Agents must communicate using reliable, machine-readable data formats (JSON), not prose.
- **Security:** All agent-generated code must execute in a fully isolated sandbox.

### 2.1. Proposed Architecture Diagram (Conceptual)

```
[ User (TUI) ] -> [ Orchestrator v3 ]
                      |
                      | (Delegates ALL agent tasks)
                      v
              [ AgentManager (The New Core) ]
               |        |        |
    (Threaded, Non-Blocking, Timeouts)
     /              |               \
    v               v                v
[ Agent A ]  <- [ Message Bus ] ->  [ Agent B ]
    |               ^
    | (Executes Code) | (Subscribes to results)
    v               |
[ Secure Docker Sandbox ]
```

### 2.2. Component Redesign Deep-Dive

#### 2.2.1. Orchestration Engine (`orchestrator_v3.py`)
The orchestrator's role will be simplified. It will manage the UI state and delegate *all* agent-related work.
- **Refactor:** Remove all direct calls to `EnhancedAgentChat`.
- **Integrate:** All agent tasks will be dispatched through the `AgentManager`.
- **New UI Logic:** The TUI will be updated to show "Task in progress..." messages and handle the success/error callbacks from the `AgentManager` to display results without freezing.

#### 2.2.2. The New Core - Resilient Agent Execution (`agent_manager.py`)
This existing module will be promoted to the central nervous system of the application.
- **Integrate:** It will be fully integrated into the new `Orchestrator v3`.
- **Mandate:** All LLM calls and code executions *must* be routed through the `AgentManager`'s `execute_agent_task` function. This provides immediate stability via its built-in threading and timeouts.

#### 2.2.3. Team Collaboration (`collaboration_v2.py`)
This module will be rewritten to use structured data and parallel execution.
- **Deprecate Prompt Parsing:** The "Overseer/Planner" agent's prompt will be engineered to require a JSON object as output. Modern models (like GPT-4 and Gemini) support "function calling" or "tool use" which is ideal for this.
- **Example JSON Task List:**
  ```json
  {
    "tasks": [
      { "task_id": 1, "agent": "developer", "description": "Create the main server file `server.py` with a basic Flask app.", "dependencies": [] },
      { "task_id": 2, "agent": "developer", "description": "Create a `models.py` for data structures.", "dependencies": [] },
      { "task_id": 3, "agent": "tester", "description": "Write a unit test for the `models.py`.", "dependencies": [2] }
    ]
  }
  ```
- **Parallel Dispatch:** The new collaboration engine will parse this JSON and use the `AgentManager` to dispatch all tasks with no dependencies in parallel. It will then manage the dependency graph, dispatching new tasks as their prerequisites are met.

#### 2.2.4. Secure Code Execution Sandbox (`docker_executor.py`)
The `subprocess` model will be replaced entirely for security.
- **New Module:** A new `docker_executor.py` will be created.
- **Functionality:** It will use the Docker SDK (or a CLI wrapper) to:
    1. Create an ephemeral, isolated Docker container for each code execution task.
    2. Copy the necessary workspace files into the container.
    3. Execute the code.
    4. Retrieve the output, errors, and any file artifacts.
    5. Destroy the container.
- **Benefit:** Provides maximum security, prevents filesystem contamination, and allows for per-task dependency management via custom Docker images.

--- 

## 3. Phased Development Roadmap

This redesign can be implemented in a series of manageable phases.

#### **Phase 1: Foundation & Stability (Highest Priority)**
*Goal: Make the application stable and non-blocking.*
1.  **Integrate AgentManager:** Refactor `orchestrator_v2.py` to initialize and use `AgentManager`.
2.  **Delegate Agent Calls:** Replace all direct `EnhancedAgentChat.send_message()` calls in the solo agent mode with non-blocking calls via `AgentManager.execute_agent_task()`.
3.  **Update UI for Asynchronicity:** Modify the TUI to show "Task in progress..." messages and handle the success/error callbacks from the `AgentManager` to display results without freezing.

#### **Phase 2: Structured Workflows**
*Goal: Make the team collaboration mode reliable and efficient.*
1.  **Enforce JSON Output:** Re-prompt the "Overseer" agent to generate JSON task lists. Implement strict validation to parse this output.
2.  **Rewrite Task Logic:** Rewrite `collaboration_enhanced.py` to be a new `collaboration_v2.py`. This new module will read the JSON task graph.
3.  **Enable Parallel Execution:** Use the `AgentManager` to dispatch multiple tasks concurrently based on the dependency graph.

#### **Phase 3: Security Hardening**
*Goal: Eliminate security vulnerabilities from code execution.*
1.  **Develop Docker Executor:** Create the `docker_executor.py` module with the core functionality described in section 2.2.4.
2.  **Integrate Sandbox:** Modify the `AgentManager` and relevant agents (e.g., "developer," "tester") to use the new `DockerCodeExecutor` instead of the old `CodeExecutor`.

#### **Phase 4: Advanced Features & Polish**
*Goal: Enhance agent capabilities and intelligence.*
1.  **Implement Message Bus:** Introduce a simple, in-memory message bus (e.g., Python's `Queue`) that allows agents to publish findings that other agents can subscribe to, creating a more dynamic and event-driven system.
2.  **Introduce a "Critic" Agent:** Add a new agent whose role is to review code generated by the developer agent against a set of quality criteria before it is committed.

--- 

## 4. New Feature Brainstorm for Future Sprints

- **Interactive Debugging:** An agent that can pause execution, inspect variables, and allow the user to guide its debugging process.
- **Web-Based UI:** A more sophisticated front-end to visualize the agent's actions, workspace, and communication in real-time.
- **Long-Term Memory:** Integrate a vector database (e.g., ChromaDB, Pinecone) to give the agent team persistent memory of past projects and user preferences.
- **Self-Healing Capabilities:** An agent that monitors the other agents and can restart or debug them if they get stuck in a loop or fail.
- **CI/CD Integration:** An agent that can automatically create GitHub Actions workflows to test and deploy the generated code.

By following this plan, the AI Dev Team project can be transformed from an unstable prototype into a robust, secure, and powerful platform for automated software engineering.
