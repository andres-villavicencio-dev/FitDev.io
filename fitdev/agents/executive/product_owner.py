#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Product Owner Agent for FitDev.io
"""

from typing import Dict, Any, List
from fitdev.models.agent import BaseAgent


class ProductOwnerAgent(BaseAgent):
    """Product Owner agent responsible for defining requirements and maximizing value."""
    
    def __init__(self, name: str = "Product Owner"):
        """Initialize the Product Owner agent.
        
        Args:
            name: Agent name (default: "Product Owner")
        """
        description = """Defines product requirements, maintains the backlog, and ensures 
                        that development work delivers maximum value to users. Translates 
                        business needs into technical requirements."""
        super().__init__(name, "executive", description)
        
        # Add Product Owner-specific skills
        self.add_skill("Requirement Analysis")
        self.add_skill("User Story Creation")
        self.add_skill("Backlog Management")
        self.add_skill("Value Assessment")
        
        # Product Owner-specific performance metrics
        self.update_metric("requirement_clarity", 0.0)
        self.update_metric("backlog_health", 0.0)
        self.update_metric("value_delivery", 0.0)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task assigned to this agent.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results and metadata
        """
        # Task execution logic for the Product Owner agent
        task_type = task.get("type", "")
        results = {"status": "completed", "agent": self.name}
        
        if task_type == "requirement_gathering":
            # Logic for requirement gathering tasks
            results["requirements"] = self._gather_requirements(task)
            
        elif task_type == "backlog_prioritization":
            # Logic for backlog prioritization tasks
            results["backlog"] = self._prioritize_backlog(task)
            
        elif task_type == "user_story_creation":
            # Logic for user story creation tasks
            results["user_stories"] = self._create_user_stories(task)
        
        # Update metrics based on task execution
        self._update_metrics_from_task(task)
        
        return results
    
    def evaluate_performance(self) -> float:
        """Evaluate Product Owner agent's performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        # Weight factors for different metrics
        weights = {
            "requirement_clarity": 0.35,
            "backlog_health": 0.3,
            "value_delivery": 0.35
        }
        
        # Calculate weighted performance score
        score = 0.0
        for metric, weight in weights.items():
            if metric in self.performance_metrics:
                # Normalize metric value to 0.0-1.0 range if needed
                metric_value = min(1.0, max(0.0, self.performance_metrics[metric]))
                score += metric_value * weight
        
        return score
    
    def _gather_requirements(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Gather product requirements from stakeholders.
        
        Args:
            task: Task containing requirement gathering parameters
            
        Returns:
            Gathered requirements
        """
        stakeholders = task.get("stakeholders", [])
        domain = task.get("domain", "")
        
        # Simple requirement gathering (placeholder implementation)
        requirements = []
        
        # TODO: Implement more sophisticated requirement gathering logic
        
        return {
            "functional_requirements": requirements,
            "non_functional_requirements": [],
            "stakeholder_coverage": len(stakeholders)
        }
    
    def _prioritize_backlog(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Prioritize product backlog items.
        
        Args:
            task: Task containing backlog prioritization parameters
            
        Returns:
            Prioritized backlog
        """
        backlog_items = task.get("backlog_items", [])
        criteria = task.get("criteria", {})
        
        # Simple backlog prioritization (placeholder implementation)
        prioritized_items = []
        
        # TODO: Implement more sophisticated prioritization logic
        
        return {
            "prioritized_items": prioritized_items,
            "rationale": "Prioritized based on value and effort"
        }
    
    def _create_user_stories(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create user stories from requirements.
        
        Args:
            task: Task containing user story creation parameters
            
        Returns:
            Created user stories
        """
        requirements = task.get("requirements", [])
        personas = task.get("personas", [])
        
        # Simple user story creation (placeholder implementation)
        user_stories = []
        
        # TODO: Implement more sophisticated user story creation logic
        
        return {
            "user_stories": user_stories,
            "acceptance_criteria": [],
            "coverage": 0.0
        }
    
    def _update_metrics_from_task(self, task: Dict[str, Any]) -> None:
        """Update agent's performance metrics based on task execution.
        
        Args:
            task: Completed task
        """
        task_type = task.get("type", "")
        
        if task_type == "requirement_gathering":
            # Update metrics related to requirement gathering
            current = self.performance_metrics.get("requirement_clarity", 0.0)
            self.update_metric("requirement_clarity", current + 0.1)
            
        elif task_type == "backlog_prioritization":
            # Update metrics related to backlog prioritization
            current = self.performance_metrics.get("backlog_health", 0.0)
            self.update_metric("backlog_health", current + 0.1)
            
        elif task_type == "user_story_creation":
            # Update metrics related to user story creation
            current = self.performance_metrics.get("value_delivery", 0.0)
            self.update_metric("value_delivery", current + 0.1)
