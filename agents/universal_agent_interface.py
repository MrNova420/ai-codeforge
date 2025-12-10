#!/usr/bin/env python3
"""
Universal Agent Interface - Human-readable input for all agents
Makes ALL agents work like standard AI models (ChatGPT, Claude, etc.)

Simple usage:
    agent = UniversalAgent("felix")
    response = agent("Create a Python function to calculate fibonacci")
    print(response)
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import json


@dataclass
class AgentResponse:
    """Standardized agent response."""
    content: str  # Main response text
    agent_name: str  # Which agent responded
    success: bool = True
    metadata: Dict[str, Any] = None
    thinking: Optional[str] = None  # Chain of thought
    tool_calls: List[Dict] = None  # Any tools used
    
    def __str__(self) -> str:
        """Natural string representation."""
        return self.content


class UniversalAgent:
    """
    Universal agent interface that works like standard AI models.
    
    Makes every specialized agent accessible with simple human-readable input.
    No need to understand the internal structure - just talk naturally!
    
    Examples:
        # Architecture design
        agent = UniversalAgent("aurora")
        agent("Design a microservices architecture for an e-commerce platform")
        
        # Code generation
        agent = UniversalAgent("felix")
        agent("Create a REST API endpoint for user registration")
        
        # Testing
        agent = UniversalAgent("quinn")
        agent("Write pytest tests for the login function")
        
        # Research
        agent = UniversalAgent("researcher")
        agent("What are the best practices for API rate limiting?")
    """
    
    def __init__(
        self,
        agent_name: str,
        config: Optional[Dict] = None,
        vector_memory: Optional[Any] = None,
        tools: Optional[List] = None
    ):
        """
        Initialize universal agent interface.
        
        Args:
            agent_name: Name of agent (felix, aurora, quinn, etc.)
            config: Optional configuration
            vector_memory: Optional memory system
            tools: Optional tool access
        """
        self.agent_name = agent_name
        self.config = config or {}
        self.vector_memory = vector_memory
        self.tools = tools or []
        
        # Load agent profile
        self.profile = self._load_agent_profile(agent_name)
        
        # Initialize base LLM (would connect to actual LLM)
        self.llm = self._init_llm()
        
        # Conversation history
        self.history: List[Dict[str, str]] = []
    
    def __call__(self, prompt: str, **kwargs) -> AgentResponse:
        """
        Main interface - call agent with human-readable prompt.
        
        Args:
            prompt: Natural language prompt
            **kwargs: Additional options (temperature, max_tokens, etc.)
            
        Returns:
            AgentResponse with result
        """
        return self.chat(prompt, **kwargs)
    
    def chat(
        self,
        prompt: str,
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        system_override: Optional[str] = None
    ) -> AgentResponse:
        """
        Chat with agent using natural language.
        
        Args:
            prompt: Your message/question/task
            stream: Whether to stream response
            temperature: Creativity (0-1)
            max_tokens: Max response length
            system_override: Override agent personality
            
        Returns:
            Agent's response
        """
        # Build system prompt with agent personality
        system_prompt = system_override or self._build_system_prompt()
        
        # Add to history
        self.history.append({"role": "user", "content": prompt})
        
        # Check if memory/context should be added
        context = self._get_relevant_context(prompt)
        if context:
            prompt = f"{context}\n\nUser request: {prompt}"
        
        # Generate response
        response_text = self._generate_response(
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )
        
        # Add to history
        self.history.append({"role": "assistant", "content": response_text})
        
        # Store in memory if available
        if self.vector_memory:
            self._store_in_memory(prompt, response_text)
        
        return AgentResponse(
            content=response_text,
            agent_name=self.agent_name,
            success=True,
            metadata={
                'temperature': temperature,
                'tokens': len(response_text.split())
            }
        )
    
    def _load_agent_profile(self, agent_name: str) -> Dict[str, Any]:
        """Load agent personality and capabilities."""
        # Agent profiles with specialties
        profiles = {
            # Planners & Designers
            'aurora': {
                'role': 'System Architect',
                'specialty': 'High-level system design, architecture patterns, scalability',
                'personality': 'Strategic, visionary, thinks in systems',
                'capabilities': ['architecture_design', 'pattern_selection', 'tech_stack']
            },
            'felix': {
                'role': 'UI/UX Designer & Developer',
                'specialty': 'User interfaces, frontend development, user experience',
                'personality': 'Creative, user-focused, attention to detail',
                'capabilities': ['ui_design', 'frontend_code', 'ux_optimization']
            },
            'sage': {
                'role': 'Product Manager',
                'specialty': 'Requirements analysis, project planning, stakeholder communication',
                'personality': 'Organized, communicative, goal-oriented',
                'capabilities': ['requirements', 'planning', 'prioritization']
            },
            'ember': {
                'role': 'Creative Strategist',
                'specialty': 'Innovation, creative solutions, outside-the-box thinking',
                'personality': 'Bold, innovative, challenges conventions',
                'capabilities': ['brainstorming', 'innovation', 'creative_solutions']
            },
            
            # Critics & Judges
            'orion': {
                'role': 'Code Reviewer',
                'specialty': 'Code quality, best practices, maintainability',
                'personality': 'Critical, detail-oriented, high standards',
                'capabilities': ['code_review', 'quality_assessment', 'best_practices']
            },
            'atlas': {
                'role': 'Performance Analyst',
                'specialty': 'Optimization, performance tuning, efficiency',
                'personality': 'Data-driven, analytical, performance-focused',
                'capabilities': ['performance_analysis', 'optimization', 'profiling']
            },
            'mira': {
                'role': 'Security Expert',
                'specialty': 'Security vulnerabilities, threat modeling, secure coding',
                'personality': 'Vigilant, thorough, security-first mindset',
                'capabilities': ['security_audit', 'threat_analysis', 'secure_design']
            },
            'vex': {
                'role': 'Devil\'s Advocate',
                'specialty': 'Critical thinking, finding flaws, edge cases',
                'personality': 'Skeptical, questioning, plays devil\'s advocate',
                'capabilities': ['critique', 'edge_cases', 'risk_analysis']
            },
            
            # Developers
            'sol': {
                'role': 'Full-Stack Developer',
                'specialty': 'End-to-end development, backend + frontend',
                'personality': 'Versatile, pragmatic, gets things done',
                'capabilities': ['fullstack_dev', 'api_development', 'database_design']
            },
            'echo': {
                'role': 'Frontend Developer',
                'specialty': 'Modern web apps, React, Vue, responsive design',
                'personality': 'UI-focused, modern, loves frameworks',
                'capabilities': ['react', 'vue', 'css', 'responsive_design']
            },
            'nova': {
                'role': 'Backend Developer',
                'specialty': 'APIs, databases, server-side logic',
                'personality': 'Logic-focused, scalable, performance-oriented',
                'capabilities': ['api_dev', 'database', 'backend_logic']
            },
            'quinn': {
                'role': 'QA Engineer',
                'specialty': 'Testing, quality assurance, test automation',
                'personality': 'Thorough, systematic, quality-obsessed',
                'capabilities': ['test_generation', 'qa', 'automation']
            },
            'blaze': {
                'role': 'DevOps Engineer',
                'specialty': 'CI/CD, deployment, infrastructure',
                'personality': 'Automation-focused, reliability-oriented',
                'capabilities': ['devops', 'deployment', 'cicd']
            },
            'ivy': {
                'role': 'Data Engineer',
                'specialty': 'Data pipelines, ETL, data processing',
                'personality': 'Data-driven, pipeline-focused',
                'capabilities': ['data_pipeline', 'etl', 'data_processing']
            },
            'zephyr': {
                'role': 'ML Engineer',
                'specialty': 'Machine learning, AI models, data science',
                'personality': 'AI-focused, experimental, research-oriented',
                'capabilities': ['ml', 'ai_models', 'data_science']
            },
            
            # Assistants
            'pixel': {
                'role': 'Documentation Writer',
                'specialty': 'Clear documentation, technical writing',
                'personality': 'Clear, concise, user-friendly',
                'capabilities': ['documentation', 'technical_writing', 'guides']
            },
            'script': {
                'role': 'Automation Expert',
                'specialty': 'Scripts, automation, task automation',
                'personality': 'Efficiency-focused, automates everything',
                'capabilities': ['scripting', 'automation', 'cli_tools']
            },
            'turbo': {
                'role': 'Optimization Specialist',
                'specialty': 'Performance optimization, speed improvements',
                'personality': 'Speed-obsessed, optimization-focused',
                'capabilities': ['optimization', 'performance', 'profiling']
            },
            'sentinel': {
                'role': 'System Monitor',
                'specialty': 'Monitoring, alerts, system health',
                'personality': 'Vigilant, proactive, always watching',
                'capabilities': ['monitoring', 'alerts', 'health_checks']
            },
            
            # Specialists
            'helix': {
                'role': 'Team Coordinator',
                'specialty': 'Task delegation, team coordination, orchestration',
                'personality': 'Leader, coordinator, big-picture thinker',
                'capabilities': ['coordination', 'delegation', 'planning']
            },
            'patch': {
                'role': 'Debugger/Fixer',
                'specialty': 'Bug fixing, debugging, troubleshooting',
                'personality': 'Problem-solver, patient, systematic',
                'capabilities': ['debugging', 'bug_fixing', 'troubleshooting']
            },
            'pulse': {
                'role': 'Monitoring Expert',
                'specialty': 'System monitoring, metrics, observability',
                'personality': 'Data-driven, monitoring-focused',
                'capabilities': ['monitoring', 'metrics', 'observability']
            },
            'link': {
                'role': 'Integration Specialist',
                'specialty': 'System integration, API integration, connectors',
                'personality': 'Connection-focused, integration expert',
                'capabilities': ['integration', 'api_connectors', 'webhooks']
            },
            
            # Special
            'researcher': {
                'role': 'Research Agent',
                'specialty': 'Web research, knowledge synthesis, documentation',
                'personality': 'Curious, thorough, knowledge-seeker',
                'capabilities': ['web_research', 'synthesis', 'fact_finding']
            },
            'architect': {
                'role': 'System Architect',
                'specialty': 'System design, architecture planning',
                'personality': 'Strategic, high-level thinker',
                'capabilities': ['system_design', 'architecture', 'patterns']
            }
        }
        
        return profiles.get(agent_name.lower(), {
            'role': 'General AI Assistant',
            'specialty': 'General purpose assistance',
            'personality': 'Helpful, versatile, adaptive',
            'capabilities': ['general_assistance']
        })
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with agent personality."""
        profile = self.profile
        
        prompt = f"""You are {self.agent_name.capitalize()}, a {profile['role']}.

Your specialty: {profile['specialty']}

Your personality: {profile['personality']}

Your capabilities:
{chr(10).join(f'- {cap}' for cap in profile.get('capabilities', []))}

Always stay in character and provide responses that match your expertise and personality.
Be helpful, clear, and actionable in your responses.
"""
        return prompt
    
    def _get_relevant_context(self, prompt: str) -> Optional[str]:
        """Get relevant context from memory."""
        if not self.vector_memory:
            return None
        
        try:
            # Query similar past interactions
            memories = self.vector_memory.recall_memories(
                query=prompt,
                n_results=3
            )
            
            if memories:
                context = "Relevant past experience:\n"
                for mem in memories[:2]:
                    context += f"- {mem['content'][:100]}...\n"
                return context
        except:
            pass
        
        return None
    
    def _generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
        stream: bool
    ) -> str:
        """Generate response using LLM."""
        # This would call actual LLM (OpenAI, Gemini, Ollama)
        # For now, return formatted response
        
        # Build messages
        messages = [
            {"role": "system", "content": system_prompt},
            *self.history[-6:],  # Last 3 exchanges for context
            {"role": "user", "content": user_prompt}
        ]
        
        # Call LLM
        if self.llm:
            response = self.llm.generate(messages, temperature, max_tokens)
            return response
        
        # Fallback response
        return f"[{self.agent_name.capitalize()}]: I would help with: {user_prompt[:100]}..."
    
    def _init_llm(self):
        """Initialize LLM connection."""
        # Would initialize actual LLM here
        # Could be OpenAI, Gemini, Ollama, etc.
        return None
    
    def _store_in_memory(self, prompt: str, response: str):
        """Store interaction in memory."""
        try:
            self.vector_memory.store_memory(
                memory_type='task_summaries',
                content=f"Q: {prompt}\nA: {response}",
                metadata={
                    'agent': self.agent_name,
                    'type': 'chat_interaction'
                }
            )
        except:
            pass
    
    def clear_history(self):
        """Clear conversation history."""
        self.history.clear()
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return self.profile.get('capabilities', [])
    
    def __repr__(self) -> str:
        """String representation."""
        return f"UniversalAgent({self.agent_name} - {self.profile.get('role', 'AI Assistant')})"


# Convenience function for quick agent access
def ask_agent(agent_name: str, prompt: str, **kwargs) -> str:
    """
    Quick function to ask any agent a question.
    
    Usage:
        response = ask_agent("felix", "Create a login form in React")
        response = ask_agent("quinn", "Write tests for the API")
        response = ask_agent("aurora", "Design a scalable architecture")
    
    Args:
        agent_name: Name of agent
        prompt: Your question/task
        **kwargs: Additional options
        
    Returns:
        Agent's response as string
    """
    agent = UniversalAgent(agent_name)
    response = agent(prompt, **kwargs)
    return str(response)
