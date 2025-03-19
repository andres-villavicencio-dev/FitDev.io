#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reinforcement Learning System for FitDev.io

This module provides mechanisms for agents to learn from compensation feedback,
improving their performance over time through reinforcement learning.
"""

from typing import Dict, List, Any, Optional, Tuple, Callable
import random
import math
import json
import logging
import numpy as np
from pathlib import Path
import os

logger = logging.getLogger(__name__)


class ParameterLearningSystem:
    """Parameter-based learning system that uses compensation as feedback."""
    
    def __init__(self, agent_id: str, role: str, learning_rate: float = 0.05):
        """Initialize the parameter learning system.
        
        Args:
            agent_id: ID of the agent
            role: Role of the agent
            learning_rate: Rate at which parameters are updated (0.0 to 1.0)
        """
        self.agent_id = agent_id
        self.role = role
        self.learning_rate = learning_rate
        self.parameters: Dict[str, float] = {}
        self.parameter_history: List[Dict[str, Any]] = []
        
        # Initialize default parameters based on role
        self._initialize_parameters()
    
    def _initialize_parameters(self) -> None:
        """Initialize default parameters based on agent role."""
        # Common parameters for all agents
        self.parameters["thoroughness"] = 0.5  # How detailed the work should be
        self.parameters["creativity"] = 0.5    # How creative vs. conventional
        self.parameters["risk_taking"] = 0.5   # Willingness to try new approaches
        
        # Role-specific parameters
        if "frontend" in self.role.lower():
            self.parameters["design_focus"] = 0.5  # UI/UX focus vs. pure functionality
            self.parameters["accessibility_focus"] = 0.5  # Emphasis on accessibility
        
        elif "backend" in self.role.lower():
            self.parameters["performance_focus"] = 0.5  # Optimization vs. readability
            self.parameters["security_focus"] = 0.5  # Security emphasis
            self.parameters["code_reusability"] = 0.5  # Reusability vs. specialized efficiency
        
        elif "qa" in self.role.lower():
            self.parameters["test_coverage"] = 0.5  # Breadth vs. depth of testing
            self.parameters["edge_case_focus"] = 0.5  # Emphasis on edge cases
        
        # Save initial parameters to history
        self._record_parameters(0.0)  # Initial compensation of 0
    
    def get_parameter(self, name: str) -> float:
        """Get the current value of a parameter.
        
        Args:
            name: Parameter name
            
        Returns:
            Current parameter value
        """
        return self.parameters.get(name, 0.5)  # Default to 0.5 if not found
    
    def set_parameter(self, name: str, value: float) -> None:
        """Manually set a parameter value.
        
        Args:
            name: Parameter name
            value: New parameter value (0.0 to 1.0)
        """
        self.parameters[name] = max(0.0, min(1.0, value))
    
    def _record_parameters(self, compensation: float) -> None:
        """Record current parameters and associated compensation.
        
        Args:
            compensation: Compensation received for this parameter set
        """
        self.parameter_history.append({
            "parameters": self.parameters.copy(),
            "compensation": compensation,
            "timestamp": None  # Could add a timestamp here
        })
    
    def update_from_compensation(self, compensation: float, task_type: str) -> None:
        """Update parameters based on compensation received.
        
        Args:
            compensation: Compensation received
            task_type: Type of task that was completed
        """
        # Record current parameters with compensation
        self._record_parameters(compensation)
        
        # Only adjust if we have enough history
        if len(self.parameter_history) < 2:
            return
        
        # Get previous parameters and compensation
        prev_record = self.parameter_history[-2]
        prev_params = prev_record["parameters"]
        prev_comp = prev_record["compensation"]
        
        # Determine if compensation improved
        improved = compensation > prev_comp
        
        # Learn rate adjustment based on improvement
        adjust_rate = self.learning_rate if improved else -self.learning_rate * 0.5
        
        # Update each parameter
        for param_name in self.parameters:
            # Skip parameters not relevant to this task type
            if not self._is_parameter_relevant(param_name, task_type):
                continue
                
            # Random exploration with probability decreasing over time
            if random.random() < 0.1 * (1.0 / math.sqrt(len(self.parameter_history))):
                # Explore: make a random adjustment
                self.parameters[param_name] += random.uniform(-0.1, 0.1)
            else:
                # Exploit: adjust in the direction that improved compensation
                current_value = self.parameters[param_name]
                prev_value = prev_params.get(param_name, current_value)
                
                # Calculate parameter delta
                param_delta = current_value - prev_value
                
                # Adjust parameter in the same direction if improved, otherwise reverse
                adjustment = adjust_rate * (1.0 if param_delta * adjust_rate > 0 else -1.0)
                self.parameters[param_name] += adjustment
            
            # Ensure parameter stays within bounds
            self.parameters[param_name] = max(0.0, min(1.0, self.parameters[param_name]))
        
        logger.debug(f"Updated parameters for {self.role} based on compensation: {compensation}")
    
    def _is_parameter_relevant(self, param_name: str, task_type: str) -> bool:
        """Determine if a parameter is relevant to a task type.
        
        Args:
            param_name: Name of the parameter
            task_type: Type of task
            
        Returns:
            True if the parameter is relevant to the task type
        """
        # Map task types to relevant parameters
        relevance_map = {
            # Frontend-specific task types
            "component_implementation": [
                "thoroughness", "creativity", "design_focus", "accessibility_focus"
            ],
            "styling": [
                "creativity", "design_focus", "accessibility_focus"
            ],
            "frontend_integration": [
                "thoroughness", "creativity", "accessibility_focus"
            ],
            
            # Backend-specific task types
            "api_development": [
                "thoroughness", "performance_focus", "security_focus", "code_reusability"
            ],
            "database_implementation": [
                "performance_focus", "thoroughness", "security_focus"
            ],
            "service_implementation": [
                "code_reusability", "thoroughness", "security_focus"
            ],
            
            # QA-specific task types
            "testing": [
                "thoroughness", "test_coverage", "edge_case_focus"
            ],
            
            # Add more mappings as needed
        }
        
        # Common parameters relevant to all tasks
        if param_name in ["thoroughness", "risk_taking"]:
            return True
        
        # Check if parameter is in the relevance map for this task
        return param_name in relevance_map.get(task_type, [])
    
    def get_optimal_parameters(self) -> Dict[str, float]:
        """Get the parameter set that produced the highest compensation.
        
        Returns:
            Dictionary of optimal parameters
        """
        if not self.parameter_history:
            return self.parameters.copy()
            
        # Find the record with the highest compensation
        best_record = max(self.parameter_history, key=lambda x: x["compensation"])
        return best_record["parameters"].copy()
    
    def save_to_file(self, directory: str = "data/learning") -> None:
        """Save learning data to a file.
        
        Args:
            directory: Directory to save the file to
        """
        # Create directory if it doesn't exist
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create a filename based on agent ID and role
        filename = f"{directory}/{self.agent_id}_{self.role}_parameters.json"
        
        # Save data to file
        with open(filename, 'w') as f:
            json.dump({
                "agent_id": self.agent_id,
                "role": self.role,
                "learning_rate": self.learning_rate,
                "parameters": self.parameters,
                "history": self.parameter_history
            }, f, indent=2, default=str)  # default=str handles datetime serialization
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'ParameterLearningSystem':
        """Load learning data from a file.
        
        Args:
            filename: Path to the file to load
            
        Returns:
            Initialized ParameterLearningSystem
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Create a new instance
        instance = cls(data["agent_id"], data["role"], data["learning_rate"])
        
        # Load parameters and history
        instance.parameters = data["parameters"]
        instance.parameter_history = data["history"]
        
        return instance


