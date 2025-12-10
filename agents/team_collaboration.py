#!/usr/bin/env python3
"""
Advanced Team Collaboration - Agents working together autonomously
Agents can:
- Talk to each other directly
- Delegate tasks to teammates
- Request help and reviews
- Iterate and improve together
- Self-organize based on expertise
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from agents.universal_agent_interface import UniversalAgent
from messaging.message_bus import get_message_bus, Event


@dataclass
class AgentMessage:
    """Message between agents."""
    from_agent: str
    to_agent: str
    message_type: str  # request, response, feedback, help
    content: str
    context: Optional[Dict] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    message_id: str = field(default_factory=lambda: f"msg_{datetime.now().timestamp()}")


@dataclass
class TeamTask:
    """Task that can be worked on by multiple agents."""
    task_id: str
    description: str
    assigned_to: List[str]
    created_by: str
    status: str = "pending"  # pending, in_progress, review, complete
    result: Optional[Any] = None
    conversation: List[AgentMessage] = field(default_factory=list)
    iterations: int = 0
    max_iterations: int = 3


class AgentTeam:
    """
    Team of agents that work together autonomously.
    
    Agents can:
    - Send messages to each other
    - Delegate subtasks
    - Request reviews and feedback
    - Iterate based on peer feedback
    - Self-organize based on expertise
    
    Example:
        team = AgentTeam()
        
        # Add agents
        team.add_agent("felix", UniversalAgent("felix"))
        team.add_agent("quinn", UniversalAgent("quinn"))
        team.add_agent("orion", UniversalAgent("orion"))
        
        # Assign collaborative task
        result = await team.collaborative_task(
            "Create a login system with tests and code review"
        )
    """
    
    def __init__(self):
        """Initialize agent team."""
        self.agents: Dict[str, UniversalAgent] = {}
        self.message_bus = get_message_bus()
        self.active_tasks: Dict[str, TeamTask] = {}
        self.conversation_history: List[AgentMessage] = []
        
        # Agent capabilities mapping
        self.agent_expertise = {}
    
    def add_agent(self, name: str, agent: UniversalAgent) -> None:
        """
        Add agent to team.
        
        Args:
            name: Agent name
            agent: UniversalAgent instance
        """
        self.agents[name] = agent
        self.agent_expertise[name] = agent.get_capabilities()
        
        # Subscribe to messages for this agent
        self.message_bus.subscribe(
            f'agent.message.{name}',
            self._handle_agent_message
        )
    
    async def collaborative_task(
        self,
        task_description: str,
        required_roles: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute task with multiple agents collaborating.
        
        Workflow:
        1. Analyze task and select agents
        2. Primary agent starts work
        3. Agents communicate and delegate
        4. Review and iterate
        5. Final approval
        
        Args:
            task_description: Task to complete
            required_roles: Optional specific roles needed
            
        Returns:
            Task result with conversation history
        """
        print(f"🤝 Starting collaborative task: {task_description[:50]}...")
        
        # Step 1: Select agents for task
        selected_agents = self._select_agents_for_task(task_description, required_roles)
        print(f"   Selected team: {', '.join(selected_agents)}")
        
        # Step 2: Create team task
        task = TeamTask(
            task_id=f"task_{datetime.now().timestamp()}",
            description=task_description,
            assigned_to=selected_agents,
            created_by="orchestrator"
        )
        self.active_tasks[task.task_id] = task
        
        # Step 3: Primary agent starts
        primary_agent = selected_agents[0]
        print(f"   Primary agent: {primary_agent}")
        
        task.status = "in_progress"
        initial_result = await self._agent_work(primary_agent, task_description, task)
        
        # Step 4: Collaboration loop
        for iteration in range(task.max_iterations):
            print(f"   Iteration {iteration + 1}/{task.max_iterations}")
            
            # Get feedback from other team members
            feedback_needed = await self._check_if_feedback_needed(task, initial_result)
            
            if not feedback_needed:
                print("   ✓ No feedback needed - task looks good")
                break
            
            # Collect feedback
            feedback = await self._collect_team_feedback(task, initial_result, selected_agents[1:])
            
            # Apply improvements
            if feedback:
                print(f"   Applying feedback from {len(feedback)} agents...")
                initial_result = await self._apply_feedback(primary_agent, initial_result, feedback, task)
                task.iterations += 1
        
        # Step 5: Final result
        task.status = "complete"
        task.result = initial_result
        
        print("   ✅ Collaborative task complete!")
        
        return {
            'success': True,
            'result': initial_result,
            'team': selected_agents,
            'iterations': task.iterations,
            'conversation': [msg.__dict__ for msg in task.conversation]
        }
    
    def _select_agents_for_task(
        self,
        task: str,
        required_roles: Optional[List[str]] = None
    ) -> List[str]:
        """Select best agents for task based on expertise."""
        if required_roles:
            return required_roles
        
        # Analyze task keywords
        task_lower = task.lower()
        selected = []
        
        # Coding task
        if any(kw in task_lower for kw in ['code', 'implement', 'create', 'build', 'develop']):
            selected.append('felix')
        
        # Testing task
        if any(kw in task_lower for kw in ['test', 'qa', 'quality', 'verify']):
            selected.append('quinn')
        
        # Review/quality
        if any(kw in task_lower for kw in ['review', 'check', 'analyze', 'improve']):
            selected.append('orion')
        
        # Architecture/design
        if any(kw in task_lower for kw in ['design', 'architect', 'system', 'structure']):
            selected.append('aurora')
        
        # Security
        if any(kw in task_lower for kw in ['security', 'secure', 'vulnerability']):
            selected.append('mira')
        
        # Default: developer + tester + reviewer
        if not selected:
            selected = ['felix', 'quinn', 'orion']
        
        return selected[:3]  # Max 3 agents per task
    
    async def _agent_work(
        self,
        agent_name: str,
        task: str,
        team_task: TeamTask
    ) -> Any:
        """Agent does their work on the task."""
        agent = self.agents.get(agent_name)
        if not agent:
            return f"Agent {agent_name} not found"
        
        # Send message to team
        msg = AgentMessage(
            from_agent=agent_name,
            to_agent="team",
            message_type="status",
            content=f"Starting work on: {task[:50]}..."
        )
        team_task.conversation.append(msg)
        
        # Do the work
        result = agent(task)
        
        # Announce completion
        msg = AgentMessage(
            from_agent=agent_name,
            to_agent="team",
            message_type="response",
            content=f"Completed work. Result length: {len(str(result))} chars"
        )
        team_task.conversation.append(msg)
        
        return result
    
    async def _check_if_feedback_needed(
        self,
        task: TeamTask,
        result: Any
    ) -> bool:
        """Check if result needs peer feedback."""
        # Simple heuristic: always get feedback if not final iteration
        if task.iterations >= task.max_iterations - 1:
            return False
        
        # Check result quality
        result_str = str(result)
        if len(result_str) < 50:
            return True  # Too short, needs work
        
        # If error mentioned in result
        if any(kw in result_str.lower() for kw in ['error', 'failed', 'unable']):
            return True
        
        return task.iterations < 1  # At least one feedback round
    
    async def _collect_team_feedback(
        self,
        task: TeamTask,
        result: Any,
        feedback_agents: List[str]
    ) -> List[Dict[str, str]]:
        """Collect feedback from team members."""
        feedback_list = []
        
        for agent_name in feedback_agents:
            agent = self.agents.get(agent_name)
            if not agent:
                continue
            
            # Request feedback
            feedback_prompt = f"""Review this work and provide constructive feedback:

Task: {task.description}

Work completed:
{str(result)[:1000]}

Provide specific suggestions for improvement."""
            
            feedback_response = agent(feedback_prompt)
            
            # Record message
            msg = AgentMessage(
                from_agent=agent_name,
                to_agent=task.assigned_to[0],
                message_type="feedback",
                content=str(feedback_response)
            )
            task.conversation.append(msg)
            
            feedback_list.append({
                'agent': agent_name,
                'feedback': str(feedback_response)
            })
        
        return feedback_list
    
    async def _apply_feedback(
        self,
        agent_name: str,
        original_work: Any,
        feedback: List[Dict[str, str]],
        task: TeamTask
    ) -> Any:
        """Agent improves work based on feedback."""
        agent = self.agents.get(agent_name)
        if not agent:
            return original_work
        
        # Compile feedback
        feedback_summary = "\n\n".join([
            f"Feedback from {f['agent']}:\n{f['feedback']}"
            for f in feedback
        ])
        
        # Request improvement
        improve_prompt = f"""Improve your work based on team feedback:

Original work:
{str(original_work)[:1000]}

Team feedback:
{feedback_summary}

Provide improved version addressing the feedback."""
        
        improved = agent(improve_prompt)
        
        # Record improvement
        msg = AgentMessage(
            from_agent=agent_name,
            to_agent="team",
            message_type="response",
            content="Applied team feedback and improved work"
        )
        task.conversation.append(msg)
        
        return improved
    
    async def agent_to_agent_chat(
        self,
        from_agent: str,
        to_agent: str,
        message: str
    ) -> str:
        """Direct communication between two agents."""
        sender = self.agents.get(from_agent)
        receiver = self.agents.get(to_agent)
        
        if not sender or not receiver:
            return "Agent not found"
        
        # Record message
        msg = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type="request",
            content=message
        )
        self.conversation_history.append(msg)
        
        # Receiver processes message
        response = receiver(f"Message from {from_agent}: {message}")
        
        # Record response
        reply = AgentMessage(
            from_agent=to_agent,
            to_agent=from_agent,
            message_type="response",
            content=str(response)
        )
        self.conversation_history.append(reply)
        
        return str(response)
    
    async def delegate_task(
        self,
        from_agent: str,
        to_agent: str,
        task: str
    ) -> Any:
        """One agent delegates task to another."""
        print(f"📤 {from_agent} delegating to {to_agent}: {task[:50]}...")
        
        receiver = self.agents.get(to_agent)
        if not receiver:
            return f"Agent {to_agent} not available"
        
        # Record delegation
        msg = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type="request",
            content=f"Delegated task: {task}"
        )
        self.conversation_history.append(msg)
        
        # Execute delegated task
        result = receiver(task)
        
        # Record completion
        reply = AgentMessage(
            from_agent=to_agent,
            to_agent=from_agent,
            message_type="response",
            content=f"Task completed: {str(result)[:100]}..."
        )
        self.conversation_history.append(reply)
        
        print(f"   ✅ {to_agent} completed delegated task")
        
        return result
    
    def get_conversation_history(self, limit: int = 50) -> List[Dict]:
        """Get recent conversation history."""
        return [msg.__dict__ for msg in self.conversation_history[-limit:]]
    
    def get_team_stats(self) -> Dict[str, Any]:
        """Get team collaboration statistics."""
        return {
            'total_agents': len(self.agents),
            'active_tasks': len(self.active_tasks),
            'messages_exchanged': len(self.conversation_history),
            'agents': list(self.agents.keys())
        }
    
    async def _handle_agent_message(self, event: Event) -> None:
        """Handle incoming agent message from message bus."""
        # Process inter-agent messages
        pass
    
    def visualize_conversation(self, task_id: Optional[str] = None) -> str:
        """Visualize conversation between agents."""
        if task_id and task_id in self.active_tasks:
            messages = self.active_tasks[task_id].conversation
        else:
            messages = self.conversation_history[-20:]
        
        output = "Agent Conversation:\n" + "=" * 60 + "\n\n"
        
        for msg in messages:
            output += f"[{msg.timestamp}] {msg.from_agent} → {msg.to_agent}\n"
            output += f"Type: {msg.message_type}\n"
            output += f"Message: {msg.content[:100]}...\n"
            output += "-" * 60 + "\n"
        
        return output


# Global team instance
_global_team = None


def get_agent_team() -> AgentTeam:
    """Get global agent team (singleton)."""
    global _global_team
    if _global_team is None:
        _global_team = AgentTeam()
    return _global_team


async def team_work(task: str, agents: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Quick function for team collaboration.
    
    Usage:
        result = await team_work("Create authentication system with tests")
    """
    team = get_agent_team()
    return await team.collaborative_task(task, agents)
