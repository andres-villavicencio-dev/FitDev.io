#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Browser Capabilities for FitDev.io

This module provides utilities for agents to gather information from the web.
"""

import os
import logging
import requests
from typing import Dict, Any, List, Optional, Union
from urllib.parse import urlparse
import json
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class WebBrowser:
    """A browser utility for agents to gather information from the web."""
    
    def __init__(self, user_agent: str = None):
        """Initialize the web browser.
        
        Args:
            user_agent: User agent string to use for requests
        """
        self.user_agent = user_agent or "FitDev.io Agent Browser/1.0"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})
        
    def fetch_url(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Fetch content from a URL.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary containing status, content, and metadata
        """
        try:
            # Validate URL to prevent security issues
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                return {
                    "status": "error",
                    "error": "Invalid URL format",
                    "url": url
                }
            
            # Make the request
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            # Get content type from headers
            content_type = response.headers.get('Content-Type', '').lower()
            
            # Process based on content type
            if 'text/html' in content_type:
                # Parse HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract title
                title = soup.title.string if soup.title else ""
                
                # Extract main text content
                main_content = ""
                for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
                    text = tag.get_text(strip=True)
                    if text:
                        main_content += text + "\n\n"
                
                return {
                    "status": "success",
                    "url": url,
                    "title": title,
                    "content_type": "html",
                    "content": main_content,
                    "raw_html": response.text,
                    "status_code": response.status_code
                }
                
            elif 'application/json' in content_type:
                # Return JSON content
                return {
                    "status": "success",
                    "url": url,
                    "content_type": "json",
                    "content": response.json(),
                    "status_code": response.status_code
                }
                
            else:
                # Return raw text for other content types
                return {
                    "status": "success",
                    "url": url,
                    "content_type": "text",
                    "content": response.text,
                    "status_code": response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            return {
                "status": "error",
                "url": url,
                "error": str(e)
            }
    
    def search(self, query: str, search_engine: str = "duckduckgo") -> Dict[str, Any]:
        """Perform a web search using a search engine.
        
        Args:
            query: Search query
            search_engine: Search engine to use ("duckduckgo", "google", etc.)
            
        Returns:
            Dictionary containing search results
            
        Note:
            This is a simplified implementation. Real implementation would
            require proper API keys and more sophisticated parsing.
        """
        # Placeholder implementation - would need to be replaced with actual API calls
        if search_engine == "duckduckgo":
            search_url = f"https://html.duckduckgo.com/html/?q={query}"
        else:
            return {
                "status": "error",
                "error": f"Search engine '{search_engine}' not implemented"
            }
        
        try:
            # Make the request
            response = self.session.get(search_url)
            response.raise_for_status()
            
            # Parse the results (very basic parsing, would need to be enhanced)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.select('.result'):
                title_elem = result.select_one('.result__title')
                link_elem = result.select_one('.result__url')
                snippet_elem = result.select_one('.result__snippet')
                
                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    url = link_elem.text.strip()
                    snippet = snippet_elem.text.strip() if snippet_elem else ""
                    
                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet
                    })
            
            return {
                "status": "success",
                "query": query,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error searching for '{query}': {str(e)}")
            return {
                "status": "error",
                "query": query,
                "error": str(e)
            }
    
    def research_topic(self, topic: str, max_pages: int = 3) -> Dict[str, Any]:
        """Research a topic by searching and following relevant links.
        
        Args:
            topic: Topic to research
            max_pages: Maximum number of pages to fetch
            
        Returns:
            Dictionary containing research results
        """
        # First, perform a search
        search_results = self.search(topic)
        
        if search_results["status"] != "success":
            return search_results
        
        # Extract top results
        top_results = search_results["results"][:max_pages]
        
        # Fetch each result
        detailed_results = []
        for result in top_results:
            url = result["url"]
            page_content = self.fetch_url(url)
            
            if page_content["status"] == "success":
                detailed_results.append({
                    "title": result["title"],
                    "url": url,
                    "content": page_content["content"]
                })
        
        # Compile research summary
        return {
            "status": "success",
            "topic": topic,
            "sources": detailed_results,
            "total_sources": len(detailed_results)
        }

# Global instance of the web browser
browser = WebBrowser()