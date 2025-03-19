#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Backend Developer Critic for FitDev.io
"""

from typing import Dict, Any, List
from fitdev.models.critic import BaseCritic


class BackendDeveloperCritic(BaseCritic):
    """Critic agent for evaluating Backend Developer's work."""
    
    def __init__(self, name: str = "Backend Developer Critic"):
        """Initialize the Backend Developer Critic agent.
        
        Args:
            name: Critic agent name (default: "Backend Developer Critic")
        """
        description = """Evaluates APIs, database designs, and server-side services 
                        developed by the Backend Developer. Provides feedback on code quality, 
                        performance, security, and scalability."""
        super().__init__(name, "Backend Developer", description)
        
        # Add evaluation criteria specific to Backend Developer
        self.add_evaluation_criterion("Code Quality")
        self.add_evaluation_criterion("API Design")
        self.add_evaluation_criterion("Database Optimization")
        self.add_evaluation_criterion("Security Practices")
        self.add_evaluation_criterion("Performance Efficiency")
        
        # Critic-specific performance metrics
        self.update_metric("code_review_quality", 0.5)
        self.update_metric("architecture_insight", 0.5)
        self.update_metric("security_knowledge", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the Backend Developer.
        
        Args:
            work_output: Work output and metadata from the Backend Developer
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "api_development":
            # Evaluate API development output
            api = work_output.get("api", {})
            
            # Check code
            code = api.get("code", "")
            if not code:
                feedback.append("No API implementation code provided")
                suggestions.append("Implement the API endpoint")
                score += 0.0
            elif len(code.strip().split("\n")) < 10:
                feedback.append("API implementation is minimal")
                suggestions.append("Develop a more complete API implementation")
                score += 0.3
            else:
                feedback.append("API has a reasonable implementation")
                score += 0.7
            
            # Check endpoint and method
            endpoint = api.get("endpoint", "")
            method = api.get("method", "")
            if not endpoint or not method:
                feedback.append("API endpoint or method not specified")
                suggestions.append("Clearly define API endpoint and HTTP method")
                score += 0.0
            else:
                feedback.append(f"API implements {method} {endpoint}")
                score += 0.8
            
            # Check authentication
            auth_required = api.get("auth_required", False)
            if auth_required and "jwt_required" not in code and "auth" not in code.lower():
                feedback.append("Authentication is required but not properly implemented")
                suggestions.append("Add proper authentication checks")
                score += 0.3
            elif auth_required:
                feedback.append("API includes authentication requirements")
                score += 0.9
            
            # Check documentation
            documentation = api.get("documentation", "")
            if not documentation:
                feedback.append("API lacks documentation")
                suggestions.append("Add comprehensive API documentation")
                score += 0.0
            else:
                feedback.append("API includes documentation")
                score += 0.8
            
            # Normalize score
            score = score / 4.0  # Average of the four aspects
            
            # Add more specific suggestions
            suggestions.append("Add input validation for all parameters")
            suggestions.append("Implement proper error status codes (4xx, 5xx)")
            suggestions.append("Consider rate limiting for public APIs")
            suggestions.append("Add response caching headers where appropriate")
            
        elif task_type == "database_implementation":
            # Evaluate database implementation output
            database = work_output.get("database", {})
            
            # Check code
            code = database.get("code", "")
            if not code:
                feedback.append("No database schema or query code provided")
                suggestions.append("Implement the database schema and queries")
                score += 0.0
            elif len(code.strip().split("\n")) < 15:
                feedback.append("Database implementation is minimal")
                suggestions.append("Develop a more complete database implementation")
                score += 0.3
            else:
                feedback.append("Database has a reasonable implementation")
                score += 0.7
            
            # Check database type
            db_type = database.get("db_type", "")
            if not db_type:
                feedback.append("Database type not specified")
                suggestions.append("Specify the database type (SQL, NoSQL, etc.)")
                score += 0.0
            else:
                feedback.append(f"Implementation uses {db_type} database")
                score += 0.8
            
            # Check entities and relationships
            entities = database.get("entities", 0)
            relationships = database.get("relationships", 0)
            if entities <= 0:
                feedback.append("No database entities defined")
                suggestions.append("Define the required database entities")
                score += 0.0
            else:
                feedback.append(f"Schema includes {entities} entities with {relationships} relationships")
                score += 0.7
            
            # Check optimization
            optimized = database.get("optimized", False)
            indexes = database.get("indexes", False)
            if not optimized or not indexes:
                feedback.append("Database lacks optimization considerations")
                suggestions.append("Add appropriate indexes and optimizations")
                score += 0.3
            else:
                feedback.append("Database includes optimization considerations")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the four aspects
            
            # Add more specific suggestions
            suggestions.append("Define appropriate foreign key constraints")
            suggestions.append("Consider adding database migrations for version control")
            suggestions.append("Include index creation for frequently queried columns")
            suggestions.append("Add appropriate data validation at the database level")
            
        elif task_type == "service_implementation":
            # Evaluate service implementation output
            service = work_output.get("service", {})
            
            # Check code
            code = service.get("code", "")
            if not code:
                feedback.append("No service implementation code provided")
                suggestions.append("Implement the service layer")
                score += 0.0
            elif len(code.strip().split("\n")) < 15:
                feedback.append("Service implementation is minimal")
                suggestions.append("Develop a more complete service implementation")
                score += 0.3
            else:
                feedback.append("Service has a reasonable implementation")
                score += 0.7
            
            # Check service name and operations
            service_name = service.get("service_name", "")
            operations = service.get("operations", 0)
            if not service_name:
                feedback.append("Service name not specified")
                suggestions.append("Clearly name your service for better identification")
                score += 0.2
            elif operations <= 0:
                feedback.append(f"Service {service_name} has no defined operations")
                suggestions.append("Implement the required operations for the service")
                score += 0.3
            else:
                feedback.append(f"Service {service_name} implements {operations} operations")
                score += 0.8
            
            # Check error handling
            error_handling = service.get("error_handling", False)
            if not error_handling:
                feedback.append("Service lacks error handling")
                suggestions.append("Add comprehensive error handling")
                score += 0.0
            else:
                feedback.append("Service includes error handling")
                score += 0.9
            
            # Check unit tests
            unit_tests = service.get("unit_tests", False)
            if not unit_tests:
                feedback.append("Service lacks unit tests")
                suggestions.append("Add unit tests for the service")
                score += 0.0
            else:
                feedback.append("Service includes unit tests")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the four aspects
            
            # Add more specific suggestions
            suggestions.append("Apply dependency injection for better testability")
            suggestions.append("Consider adding logging for important operations")
            suggestions.append("Implement transaction management for database operations")
            suggestions.append("Add method-level documentation for public methods")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("code_review_quality", min(1.0, self.performance_metrics.get("code_review_quality", 0.5) + 0.05))
        self.update_metric("architecture_insight", min(1.0, self.performance_metrics.get("architecture_insight", 0.5) + 0.05))
        self.update_metric("security_knowledge", min(1.0, self.performance_metrics.get("security_knowledge", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)
