#!/usr/bin/env python3
"""
Web Tools - HTTP requests, web scraping, API testing
Advanced web interaction tools for agents
"""

from typing import Dict, List, Optional, Any
from tools.base_tool import BaseTool, ToolResult
import requests


class HTTPRequestTool(BaseTool):
    """Make HTTP requests (GET, POST, PUT, DELETE)."""
    
    name = "http_request"
    description = "Make HTTP request to any URL"
    
    def __call__(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict] = None,
        data: Optional[Dict] = None,
        timeout: int = 30
    ) -> ToolResult:
        """Make HTTP request."""
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data if method.upper() in ['POST', 'PUT'] else None,
                params=data if method.upper() == 'GET' else None,
                timeout=timeout
            )
            
            # Try to parse JSON
            try:
                response_data = response.json()
            except Exception:
                # Not JSON, use text
                response_data = response.text
            
            return ToolResult(
                success=response.status_code < 400,
                data={
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'body': response_data,
                    'url': response.url
                },
                error=None if response.status_code < 400 else f"HTTP {response.status_code}"
            )
        except Exception as e:
            return ToolResult(success=False, data={}, error=str(e))


class WebScraperTool(BaseTool):
    """Scrape and extract data from web pages."""
    
    name = "web_scraper"
    description = "Extract data from web pages"
    
    def __call__(
        self,
        url: str,
        selector: Optional[str] = None,
        extract_type: str = "text"
    ) -> ToolResult:
        """Scrape web page."""
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            return ToolResult(
                success=False,
                data={},
                error="BeautifulSoup not installed. Run: pip install beautifulsoup4"
            )
        
        try:
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if selector:
                elements = soup.select(selector)
                if extract_type == "text":
                    data = [el.get_text(strip=True) for el in elements]
                elif extract_type == "html":
                    data = [str(el) for el in elements]
                elif extract_type == "attrs":
                    data = [dict(el.attrs) for el in elements]
                else:
                    data = elements
            else:
                # Extract all text
                data = soup.get_text(separator='\n', strip=True)
            
            return ToolResult(
                success=True,
                data={
                    'url': url,
                    'title': soup.title.string if soup.title else None,
                    'extracted': data
                }
            )
        except Exception as e:
            return ToolResult(success=False, data={}, error=str(e))


class APITesterTool(BaseTool):
    """Test REST APIs comprehensively."""
    
    name = "api_tester"
    description = "Test REST API endpoints"
    
    def __call__(
        self,
        base_url: str,
        endpoints: List[Dict[str, Any]],
        headers: Optional[Dict] = None
    ) -> ToolResult:
        """
        Test multiple API endpoints.
        
        Args:
            base_url: Base API URL
            endpoints: List of endpoint configs [{method, path, expected_status}]
            headers: Common headers
        """
        results = []
        
        for endpoint in endpoints:
            method = endpoint.get('method', 'GET')
            path = endpoint.get('path', '/')
            expected = endpoint.get('expected_status', 200)
            
            url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
            
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    timeout=10
                )
                
                passed = response.status_code == expected
                
                results.append({
                    'endpoint': f"{method} {path}",
                    'status_code': response.status_code,
                    'expected': expected,
                    'passed': passed,
                    'response_time': response.elapsed.total_seconds()
                })
            except Exception as e:
                results.append({
                    'endpoint': f"{method} {path}",
                    'passed': False,
                    'error': str(e)
                })
        
        total = len(results)
        passed = sum(1 for r in results if r.get('passed', False))
        
        return ToolResult(
            success=passed == total,
            data={
                'total_tests': total,
                'passed': passed,
                'failed': total - passed,
                'results': results
            }
        )
