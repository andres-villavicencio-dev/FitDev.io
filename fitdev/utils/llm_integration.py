#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LLM Integration Utilities for FitDev.io

This module provides utilities to connect FitDev.io agents with
Large Language Models for more intelligent task execution.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Union
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class LLMProvider:
    """Base class for LLM providers."""
    
    def __init__(self, model_name: str = None, api_key: str = None):
        """Initialize the LLM provider.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the provider
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")
        
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text from the LLM.
        
        Args:
            prompt: Text prompt to send to the LLM
            **kwargs: Additional arguments to pass to the LLM
            
        Returns:
            Generated text response
        """
        raise NotImplementedError("Subclasses must implement this method")


class OpenAIProvider(LLMProvider):
    """OpenAI API integration."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key: str = None):
        """Initialize the OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model to use
            api_key: OpenAI API key
        """
        super().__init__(model_name, api_key or os.getenv("OPENAI_API_KEY", ""))
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
    def generate_text(self, prompt: str, 
                     system_message: str = None,
                     max_tokens: int = 500,
                     temperature: float = 0.7) -> str:
        """Generate text using OpenAI's Chat API.
        
        Args:
            prompt: Text prompt to send to the LLM
            system_message: System message to set context
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If the API call fails
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
            
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return f"Error generating response: {str(e)}"


class OllamaProvider(LLMProvider):
    """Ollama local LLM integration."""
    
    def __init__(self, model_name: str = "gemma3", api_base: str = None):
        """Initialize the Ollama provider.
        
        Args:
            model_name: Name of the Ollama model to use (supported: gemma3, mistral-small)
            api_base: Base URL for the Ollama API
        """
        # Validate model name is one of the supported models
        if model_name not in ["gemma3", "mistral-small"]:
            logger.warning(f"Model {model_name} is not in the supported list (gemma3, mistral-small). Using gemma3 as default.")
            model_name = "gemma3"
            
        super().__init__(model_name)
        self.api_base = api_base or os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
        self.api_url = f"{self.api_base}/api/generate"
        
    def generate_text(self, prompt: str, 
                     system_message: str = None,
                     max_tokens: int = 500,
                     temperature: float = 0.7) -> str:
        """Generate text using Ollama's API.
        
        Args:
            prompt: Text prompt to send to the LLM
            system_message: System message to set context
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If the API call fails
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        # Combine system message and prompt if provided
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"
        
        data = {
            "model": self.model_name,
            "prompt": full_prompt,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "No response generated")
            
        except Exception as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            return f"Error generating response: {str(e)}"


class LLMManager:
    """Manager for interacting with different LLM providers."""
    
    def __init__(self, default_provider: str = "openai"):
        """Initialize the LLM manager.
        
        Args:
            default_provider: Default LLM provider to use
        """
        self.default_provider = default_provider
        self.providers = {}
        
        # Initialize default providers from environment variables
        if os.getenv("OPENAI_API_KEY"):
            self.providers["openai"] = OpenAIProvider()
            
        # Initialize Ollama if it's set to be used
        if default_provider == "ollama" or os.getenv("USE_OLLAMA", "").lower() in ("true", "1", "yes"):
            self.providers["ollama"] = OllamaProvider()
    
    def add_provider(self, name: str, provider: LLMProvider) -> None:
        """Add a new LLM provider.
        
        Args:
            name: Provider name
            provider: LLM provider instance
        """
        self.providers[name] = provider
    
    def get_provider(self, name: str = None) -> Optional[LLMProvider]:
        """Get a provider by name.
        
        Args:
            name: Provider name (uses default_provider if None)
            
        Returns:
            LLM provider instance or None if not found
        """
        name = name or self.default_provider
        return self.providers.get(name)
    
    def generate_text(self, prompt: str, provider_name: str = None, **kwargs) -> str:
        """Generate text using the specified provider.
        
        Args:
            prompt: Text prompt to send to the LLM
            provider_name: Name of the provider to use (uses default if None)
            **kwargs: Additional arguments to pass to the provider
            
        Returns:
            Generated text response
            
        Raises:
            ValueError: If the specified provider doesn't exist
        """
        provider = self.get_provider(provider_name)
        
        if not provider:
            available = ", ".join(self.providers.keys())
            raise ValueError(
                f"Provider '{provider_name or self.default_provider}' not found. "
                f"Available providers: {available}"
            )
        
        return provider.generate_text(prompt, **kwargs)
    
    def generate_agent_response(self, 
                              agent_role: str, 
                              agent_name: str,
                              task_description: str,
                              task_context: Dict[str, Any] = None,
                              provider_name: str = None) -> str:
        """Generate a response for an agent's task execution.
        
        Args:
            agent_role: Role of the agent (e.g., "Frontend Developer")
            agent_name: Name of the agent
            task_description: Description of the task
            task_context: Additional context for the task
            provider_name: Name of the provider to use
            
        Returns:
            Generated response with the agent's work output
        """
        system_message = f"""You are {agent_name}, a {agent_role} in a software development organization. 
Your task is to produce high-quality work based on the given requirements. 
Provide detailed, professional output as if you were a real software developer."""
        
        context_str = ""
        if task_context:
            context_str = "Additional context:\n" + json.dumps(task_context, indent=2)
        
        prompt = f"""Task: {task_description}

{context_str}

Please complete this task with high-quality, detailed output. 
Include any relevant code, documentation, or explanations in your response.
Structure your response as a JSON object with appropriate fields for the work output."""
        
        return self.generate_text(
            prompt=prompt,
            provider_name=provider_name,
            system_message=system_message,
            max_tokens=1000,
            temperature=0.7
        )

# Import config
from fitdev.config.config import load_config

# Load config
config = load_config()
llm_config = config.get("llm", {})
agents_config = config.get("agents", {})
ollama_config = agents_config.get("ollama", {})

# Global instance of the LLM manager
llm_manager = LLMManager(default_provider=os.getenv("DEFAULT_LLM_PROVIDER", llm_config.get("default_provider", "ollama")))

# If using Ollama, initialize with the configured default model
if "ollama" in llm_manager.providers:
    default_ollama_model = os.getenv("OLLAMA_MODEL", ollama_config.get("default_model", "gemma3"))
    llm_manager.providers["ollama"] = OllamaProvider(model_name=default_ollama_model)