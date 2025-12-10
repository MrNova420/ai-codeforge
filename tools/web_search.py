#!/usr/bin/env python3
"""
Web Search Tool - Enables agents to search the internet
Implements the Researcher capabilities from SCALING_TO_LARGE_PROJECTS.md
"""

import requests
from typing import Dict, Any, List
from .base_tool import BaseTool, ToolResult


class WebSearchTool(BaseTool):
    """
    Web search using DuckDuckGo (no API key required).
    
    Alternative: Can be swapped for Google Custom Search, Bing, etc.
    """
    
    def __init__(self, max_results: int = 5):
        super().__init__()
        self.max_results = max_results
        self.base_url = "https://api.duckduckgo.com/"
    
    @property
    def name(self) -> str:
        return "web_search"
    
    @property
    def description(self) -> str:
        return "Search the web for information. Returns titles, snippets, and URLs."
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    
    def execute(self, query: str, max_results: int = None) -> ToolResult:
        """
        Execute web search.
        
        Args:
            query: Search query string
            max_results: Maximum results (defaults to self.max_results)
            
        Returns:
            ToolResult with list of search results
        """
        if max_results is None:
            max_results = self.max_results
        
        try:
            # DuckDuckGo Instant Answer API
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extract results
            results = []
            
            # Get related topics
            for topic in data.get('RelatedTopics', [])[:max_results]:
                if 'Text' in topic and 'FirstURL' in topic:
                    results.append({
                        'title': topic.get('Text', '')[:100] + '...',
                        'snippet': topic.get('Text', ''),
                        'url': topic.get('FirstURL', '')
                    })
            
            # If no results, try abstract
            if not results and data.get('Abstract'):
                results.append({
                    'title': data.get('Heading', ''),
                    'snippet': data.get('Abstract', ''),
                    'url': data.get('AbstractURL', '')
                })
            
            return ToolResult(
                success=True,
                data=results,
                metadata={
                    'query': query,
                    'result_count': len(results),
                    'source': 'DuckDuckGo'
                }
            )
            
        except (requests.Timeout, requests.ConnectionError) as e:
            # Network issue - provide helpful fallback
            return ToolResult(
                success=False,
                data=[],
                error=f"Network unavailable. Search for '{query}' manually or check internet connection.",
                metadata={'query': query, 'offline': True}
            )
        except requests.RequestException as e:
            return ToolResult(
                success=False,
                data=[],
                error=f"Search failed: {str(e)}",
                metadata={'query': query}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                data=[],
                error=f"Unexpected error: {str(e)}",
                metadata={'query': query}
            )


class WebPageReaderTool(BaseTool):
    """
    Read and extract content from a web page.
    Uses beautifulsoup4 for HTML parsing.
    """
    
    @property
    def name(self) -> str:
        return "read_webpage"
    
    @property
    def description(self) -> str:
        return "Read and extract text content from a web page URL."
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to read"
                },
                "max_length": {
                    "type": "integer",
                    "description": "Maximum characters to return",
                    "default": 5000
                }
            },
            "required": ["url"]
        }
    
    def execute(self, url: str, max_length: int = 5000) -> ToolResult:
        """
        Read a webpage and extract text.
        
        Args:
            url: Web page URL
            max_length: Maximum characters to return
            
        Returns:
            ToolResult with extracted text
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            return ToolResult(
                success=False,
                data=None,
                error="beautifulsoup4 not installed. Run: pip install beautifulsoup4"
            )
        
        try:
            # Fetch page
            headers = {
                'User-Agent': 'Mozilla/5.0 (AI Dev Team Research Bot)'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Truncate if needed
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return ToolResult(
                success=True,
                data=text,
                metadata={
                    'url': url,
                    'length': len(text),
                    'title': soup.title.string if soup.title else 'No title'
                }
            )
            
        except requests.RequestException as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Failed to fetch page: {str(e)}"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Error parsing page: {str(e)}"
            )
