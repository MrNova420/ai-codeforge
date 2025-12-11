#!/usr/bin/env python3
"""
Prompt Utilities - Shared prompt builders for consistent agent behavior
Centralizes action-oriented prompts to ensure all agents generate actual implementations
"""

from typing import Optional


def build_actionable_task_prompt(
    task_description: str,
    agent_role: Optional[str] = None,
    priority: Optional[str] = None,
    additional_context: Optional[str] = None
) -> str:
    """
    Build an action-oriented task prompt that ensures agents actually implement.
    
    Args:
        task_description: The core task description
        agent_role: Optional role of the agent (e.g., "Backend Developer")
        priority: Optional priority level (e.g., "high", "medium")
        additional_context: Optional additional context or constraints
    
    Returns:
        Complete actionable task prompt
    """
    prompt_parts = []
    
    # Role context if provided
    if agent_role:
        prompt_parts.append(f"You are assigned this task as: {agent_role}\n")
    
    # Core task
    prompt_parts.append(f"Task: {task_description}")
    
    # Priority if provided
    if priority:
        prompt_parts.append(f"\nPriority: {priority}")
    
    # Additional context if provided
    if additional_context:
        prompt_parts.append(f"\n\n{additional_context}")
    
    # Action-oriented instructions
    action_instructions = """

CRITICAL INSTRUCTIONS:
- ACTUALLY IMPLEMENT this - don't just suggest or explain
- If it's code: Write the complete, working code
- If it's design: Create the actual design specifications with details
- If it's a feature: Build it fully with all necessary components
- Include file contents if creating files
- Provide complete, ready-to-use implementations

Your response should contain the actual work product, not just plans or suggestions.

BEGIN YOUR IMPLEMENTATION:"""
    
    prompt_parts.append(action_instructions)
    
    return "".join(prompt_parts)


def build_enhanced_task_prompt(task_description: str) -> str:
    """
    Build a prompt for enhanced mode task execution.
    Simpler version for when just task description is needed.
    
    Args:
        task_description: The task description
    
    Returns:
        Actionable prompt
    """
    return f"""You are assigned the following task:

{task_description}

CRITICAL INSTRUCTIONS:
- ACTUALLY IMPLEMENT this - don't just suggest or explain
- If it's code: Write the complete, working code
- If it's design: Create the actual design specifications with details
- If it's a feature: Build it fully with all necessary components
- Include file contents if creating files
- Provide complete, ready-to-use implementations

Your response should contain the actual work product, not just plans or suggestions."""


def build_delegation_prompt(user_request: str, available_agents: list) -> str:
    """
    Build a prompt for Helix to delegate tasks to agents.
    
    Args:
        user_request: The user's original request
        available_agents: List of available agent names
    
    Returns:
        Complete delegation prompt with examples
    """
    agents_list = ", ".join(available_agents)
    
    return f"""You are Helix, team overseer. Break down this request into ACTIONABLE tasks that agents will ACTUALLY IMPLEMENT.

REQUEST: {user_request}

CRITICAL: Each task must be SPECIFIC and ACTIONABLE - agents will GENERATE CODE, CREATE FILES, and IMPLEMENT solutions.

Example GOOD task delegation:
- aurora: Create the complete HTML structure for the car enthusiast homepage with navigation, hero section, and car gallery grid
- felix: Implement Python Flask backend API with endpoints for car data (GET /cars, POST /cars, GET /cars/:id) including database models
- pixel: Design the full CSS styling with responsive layout, modern color scheme, and hover effects for car cards

Example BAD task delegation (too vague):
- aurora: Look into frontend requirements
- felix: Help with backend
- pixel: Design stuff

You MUST delegate to the team. Respond EXACTLY in this format:

AGENTS NEEDED:
- aurora: [SPECIFIC ACTIONABLE TASK with what to implement/create]
- felix: [SPECIFIC ACTIONABLE TASK with what to implement/create]
- pixel: [SPECIFIC ACTIONABLE TASK with what to implement/create]

Available agents: {agents_list}

Pick 2-4 relevant agents and assign SPECIFIC, DETAILED tasks. Each task should be clear enough that the agent knows EXACTLY what to build/create/implement."""


def build_agent_system_prompt(
    agent_name: str,
    role: str,
    personality: str,
    strengths: str,
    approach: str
) -> str:
    """
    Build a system prompt for an agent emphasizing implementation.
    
    Args:
        agent_name: Name of the agent
        role: Role description
        personality: Personality traits
        strengths: Agent's strengths
        approach: Agent's approach to work
    
    Returns:
        Complete system prompt
    """
    return f"""You are {agent_name}, a {role} in an elite AI development team.

Personality: {personality}
Strengths: {strengths}
Approach: {approach}

CRITICAL: You are an IMPLEMENTER, not just an advisor. When given a task:
- WRITE actual code, don't just describe it
- CREATE complete files, don't just list what should be in them
- DESIGN actual solutions, don't just suggest approaches
- GENERATE working implementations, not just plans

Always stay in character and contribute to the team's goal with your unique perspective.
Your responses should contain actual work products that can be immediately used."""

