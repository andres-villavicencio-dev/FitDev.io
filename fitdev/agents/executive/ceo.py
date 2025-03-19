#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CEO/Project Manager Agent for FitDev.io
"""

from typing import Dict, Any, List
from fitdev.models.agent import BaseAgent
from fitdev.models.task import Task, TaskStatus


class CEOAgent(BaseAgent):
    """CEO/Project Manager agent responsible for overall project direction and coordination."""
    
    def __init__(self, name: str = "CEO/Project Manager"):
        """Initialize the CEO agent.
        
        Args:
            name: Agent name (default: "CEO/Project Manager")
        """
        description = """Sets overall direction, prioritizes work, manages resources, 
                        and ensures alignment with organizational goals. Evaluates 
                        project success and makes strategic decisions."""
        super().__init__(name, "executive", description)
        
        # Add CEO-specific skills
        self.add_skill("Project Management")
        self.add_skill("Resource Allocation")
        self.add_skill("Strategic Planning")
        self.add_skill("Team Coordination")
        
        # CEO-specific performance metrics
        self.update_metric("projects_completed", 0.0)
        self.update_metric("team_productivity", 0.0)
        self.update_metric("strategic_alignment", 0.0)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task assigned to this agent.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results and metadata
        """
        # Task execution logic for the CEO agent
        task_type = task.get("type", "")
        results = {"status": "completed", "agent": self.name}
        
        if task_type == "project_planning":
            # Logic for project planning tasks
            results["plan"] = self._create_project_plan(task)
            
        elif task_type == "resource_allocation":
            # Logic for resource allocation tasks
            results["allocation"] = self._allocate_resources(task)
            
        elif task_type == "performance_review":
            # Logic for performance review tasks
            results["review"] = self._review_performance(task)
        
        # Update metrics based on task execution
        self._update_metrics_from_task(task)
        
        return results
    
    def evaluate_performance(self) -> float:
        """Evaluate CEO agent's performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        # Weight factors for different metrics
        weights = {
            "projects_completed": 0.3,
            "team_productivity": 0.4,
            "strategic_alignment": 0.3
        }
        
        # Calculate weighted performance score
        score = 0.0
        for metric, weight in weights.items():
            if metric in self.performance_metrics:
                # Normalize metric value to 0.0-1.0 range if needed
                metric_value = min(1.0, max(0.0, self.performance_metrics[metric]))
                score += metric_value * weight
        
        return score
    
    def _create_project_plan(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a project plan based on requirements.
        
        Args:
            task: Task containing project requirements
            
        Returns:
            Project plan details
        """
        requirements = task.get("requirements", [])
        timeline = task.get("timeline", 30)  # Default 30 days
        
        # Create a simple project plan (placeholder implementation)
        phases = [
            {"name": "Requirements Analysis", "duration": timeline * 0.2},
            {"name": "Design", "duration": timeline * 0.3},
            {"name": "Implementation", "duration": timeline * 0.3},
            {"name": "Testing", "duration": timeline * 0.15},
            {"name": "Deployment", "duration": timeline * 0.05}
        ]
        
        # TODO: Implement more sophisticated planning logic
        
        return {
            "phases": phases,
            "total_duration": timeline,
            "requirements_addressed": len(requirements)
        }
    
    def _allocate_resources(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Allocate resources to project components.
        
        Args:
            task: Task containing resource allocation requirements
            
        Returns:
            Resource allocation details
        """
        components = task.get("components", [])
        available_agents = task.get("available_agents", [])
        
        # Simple resource allocation (placeholder implementation)
        allocations = []
        
        # TODO: Implement more sophisticated allocation logic
        
        return {
            "allocations": allocations,
            "unallocated_components": [],
            "agent_utilization": 0.0
        }
    
    def _review_performance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Review team performance.
        
        Args:
            task: Task containing performance review requirements
            
        Returns:
            Performance review details
        """
        agents = task.get("agents", [])
        metrics = task.get("metrics", {})
        
        # Simple performance review (placeholder implementation)
        reviews = []
        
        # TODO: Implement more sophisticated review logic
        
        return {
            "reviews": reviews,
            "team_score": 0.0,
            "recommendations": []
        }
    
    def _update_metrics_from_task(self, task: Dict[str, Any]) -> None:
        """Update agent's performance metrics based on task execution.
        
        Args:
            task: Completed task
        """
        task_type = task.get("type", "")
        
        if task_type == "project_planning":
            # Update metrics related to project planning
            current = self.performance_metrics.get("projects_completed", 0.0)
            self.update_metric("projects_completed", current + 0.1)
            
        elif task_type == "resource_allocation":
            # Update metrics related to resource allocation
            current = self.performance_metrics.get("team_productivity", 0.0)
            self.update_metric("team_productivity", current + 0.1)
            
        elif task_type == "performance_review":
            # Update metrics related to performance reviews
            current = self.performance_metrics.get("strategic_alignment", 0.0)
            self.update_metric("strategic_alignment", current + 0.1)
