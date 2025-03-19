#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Backend Developer Agent for FitDev.io
"""

from typing import Dict, Any, List
import logging
import json
import random
from fitdev.models.agent import BaseAgent, UTILS_AVAILABLE

logger = logging.getLogger(__name__)


class BackendDeveloperAgent(BaseAgent):
    """Backend Developer agent responsible for implementing server-side logic."""
    
    def __init__(self, name: str = "Backend Developer"):
        """Initialize the Backend Developer agent.
        
        Args:
            name: Agent name (default: "Backend Developer")
        """
        description = """Develops server-side logic, database structures, and APIs. 
                        Ensures system performance, security, and scalability."""
        super().__init__(name, "development", description)
        
        # Add Backend Developer-specific skills
        self.add_skill("Server-side Programming")
        self.add_skill("Database Design")
        self.add_skill("API Development")
        self.add_skill("Performance Optimization")
        self.add_skill("Security Practices")
        
        # Backend Developer-specific performance metrics
        self.update_metric("code_quality", 0.0)
        self.update_metric("system_performance", 0.0)
        self.update_metric("api_design", 0.0)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task assigned to this agent.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results and metadata
        """
        # If LLM or learning is enabled, use enhanced execution
        if (self.llm_enabled or self.learning_enabled) and UTILS_AVAILABLE:
            logger.info(f"Backend Developer executing task with enhanced capabilities: {task.get('title', 'Unknown task')}")
            
            # Get task details
            task_description = task.get("description", "")
            task_type = task.get("type", "")
            
            # Make sure last_used is initialized
            if not hasattr(self, 'last_used'):
                self._initialize_learning_systems()
                
            # Record task type for learning
            self.last_used["task_type"] = task_type
            
            # Get execution strategy from learning system if enabled
            if self.learning_enabled:
                strategy = self.get_task_execution_strategy(task_type)
                logger.info(f"Using strategy: {strategy['name']} - {strategy['description']}")
                
                # Adjust parameters based on learning
                thoroughness = self.get_parameter("thoroughness")
                security_focus = self.get_parameter("security_focus") if task_type == "api_development" else 0.5
                performance_focus = self.get_parameter("performance_focus") if task_type == "database_implementation" else 0.5
                
                logger.debug(f"Parameters - thoroughness: {thoroughness:.2f}, " +
                           f"security_focus: {security_focus:.2f}, performance_focus: {performance_focus:.2f}")
            
            # For backend tasks that might benefit from research, do that first
            research_results = None
            if self.browser_enabled and task_description:
                # Use learning parameters to decide whether to research
                should_research = True
                if self.learning_enabled:
                    # More thorough agents are more likely to do research
                    research_threshold = 0.3 if self.get_parameter("thoroughness") > 0.7 else 0.6
                    should_research = random.random() < research_threshold
                
                if should_research and task_type in ["api_development", "database_implementation", "service_implementation"]:
                    # Determine what to research based on task type
                    research_topic = None
                    if task_type == "api_development":
                        api_tech = task.get("technology", "REST")
                        research_topic = f"best practices for {api_tech} API design and implementation"
                    elif task_type == "database_implementation":
                        db_type = task.get("db_type", "SQL")
                        research_topic = f"{db_type} database design optimization and best practices"
                    elif task_type == "service_implementation":
                        service_type = task.get("service_type", "microservice")
                        research_topic = f"{service_type} architecture patterns and implementation"
                    
                    if research_topic:
                        logger.info(f"Backend Developer researching: {research_topic}")
                        research_results = self.research_topic(research_topic, max_pages=2)
                        # Store in memory for future tasks
                        self.set_memory(f"research_{task_type}", research_results)
            
            # Prepare context for LLM
            task_context = {
                "task_type": task_type,
                "agent_skills": self.skills,
                "task_details": task
            }
            
            if research_results and research_results.get("status") == "success":
                task_context["research_results"] = research_results
            
            # Add learning parameters to context if available
            if self.learning_enabled:
                task_context["parameters"] = {
                    param: self.get_parameter(param)
                    for param in ["thoroughness", "security_focus", "performance_focus", 
                                 "risk_taking", "code_reusability"]
                    if hasattr(self.parameter_learning, "parameters") and 
                    param in self.parameter_learning.parameters
                }
                
                # Add execution strategy
                if hasattr(self, "last_used") and "strategy" in self.last_used:
                    task_context["strategy"] = self.last_used["strategy"]
            
            # Get optimized prompt if learning is enabled
            if self.learning_enabled and self.llm_enabled:
                # Create prompt context with all relevant information
                prompt_context = {
                    "task_description": task_description,
                    "task_type": task_type,
                    "role": self.role,
                    "api_type": task.get("technology", "REST") if task_type == "api_development" else "",
                    "db_type": task.get("db_type", "SQL") if task_type == "database_implementation" else "",
                    "service_type": task.get("service_type", "microservice") if task_type == "service_implementation" else ""
                }
                
                # Get optimized prompt
                optimized_prompt = self.get_optimized_prompt(task_type, prompt_context)
                
                # Use this prompt for the LLM task
                system_message = f"You are {self.name}, a backend developer specialized in server-side logic, databases, and APIs."
                try:
                    response = self.get_llm_response(optimized_prompt, system_message)
                    
                    # Try to parse as JSON
                    try:
                        json_response = json.loads(response)
                        if isinstance(json_response, dict):
                            json_response["agent"] = self.name
                            json_response["status"] = "completed"
                            # Update metrics based on task execution
                            self._update_metrics_from_task(task)
                            return json_response
                    except json.JSONDecodeError:
                        # Continue with regular LLM execution if parsing fails
                        pass
                except Exception as e:
                    logger.error(f"Error with optimized prompt: {str(e)}")
            
            # Fall back to standard LLM execution if optimized prompt fails
            if self.llm_enabled:
                try:
                    llm_results = self.execute_task_with_llm(task)
                    if llm_results and llm_results["status"] == "completed":
                        # Update metrics based on task execution
                        self._update_metrics_from_task(task)
                        return llm_results
                except Exception as e:
                    logger.error(f"Error executing task with LLM: {str(e)}")
                    # Fall back to standard implementation
        
        # Standard implementation logic based on task type
        task_type = task.get("type", "")
        results = {"status": "completed", "agent": self.name}
        
        if task_type == "api_development":
            # Logic for API development tasks
            results["api"] = self._develop_api(task)
            
        elif task_type == "database_implementation":
            # Logic for database implementation tasks
            results["database"] = self._implement_database(task)
            
        elif task_type == "service_implementation":
            # Logic for service implementation tasks
            results["service"] = self._implement_service(task)
        
        # Update metrics based on task execution
        self._update_metrics_from_task(task)
        
        return results
    
    def evaluate_performance(self) -> float:
        """Evaluate Backend Developer agent's performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        # Weight factors for different metrics
        weights = {
            "code_quality": 0.3,
            "system_performance": 0.35,
            "api_design": 0.35
        }
        
        # Calculate weighted performance score
        score = 0.0
        for metric, weight in weights.items():
            if metric in self.performance_metrics:
                # Normalize metric value to 0.0-1.0 range if needed
                metric_value = min(1.0, max(0.0, self.performance_metrics[metric]))
                score += metric_value * weight
        
        return score
    
    def _develop_api(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Develop an API endpoint.
        
        Args:
            task: Task containing API requirements
            
        Returns:
            API implementation details
        """
        endpoint = task.get("endpoint", "")
        method = task.get("method", "GET")
        auth_required = task.get("auth_required", False)
        
        # Simple API implementation (placeholder implementation)
        code_snippet = """
        @app.route('/api/endpoint', methods=['GET'])
        @jwt_required() # If authentication is required
        def get_data():
            try:
                # Query database or perform operation
                data = service.get_data()
                return jsonify(data), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        """
        
        # TODO: Implement more sophisticated API development logic
        
        return {
            "code": code_snippet,
            "endpoint": endpoint,
            "method": method,
            "auth_required": auth_required,
            "documentation": "API documentation"
        }
    
    def _implement_database(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Implement database schema and operations.
        
        Args:
            task: Task containing database requirements
            
        Returns:
            Database implementation details
        """
        db_type = task.get("db_type", "SQL")
        entities = task.get("entities", [])
        relationships = task.get("relationships", [])
        
        # Simple database implementation (placeholder implementation)
        schema_code = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE posts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            title VARCHAR(100) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # TODO: Implement more sophisticated database schema generation
        
        return {
            "code": schema_code,
            "db_type": db_type,
            "entities": len(entities),
            "relationships": len(relationships),
            "indexes": True,
            "optimized": True
        }
    
    def _implement_service(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Implement a service layer component.
        
        Args:
            task: Task containing service requirements
            
        Returns:
            Service implementation details
        """
        service_name = task.get("service_name", "")
        dependencies = task.get("dependencies", [])
        operations = task.get("operations", [])
        
        # Simple service implementation (placeholder implementation)
        service_code = """
        class UserService:
            def __init__(self, user_repository, email_service):
                self.user_repository = user_repository
                self.email_service = email_service
            
            def get_user(self, user_id):
                return self.user_repository.find_by_id(user_id)
            
            def create_user(self, user_data):
                # Validate user data
                # Create user in repository
                user = self.user_repository.create(user_data)
                # Send welcome email
                self.email_service.send_welcome_email(user.email)
                return user
        """
        
        # TODO: Implement more sophisticated service layer generation
        
        return {
            "code": service_code,
            "service_name": service_name,
            "operations": len(operations),
            "error_handling": True,
            "unit_tests": True
        }
    
    def _update_metrics_from_task(self, task: Dict[str, Any]) -> None:
        """Update agent's performance metrics based on task execution.
        
        Args:
            task: Completed task
        """
        task_type = task.get("type", "")
        
        if task_type == "api_development":
            # Update metrics related to API development
            current = self.performance_metrics.get("api_design", 0.0)
            self.update_metric("api_design", current + 0.1)
            
        elif task_type == "database_implementation":
            # Update metrics related to database implementation
            current = self.performance_metrics.get("system_performance", 0.0)
            self.update_metric("system_performance", current + 0.1)
            
        elif task_type == "service_implementation":
            # Update metrics related to service implementation
            current = self.performance_metrics.get("code_quality", 0.0)
            self.update_metric("code_quality", current + 0.1)
