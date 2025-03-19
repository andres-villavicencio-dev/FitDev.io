#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Frontend Developer Agent for FitDev.io
"""

from typing import Dict, Any, List
import logging
import json
import random
from fitdev.models.agent import BaseAgent, UTILS_AVAILABLE

logger = logging.getLogger(__name__)


class FrontendDeveloperAgent(BaseAgent):
    """Frontend Developer agent responsible for implementing user interfaces."""
    
    def __init__(self, name: str = "Frontend Developer"):
        """Initialize the Frontend Developer agent.
        
        Args:
            name: Agent name (default: "Frontend Developer")
        """
        description = """Implements user interfaces and client-side functionality. 
                        Focuses on usability, responsiveness, and visual implementation 
                        of designs."""
        super().__init__(name, "development", description)
        
        # Add Frontend Developer-specific skills
        self.add_skill("HTML/CSS")
        self.add_skill("JavaScript/TypeScript")
        self.add_skill("React/Vue/Angular")
        self.add_skill("Responsive Design")
        self.add_skill("UI/UX Implementation")
        
        # Frontend Developer-specific performance metrics
        self.update_metric("code_quality", 0.0)
        self.update_metric("ui_responsiveness", 0.0)
        self.update_metric("accessibility", 0.0)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task assigned to this agent.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results and metadata
        """
        # If LLM or learning is enabled, use enhanced execution
        if (self.llm_enabled or self.learning_enabled) and UTILS_AVAILABLE:
            logger.info(f"Frontend Developer executing task with enhanced capabilities: {task.get('title', 'Unknown task')}")
            
            # Get task details
            task_description = task.get("description", "")
            task_type = task.get("type", "")
            
            # Record task type for learning
            self.last_used["task_type"] = task_type
            
            # Get execution strategy from learning system if enabled
            if self.learning_enabled:
                strategy = self.get_task_execution_strategy(task_type)
                logger.info(f"Using strategy: {strategy['name']} - {strategy['description']}")
                
                # Adjust parameters based on learning
                thoroughness = self.get_parameter("thoroughness")
                creativity = self.get_parameter("creativity")
                design_focus = self.get_parameter("design_focus") if task_type == "component_implementation" else 0.5
                
                logger.debug(f"Parameters - thoroughness: {thoroughness:.2f}, " +
                           f"creativity: {creativity:.2f}, design_focus: {design_focus:.2f}")
            
            # For frontend tasks that might benefit from research, do that first
            research_results = None
            if self.browser_enabled and task_description:
                # Use learning parameters to decide whether to research
                should_research = True
                if self.learning_enabled:
                    # More thorough agents are more likely to do research
                    research_threshold = 0.3 if self.get_parameter("thoroughness") > 0.7 else 0.6
                    should_research = random.random() < research_threshold
                
                if should_research and task_type in ["component_implementation", "styling"]:
                    # Determine what to research based on task type
                    research_topic = None
                    if "component" in task_description.lower():
                        component_type = task.get("component_type", "UI component")
                        framework = task.get("framework", "React")
                        research_topic = f"best practices for {framework} {component_type} implementation"
                    elif "style" in task_description.lower() or task_type == "styling":
                        style_type = task.get("style_type", "CSS")
                        research_topic = f"modern {style_type} styling techniques and best practices"
                    
                    if research_topic:
                        logger.info(f"Frontend Developer researching: {research_topic}")
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
                    for param in ["thoroughness", "creativity", "risk_taking", 
                                 "design_focus", "accessibility_focus"]
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
                    "framework": task.get("framework", "React"),
                    "component_type": task.get("component_type", "")
                }
                
                # Get optimized prompt
                optimized_prompt = self.get_optimized_prompt(task_type, prompt_context)
                
                # Use this prompt for the LLM task
                system_message = f"You are {self.name}, a frontend developer specialized in building user interfaces."
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
        
        if task_type == "component_implementation":
            # Logic for component implementation tasks
            results["component"] = self._implement_component(task)
            
        elif task_type == "styling":
            # Logic for styling tasks
            results["styles"] = self._implement_styles(task)
            
        elif task_type == "frontend_integration":
            # Logic for integration tasks
            results["integration"] = self._integrate_with_backend(task)
        
        # Update metrics based on task execution
        self._update_metrics_from_task(task)
        
        return results
    
    def evaluate_performance(self) -> float:
        """Evaluate Frontend Developer agent's performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        # Weight factors for different metrics
        weights = {
            "code_quality": 0.3,
            "ui_responsiveness": 0.4,
            "accessibility": 0.3
        }
        
        # Calculate weighted performance score
        score = 0.0
        for metric, weight in weights.items():
            if metric in self.performance_metrics:
                # Normalize metric value to 0.0-1.0 range if needed
                metric_value = min(1.0, max(0.0, self.performance_metrics[metric]))
                score += metric_value * weight
        
        return score
    
    def _implement_component(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Implement a frontend component.
        
        Args:
            task: Task containing component requirements
            
        Returns:
            Component implementation details
        """
        component_type = task.get("component_type", "")
        requirements = task.get("requirements", [])
        framework = task.get("framework", "React")
        
        # Simple component implementation (placeholder implementation)
        code_snippet = """
        import React, { useState } from 'react';
        
        interface Props {
          // Component props
        }
        
        export const Component: React.FC<Props> = (props) => {
          const [state, setState] = useState();
          
          return (
            <div className="component">
              {/* Component content */}
            </div>
          );
        };
        """
        
        # TODO: Implement more sophisticated component generation logic
        
        return {
            "code": code_snippet,
            "framework": framework,
            "component_type": component_type,
            "test_coverage": True
        }
    
    def _implement_styles(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Implement styles for a component or view.
        
        Args:
            task: Task containing styling requirements
            
        Returns:
            Styling implementation details
        """
        component = task.get("component", "")
        style_type = task.get("style_type", "CSS")
        theme = task.get("theme", {})
        
        # Simple styling implementation (placeholder implementation)
        style_code = """
        .component {
          display: flex;
          flex-direction: column;
          padding: 1rem;
          border-radius: 4px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .component-header {
          font-size: 1.5rem;
          margin-bottom: 1rem;
        }
        
        .component-body {
          flex: 1;
        }
        """
        
        # TODO: Implement more sophisticated styling logic
        
        return {
            "code": style_code,
            "style_type": style_type,
            "responsive": True,
            "theme_compatibility": True
        }
    
    def _integrate_with_backend(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate frontend with backend services.
        
        Args:
            task: Task containing integration requirements
            
        Returns:
            Integration implementation details
        """
        apis = task.get("apis", [])
        auth_required = task.get("auth_required", False)
        data_format = task.get("data_format", "JSON")
        
        # Simple integration implementation (placeholder implementation)
        integration_code = """
        import axios from 'axios';
        
        const API_BASE_URL = process.env.REACT_APP_API_URL;
        
        export const fetchData = async () => {
          try {
            const response = await axios.get(`${API_BASE_URL}/endpoint`);
            return response.data;
          } catch (error) {
            console.error('Error fetching data:', error);
            throw error;
          }
        };
        """
        
        # TODO: Implement more sophisticated integration logic
        
        return {
            "code": integration_code,
            "apis_integrated": len(apis),
            "auth_handling": auth_required,
            "error_handling": True
        }
    
    def _update_metrics_from_task(self, task: Dict[str, Any]) -> None:
        """Update agent's performance metrics based on task execution.
        
        Args:
            task: Completed task
        """
        task_type = task.get("type", "")
        
        if task_type == "component_implementation":
            # Update metrics related to component implementation
            current = self.performance_metrics.get("code_quality", 0.0)
            self.update_metric("code_quality", current + 0.1)
            
        elif task_type == "styling":
            # Update metrics related to styling implementation
            current = self.performance_metrics.get("ui_responsiveness", 0.0)
            self.update_metric("ui_responsiveness", current + 0.1)
            
        elif task_type == "frontend_integration":
            # Update metrics related to integration implementation
            current = self.performance_metrics.get("accessibility", 0.0)
            self.update_metric("accessibility", current + 0.1)
