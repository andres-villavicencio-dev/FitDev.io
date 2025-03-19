#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CTO/Technical Architect Critic for FitDev.io
"""

from typing import Dict, Any, List
from models.critic import BaseCritic


class CTOCritic(BaseCritic):
    """Critic agent for evaluating CTO/Technical Architect's work."""
    
    def __init__(self, name: str = "CTO/Technical Architect Critic"):
        """Initialize the CTO Critic agent.
        
        Args:
            name: Critic agent name (default: "CTO/Technical Architect Critic")
        """
        description = """Evaluates system architecture designs, technology selections, 
                        and technical standards set by the CTO/Technical Architect. 
                        Provides feedback on improving architecture decisions and 
                        technical direction."""
        super().__init__(name, "CTO/Technical Architect", description)
        
        # Add evaluation criteria specific to CTO/Technical Architect
        self.add_evaluation_criterion("Architecture Scalability")
        self.add_evaluation_criterion("Technology Stack Appropriateness")
        self.add_evaluation_criterion("Security Considerations")
        self.add_evaluation_criterion("Maintainability")
        self.add_evaluation_criterion("Performance Optimization")
        
        # Critic-specific performance metrics
        self.update_metric("technical_accuracy", 0.5)
        self.update_metric("architecture_insight", 0.5)
        self.update_metric("evaluation_depth", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the CTO/Technical Architect.
        
        Args:
            work_output: Work output and metadata from the CTO/Technical Architect
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "architecture_design":
            # Evaluate architecture design output
            architecture = work_output.get("architecture", {})
            
            # Check components
            components = architecture.get("components", [])
            if not components:
                feedback.append("Architecture lacks defined components")
                suggestions.append("Define core system components and their responsibilities")
                score += 0.0
            elif len(components) < 3:
                feedback.append("Architecture has minimal components defined")
                suggestions.append("Consider breaking down the system into more modular components")
                score += 0.3
            else:
                feedback.append(f"Architecture includes {len(components)} well-defined components")
                score += 0.8
            
            # Check connections/interfaces
            connections = architecture.get("connections", [])
            if not connections and len(components) > 1:
                feedback.append("No component connections/interfaces defined")
                suggestions.append("Specify how components interact with each other")
                score += 0.0
            elif connections:
                feedback.append(f"Architecture defines {len(connections)} component connections")
                score += 0.7
            
            # Check scalability factors
            scalability = architecture.get("scalability_factors", [])
            if not scalability:
                feedback.append("No scalability considerations in the architecture")
                suggestions.append("Include specific strategies for system scalability")
                score += 0.0
            else:
                feedback.append(f"Architecture includes {len(scalability)} scalability considerations")
                score += 0.8
            
            # Normalize score
            score = score / 3.0  # Average of the three aspects
            
            # Add more specific suggestions
            suggestions.append("Consider adding security layers in the architecture")
            suggestions.append("Include data flow diagrams for better understanding")
            suggestions.append("Specify performance requirements for each component")
            
        elif task_type == "technology_selection":
            # Evaluate technology selection output
            technology = work_output.get("technology", {})
            
            # Check frontend technologies
            frontend = technology.get("frontend", [])
            if not frontend:
                feedback.append("No frontend technologies specified")
                suggestions.append("Select appropriate frontend technologies based on requirements")
                score += 0.0
            else:
                feedback.append(f"Selected {len(frontend)} frontend technologies")
                score += 0.6
            
            # Check backend technologies
            backend = technology.get("backend", [])
            if not backend:
                feedback.append("No backend technologies specified")
                suggestions.append("Select appropriate backend technologies based on requirements")
                score += 0.0
            else:
                feedback.append(f"Selected {len(backend)} backend technologies")
                score += 0.6
            
            # Check database technologies
            database = technology.get("database", [])
            if not database:
                feedback.append("No database technologies specified")
                suggestions.append("Select appropriate database technologies based on requirements")
                score += 0.0
            else:
                feedback.append(f"Selected {len(database)} database technologies")
                score += 0.7
            
            # Check devops technologies
            devops = technology.get("devops", [])
            if not devops:
                feedback.append("No DevOps technologies specified")
                suggestions.append("Select appropriate DevOps technologies for CI/CD")
                score += 0.0
            else:
                feedback.append(f"Selected {len(devops)} DevOps technologies")
                score += 0.6
            
            # Check justification
            justification = technology.get("justification", "")
            if not justification:
                feedback.append("No justification provided for technology choices")
                suggestions.append("Provide rationale for technology selections")
                score += 0.0
            else:
                feedback.append("Technology choices include justification")
                score += 0.8
            
            # Normalize score
            score = score / 5.0  # Average of the five aspects
            
            # Add more specific suggestions
            suggestions.append("Consider technology maturity in selection criteria")
            suggestions.append("Evaluate learning curve for the team with new technologies")
            suggestions.append("Include performance benchmarks for selected technologies")
            
        elif task_type == "technical_review":
            # Evaluate technical review output
            review = work_output.get("review", {})
            
            # Check findings
            findings = review.get("findings", [])
            if not findings:
                feedback.append("No findings reported in the technical review")
                suggestions.append("Include detailed findings from code or architecture review")
                score += 0.0
            else:
                feedback.append(f"Technical review includes {len(findings)} findings")
                score += 0.7
            
            # Check recommendations
            recommendations = review.get("recommendations", [])
            if not recommendations:
                feedback.append("No recommendations provided in the technical review")
                suggestions.append("Provide specific recommendations for each finding")
                score += 0.0
            else:
                feedback.append(f"Technical review includes {len(recommendations)} recommendations")
                score += 0.8
            
            # Check overall score
            overall_score = review.get("overall_score", 0.0)
            if overall_score == 0.0:
                feedback.append("No overall score provided for the technical review")
                suggestions.append("Include an overall assessment score")
                score += 0.0
            else:
                feedback.append(f"Technical review includes an overall score of {overall_score:.2f}")
                score += 0.6
            
            # Normalize score
            score = score / 3.0  # Average of the three aspects
            
            # Add more specific suggestions
            suggestions.append("Categorize findings by severity/impact")
            suggestions.append("Include code snippets or diagrams for clarity")
            suggestions.append("Add implementation complexity assessment for recommendations")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("technical_accuracy", min(1.0, self.performance_metrics.get("technical_accuracy", 0.5) + 0.05))
        self.update_metric("architecture_insight", min(1.0, self.performance_metrics.get("architecture_insight", 0.5) + 0.05))
        self.update_metric("evaluation_depth", min(1.0, self.performance_metrics.get("evaluation_depth", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)
