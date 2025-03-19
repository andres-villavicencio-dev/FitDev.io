#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base Agent Model for FitDev.io
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import uuid


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
        
    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.name} ({self.role})"
