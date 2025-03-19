#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base Agent Model for FitDev.io
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import uuid
import logging
import os
import json
from pathlib import Path

# Import utilities from separate modules (will be available when called from main app)
try:
    from fitdev.utils.llm_integration import llm_manager
    from fitdev.utils.browser import browser
    from fitdev.models.reinforcement import (
        ParameterLearningSystem,
        PromptEngineeringSystem,
        TaskStrategySystem
    )
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False
    

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all FitDev.io agents."""
    
    def __init__(self, name: str, role: str, description: str):
        """Initialize a base agent.
        
        Args:
            name: Agent name
            role: Agent role category
            description: Detailed description of agent's responsibilities
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.description = description
        self.skills: List[str] = []
        self.performance_metrics: Dict[str, float] = {}
        self.compensation: float = 0.0
        self.memory: Dict[str, Any] = {}
        self.llm_enabled = os.getenv("ENABLE_LLM", "").lower() in ("true", "1", "yes")
        self.browser_enabled = os.getenv("ENABLE_BROWSER", "").lower() in ("true", "1", "yes")
        self.learning_enabled = os.getenv("ENABLE_LEARNING", "").lower() in ("true", "1", "yes")
        
        # Initialize reinforcement learning systems if enabled
        if self.learning_enabled and UTILS_AVAILABLE:
            self._initialize_learning_systems()
            self._load_learning_data()
        else:
            self.parameter_learning = None
            self.prompt_engineering = None
            self.task_strategy = None
        
    @abstractmethod
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task assigned to this agent.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results and metadata
        """
        pass
    
    @abstractmethod
    def evaluate_performance(self) -> float:
        """Evaluate agent's performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        pass
    
    def calculate_compensation(self, base_rate: float) -> float:
        """Calculate agent's compensation based on performance.
        
        Args:
            base_rate: Base compensation rate for this agent's role
            
        Returns:
            Final compensation amount
        """
        performance_score = self.evaluate_performance()
        self.compensation = base_rate * performance_score
        
        # Update learning systems with new compensation data if enabled
        if self.learning_enabled and UTILS_AVAILABLE:
            self._update_learning_systems(self.compensation)
            
        return self.compensation
    
    def add_skill(self, skill: str) -> None:
        """Add a skill to the agent's skillset.
        
        Args:
            skill: Skill description
        """
        if skill not in self.skills:
            self.skills.append(skill)
    
    def update_metric(self, metric_name: str, value: float) -> None:
        """Update a performance metric for this agent.
        
        Args:
            metric_name: Name of the metric
            value: New value for the metric
        """
        self.performance_metrics[metric_name] = value
    
    def get_memory(self, key: str, default: Any = None) -> Any:
        """Get a value from agent's memory.
        
        Args:
            key: Memory key
            default: Default value if key doesn't exist
            
        Returns:
            Value from memory or default
        """
        return self.memory.get(key, default)
    
    def set_memory(self, key: str, value: Any) -> None:
        """Store a value in agent's memory.
        
        Args:
            key: Memory key
            value: Value to store
        """
        self.memory[key] = value
    
    def search_web(self, query: str) -> Dict[str, Any]:
        """Search the web for information.
        
        Args:
            query: Search query
            
        Returns:
            Search results
        """
        if not self.browser_enabled or not UTILS_AVAILABLE:
            logger.warning(f"Browser capabilities not enabled for {self.name}")
            return {"status": "error", "error": "Browser capabilities not enabled"}
            
        try:
            return browser.search(query)
        except Exception as e:
            logger.error(f"Error during web search: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def browse_url(self, url: str) -> Dict[str, Any]:
        """Browse a specific URL.
        
        Args:
            url: URL to browse
            
        Returns:
            Content from the URL
        """
        if not self.browser_enabled or not UTILS_AVAILABLE:
            logger.warning(f"Browser capabilities not enabled for {self.name}")
            return {"status": "error", "error": "Browser capabilities not enabled"}
            
        try:
            return browser.fetch_url(url)
        except Exception as e:
            logger.error(f"Error browsing URL: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def research_topic(self, topic: str, max_pages: int = 3) -> Dict[str, Any]:
        """Research a topic by searching and following relevant links.
        
        Args:
            topic: Topic to research
            max_pages: Maximum number of pages to fetch
            
        Returns:
            Research results
        """
        if not self.browser_enabled or not UTILS_AVAILABLE:
            logger.warning(f"Browser capabilities not enabled for {self.name}")
            return {"status": "error", "error": "Browser capabilities not enabled"}
            
        try:
            return browser.research_topic(topic, max_pages)
        except Exception as e:
            logger.error(f"Error researching topic: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def get_llm_response(self, prompt: str, system_message: str = None) -> str:
        """Get a response from the LLM.
        
        Args:
            prompt: Prompt to send to the LLM
            system_message: Optional system message
            
        Returns:
            LLM response
        """
        if not self.llm_enabled or not UTILS_AVAILABLE:
            logger.warning(f"LLM capabilities not enabled for {self.name}")
            return "LLM capabilities not enabled"
            
        try:
            return llm_manager.generate_text(
                prompt=prompt,
                system_message=system_message,
                max_tokens=1000,
                temperature=0.7
            )
        except Exception as e:
            logger.error(f"Error getting LLM response: {str(e)}")
            return f"Error getting response: {str(e)}"
    
    def execute_task_with_llm(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using LLM capabilities.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results generated by the LLM
        """
        if not self.llm_enabled or not UTILS_AVAILABLE:
            logger.warning(f"LLM capabilities not enabled for {self.name}")
            return {
                "status": "completed",
                "agent": self.name,
                "error": "LLM capabilities not enabled, using placeholder implementation"
            }
            
        try:
            # Prepare the prompt with task details
            task_description = task.get("description", task.get("title", "Unknown task"))
            task_type = task.get("type", "")
            
            # Get LLM response
            llm_response = llm_manager.generate_agent_response(
                agent_role=self.role,
                agent_name=self.name,
                task_description=task_description,
                task_context={
                    "task_type": task_type,
                    "agent_skills": self.skills,
                    "task_details": task
                }
            )
            
            # Try to parse the response as JSON
            try:
                result = json.loads(llm_response)
                if isinstance(result, dict):
                    result["agent"] = self.name
                    result["status"] = "completed"
                    return result
            except json.JSONDecodeError:
                # If not valid JSON, return the raw response
                pass
                
            # Return the raw response if JSON parsing fails
            return {
                "status": "completed",
                "agent": self.name,
                "result": llm_response
            }
            
        except Exception as e:
            logger.error(f"Error executing task with LLM: {str(e)}")
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e)
            }
        
    def _initialize_learning_systems(self) -> None:
        """Initialize the reinforcement learning systems."""
        self.parameter_learning = ParameterLearningSystem(self.id, self.role)
        self.prompt_engineering = PromptEngineeringSystem(self.id, self.role)
        self.task_strategy = TaskStrategySystem(self.id, self.role)
        
        # Track the last used strategy and prompt for updating later
        self.last_used = {
            "task_type": "",
            "strategy": "",
            "prompt_template": ""
        }
    
    def _load_learning_data(self) -> None:
        """Load learning data from files if available."""
        data_dir = os.getenv("LEARNING_DATA_DIR", "data/learning")
        
        # Create directory if it doesn't exist
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        
        # Try to load parameter learning data
        param_file = f"{data_dir}/{self.id}_{self.role}_parameters.json"
        if os.path.exists(param_file):
            try:
                self.parameter_learning = ParameterLearningSystem.load_from_file(param_file)
                logger.info(f"Loaded parameter learning data for {self.name}")
            except Exception as e:
                logger.error(f"Failed to load parameter learning data: {e}")
        
        # Try to load prompt engineering data
        prompt_file = f"{data_dir}/{self.id}_{self.role}_prompts.json"
        if os.path.exists(prompt_file):
            try:
                self.prompt_engineering = PromptEngineeringSystem.load_from_file(prompt_file)
                logger.info(f"Loaded prompt engineering data for {self.name}")
            except Exception as e:
                logger.error(f"Failed to load prompt engineering data: {e}")
        
        # Try to load task strategy data
        strategy_file = f"{data_dir}/{self.id}_{self.role}_strategies.json"
        if os.path.exists(strategy_file):
            try:
                self.task_strategy = TaskStrategySystem.load_from_file(strategy_file)
                logger.info(f"Loaded task strategy data for {self.name}")
            except Exception as e:
                logger.error(f"Failed to load task strategy data: {e}")
    
    def _update_learning_systems(self, compensation: float) -> None:
        """Update learning systems with new compensation data.
        
        Args:
            compensation: Compensation received
        """
        task_type = self.last_used.get("task_type", "")
        if not task_type:
            return
            
        # Update parameter learning system
        if self.parameter_learning:
            self.parameter_learning.update_from_compensation(compensation, task_type)
            
            # Save updated data
            try:
                self.parameter_learning.save_to_file()
            except Exception as e:
                logger.error(f"Failed to save parameter learning data: {e}")
        
        # Update prompt engineering system
        if self.prompt_engineering and self.last_used.get("prompt_template"):
            self.prompt_engineering.record_result(
                task_type, 
                self.last_used["prompt_template"],
                compensation
            )
            
            # Save updated data
            try:
                self.prompt_engineering.save_to_file()
            except Exception as e:
                logger.error(f"Failed to save prompt engineering data: {e}")
        
        # Update task strategy system
        if self.task_strategy and self.last_used.get("strategy"):
            self.task_strategy.record_result(
                task_type, 
                self.last_used["strategy"],
                compensation
            )
            
            # Save updated data
            try:
                self.task_strategy.save_to_file()
            except Exception as e:
                logger.error(f"Failed to save task strategy data: {e}")
                
        logger.debug(f"Updated learning systems for {self.name} with compensation: {compensation}")
    
    def get_task_execution_strategy(self, task_type: str) -> Dict[str, Any]:
        """Get the best strategy for executing a task.
        
        Args:
            task_type: Type of task
            
        Returns:
            Task execution strategy
        """
        if not self.learning_enabled or not self.task_strategy:
            # Default strategy if learning not enabled
            return {
                "name": "Standard Approach",
                "description": "Default implementation strategy",
                "steps": ["analyze", "implement", "test"]
            }
            
        # Get strategy from learning system
        strategy = self.task_strategy.get_strategy(task_type)
        
        # Record for later update
        self.last_used["task_type"] = task_type
        self.last_used["strategy"] = strategy["name"]
        
        return strategy
    
    def get_optimized_prompt(self, task_type: str, context: Dict[str, Any]) -> str:
        """Get an optimized prompt for LLM interaction.
        
        Args:
            task_type: Type of task
            context: Context variables for the prompt
            
        Returns:
            Optimized prompt
        """
        if not self.learning_enabled or not self.prompt_engineering:
            # Default prompt if learning not enabled
            return f"Complete this {task_type} task: {context.get('task_description', '')}"
            
        # Get prompt from learning system
        prompt = self.prompt_engineering.get_prompt(task_type, context)
        
        # Record for later update
        self.last_used["task_type"] = task_type
        self.last_used["prompt_template"] = prompt
        
        return prompt
    
    def get_parameter(self, name: str) -> float:
        """Get the current value of a learning parameter.
        
        Args:
            name: Parameter name
            
        Returns:
            Current parameter value (0.0 to 1.0)
        """
        if not self.learning_enabled or not self.parameter_learning:
            return 0.5  # Default middle value
            
        return self.parameter_learning.get_parameter(name)
    
    def save_learning_data(self) -> None:
        """Save all learning data to files."""
        if not self.learning_enabled:
            return
            
        if self.parameter_learning:
            try:
                self.parameter_learning.save_to_file()
            except Exception as e:
                logger.error(f"Failed to save parameter learning data: {e}")
                
        if self.prompt_engineering:
            try:
                self.prompt_engineering.save_to_file()
            except Exception as e:
                logger.error(f"Failed to save prompt engineering data: {e}")
                
        if self.task_strategy:
            try:
                self.task_strategy.save_to_file()
            except Exception as e:
                logger.error(f"Failed to save task strategy data: {e}")
    
    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.name} ({self.role})"
