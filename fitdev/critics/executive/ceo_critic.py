#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CEO/Project Manager Critic for FitDev.io
"""

from typing import Dict, Any, List
from fitdev.models.critic import BaseCritic


class CEOCritic(BaseCritic):
    """Critic agent for evaluating CEO/Project Manager's work."""
    
    def __init__(self, name: str = "CEO/Project Manager Critic"):
        """Initialize the CEO Critic agent.
        
        Args:
            name: Critic agent name (default: "CEO/Project Manager Critic")
        """
        description = """Evaluates project plans, resource allocation decisions, 
                        and strategic alignment of the CEO/Project Manager's work. 
                        Provides feedback on improving project management and leadership."""
        super().__init__(name, "CEO/Project Manager", description)
        
        # Add evaluation criteria specific to CEO/Project Manager
        self.add_evaluation_criterion("Project Plan Completeness")
        self.add_evaluation_criterion("Resource Allocation Efficiency")
        self.add_evaluation_criterion("Strategic Alignment")
        self.add_evaluation_criterion("Risk Assessment")
        self.add_evaluation_criterion("Timeline Realism")
        
        # Critic-specific performance metrics
        self.update_metric("feedback_quality", 0.5)
        self.update_metric("suggestion_actionability", 0.5)
        self.update_metric("evaluation_thoroughness", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the CEO/Project Manager.
        
        Args:
            work_output: Work output and metadata from the CEO/Project Manager
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "project_planning":
            # Evaluate project planning output
            plan = work_output.get("plan", {})
            
            # Check phases
            phases = plan.get("phases", [])
            if not phases:
                feedback.append("Project plan lacks defined phases")
                suggestions.append("Include clear project phases with milestones")
                score += 0.0
            elif len(phases) < 3:
                feedback.append("Project plan has minimal phases defined")
                suggestions.append("Add more detailed phase breakdown for better tracking")
                score += 0.3
            else:
                feedback.append("Project plan has well-defined phases")
                score += 0.8
            
            # Check timeline
            timeline = plan.get("total_duration", 0)
            if timeline <= 0:
                feedback.append("Project timeline is not specified")
                suggestions.append("Define a realistic timeline for the project")
                score += 0.0
            elif timeline < 5:
                feedback.append("Project timeline may be too aggressive")
                suggestions.append("Consider a more realistic timeline with buffer for delays")
                score += 0.4
            else:
                feedback.append("Project timeline appears reasonable")
                score += 0.7
            
            # Check requirements coverage
            req_addressed = plan.get("requirements_addressed", 0)
            if req_addressed <= 0:
                feedback.append("No requirements addressed in the plan")
                suggestions.append("Ensure all requirements are accounted for in the plan")
                score += 0.0
            else:
                feedback.append(f"Plan addresses {req_addressed} requirements")
                score += 0.6
            
            # Normalize score
            score = score / 3.0  # Average of the three aspects
            
            # Add more specific suggestions
            suggestions.append("Include risk assessment and mitigation strategies")
            suggestions.append("Add resource allocation details to each phase")
            
        elif task_type == "resource_allocation":
            # Evaluate resource allocation output
            allocation = work_output.get("allocation", {})
            
            # Check allocations
            allocations = allocation.get("allocations", [])
            if not allocations:
                feedback.append("No resource allocations defined")
                suggestions.append("Provide detailed resource allocations for each component")
                score += 0.0
            else:
                feedback.append(f"Resource allocation plan includes {len(allocations)} allocations")
                score += 0.6
            
            # Check unallocated components
            unallocated = allocation.get("unallocated_components", [])
            if unallocated:
                feedback.append(f"There are {len(unallocated)} unallocated components")
                suggestions.append("Ensure all components have resources allocated")
                score += 0.3
            else:
                feedback.append("All components have resource allocations")
                score += 0.8
            
            # Check agent utilization
            utilization = allocation.get("agent_utilization", 0.0)
            if utilization < 0.5:
                feedback.append("Agent utilization is low")
                suggestions.append("Optimize resource allocation for better agent utilization")
                score += 0.3
            elif utilization > 0.9:
                feedback.append("Agent utilization is very high, risking burnout")
                suggestions.append("Consider adding more resources or extending timeline")
                score += 0.4
            else:
                feedback.append("Agent utilization is at an optimal level")
                score += 0.9
            
            # Normalize score
            score = score / 3.0  # Average of the three aspects
            
            # Add more specific suggestions
            suggestions.append("Include skills matching in resource allocation")
            suggestions.append("Add contingency resources for high-risk components")
            
        elif task_type == "performance_review":
            # Evaluate performance review output
            review = work_output.get("review", {})
            
            # Check reviews
            reviews = review.get("reviews", [])
            if not reviews:
                feedback.append("No individual reviews provided")
                suggestions.append("Include individual performance assessments")
                score += 0.0
            else:
                feedback.append(f"Performance review includes {len(reviews)} individual assessments")
                score += 0.7
            
            # Check team score
            team_score = review.get("team_score", 0.0)
            if team_score <= 0.0:
                feedback.append("Team score is not provided")
                suggestions.append("Include overall team performance score")
                score += 0.0
            else:
                feedback.append(f"Team performance score is {team_score:.2f}")
                score += 0.6
            
            # Check recommendations
            recommendations = review.get("recommendations", [])
            if not recommendations:
                feedback.append("No improvement recommendations provided")
                suggestions.append("Include specific recommendations for improvement")
                score += 0.0
            else:
                feedback.append(f"Performance review includes {len(recommendations)} recommendations")
                score += 0.8
            
            # Normalize score
            score = score / 3.0  # Average of the three aspects
            
            # Add more specific suggestions
            suggestions.append("Include quantitative metrics in performance evaluations")
            suggestions.append("Add specific action items for performance improvement")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("feedback_quality", min(1.0, self.performance_metrics.get("feedback_quality", 0.5) + 0.05))
        self.update_metric("suggestion_actionability", min(1.0, self.performance_metrics.get("suggestion_actionability", 0.5) + 0.05))
        self.update_metric("evaluation_thoroughness", min(1.0, self.performance_metrics.get("evaluation_thoroughness", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)
