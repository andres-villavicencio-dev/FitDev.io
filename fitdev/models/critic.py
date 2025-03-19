#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base Critic Agent Model for FitDev.io
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import uuid


class BaseCritic(ABC):
    """Base class for all FitDev.io critic agents."""
    
    def __init__(self, name: str, target_role: str, description: str):
        """Initialize a base critic agent.
        
        Args:
            name: Critic agent name
            target_role: The role this critic evaluates
            description: Detailed description of critic's responsibilities
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.target_role = target_role
        self.description = description
        self.evaluation_criteria: List[str] = []
        self.evaluations_performed: int = 0
        self.performance_metrics: Dict[str, float] = {}
        
    @abstractmethod
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from a target agent.
        
        Args:
            work_output: Work output and metadata from the target agent
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        pass
    
    def evaluate_performance(self) -> float:
        """Evaluate critic agent's own performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        # Default implementation - can be overridden by specific critics
        if not self.performance_metrics:
            return 0.5  # Default middle score if no metrics
            
        # Average of all metrics
        total = sum(self.performance_metrics.values())
        count = len(self.performance_metrics)
        
        return min(1.0, max(0.0, total / count if count > 0 else 0.5))
    
    def add_evaluation_criterion(self, criterion: str) -> None:
        """Add an evaluation criterion.
        
        Args:
            criterion: Description of the evaluation criterion
        """
        if criterion not in self.evaluation_criteria:
            self.evaluation_criteria.append(criterion)
    
    def update_metric(self, metric_name: str, value: float) -> None:
        """Update a performance metric for this critic.
        
        Args:
            metric_name: Name of the metric
            value: New value for the metric (should be between 0.0 and 1.0)
        """
        self.performance_metrics[metric_name] = min(1.0, max(0.0, value))
    
    def get_evaluation_report(self, score: float, feedback: List[str], 
                             suggestions: List[str]) -> Dict[str, Any]:
        """Generate a standardized evaluation report.
        
        Args:
            score: Overall evaluation score (0.0 to 1.0)
            feedback: List of feedback points
            suggestions: List of improvement suggestions
            
        Returns:
            Structured evaluation report
        """
        self.evaluations_performed += 1
        
        return {
            "critic": self.name,
            "target_role": self.target_role,
            "evaluation_id": str(uuid.uuid4()),
            "timestamp": "",  # Can be filled with actual timestamp if needed
            "score": score,
            "feedback": feedback,
            "suggestions": suggestions,
            "criteria_used": self.evaluation_criteria,
        }
        
    def __repr__(self) -> str:
        """String representation of the critic agent."""
        return f"{self.name} (Critic for {self.target_role})"