#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Technical Writer Critic for FitDev.io
"""

from typing import Dict, Any, List
from models.critic import BaseCritic


class TechnicalWriterCritic(BaseCritic):
    """Critic agent for evaluating Technical Writer's work."""
    
    def __init__(self, name: str = "Technical Writer Critic"):
        """Initialize the Technical Writer Critic agent.
        
        Args:
            name: Critic agent name (default: "Technical Writer Critic")
        """
        description = """Evaluates documentation created by the Technical Writer.
                      Provides feedback on clarity, completeness, accuracy, and
                      organization of technical documentation."""
        super().__init__(name, "Technical Writer", description)
        
        # Add evaluation criteria specific to Technical Writer
        self.add_evaluation_criterion("Clarity and Readability")
        self.add_evaluation_criterion("Technical Accuracy")
        self.add_evaluation_criterion("Completeness")
        self.add_evaluation_criterion("Structure and Organization")
        self.add_evaluation_criterion("Audience Appropriateness")
        
        # Critic-specific performance metrics
        self.update_metric("documentation_analysis", 0.5)
        self.update_metric("content_quality_assessment", 0.5)
        self.update_metric("audience_awareness", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the Technical Writer.
        
        Args:
            work_output: Work output and metadata from the Technical Writer
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "api_documentation":
            # Evaluate API documentation output
            documentation = work_output.get("documentation", {})
            
            # Check title and content
            title = documentation.get("title", "")
            content = documentation.get("content", "")
            
            if not title or not content:
                feedback.append("Documentation is missing title or content")
                suggestions.append("Ensure documentation has a clear title and substantive content")
                score += 0.0
            elif len(content.split()) < 100:
                feedback.append("API documentation is too brief")
                suggestions.append("Expand documentation with more details and examples")
                score += 0.3
            else:
                feedback.append("Documentation has appropriate length and structure")
                score += 0.8
            
            # Check endpoints documented
            endpoints_documented = documentation.get("endpoints_documented", 0)
            if endpoints_documented <= 0:
                feedback.append("No API endpoints are documented")
                suggestions.append("Document all API endpoints with their parameters and responses")
                score += 0.0
            else:
                feedback.append(f"Documentation covers {endpoints_documented} API endpoints")
                score += 0.7
                
                # Check for completeness
                if "## Authentication" not in content:
                    feedback.append("Authentication section is missing or incomplete")
                    suggestions.append("Add detailed authentication information")
                    score += 0.0
                else:
                    feedback.append("Documentation includes authentication information")
                    score += 0.8
                
                if "## Error Codes" not in content:
                    feedback.append("Error codes section is missing")
                    suggestions.append("Add a comprehensive error codes section")
                    score += 0.3
                else:
                    feedback.append("Documentation includes error codes section")
                    score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions for API documentation
            suggestions.append("Add more code examples showing real-world API usage")
            suggestions.append("Include request/response examples for each endpoint")
            suggestions.append("Add rate limiting information")
            suggestions.append("Include versioning information")
            
        elif task_type == "user_guide":
            # Evaluate user guide output
            guide = work_output.get("guide", {})
            
            # Check title and content
            title = guide.get("title", "")
            content = guide.get("content", "")
            
            if not title or not content:
                feedback.append("User guide is missing title or content")
                suggestions.append("Ensure guide has a clear title and substantive content")
                score += 0.0
            elif len(content.split()) < 200:
                feedback.append("User guide is too brief for comprehensive coverage")
                suggestions.append("Expand guide with more details and examples")
                score += 0.3
            else:
                feedback.append("User guide has appropriate length and structure")
                score += 0.8
            
            # Check features documented
            features_documented = guide.get("features_documented", 0)
            if features_documented <= 0:
                feedback.append("No features are documented in the user guide")
                suggestions.append("Document all key features with instructions")
                score += 0.0
            else:
                feedback.append(f"Guide covers {features_documented} features")
                score += 0.7
            
            # Check audience appropriateness
            audience = guide.get("target_audience", "")
            if not audience:
                feedback.append("Target audience is not specified")
                suggestions.append("Clearly define the target audience")
                score += 0.4
            else:
                feedback.append(f"Guide is targeted for {audience}")
                score += 0.8
                
                # Check if content matches audience
                if "end users" in audience.lower() and "code" in content.lower():
                    feedback.append("Guide contains technical code examples inappropriate for end users")
                    suggestions.append("Adapt content to be more accessible to non-technical users")
                    score += 0.4
                elif "developers" in audience.lower() and "code" not in content.lower():
                    feedback.append("Guide lacks technical details needed for developers")
                    suggestions.append("Add code examples and technical details for developer audience")
                    score += 0.4
            
            # Check for troubleshooting section
            if "## Troubleshooting" not in content:
                feedback.append("Troubleshooting section is missing")
                suggestions.append("Add a comprehensive troubleshooting section")
                score += 0.3
            else:
                feedback.append("Guide includes troubleshooting information")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions for user guides
            suggestions.append("Add a table of contents for easier navigation")
            suggestions.append("Include more screenshots to illustrate UI elements")
            suggestions.append("Add a glossary of terms")
            suggestions.append("Create a quick-start section for new users")
            
        elif task_type == "developer_documentation":
            # Evaluate developer documentation output
            documentation = work_output.get("documentation", {})
            
            # Check title and content
            title = documentation.get("title", "")
            content = documentation.get("content", "")
            
            if not title or not content:
                feedback.append("Developer documentation is missing title or content")
                suggestions.append("Ensure documentation has a clear title and substantive content")
                score += 0.0
            elif len(content.split()) < 300:
                feedback.append("Developer documentation is too brief for comprehensive coverage")
                suggestions.append("Expand documentation with more technical details")
                score += 0.3
            else:
                feedback.append("Documentation has appropriate length and structure")
                score += 0.8
            
            # Check modules documented
            modules_documented = documentation.get("modules_documented", 0)
            if modules_documented <= 0:
                feedback.append("No modules are documented")
                suggestions.append("Document all key modules with their classes and methods")
                score += 0.0
            else:
                feedback.append(f"Documentation covers {modules_documented} modules")
                score += 0.7
            
            # Check for architecture section
            if "## Architecture" not in content:
                feedback.append("Architecture section is missing or incomplete")
                suggestions.append("Add detailed architecture information with diagrams")
                score += 0.2
            else:
                feedback.append("Documentation includes architecture information")
                score += 0.8
            
            # Check for development setup section
            if "## Development Setup" not in content:
                feedback.append("Development setup section is missing")
                suggestions.append("Add comprehensive setup instructions")
                score += 0.2
            else:
                feedback.append("Documentation includes development setup instructions")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions for developer documentation
            suggestions.append("Add class inheritance diagrams")
            suggestions.append("Include performance considerations")
            suggestions.append("Add examples for common use cases")
            suggestions.append("Document API version compatibility")
            suggestions.append("Include contribution guidelines")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("documentation_analysis", min(1.0, self.performance_metrics.get("documentation_analysis", 0.5) + 0.05))
        self.update_metric("content_quality_assessment", min(1.0, self.performance_metrics.get("content_quality_assessment", 0.5) + 0.05))
        self.update_metric("audience_awareness", min(1.0, self.performance_metrics.get("audience_awareness", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)