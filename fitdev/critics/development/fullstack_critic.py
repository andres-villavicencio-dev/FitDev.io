#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Full Stack Developer Critic for FitDev.io
"""

from typing import Dict, Any, List
from models.critic import BaseCritic


class FullStackDeveloperCritic(BaseCritic):
    """Critic agent for evaluating Full Stack Developer's work."""
    
    def __init__(self, name: str = "Full Stack Developer Critic"):
        """Initialize the Full Stack Developer Critic agent.
        
        Args:
            name: Critic agent name (default: "Full Stack Developer Critic")
        """
        description = """Evaluates complete feature implementations spanning frontend 
                        and backend, system integrations, and end-to-end testing by the 
                        Full Stack Developer. Provides feedback on code quality, 
                        feature completeness, and integration quality."""
        super().__init__(name, "Full Stack Developer", description)
        
        # Add evaluation criteria specific to Full Stack Developer
        self.add_evaluation_criterion("Feature Completeness")
        self.add_evaluation_criterion("Integration Quality")
        self.add_evaluation_criterion("Code Quality")
        self.add_evaluation_criterion("End-to-End Testing")
        self.add_evaluation_criterion("User Experience Flow")
        
        # Critic-specific performance metrics
        self.update_metric("feature_review_quality", 0.5)
        self.update_metric("full_stack_knowledge", 0.5)
        self.update_metric("integration_insight", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the Full Stack Developer.
        
        Args:
            work_output: Work output and metadata from the Full Stack Developer
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "feature_implementation":
            # Evaluate feature implementation output
            feature = work_output.get("feature", {})
            
            # Check frontend code
            frontend_code = feature.get("frontend_code", "")
            if not frontend_code:
                feedback.append("No frontend implementation provided")
                suggestions.append("Implement the frontend component of the feature")
                score += 0.0
            elif len(frontend_code.strip().split("\n")) < 15:
                feedback.append("Frontend implementation is minimal")
                suggestions.append("Develop a more complete frontend implementation")
                score += 0.3
            else:
                feedback.append("Frontend has a reasonable implementation")
                score += 0.7
            
            # Check backend code
            backend_code = feature.get("backend_code", "")
            if not backend_code:
                feedback.append("No backend implementation provided")
                suggestions.append("Implement the backend component of the feature")
                score += 0.0
            elif len(backend_code.strip().split("\n")) < 15:
                feedback.append("Backend implementation is minimal")
                suggestions.append("Develop a more complete backend implementation")
                score += 0.3
            else:
                feedback.append("Backend has a reasonable implementation")
                score += 0.7
            
            # Check feature name and requirements met
            feature_name = feature.get("feature_name", "")
            requirements_met = feature.get("requirements_met", 0)
            if not feature_name:
                feedback.append("Feature name not specified")
                suggestions.append("Clearly name your feature for better identification")
                score += 0.2
            elif requirements_met <= 0:
                feedback.append(f"Feature '{feature_name}' meets no requirements")
                suggestions.append("Ensure the feature addresses specific requirements")
                score += 0.0
            else:
                feedback.append(f"Feature '{feature_name}' meets {requirements_met} requirements")
                score += 0.8
            
            # Check test coverage
            test_coverage = feature.get("test_coverage", False)
            if not test_coverage:
                feedback.append("Feature lacks test coverage")
                suggestions.append("Add tests for the feature")
                score += 0.0
            else:
                feedback.append("Feature includes test coverage")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the four aspects
            
            # Add more specific suggestions
            suggestions.append("Ensure consistent error handling between frontend and backend")
            suggestions.append("Add loading states and error states in the UI")
            suggestions.append("Consider implementing optimistic UI updates")
            suggestions.append("Add data validation on both client and server sides")
            
        elif task_type == "system_integration":
            # Evaluate system integration output
            integration = work_output.get("integration", {})
            
            # Check code
            code = integration.get("code", "")
            if not code:
                feedback.append("No integration code provided")
                suggestions.append("Implement the integration code")
                score += 0.0
            elif len(code.strip().split("\n")) < 20:
                feedback.append("Integration implementation is minimal")
                suggestions.append("Develop a more complete integration")
                score += 0.3
            else:
                feedback.append("Integration has a reasonable implementation")
                score += 0.7
            
            # Check components integrated
            components = integration.get("components_integrated", 0)
            if components <= 0:
                feedback.append("No components integrated")
                suggestions.append("Define and integrate the necessary components")
                score += 0.0
            elif components < 2:
                feedback.append("Limited component integration")
                suggestions.append("Integrate more components for a complete solution")
                score += 0.4
            else:
                feedback.append(f"Integration connects {components} components")
                score += 0.8
            
            # Check interfaces implemented
            interfaces = integration.get("interfaces_implemented", 0)
            if interfaces <= 0:
                feedback.append("No interfaces implemented")
                suggestions.append("Define and implement the necessary interfaces")
                score += 0.0
            else:
                feedback.append(f"Integration implements {interfaces} interfaces")
                score += 0.7
            
            # Check error handling
            error_handling = integration.get("error_handling", False)
            if not error_handling:
                feedback.append("Integration lacks error handling")
                suggestions.append("Add comprehensive error handling")
                score += 0.0
            else:
                feedback.append("Integration includes error handling")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the four aspects
            
            # Add more specific suggestions
            suggestions.append("Consider implementing a circuit breaker pattern for resilience")
            suggestions.append("Add logging for integration events and errors")
            suggestions.append("Implement retry logic for transient failures")
            suggestions.append("Add metrics/telemetry for monitoring integration health")
            
        elif task_type == "end_to_end_test":
            # Evaluate end-to-end test output
            test = work_output.get("test", {})
            
            # Check code
            code = test.get("code", "")
            if not code:
                feedback.append("No test code provided")
                suggestions.append("Implement end-to-end tests")
                score += 0.0
            elif len(code.strip().split("\n")) < 15:
                feedback.append("Test implementation is minimal")
                suggestions.append("Develop more comprehensive tests")
                score += 0.3
            else:
                feedback.append("Tests have a reasonable implementation")
                score += 0.7
            
            # Check feature coverage
            feature = test.get("feature", "")
            if not feature:
                feedback.append("Test doesn't specify which feature it covers")
                suggestions.append("Clearly identify the feature being tested")
                score += 0.2
            else:
                feedback.append(f"Tests cover the '{feature}' feature")
                score += 0.8
            
            # Check scenarios covered
            scenarios = test.get("scenarios_covered", 0)
            if scenarios <= 0:
                feedback.append("No test scenarios defined")
                suggestions.append("Define specific test scenarios for comprehensive coverage")
                score += 0.0
            elif scenarios < 3:
                feedback.append("Limited test scenario coverage")
                suggestions.append("Add more test scenarios for better coverage")
                score += 0.4
            else:
                feedback.append(f"Tests cover {scenarios} scenarios")
                score += 0.9
            
            # Check test framework
            framework = test.get("framework", "")
            if not framework:
                feedback.append("No test framework specified")
                suggestions.append("Specify which test framework is being used")
                score += 0.2
            else:
                feedback.append(f"Tests use the {framework} framework")
                score += 0.7
            
            # Normalize score
            score = score / 4.0  # Average of the four aspects
            
            # Add more specific suggestions
            suggestions.append("Include positive and negative test cases")
            suggestions.append("Add tests for edge cases and error handling")
            suggestions.append("Consider using test data factories for consistent test data")
            suggestions.append("Add setup and teardown procedures for test isolation")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("feature_review_quality", min(1.0, self.performance_metrics.get("feature_review_quality", 0.5) + 0.05))
        self.update_metric("full_stack_knowledge", min(1.0, self.performance_metrics.get("full_stack_knowledge", 0.5) + 0.05))
        self.update_metric("integration_insight", min(1.0, self.performance_metrics.get("integration_insight", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)
