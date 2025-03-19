#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for LLM and browser integration in FitDev.io
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from fitdev
from fitdev.utils.llm_integration import llm_manager, OpenAIProvider, OllamaProvider
from fitdev.utils.browser import browser
from fitdev.organization import Organization
from fitdev.models.task import Task
from fitdev.agents.development.frontend import FrontendDeveloperAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def test_llm_setup():
    """Test LLM setup by getting a simple response."""
    # Check if OpenAI API key is set
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        # Add OpenAI provider
        llm_manager.add_provider("openai", OpenAIProvider(model_name="gpt-3.5-turbo"))
        logger.info("Testing OpenAI provider...")
        
        # Generate a simple response
        response = llm_manager.generate_text(
            "What are the benefits of using React for frontend development?", 
            provider_name="openai"
        )
        
        logger.info(f"OpenAI response: {response[:100]}...")
    
    # Check for Ollama
    ollama_base = os.getenv("OLLAMA_API_BASE")
    if ollama_base or os.path.exists("/usr/local/bin/ollama") or os.path.exists("/usr/bin/ollama"):
        # Add Ollama provider
        llm_manager.add_provider("ollama", OllamaProvider(model_name="llama3:latest"))
        logger.info("Testing Ollama provider...")
        
        try:
            # Generate a simple response
            response = llm_manager.generate_text(
                "What are the benefits of using React for frontend development?", 
                provider_name="ollama"
            )
            
            logger.info(f"Ollama response: {response[:100]}...")
        except Exception as e:
            logger.error(f"Error with Ollama: {str(e)}")
    
    logger.info("Available LLM providers: " + ", ".join(llm_manager.providers.keys()))

def test_browser_capabilities():
    """Test browser capabilities."""
    logger.info("Testing browser capabilities...")
    
    # Test URL fetching
    url = "https://reactjs.org"
    logger.info(f"Fetching content from {url}...")
    
    try:
        result = browser.fetch_url(url)
        if result["status"] == "success":
            logger.info(f"Successfully fetched content. Title: {result.get('title', 'Unknown')}")
        else:
            logger.error(f"Error fetching URL: {result.get('error', 'Unknown error')}")
    except Exception as e:
        logger.error(f"Exception during URL fetch: {str(e)}")
    
    # Test search
    query = "React components best practices"
    logger.info(f"Searching for: {query}...")
    
    try:
        result = browser.search(query)
        if result["status"] == "success":
            logger.info(f"Found {len(result.get('results', []))} search results")
        else:
            logger.error(f"Error during search: {result.get('error', 'Unknown error')}")
    except Exception as e:
        logger.error(f"Exception during search: {str(e)}")

def test_frontend_developer_with_llm():
    """Test Frontend Developer agent with LLM capabilities."""
    logger.info("Testing Frontend Developer agent with LLM capabilities...")
    
    # Enable LLM
    os.environ["ENABLE_LLM"] = "true"
    os.environ["ENABLE_BROWSER"] = "true"
    
    # Create a frontend developer agent
    frontend_dev = FrontendDeveloperAgent()
    
    # Create a task
    task = {
        "id": "task-123",
        "title": "Create User Profile Component",
        "description": "Implement a responsive user profile component with avatar, user details, and edit functionality",
        "type": "component_implementation",
        "component_type": "profile",
        "framework": "React"
    }
    
    # Execute the task
    logger.info(f"Executing task: {task['title']}...")
    
    try:
        result = frontend_dev.execute_task(task)
        logger.info(f"Task execution result status: {result.get('status', 'unknown')}")
        
        # Check if component was generated
        if "component" in result:
            component = result["component"]
            code = component.get("code", "")
            logger.info(f"Generated component code length: {len(code)} characters")
            
            # Show a snippet of the code
            if code:
                logger.info(f"Code snippet: {code[:200]}...")
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting LLM and browser integration tests")
    
    # Test LLM setup
    test_llm_setup()
    
    # Test browser capabilities
    test_browser_capabilities()
    
    # Test Frontend Developer with LLM
    test_frontend_developer_with_llm()
    
    logger.info("LLM and browser integration tests completed")