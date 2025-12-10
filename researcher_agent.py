#!/usr/bin/env python3
"""
Researcher Agent - Web research and knowledge synthesis
Implements the Researcher role from SCALING_TO_LARGE_PROJECTS.md

This agent can:
1. Search the web for information
2. Read and analyze documentation
3. Synthesize findings into actionable reports
4. Extract code examples from sources
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from tools.web_search import WebSearchTool, WebPageReaderTool
from tools.registry import get_registry


@dataclass
class ResearchReport:
    """Result of a research task."""
    query: str
    summary: str
    sources: List[Dict[str, str]]
    key_findings: List[str]
    code_examples: List[str]
    recommendations: List[str]
    

class ResearcherAgent:
    """
    Researcher Agent - The team's knowledge acquisition specialist.
    
    Workflow:
    1. Receives a research question
    2. Performs web searches
    3. Reads relevant pages
    4. Synthesizes information
    5. Returns actionable report
    """
    
    def __init__(self, llm_agent=None):
        """
        Initialize Researcher.
        
        Args:
            llm_agent: The base LLM agent for synthesis (e.g., from agent_chat_enhanced)
        """
        self.llm_agent = llm_agent
        self.web_search = WebSearchTool(max_results=5)
        self.page_reader = WebPageReaderTool()
        
        # Register tools
        registry = get_registry()
        if self.web_search.name not in registry.list_tools():
            registry.register_tool(self.web_search)
        if self.page_reader.name not in registry.list_tools():
            registry.register_tool(self.page_reader)
        
        # Grant tools to researcher
        registry.grant_tool_to_agent('researcher', self.web_search.name)
        registry.grant_tool_to_agent('researcher', self.page_reader.name)
    
    def research(self, question: str, depth: str = 'normal') -> ResearchReport:
        """
        Conduct research on a question.
        
        Args:
            question: The research question
            depth: 'quick' (1 search), 'normal' (search + read), 'deep' (multiple searches + analysis)
            
        Returns:
            ResearchReport with findings
        """
        print(f"🔍 Researching: {question}")
        
        # Step 1: Initial search
        search_result = self.web_search(query=question, max_results=5)
        
        if not search_result.success:
            return ResearchReport(
                query=question,
                summary=f"Research failed: {search_result.error}",
                sources=[],
                key_findings=[],
                code_examples=[],
                recommendations=[]
            )
        
        search_results = search_result.data
        print(f"   Found {len(search_results)} results")
        
        # Step 2: Read top pages (if depth allows)
        page_contents = []
        if depth in ['normal', 'deep'] and search_results:
            for i, result in enumerate(search_results[:3], 1):  # Read top 3
                print(f"   Reading page {i}/3...")
                url = result.get('url', '')
                if url:
                    page_result = self.page_reader(url=url, max_length=3000)
                    if page_result.success:
                        page_contents.append({
                            'url': url,
                            'title': result.get('title', ''),
                            'content': page_result.data
                        })
        
        # Step 3: Synthesize findings
        print("   Synthesizing findings...")
        report = self._synthesize_report(
            question,
            search_results,
            page_contents
        )
        
        return report
    
    def _synthesize_report(
        self,
        question: str,
        search_results: List[Dict],
        page_contents: List[Dict]
    ) -> ResearchReport:
        """
        Synthesize research findings into a report.
        
        If LLM agent is available, use it for synthesis.
        Otherwise, create a simple structured report.
        """
        sources = [
            {
                'title': r.get('title', ''),
                'url': r.get('url', ''),
                'snippet': r.get('snippet', '')
            }
            for r in search_results
        ]
        
        # Extract key findings from snippets
        key_findings = []
        for result in search_results:
            snippet = result.get('snippet', '')
            if snippet and len(snippet) > 50:
                # Take first meaningful sentence
                sentences = snippet.split('.')
                if sentences:
                    key_findings.append(sentences[0].strip() + '.')
        
        # Look for code in page contents
        code_examples = []
        for page in page_contents:
            content = page.get('content', '')
            # Simple code detection (look for common patterns)
            if any(pattern in content for pattern in ['def ', 'function ', 'class ', 'import ', 'const ']):
                # Extract code blocks (simple heuristic)
                lines = content.split('\n')
                in_code = False
                code_block = []
                for line in lines:
                    if any(line.strip().startswith(kw) for kw in ['def ', 'function', 'class ', 'import']):
                        in_code = True
                    if in_code:
                        code_block.append(line)
                        if len(code_block) > 15:  # Limit block size
                            break
                if code_block:
                    code_examples.append('\n'.join(code_block))
        
        # Generate recommendations
        recommendations = []
        if search_results:
            recommendations.append(f"Review documentation at: {search_results[0].get('url', '')}")
        if code_examples:
            recommendations.append("Code examples found - adapt for your use case")
        if page_contents:
            recommendations.append(f"Further reading available from {len(page_contents)} sources")
        
        # Create summary
        summary = f"Research completed for: '{question}'\n\n"
        summary += f"Found {len(search_results)} relevant sources.\n"
        if key_findings:
            summary += f"\nKey Findings:\n"
            for i, finding in enumerate(key_findings[:3], 1):
                summary += f"{i}. {finding}\n"
        
        return ResearchReport(
            query=question,
            summary=summary,
            sources=sources,
            key_findings=key_findings[:5],
            code_examples=code_examples[:2],
            recommendations=recommendations
        )
    
    def quick_answer(self, question: str) -> str:
        """
        Quick research for a simple answer.
        
        Returns just a summary string, not full report.
        """
        report = self.research(question, depth='quick')
        return report.summary
    
    def format_report_markdown(self, report: ResearchReport) -> str:
        """Format research report as markdown."""
        md = f"# Research Report: {report.query}\n\n"
        
        md += "## Summary\n"
        md += f"{report.summary}\n\n"
        
        if report.key_findings:
            md += "## Key Findings\n"
            for i, finding in enumerate(report.key_findings, 1):
                md += f"{i}. {finding}\n"
            md += "\n"
        
        if report.sources:
            md += "## Sources\n"
            for source in report.sources:
                md += f"- [{source['title']}]({source['url']})\n"
            md += "\n"
        
        if report.code_examples:
            md += "## Code Examples\n"
            for i, code in enumerate(report.code_examples, 1):
                md += f"### Example {i}\n```\n{code}\n```\n\n"
        
        if report.recommendations:
            md += "## Recommendations\n"
            for rec in report.recommendations:
                md += f"- {rec}\n"
        
        return md
