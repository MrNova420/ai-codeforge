
# AI Dev Team: Agent Enhancement Strategy

**Document Purpose:** This document outlines a strategic vision for fundamentally upgrading the intelligence, memory, and capabilities of the individual AI agents within the AI Dev Team project. This plan builds upon the foundational stability provided by the `PROJECT_REVISION_PLAN.md`.

---

## 1. Core Philosophies for Advanced Agent Design

To elevate the agents from simple command-responders to genuine digital colleagues, we will adopt the following design principles:

1.  **Role Specialization:** Each agent should have a clearly defined role and a curated set of tools, just like a human software team. An agent that tries to do everything will be mediocre at everything.
2.  **Tool-Assisted Reliability:** An agent's intelligence is not just in its base model, but in the tools it can use. Complex tasks should be broken down into a series of tool uses (e.g., `read_file`, `run_test`, `search_web`). This makes their work more predictable, auditable, and reliable.
3.  **Statefulness & Context:** Agents must have memory of their current task context (a "scratchpad") and a persistent memory of past projects (long-term memory).
4.  **Self-Correction & Reflection:** Agents should be capable of recognizing their own errors and attempting to fix them.

---

## 2. System-Wide Agent Enhancements

These are foundational upgrades that will benefit all agents in the system.

### 2.1. Long-Term Memory (The Team's Brain)

This is the most critical enhancement for creating a learning system.

- **Mechanism:** Implement a vector database. For simplicity and local-first operation, `ChromaDB` or `FAISS` are excellent choices. A dedicated `MemoryManager` module will encapsulate all interactions with this database.
- **What to Store:**
    - **Task Summaries:** Upon successful completion of a complex task, the Overseer agent will generate a summary: "To add a user login endpoint, we created a new route in `server.py`, added a `User` model, and wrote a test in `test_auth.py`."
    - **Error Resolutions:** When a bug is fixed, the "aha!" moment is stored: "Error `TypeError: 'NoneType' object is not iterable` was caused by the database connection failing silently. Resolved by adding a connection check and retry logic."
    - **Key Code Snippets:** Particularly elegant or important functions or configurations.
    - **User Feedback:** Explicit corrections or architectural decisions from the human user.
- **Workflow:**
    1.  **Recall:** Before the Overseer plans a new task, it formulates a query to the `MemoryManager` to retrieve relevant context from past projects.
    2.  **Context Injection:** The retrieved memories are injected into the Overseer's context window, giving it a head-start and preventing it from repeating past mistakes.
    3.  **Memorization:** After a task is complete (or a major milestone is reached), a "Memory Synthesis" step is triggered, where the key takeaways are embedded and stored in the vector database.

### 2.2. A Rich and Dynamic Toolbelt

Agents become exponentially more useful when they can act on the environment. We will standardize and expand their tool-use (function calling) capabilities.

- **Standardize on Function Calling:** All agents *must* interact with the system via structured tool calls, not by outputting shell commands in prose.
- **`ToolRegistry` Module:**
    - A central registry will define all available tools (e.g., `read_file`, `write_file`, `run_linter`, `execute_tests`, `search_codebase`).
    - Agents will be initialized with a specific set of tools tailored to their role.
- **Dynamic Tool Granting:** For advanced scenarios, an agent could request a tool it doesn't have. For example, a Developer agent might determine it needs to interact with a Git repository and request the `git_clone` tool from the Orchestrator.

### 2.3. Stateful Task Execution (Agent Scratchpad)

- **Problem:** In a simple request-response model, an agent has no memory between turns. It can't remember a file it just read or a variable it was tracking.
- **Solution:** Each agent task processed by the `AgentManager` will have an associated `TaskState` object (a "scratchpad").
- **Functionality:** This object will persist for the duration of a multi-step task. It allows an agent to "think" across multiple LLM calls. For example, it can read a file in one step, store the contents in its scratchpad, and then use that content in the next step to write a new file, without having to read the first file again.

---

## 3. Enhancing Specific Agent Roles

With the core enhancements in place, we can drastically improve the existing agent roles and introduce new ones.

### 3.1. The "Project Manager" Agent (Successor to Overseer)
- **Role:** High-level planning, task decomposition, and learning.
- **Enhanced Capabilities:**
    - **Primary Output:** Its sole job is to consume the user's request and the `Long-Term Memory` context and produce a validated JSON task graph.
    - **Adaptive Re-planning:** If a task fails and the responsible agent cannot fix it, the failure report is routed back to the Project Manager. It will then analyze the error and generate a new plan, such as assigning it to a different agent or breaking the problem down further.

### 3.2. The "Software Engineer" Agent (Successor to Developer)
- **Role:** Writing, analyzing, and debugging code.
- **Enhanced Capabilities:**
    - **Core Toolbelt:** `read_file`, `write_file_chunk`, `list_directory`, `search_codebase`.
    - **Debugging Loop:** This is a crucial new behavior.
        1. The agent writes code and a test (or receives a test from the QA Engineer).
        2. The code is executed via the secure `DockerCodeExecutor`.
        3. If the test fails, the `stdout`, `stderr`, and failing test code are automatically fed back to the Software Engineer agent in its next turn.
        4. The agent is prompted: "Your code failed with the following error. Please analyze the error and provide a fix."
        5. This loop continues for a configurable number of attempts (e.g., 3) before escalating the failure to the Project Manager.

### 3.3. The "QA Engineer" Agent (New Role)
- **Role:** Ensuring code quality and correctness.
- **Enhanced Capabilities:**
    - **Test Generation:** Given a class or function written by the Software Engineer, its primary job is to write comprehensive unit tests (e.g., using `pytest` or `jest`, depending on the project). It should be an expert at identifying edge cases.
    - **Test Execution:** It uses the `DockerCodeExecutor` to run its tests against the developer's code.
    - **Structured Reporting:** It doesn't just say "pass" or "fail." It outputs a JSON object detailing which tests passed, which failed, and the logs for the failed tests.

### 3.4. The "Code Reviewer" Agent (New Role / Quality Gate)
- **Role:** Enforcing code quality, style, and best practices.
- **Function:** This agent does not write production code. It sits between the Software Engineer and the QA Engineer.
- **Workflow:**
    1. The Software Engineer submits a piece of code.
    2. The Code Reviewer receives the code and a set of project-specific guidelines (e.g., "all functions must have docstrings," "avoid nested loops deeper than 2 levels").
    3. It provides a structured review (e.g., a JSON object with comments and line numbers). If the review passes, the code proceeds to the QA stage. If not, it's sent back to the Software Engineer with the required changes.

---

## 4. Phased Implementation Plan

*(Requires the new architecture from `PROJECT_REVISION_PLAN.md` to be in place)*

1.  **Phase 1: Implement Memory & State**
    - Integrate a vector database and build the `MemoryManager`.
    - Implement the "scratchpad" (`TaskState`) object within the `AgentManager`.
    - Create the "Memorization" step at the end of a successful team collaboration.

2.  **Phase 2: The Debugging Loop**
    - Implement the automated feedback loop for the Software Engineer agent as described in 3.2. This is a huge step towards true autonomous problem-solving.

3.  **Phase 3: Introduce New Roles**
    - Formally introduce the QA Engineer and Code Reviewer agents into the team collaboration workflow, updating the Project Manager to utilize them.

By focusing on these agent-level enhancements, the AI Dev Team will evolve from a simple script-runner into a dynamic, learning system that can tackle more complex problems with greater autonomy and reliability.