class PromptEngineeringSystem:
    """System that learns optimal prompting strategies for LLM interactions."""
    
    def __init__(self, agent_id: str, role: str):
        """Initialize the prompt engineering system.
        
        Args:
            agent_id: ID of the agent
            role: Role of the agent
        """
        self.agent_id = agent_id
        self.role = role
        self.prompt_templates: Dict[str, List[str]] = {}
        self.prompt_results: Dict[str, List[Dict[str, Any]]] = {}
        
        # Initialize default prompt templates
        self._initialize_prompt_templates()
    
    def _initialize_prompt_templates(self) -> None:
        """Initialize default prompt templates based on agent role."""
        # Common templates for all agents
        self.prompt_templates["general"] = [
            "Complete the following task: {task_description}",
            "As a {role}, your task is to: {task_description}",
            "You are a {role} working on: {task_description}. Provide a detailed solution."
        ]
        
        # Role-specific templates
        if "frontend" in self.role.lower():
            self.prompt_templates["component_implementation"] = [
                "Create a {framework} component for: {task_description}. Include code and explanations.",
                "Implement a responsive {framework} UI component that: {task_description}. Focus on best practices and clean code.",
                "Design a user-friendly {framework} interface that: {task_description}. Consider accessibility and performance."
            ]
        
        elif "backend" in self.role.lower():
            self.prompt_templates["api_development"] = [
                "Develop a RESTful API endpoint that: {task_description}. Include security considerations.",
                "Create a backend service for: {task_description}. Focus on performance and scalability.",
                "Implement server-side logic for: {task_description}. Ensure proper error handling and validation.",
                "Design and implement a {api_type} API for: {task_description}. Focus on best practices, security, and thorough documentation."
            ]
            
            self.prompt_templates["database_implementation"] = [
                "Design a {db_type} database schema for: {task_description}. Ensure proper normalization and indexing.",
                "Develop an optimized database structure for: {task_description}. Focus on query performance and data integrity.",
                "Create a scalable database design for: {task_description}. Include considerations for future growth and data relationships."
            ]
            
            self.prompt_templates["service_implementation"] = [
                "Implement a service layer component for: {task_description}. Ensure proper separation of concerns.",
                "Develop a {service_type} architecture for: {task_description}. Focus on maintainability and testability.",
                "Create a robust service implementation for: {task_description}. Include error handling, logging, and dependency management."
            ]
        
        # Add more role-specific templates as needed
    
    def get_prompt(self, task_type: str, context: Dict[str, Any]) -> str:
        """Get the best prompt for a given task type and context.
        
        Args:
            task_type: Type of task
            context: Context variables to fill in the prompt template
            
        Returns:
            Generated prompt
        """
        # Get templates for this task type, or fall back to general templates
        templates = self.prompt_templates.get(task_type, self.prompt_templates.get("general", []))
        
        if not templates:
            # Default template if none available
            return f"Complete this {task_type} task: {context.get('task_description', '')}"
        
        # Choose the best template based on previous results
        chosen_template = self._select_best_template(task_type, templates)
        
        # Fill in the template with context variables
        try:
            prompt = chosen_template.format(**context)
        except KeyError as e:
            # Fall back to basic prompt if template contains unavailable variables
            logger.warning(f"Template contains unavailable variable: {e}")
            prompt = f"Complete this {task_type} task: {context.get('task_description', '')}"
        
        return prompt
    
    def _select_best_template(self, task_type: str, templates: List[str]) -> str:
        """Select the best template based on previous results.
        
        Args:
            task_type: Type of task
            templates: List of available templates
            
        Returns:
            Selected template
        """
        # If no results for this task type, use epsilon-greedy strategy
        if task_type not in self.prompt_results or random.random() < 0.2:
            return random.choice(templates)
        
        # Calculate average compensation for each template
        template_scores = {}
        for result in self.prompt_results[task_type]:
            template = result["template"]
            compensation = result["compensation"]
            
            if template not in template_scores:
                template_scores[template] = []
            
            template_scores[template].append(compensation)
        
        # Calculate average score for each template
        template_averages = {
            template: sum(scores) / len(scores) 
            for template, scores in template_scores.items()
        }
        
        # Find the template with the highest average score
        best_template = max(
            [t for t in templates if t in template_averages],
            key=lambda t: template_averages.get(t, 0),
            default=random.choice(templates)
        )
        
        return best_template
    
    def add_template(self, task_type: str, template: str) -> None:
        """Add a new prompt template.
        
        Args:
            task_type: Type of task
            template: Prompt template
        """
        if task_type not in self.prompt_templates:
            self.prompt_templates[task_type] = []
        
        if template not in self.prompt_templates[task_type]:
            self.prompt_templates[task_type].append(template)
    
    def record_result(self, task_type: str, template: str, compensation: float) -> None:
        """Record the result of using a prompt template.
        
        Args:
            task_type: Type of task
            template: Prompt template used
            compensation: Compensation received
        """
        if task_type not in self.prompt_results:
            self.prompt_results[task_type] = []
        
        self.prompt_results[task_type].append({
            "template": template,
            "compensation": compensation,
            "timestamp": None  # Could add a timestamp here
        })
    
    def save_to_file(self, directory: str = "data/learning") -> None:
        """Save learning data to a file.
        
        Args:
            directory: Directory to save the file to
        """
        # Create directory if it doesn't exist
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create a filename based on agent ID and role
        filename = f"{directory}/{self.agent_id}_{self.role}_prompts.json"
        
        # Save data to file
        with open(filename, 'w') as f:
            json.dump({
                "agent_id": self.agent_id,
                "role": self.role,
                "templates": self.prompt_templates,
                "results": self.prompt_results
            }, f, indent=2, default=str)  # default=str handles datetime serialization
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'PromptEngineeringSystem':
        """Load learning data from a file.
        
        Args:
            filename: Path to the file to load
            
        Returns:
            Initialized PromptEngineeringSystem
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Create a new instance
        instance = cls(data["agent_id"], data["role"])
        
        # Load templates and results
        instance.prompt_templates = data["templates"]
        instance.prompt_results = data["results"]
        
        return instance


class TaskStrategySystem:
    """System that learns which task execution strategies work best."""
    
    def __init__(self, agent_id: str, role: str):
        """Initialize the task strategy system.
        
        Args:
            agent_id: ID of the agent
            role: Role of the agent
        """
        self.agent_id = agent_id
        self.role = role
        self.strategies: Dict[str, List[Dict[str, Any]]] = {}
        self.strategy_results: Dict[str, List[Dict[str, Any]]] = {}
        
        # Multi-armed bandit parameters
        self.exploration_rate = 0.2  # Initial exploration rate
        self.min_exploration_rate = 0.05  # Minimum exploration rate
        self.decay_factor = 0.995  # Decay rate for exploration
        
        # Initialize default strategies
        self._initialize_strategies()
    
    def _initialize_strategies(self) -> None:
        """Initialize default strategies based on agent role."""
        # Common strategies for all agents
        self.strategies["general"] = [
            {
                "name": "Thorough Analysis",
                "description": "Spend extra time analyzing the requirements before implementation",
                "steps": ["analyze", "plan", "implement", "test", "document"]
            },
            {
                "name": "Rapid Implementation",
                "description": "Focus on quickly implementing a working solution",
                "steps": ["quick_plan", "implement", "basic_test"]
            },
            {
                "name": "Research-First",
                "description": "Research similar solutions before implementation",
                "steps": ["research", "analyze", "implement", "test"]
            }
        ]
        
        # Role-specific strategies
        if "frontend" in self.role.lower():
            self.strategies["component_implementation"] = [
                {
                    "name": "Design-First Approach",
                    "description": "Focus on design and UX before implementation",
                    "steps": ["design", "prototype", "implement", "test", "refine"]
                },
                {
                    "name": "Component-Driven",
                    "description": "Break down into smaller components and implement incrementally",
                    "steps": ["decompose", "implement_components", "integrate", "test"]
                },
                {
                    "name": "Test-Driven Development",
                    "description": "Write tests first, then implement to pass tests",
                    "steps": ["write_tests", "implement", "refactor", "document"]
                }
            ]
        
        elif "backend" in self.role.lower():
            self.strategies["api_development"] = [
                {
                    "name": "Schema-First",
                    "description": "Define data schema and API contracts before implementation",
                    "steps": ["define_schema", "create_endpoints", "implement_logic", "add_validation", "test"]
                },
                {
                    "name": "Security-Focused",
                    "description": "Prioritize security measures throughout the development",
                    "steps": ["threat_model", "implement_with_security", "validate_security", "performance_test"]
                },
                {
                    "name": "Iterative API",
                    "description": "Implement basic endpoints first, then enhance incrementally",
                    "steps": ["basic_endpoints", "add_features", "optimize", "document"]
                }
            ]
            
            self.strategies["database_implementation"] = [
                {
                    "name": "Normalized Design",
                    "description": "Follow strict normalization principles for data integrity",
                    "steps": ["entity_analysis", "normalization", "relationship_mapping", "indexing", "validation"]
                },
                {
                    "name": "Performance-Optimized",
                    "description": "Focus on query performance with appropriate denormalization",
                    "steps": ["query_analysis", "schema_design", "denormalization", "indexing_strategy", "benchmark"]
                },
                {
                    "name": "Domain-Driven",
                    "description": "Design database based on domain model and aggregate boundaries",
                    "steps": ["domain_modeling", "aggregate_design", "schema_implementation", "access_patterns", "test"]
                }
            ]
            
            self.strategies["service_implementation"] = [
                {
                    "name": "Interface-First",
                    "description": "Define clear interfaces before implementation details",
                    "steps": ["interface_design", "contract_definition", "implementation", "dependency_injection", "test"]
                },
                {
                    "name": "Domain-Service Pattern",
                    "description": "Implement using domain service patterns with rich domain model",
                    "steps": ["domain_modeling", "service_design", "implementation", "integration", "validation"]
                },
                {
                    "name": "Layered Architecture",
                    "description": "Implement with clear separation of concerns in layers",
                    "steps": ["layer_definition", "interface_design", "implementation", "cross_layer_testing", "documentation"]
                }
            ]
        
        # Add more role-specific strategies as needed
    
    def get_strategy(self, task_type: str) -> Dict[str, Any]:
        """Get the best strategy for a given task type.
        
        Args:
            task_type: Type of task
            
        Returns:
            Selected strategy
        """
        # Get strategies for this task type, or fall back to general strategies
        strategies_list = self.strategies.get(task_type, self.strategies.get("general", []))
        
        if not strategies_list:
            # Default strategy if none available
            return {
                "name": "Basic Approach",
                "description": "Standard implementation approach",
                "steps": ["analyze", "implement", "test"]
            }
        
        # Choose strategy using multi-armed bandit algorithm
        return self._select_strategy(task_type, strategies_list)
    
    def _select_strategy(self, task_type: str, strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select a strategy using multi-armed bandit algorithm.
        
        Args:
            task_type: Type of task
            strategies: List of available strategies
            
        Returns:
            Selected strategy
        """
        # Explore: randomly select a strategy
        if random.random() < self.exploration_rate:
            strategy = random.choice(strategies)
            logger.debug(f"Exploring new strategy: {strategy['name']}")
            return strategy
        
        # Exploit: select best strategy based on historical data
        if task_type in self.strategy_results and self.strategy_results[task_type]:
            # Calculate average compensation for each strategy
            strategy_scores = {}
            for result in self.strategy_results[task_type]:
                strategy_name = result["strategy_name"]
                compensation = result["compensation"]
                
                if strategy_name not in strategy_scores:
                    strategy_scores[strategy_name] = []
                
                strategy_scores[strategy_name].append(compensation)
            
            # Calculate average score and confidence bounds (UCB1 algorithm)
            num_trials = len(self.strategy_results[task_type])
            ucb_scores = {}
            
            for strategy in strategies:
                name = strategy["name"]
                if name in strategy_scores:
                    # Calculate mean reward
                    mean_reward = sum(strategy_scores[name]) / len(strategy_scores[name])
                    # Calculate exploration bonus (UCB term)
                    exploration_bonus = math.sqrt(2 * math.log(num_trials) / len(strategy_scores[name]))
                    # UCB score combines exploitation (mean reward) and exploration (bonus)
                    ucb_scores[name] = mean_reward + exploration_bonus
                else:
                    # Unseen strategies get high priority
                    ucb_scores[name] = float('inf')
            
            # Select strategy with highest UCB score
            best_strategy_name = max(ucb_scores, key=ucb_scores.get)
            strategy = next((s for s in strategies if s["name"] == best_strategy_name), strategies[0])
            
            logger.debug(f"Selected best strategy: {strategy['name']} with UCB score: {ucb_scores[best_strategy_name]}")
            return strategy
        
        # If no history, select randomly
        return random.choice(strategies)
    
    def add_strategy(self, task_type: str, strategy: Dict[str, Any]) -> None:
        """Add a new strategy.
        
        Args:
            task_type: Type of task
            strategy: Strategy definition
        """
        if task_type not in self.strategies:
            self.strategies[task_type] = []
        
        # Check if strategy with same name already exists
        if not any(s["name"] == strategy["name"] for s in self.strategies[task_type]):
            self.strategies[task_type].append(strategy)
    
    def record_result(self, task_type: str, strategy_name: str, compensation: float) -> None:
        """Record the result of using a strategy.
        
        Args:
            task_type: Type of task
            strategy_name: Name of the strategy used
            compensation: Compensation received
        """
        if task_type not in self.strategy_results:
            self.strategy_results[task_type] = []
        
        self.strategy_results[task_type].append({
            "strategy_name": strategy_name,
            "compensation": compensation,
            "timestamp": None  # Could add a timestamp here
        })
        
        # Decay exploration rate
        self.exploration_rate = max(
            self.min_exploration_rate, 
            self.exploration_rate * self.decay_factor
        )
    
    def get_best_strategy(self, task_type: str) -> Optional[Dict[str, Any]]:
        """Get the strategy with the highest average compensation.
        
        Args:
            task_type: Type of task
            
        Returns:
            Best strategy or None if no data available
        """
        if task_type not in self.strategy_results or not self.strategy_results[task_type]:
            return None
        
        # Calculate average compensation for each strategy
        strategy_scores = {}
        for result in self.strategy_results[task_type]:
            strategy_name = result["strategy_name"]
            compensation = result["compensation"]
            
            if strategy_name not in strategy_scores:
                strategy_scores[strategy_name] = []
            
            strategy_scores[strategy_name].append(compensation)
        
        # Find strategy with highest average compensation
        if not strategy_scores:
            return None
            
        best_strategy_name = max(
            strategy_scores.keys(),
            key=lambda name: sum(strategy_scores[name]) / len(strategy_scores[name])
        )
        
        # Get strategy definition
        strategies = self.strategies.get(task_type, self.strategies.get("general", []))
        
        # If we don't have this strategy defined in our strategies list,
        # create a new one with the name and default values
        best_strategy = next(
            (s for s in strategies if s["name"] == best_strategy_name), 
            None
        )
        
        if best_strategy is None and best_strategy_name:
            # Create a default strategy with this name
            best_strategy = {
                "name": best_strategy_name,
                "description": f"Learned strategy for {task_type}",
                "steps": ["analyze", "implement", "test", "document"]
            }
        
        return best_strategy
    
    def save_to_file(self, directory: str = "data/learning") -> None:
        """Save learning data to a file.
        
        Args:
            directory: Directory to save the file to
        """
        # Create directory if it doesn't exist
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create a filename based on agent ID and role
        filename = f"{directory}/{self.agent_id}_{self.role}_strategies.json"
        
        # Save data to file
        with open(filename, 'w') as f:
            json.dump({
                "agent_id": self.agent_id,
                "role": self.role,
                "exploration_rate": self.exploration_rate,
                "strategies": self.strategies,
                "results": self.strategy_results
            }, f, indent=2, default=str)  # default=str handles datetime serialization
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'TaskStrategySystem':
        """Load learning data from a file.
        
        Args:
            filename: Path to the file to load
            
        Returns:
            Initialized TaskStrategySystem
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Create a new instance
        instance = cls(data["agent_id"], data["role"])
        
        # Load instance data
        instance.exploration_rate = data["exploration_rate"]
        instance.strategies = data["strategies"]
        instance.strategy_results = data["results"]
        
        return instance