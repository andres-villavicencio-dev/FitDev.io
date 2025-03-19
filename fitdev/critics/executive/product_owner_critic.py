#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Product Owner Critic for FitDev.io
"""

from typing import Dict, Any, List
from models.critic import BaseCritic


class ProductOwnerCritic(BaseCritic):
    """Critic agent for evaluating Product Owner's work."""
    
    def __init__(self, name: str = "Product Owner Critic"):
        """Initialize the Product Owner Critic agent.
        
        Args:
            name: Critic agent name (default: "Product Owner Critic")
        """
        description = """Evaluates requirements gathering, backlog management, 
                        and user story creation by the Product Owner. Provides 
                        feedback on improving value delivery and stakeholder 
                        alignment."""
        super().__init__(name, "Product Owner", description)
        
        # Add evaluation criteria specific to Product Owner
        self.add_evaluation_criterion("Requirement Clarity")
        self.add_evaluation_criterion("Stakeholder Coverage")
        self.add_evaluation_criterion("User Story Quality")
        self.add_evaluation_criterion("Prioritization Logic")
        self.add_evaluation_criterion("Value Alignment")
        
        # Critic-specific performance metrics
        self.update_metric("business_value_insight", 0.5)
        self.update_metric("requirement_analysis", 0.5)
        self.update_metric("feedback_relevance", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the Product Owner.
        
        Args:
            work_output: Work output and metadata from the Product Owner
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "requirement_gathering":
            # Evaluate requirement gathering output
            requirements = work_output.get("requirements", {})
            
            # Check functional requirements
            functional_reqs = requirements.get("functional_requirements", [])
            if not functional_reqs:
                feedback.append("No functional requirements gathered")
                suggestions.append("Interview stakeholders to gather functional requirements")
                score += 0.0
            elif len(functional_reqs) < 5:
                feedback.append("Limited functional requirements gathered")
                suggestions.append("Expand functional requirement coverage")
                score += 0.3
            else:
                feedback.append(f"Gathered {len(functional_reqs)} functional requirements")
                score += 0.8
            
            # Check non-functional requirements
            non_functional_reqs = requirements.get("non_functional_requirements", [])
            if not non_functional_reqs:
                feedback.append("No non-functional requirements gathered")
                suggestions.append("Include performance, security, and scalability requirements")
                score += 0.0
            else:
                feedback.append(f"Gathered {len(non_functional_reqs)} non-functional requirements")
                score += 0.7
            
            # Check stakeholder coverage
            stakeholder_coverage = requirements.get("stakeholder_coverage", 0)
            if stakeholder_coverage <= 0:
                feedback.append("No stakeholder coverage information")
                suggestions.append("Track which stakeholders contributed to requirements")
                score += 0.0
            elif stakeholder_coverage < 3:
                feedback.append(f"Limited stakeholder coverage ({stakeholder_coverage})")
                suggestions.append("Engage more stakeholders for comprehensive requirements")
                score += 0.4
            else:
                feedback.append(f"Good stakeholder coverage with {stakeholder_coverage} contributors")
                score += 0.9
            
            # Normalize score
            score = score / 3.0  # Average of the three aspects
            
            # Add more specific suggestions
            suggestions.append("Use requirement templates for consistency")
            suggestions.append("Add acceptance criteria to functional requirements")
            suggestions.append("Categorize requirements by feature area or priority")
            
        elif task_type == "backlog_prioritization":
            # Evaluate backlog prioritization output
            backlog = work_output.get("backlog", {})
            
            # Check prioritized items
            prioritized_items = backlog.get("prioritized_items", [])
            if not prioritized_items:
                feedback.append("No prioritized backlog items")
                suggestions.append("Prioritize backlog items based on value and effort")
                score += 0.0
            elif len(prioritized_items) < 5:
                feedback.append("Limited number of prioritized items")
                suggestions.append("Ensure comprehensive backlog coverage")
                score += 0.4
            else:
                feedback.append(f"Prioritized {len(prioritized_items)} backlog items")
                score += 0.8
            
            # Check rationale
            rationale = backlog.get("rationale", "")
            if not rationale:
                feedback.append("No rationale provided for prioritization")
                suggestions.append("Document reasoning behind prioritization decisions")
                score += 0.0
            else:
                feedback.append("Prioritization includes rationale")
                score += 0.7
            
            # Normalize score
            score = score / 2.0  # Average of the two aspects
            
            # Add more specific suggestions
            suggestions.append("Use a consistent prioritization framework (e.g., RICE, MoSCoW)")
            suggestions.append("Include business value estimates for each item")
            suggestions.append("Consider dependencies in prioritization")
            
        elif task_type == "user_story_creation":
            # Evaluate user story creation output
            user_stories = work_output.get("user_stories", {})
            
            # Check user stories
            stories = user_stories.get("user_stories", [])
            if not stories:
                feedback.append("No user stories created")
                suggestions.append("Create user stories using the standard format")
                score += 0.0
            elif len(stories) < 3:
                feedback.append("Limited number of user stories created")
                suggestions.append("Create more user stories to cover the requirements")
                score += 0.3
            else:
                feedback.append(f"Created {len(stories)} user stories")
                score += 0.8
            
            # Check acceptance criteria
            acceptance_criteria = user_stories.get("acceptance_criteria", [])
            if not acceptance_criteria:
                feedback.append("No acceptance criteria defined for user stories")
                suggestions.append("Add acceptance criteria to each user story")
                score += 0.0
            else:
                feedback.append(f"Defined acceptance criteria for user stories")
                score += 0.7
            
            # Check coverage
            coverage = user_stories.get("coverage", 0.0)
            if coverage <= 0.0:
                feedback.append("No coverage information for user stories")
                suggestions.append("Track how stories cover requirements")
                score += 0.0
            elif coverage < 0.7:
                feedback.append(f"Limited requirement coverage ({coverage:.2f})")
                suggestions.append("Ensure user stories cover all requirements")
                score += 0.4
            else:
                feedback.append(f"Good requirement coverage ({coverage:.2f})")
                score += 0.9
            
            # Normalize score
            score = score / 3.0  # Average of the three aspects
            
            # Add more specific suggestions
            suggestions.append("Use the 'As a... I want... So that...' format consistently")
            suggestions.append("Include story points or effort estimates")
            suggestions.append("Add mockups or diagrams for complex user stories")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("business_value_insight", min(1.0, self.performance_metrics.get("business_value_insight", 0.5) + 0.05))
        self.update_metric("requirement_analysis", min(1.0, self.performance_metrics.get("requirement_analysis", 0.5) + 0.05))
        self.update_metric("feedback_relevance", min(1.0, self.performance_metrics.get("feedback_relevance", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)
