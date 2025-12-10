#!/usr/bin/env python3
"""
Architect Agent - High-level system design and architecture
Part of SCALING_TO_LARGE_PROJECTS.md Phase 6

Specializes in:
- System architecture design
- Technology stack recommendations
- Design pattern suggestions
- Scalability planning
- Architecture diagrams
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ArchitecturePattern(Enum):
    """Common architecture patterns."""
    MONOLITH = "monolith"
    MICROSERVICES = "microservices"
    SERVERLESS = "serverless"
    EVENT_DRIVEN = "event_driven"
    LAYERED = "layered"
    MVC = "mvc"
    MVVM = "mvvm"
    CLEAN_ARCHITECTURE = "clean_architecture"
    HEXAGONAL = "hexagonal"


@dataclass
class SystemDesign:
    """System architecture design."""
    architecture_pattern: str
    components: List[Dict[str, Any]]
    data_flow: List[Dict[str, Any]]
    technology_stack: Dict[str, List[str]]
    scalability_notes: List[str]
    security_considerations: List[str]
    diagram_mermaid: Optional[str] = None


class ArchitectAgent:
    """
    Architect - High-level system design specialist.
    
    The Architect agent excels at:
    - Analyzing requirements and proposing system designs
    - Recommending appropriate architecture patterns
    - Suggesting technology stacks
    - Identifying potential bottlenecks
    - Planning for scalability and maintainability
    
    Philosophy: "Good architecture enables agility; bad architecture creates debt."
    """
    
    def __init__(self, llm_agent=None):
        """
        Initialize Architect agent.
        
        Args:
            llm_agent: Base LLM for generating designs
        """
        self.llm_agent = llm_agent
        self.design_patterns = self._load_patterns()
    
    def _load_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load common design patterns and their characteristics."""
        return {
            'microservices': {
                'pros': ['Scalable', 'Independent deployment', 'Technology diversity'],
                'cons': ['Complex orchestration', 'Network overhead', 'Data consistency challenges'],
                'use_when': ['Large teams', 'Need for independent scaling', 'Polyglot requirements']
            },
            'monolith': {
                'pros': ['Simple deployment', 'Easy development', 'Single codebase'],
                'cons': ['Scaling limitations', 'Technology lock-in', 'Large blast radius'],
                'use_when': ['Small team', 'Simple requirements', 'MVP/prototype']
            },
            'serverless': {
                'pros': ['Auto-scaling', 'Pay per use', 'No server management'],
                'cons': ['Cold starts', 'Vendor lock-in', 'Debugging challenges'],
                'use_when': ['Variable load', 'Event-driven', 'Cost optimization']
            },
            'event_driven': {
                'pros': ['Loose coupling', 'Asynchronous', 'Scalable'],
                'cons': ['Complex debugging', 'Eventual consistency', 'Event schema management'],
                'use_when': ['Decoupled systems', 'Real-time processing', 'Audit trails']
            }
        }
    
    def design_system(
        self,
        requirements: str,
        constraints: Optional[List[str]] = None,
        target_scale: str = "medium"
    ) -> SystemDesign:
        """
        Design a system architecture based on requirements.
        
        Args:
            requirements: System requirements description
            constraints: Optional constraints (budget, tech stack, timeline)
            target_scale: Expected scale (small, medium, large, enterprise)
            
        Returns:
            SystemDesign with architecture proposal
        """
        # Analyze requirements
        analysis = self._analyze_requirements(requirements)
        
        # Choose architecture pattern
        pattern = self._recommend_pattern(analysis, target_scale, constraints)
        
        # Design components
        components = self._design_components(requirements, pattern)
        
        # Design data flow
        data_flow = self._design_data_flow(components)
        
        # Recommend tech stack
        tech_stack = self._recommend_tech_stack(pattern, analysis)
        
        # Scalability considerations
        scalability = self._plan_scalability(pattern, target_scale)
        
        # Security considerations
        security = self._identify_security_concerns(requirements, components)
        
        # Generate diagram
        diagram = self._generate_mermaid_diagram(components, data_flow)
        
        return SystemDesign(
            architecture_pattern=pattern,
            components=components,
            data_flow=data_flow,
            technology_stack=tech_stack,
            scalability_notes=scalability,
            security_considerations=security,
            diagram_mermaid=diagram
        )
    
    def _analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze requirements to extract key characteristics."""
        req_lower = requirements.lower()
        
        analysis = {
            'has_api': any(kw in req_lower for kw in ['api', 'rest', 'graphql', 'endpoint']),
            'has_database': any(kw in req_lower for kw in ['database', 'data', 'store', 'persist']),
            'has_auth': any(kw in req_lower for kw in ['auth', 'login', 'user', 'authentication']),
            'has_realtime': any(kw in req_lower for kw in ['realtime', 'websocket', 'live', 'stream']),
            'has_batch': any(kw in req_lower for kw in ['batch', 'cron', 'scheduled', 'background']),
            'needs_scaling': any(kw in req_lower for kw in ['scale', 'million', 'high traffic', 'load']),
            'has_frontend': any(kw in req_lower for kw in ['frontend', 'ui', 'web app', 'mobile'])
        }
        
        return analysis
    
    def _recommend_pattern(
        self,
        analysis: Dict[str, Any],
        target_scale: str,
        constraints: Optional[List[str]]
    ) -> str:
        """Recommend architecture pattern based on analysis."""
        # Simple heuristics
        if target_scale == 'small' and not analysis['needs_scaling']:
            return 'monolith'
        
        if analysis['has_realtime'] and analysis['needs_scaling']:
            return 'event_driven'
        
        if target_scale == 'enterprise':
            return 'microservices'
        
        if constraints and any('serverless' in c.lower() for c in constraints):
            return 'serverless'
        
        return 'layered'  # Default
    
    def _design_components(self, requirements: str, pattern: str) -> List[Dict[str, Any]]:
        """Design system components."""
        components = []
        
        # API Gateway (if microservices or event-driven)
        if pattern in ['microservices', 'event_driven']:
            components.append({
                'name': 'API Gateway',
                'type': 'gateway',
                'responsibilities': ['Routing', 'Authentication', 'Rate limiting']
            })
        
        # Always need application layer
        components.append({
            'name': 'Application Service',
            'type': 'service',
            'responsibilities': ['Business logic', 'Request handling']
        })
        
        # Database
        components.append({
            'name': 'Database',
            'type': 'database',
            'responsibilities': ['Data persistence', 'CRUD operations']
        })
        
        # Cache (if scaling)
        if 'scale' in requirements.lower():
            components.append({
                'name': 'Cache Layer',
                'type': 'cache',
                'responsibilities': ['Performance optimization', 'Reduce DB load']
            })
        
        # Message Queue (if event-driven)
        if pattern == 'event_driven':
            components.append({
                'name': 'Message Queue',
                'type': 'queue',
                'responsibilities': ['Async processing', 'Event distribution']
            })
        
        return components
    
    def _design_data_flow(self, components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Design data flow between components."""
        flows = []
        
        # Client -> API Gateway -> Service
        if any(c['type'] == 'gateway' for c in components):
            flows.append({
                'from': 'Client',
                'to': 'API Gateway',
                'type': 'HTTP/HTTPS'
            })
            flows.append({
                'from': 'API Gateway',
                'to': 'Application Service',
                'type': 'Internal'
            })
        else:
            flows.append({
                'from': 'Client',
                'to': 'Application Service',
                'type': 'HTTP/HTTPS'
            })
        
        # Service -> Database
        flows.append({
            'from': 'Application Service',
            'to': 'Database',
            'type': 'SQL/NoSQL'
        })
        
        # Service -> Cache
        if any(c['type'] == 'cache' for c in components):
            flows.append({
                'from': 'Application Service',
                'to': 'Cache Layer',
                'type': 'Redis/Memcached'
            })
        
        # Service -> Queue
        if any(c['type'] == 'queue' for c in components):
            flows.append({
                'from': 'Application Service',
                'to': 'Message Queue',
                'type': 'Pub/Sub'
            })
        
        return flows
    
    def _recommend_tech_stack(self, pattern: str, analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """Recommend technology stack."""
        stack = {
            'backend': ['Python/FastAPI', 'Node.js/Express', 'Go'],
            'database': [],
            'cache': [],
            'frontend': [],
            'infrastructure': []
        }
        
        # Database recommendations
        if analysis['has_database']:
            stack['database'] = ['PostgreSQL', 'MongoDB', 'Redis']
        
        # Cache
        if analysis['needs_scaling']:
            stack['cache'] = ['Redis', 'Memcached']
        
        # Frontend
        if analysis['has_frontend']:
            stack['frontend'] = ['React', 'Vue.js', 'Next.js']
        
        # Infrastructure
        if pattern == 'microservices':
            stack['infrastructure'] = ['Docker', 'Kubernetes', 'API Gateway']
        elif pattern == 'serverless':
            stack['infrastructure'] = ['AWS Lambda', 'Azure Functions', 'API Gateway']
        else:
            stack['infrastructure'] = ['Docker', 'Nginx', 'PM2']
        
        return stack
    
    def _plan_scalability(self, pattern: str, target_scale: str) -> List[str]:
        """Plan for scalability."""
        notes = []
        
        if target_scale in ['large', 'enterprise']:
            notes.append("Implement horizontal scaling with load balancer")
            notes.append("Use database replication for read scaling")
            notes.append("Consider CDN for static assets")
            notes.append("Implement caching strategy at multiple layers")
        
        if pattern == 'microservices':
            notes.append("Each service can scale independently")
            notes.append("Use service mesh for inter-service communication")
        
        if pattern == 'event_driven':
            notes.append("Message queue provides natural backpressure")
            notes.append("Scale consumers based on queue depth")
        
        notes.append("Monitor performance metrics and set up auto-scaling")
        
        return notes
    
    def _identify_security_concerns(self, requirements: str, components: List[Dict]) -> List[str]:
        """Identify security considerations."""
        concerns = []
        
        concerns.append("Implement HTTPS/TLS for all external communication")
        concerns.append("Use authentication and authorization (JWT, OAuth2)")
        concerns.append("Validate and sanitize all user inputs")
        concerns.append("Implement rate limiting to prevent abuse")
        concerns.append("Regular security audits and dependency updates")
        
        if any('database' in c['type'] for c in components):
            concerns.append("Use parameterized queries to prevent SQL injection")
            concerns.append("Encrypt sensitive data at rest")
        
        return concerns
    
    def _generate_mermaid_diagram(self, components: List[Dict], data_flow: List[Dict]) -> str:
        """Generate Mermaid diagram of architecture."""
        lines = ["graph TD"]
        
        # Add components
        for i, comp in enumerate(components):
            node_id = f"C{i}"
            lines.append(f"    {node_id}[{comp['name']}]")
        
        # Add flows (simplified)
        for flow in data_flow:
            lines.append(f"    {flow['from']} --> {flow['to']}")
        
        return "\n".join(lines)
    
    def format_design_document(self, design: SystemDesign) -> str:
        """Format system design as markdown document."""
        doc = f"""# System Architecture Design

## Architecture Pattern
**{design.architecture_pattern.replace('_', ' ').title()}**

## Components

"""
        for comp in design.components:
            doc += f"### {comp['name']}\n"
            doc += f"**Type**: {comp['type']}\n\n"
            doc += "**Responsibilities:**\n"
            for resp in comp['responsibilities']:
                doc += f"- {resp}\n"
            doc += "\n"
        
        doc += "## Technology Stack\n\n"
        for category, techs in design.technology_stack.items():
            doc += f"**{category.title()}**: {', '.join(techs)}\n\n"
        
        doc += "## Scalability Considerations\n\n"
        for note in design.scalability_notes:
            doc += f"- {note}\n"
        
        doc += "\n## Security Considerations\n\n"
        for concern in design.security_considerations:
            doc += f"- {concern}\n"
        
        if design.diagram_mermaid:
            doc += f"\n## Architecture Diagram\n\n```mermaid\n{design.diagram_mermaid}\n```\n"
        
        return doc
