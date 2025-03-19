#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Frontend Developer Critic for FitDev.io
"""

from typing import Dict, Any, List
from fitdev.models.critic import BaseCritic


class FrontendDeveloperCritic(BaseCritic):
    """Critic agent for evaluating Frontend Developer's work."""
    
    def __init__(self, name: str = "Frontend Developer Critic"):
        """Initialize the Frontend Developer Critic agent.
        
        Args:
            name: Critic agent name (default: "Frontend Developer Critic")
        """
        description = """Evaluates UI components, styling, and frontend integrations 
                        developed by the Frontend Developer. Provides feedback on code quality, 
                        responsiveness, accessibility, and performance."""
        super().__init__(name, "Frontend Developer", description)
        
        # Add evaluation criteria specific to Frontend Developer
        self.add_evaluation_criterion("Code Quality")
        self.add_evaluation_criterion("UI Responsiveness")
        self.add_evaluation_criterion("Accessibility")
        self.add_evaluation_criterion("Cross-browser Compatibility")
        self.add_evaluation_criterion("Performance Optimization")
        
        # Critic-specific performance metrics
        self.update_metric("code_review_quality", 0.5)
        self.update_metric("ui_design_insight", 0.5)
        self.update_metric("best_practice_knowledge", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the Frontend Developer.
        
        Args:
            work_output: Work output and metadata from the Frontend Developer
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "component_implementation":
            # Evaluate component implementation output
            component = work_output.get("component", {})
            
            # Check code
            code = component.get("code", "")
            if not code:
                feedback.append("No component code provided")
                suggestions.append("Implement the component with appropriate React/TypeScript patterns")
                score += 0.0
            elif len(code.strip().split("\n")) < 10:
                feedback.append("Component implementation is minimal")
                suggestions.append("Develop a more complete component implementation")
                score += 0.3
            else:
                feedback.append("Component has a reasonable implementation")
                score += 0.7
            
            # Check framework usage
            framework = component.get("framework", "")
            if not framework:
                feedback.append("No framework specified for the component")
                suggestions.append("Specify which framework the component is built with")
                score += 0.0
            else:
                feedback.append(f"Component uses {framework} framework")
                score += 0.8
            
            # Check test coverage
            test_coverage = component.get("test_coverage", False)
            if not test_coverage:
                feedback.append("Component lacks test coverage")
                suggestions.append("Add unit tests for the component")
                score += 0.0
            else:
                feedback.append("Component includes test coverage")
                score += 0.9
            
            # Normalize score
            score = score / 3.0  # Average of the three aspects
            
            # Add more specific suggestions based on code review
            if "useState" in code and "useEffect" not in code:
                suggestions.append("Consider using useEffect for side effects related to state changes")
            
            if "interface Props" in code and "{}" in code:
                suggestions.append("Define explicit prop types instead of using empty interfaces")
            
            suggestions.append("Add prop validation with default values")
            suggestions.append("Consider component memoization for performance optimization")
            
        elif task_type == "styling":
            # Evaluate styling output
            styles = work_output.get("styles", {})
            
            # Check code
            style_code = styles.get("code", "")
            if not style_code:
                feedback.append("No styling code provided")
                suggestions.append("Implement styles for the component")
                score += 0.0
            elif len(style_code.strip().split("\n")) < 5:
                feedback.append("Styling implementation is minimal")
                suggestions.append("Add more comprehensive styling")
                score += 0.3
            else:
                feedback.append("Styling has a reasonable implementation")
                score += 0.7
            
            # Check style type
            style_type = styles.get("style_type", "")
            if not style_type:
                feedback.append("No styling methodology specified")
                suggestions.append("Specify styling approach (CSS, SCSS, CSS-in-JS, etc.)")
                score += 0.0
            else:
                feedback.append(f"Uses {style_type} for styling")
                score += 0.8
            
            # Check responsiveness
            responsive = styles.get("responsive", False)
            if not responsive:
                feedback.append("Styles lack responsiveness")
                suggestions.append("Add media queries for responsive design")
                score += 0.0
            else:
                feedback.append("Styling includes responsive design")
                score += 0.9
            
            # Check theme compatibility
            theme_compatibility = styles.get("theme_compatibility", False)
            if not theme_compatibility:
                feedback.append("Styles don't support theming")
                suggestions.append("Add theme variable support")
                score += 0.3
            else:
                feedback.append("Styling supports theming")
                score += 0.8
            
            # Normalize score
            score = score / 4.0  # Average of the four aspects
            
            # Add more specific suggestions
            suggestions.append("Use CSS variables for better maintainability")
            suggestions.append("Consider mobile-first approach for responsive design")
            suggestions.append("Add accessibility attributes (aria-*) where appropriate")
            
        elif task_type == "frontend_integration":
            # Evaluate frontend integration output
            integration = work_output.get("integration", {})
            
            # Check code
            integration_code = integration.get("code", "")
            if not integration_code:
                feedback.append("No integration code provided")
                suggestions.append("Implement API integration code")
                score += 0.0
            elif len(integration_code.strip().split("\n")) < 10:
                feedback.append("Integration implementation is minimal")
                suggestions.append("Develop more comprehensive integration code")
                score += 0.3
            else:
                feedback.append("Integration has a reasonable implementation")
                score += 0.7
            
            # Check APIs integrated
            apis_integrated = integration.get("apis_integrated", 0)
            if apis_integrated <= 0:
                feedback.append("No APIs integrated")
                suggestions.append("Integrate with the required backend APIs")
                score += 0.0
            else:
                feedback.append(f"Integration covers {apis_integrated} APIs")
                score += 0.8
            
            # Check auth handling
            auth_handling = integration.get("auth_handling", False)
            if not auth_handling:
                feedback.append("Integration lacks authentication handling")
                suggestions.append("Add authentication token management")
                score += 0.4
            else:
                feedback.append("Integration includes authentication handling")
                score += 0.9
            
            # Check error handling
            error_handling = integration.get("error_handling", False)
            if not error_handling:
                feedback.append("Integration lacks error handling")
                suggestions.append("Add comprehensive error handling")
                score += 0.0
            else:
                feedback.append("Integration includes error handling")
                score += 0.8
            
            # Normalize score
            score = score / 4.0  # Average of the four aspects
            
            # Add more specific suggestions
            suggestions.append("Use a consistent error handling strategy across integrations")
            suggestions.append("Add loading states for all API operations")
            suggestions.append("Consider implementing request caching for performance")
            suggestions.append("Add retry logic for failed requests")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("code_review_quality", min(1.0, self.performance_metrics.get("code_review_quality", 0.5) + 0.05))
        self.update_metric("ui_design_insight", min(1.0, self.performance_metrics.get("ui_design_insight", 0.5) + 0.05))
        self.update_metric("best_practice_knowledge", min(1.0, self.performance_metrics.get("best_practice_knowledge", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)
