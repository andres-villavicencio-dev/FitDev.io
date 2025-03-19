#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API Specialist Critic for FitDev.io
"""

from typing import Dict, Any, List
from models.critic import BaseCritic


class APISpecialistCritic(BaseCritic):
    """Critic agent for evaluating API Specialist's work."""
    
    def __init__(self, name: str = "API Specialist Critic"):
        """Initialize the API Specialist Critic agent.
        
        Args:
            name: Critic agent name (default: "API Specialist Critic")
        """
        description = """Evaluates API designs, documentation, security reviews, and versioning 
                      strategies produced by the API Specialist. Provides feedback on best practices, 
                      standards compliance, and developer experience."""
        super().__init__(name, "API Specialist", description)
        
        # Add evaluation criteria specific to API Specialist
        self.add_evaluation_criterion("API Design Quality")
        self.add_evaluation_criterion("Documentation Completeness")
        self.add_evaluation_criterion("Security Implementation")
        self.add_evaluation_criterion("Versioning Strategy")
        self.add_evaluation_criterion("Developer Experience")
        
        # Critic-specific performance metrics
        self.update_metric("standards_knowledge", 0.5)
        self.update_metric("security_expertise", 0.5)
        self.update_metric("implementation_feasibility", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the API Specialist.
        
        Args:
            work_output: Work output and metadata from the API Specialist
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "api_design":
            # Evaluate API design output
            api_design = work_output.get("api_design", {})
            
            # Check API design components
            endpoints = api_design.get("endpoints", [])
            schemas = api_design.get("schemas", [])
            principles = api_design.get("principles", [])
            
            # Evaluate endpoints
            if not endpoints:
                feedback.append("API design contains no endpoints")
                suggestions.append("Define core API endpoints with complete request/response details")
                score += 0.0
            elif len(endpoints) < 3:
                feedback.append("API design contains minimal endpoints")
                suggestions.append("Expand API with more comprehensive endpoint coverage")
                score += 0.4
            else:
                feedback.append(f"API design includes {len(endpoints)} endpoints")
                score += 0.8
            
            # Evaluate schemas/models
            if not schemas:
                feedback.append("API design lacks data models/schemas")
                suggestions.append("Define data models with property details")
                score += 0.0
            elif any(not schema.get("properties") for schema in schemas):
                feedback.append("Some schemas lack property definitions")
                suggestions.append("Add detailed properties to all schemas")
                score += 0.5
            else:
                feedback.append(f"API design includes {len(schemas)} well-defined schemas")
                score += 0.9
            
            # Evaluate design principles
            if not principles:
                feedback.append("No API design principles provided")
                suggestions.append("Include API design principles and standards")
                score += 0.2
            elif len(principles) < 5:
                feedback.append("Limited API design principles")
                suggestions.append("Expand design principles to cover more best practices")
                score += 0.6
            else:
                feedback.append(f"Design includes {len(principles)} principles")
                score += 0.9
            
            # Check for RESTful principles if REST API
            if api_design.get("api_type") == "REST":
                # Look for indications of RESTful design
                has_resource_endpoints = any("/" in endpoint.get("path", "") for endpoint in endpoints)
                has_http_methods = any(endpoint.get("method") in ["GET", "POST", "PUT", "DELETE"] for endpoint in endpoints)
                has_status_codes = any(response.get("status") for endpoint in endpoints for response in endpoint.get("responses", []))
                
                restful_score = sum([has_resource_endpoints, has_http_methods, has_status_codes]) / 3.0
                
                if restful_score < 0.5:
                    feedback.append("Design does not fully follow RESTful principles")
                    suggestions.append("Ensure design follows RESTful principles for resource identification, HTTP methods, and status codes")
                    score += 0.3
                else:
                    feedback.append("Design follows RESTful principles")
                    score += 0.9
            
            # Check for GraphQL principles if GraphQL API
            elif api_design.get("api_type") == "GraphQL":
                # Check for GraphQL-specific elements
                has_queries = any(endpoint.get("type") == "Query" for endpoint in endpoints)
                has_mutations = any(endpoint.get("type") == "Mutation" for endpoint in endpoints)
                has_types = len(schemas) > 0
                
                graphql_score = sum([has_queries, has_mutations, has_types]) / 3.0
                
                if graphql_score < 0.5:
                    feedback.append("Design does not fully follow GraphQL principles")
                    suggestions.append("Ensure design includes proper Query and Mutation types")
                    score += 0.3
                else:
                    feedback.append("Design follows GraphQL principles")
                    score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Add pagination for collection endpoints")
            suggestions.append("Include comprehensive error response schemas")
            suggestions.append("Ensure consistent naming conventions across endpoints")
            suggestions.append("Add filtering and sorting capabilities to list endpoints")
            
        elif task_type == "api_documentation":
            # Evaluate API documentation output
            documentation = work_output.get("documentation", {})
            
            # Check documentation components
            sections = documentation.get("sections", [])
            info = documentation.get("info", {})
            
            # Evaluate info section
            if not info or not info.get("title") or not info.get("description"):
                feedback.append("API documentation missing basic information")
                suggestions.append("Include complete API title, description, and version information")
                score += 0.0
            else:
                feedback.append("Documentation includes basic API information")
                score += 0.8
            
            # Evaluate sections coverage
            required_sections = ["Introduction", "Getting Started", "API Reference"]
            
            section_titles = [section.get("title") for section in sections]
            
            missing_sections = [section for section in required_sections if section not in section_titles]
            
            if missing_sections:
                feedback.append(f"Documentation missing important sections: {', '.join(missing_sections)}")
                suggestions.append(f"Add missing sections: {', '.join(missing_sections)}")
                score += 0.3
            else:
                feedback.append("Documentation covers all essential sections")
                score += 0.9
            
            # Evaluate content depth
            shallow_sections = []
            for section in sections:
                content = section.get("content", "")
                if len(content) < 200:  # Arbitrary threshold for minimal content
                    shallow_sections.append(section.get("title"))
            
            if shallow_sections:
                feedback.append(f"These sections lack depth: {', '.join(shallow_sections)}")
                suggestions.append("Expand content in shallow sections with more details and examples")
                score += 0.4
            else:
                feedback.append("All sections have substantial content")
                score += 0.9
            
            # Check for examples
            has_examples = any("example" in section.get("content", "").lower() for section in sections)
            
            if not has_examples:
                feedback.append("Documentation lacks usage examples")
                suggestions.append("Add code examples for API usage")
                score += 0.2
            else:
                feedback.append("Documentation includes usage examples")
                score += 0.8
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Add a quick start guide with complete example")
            suggestions.append("Include authentication and error handling sections")
            suggestions.append("Add interactive API explorer if possible")
            suggestions.append("Include rate limiting and throttling information")
            
        elif task_type == "api_security_review":
            # Evaluate API security review output
            security_review = work_output.get("security_review", {})
            
            # Check security review components
            issues = security_review.get("issues", [])
            recommendations = security_review.get("recommendations", [])
            compliance = security_review.get("compliance", {})
            
            # Evaluate security issues
            if not issues:
                feedback.append("Security review identified no issues")
                suggestions.append("Conduct deeper analysis to identify potential vulnerabilities")
                score += 0.3
            elif len(issues) < 3:
                feedback.append("Security review found limited issues")
                suggestions.append("Expand security analysis to cover more vulnerability categories")
                score += 0.6
            else:
                feedback.append(f"Security review identified {len(issues)} issues")
                score += 0.9
            
            # Evaluate recommendations quality
            if not recommendations:
                feedback.append("No security recommendations provided")
                suggestions.append("Provide actionable security recommendations")
                score += 0.0
            elif len(recommendations) < issues:
                feedback.append("Not all security issues have corresponding recommendations")
                suggestions.append("Ensure each security issue has at least one recommendation")
                score += 0.5
            else:
                feedback.append(f"Review provides {len(recommendations)} security recommendations")
                score += 0.9
            
            # Evaluate compliance coverage
            critical_security_controls = ["oauth2", "https", "input_validation", "rate_limiting"]
            
            missing_controls = [control for control in critical_security_controls 
                              if control in compliance and not compliance[control]]
            
            if missing_controls:
                feedback.append(f"Critical security controls missing: {', '.join(missing_controls)}")
                suggestions.append(f"Address missing security controls: {', '.join(missing_controls)}")
                score += 0.3
            else:
                feedback.append("All critical security controls addressed")
                score += 0.9
            
            # Check severity classification
            has_severity = all("severity" in issue for issue in issues)
            
            if not has_severity:
                feedback.append("Security issues lack severity classifications")
                suggestions.append("Classify issues by severity to prioritize remediation")
                score += 0.4
            else:
                feedback.append("Security issues include severity classifications")
                score += 0.8
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Include compliance requirements (GDPR, PCI DSS, etc.) if applicable")
            suggestions.append("Add security testing methodologies and tools")
            suggestions.append("Include a security incident response plan")
            suggestions.append("Recommend security monitoring and logging practices")
            
        elif task_type == "api_versioning_strategy":
            # Evaluate API versioning strategy output
            versioning = work_output.get("versioning_strategy", {})
            
            # Check versioning strategy components
            strategies = versioning.get("versioning_strategies", [])
            recommended_strategy = versioning.get("recommended_strategy", {})
            versioning_process = versioning.get("versioning_process", {})
            
            # Evaluate versioning strategies
            if not strategies:
                feedback.append("No versioning strategies presented")
                suggestions.append("Present multiple versioning approaches with pros and cons")
                score += 0.0
            elif len(strategies) < 2:
                feedback.append("Limited versioning strategy options")
                suggestions.append("Expand options with more versioning approaches")
                score += 0.5
            else:
                feedback.append(f"Strategy includes {len(strategies)} versioning approaches")
                score += 0.9
            
            # Evaluate recommended strategy
            if not recommended_strategy:
                feedback.append("No specific versioning strategy recommended")
                suggestions.append("Provide a clear recommendation with justification")
                score += 0.0
            elif not recommended_strategy.get("pros") or not recommended_strategy.get("cons"):
                feedback.append("Recommended strategy lacks pros/cons analysis")
                suggestions.append("Include detailed pros and cons for the recommended strategy")
                score += 0.5
            else:
                feedback.append("Strategy includes clear recommendation with pros/cons")
                score += 0.9
            
            # Evaluate versioning process
            if not versioning_process:
                feedback.append("No versioning process defined")
                suggestions.append("Define a clear versioning process and timeline")
                score += 0.0
            elif not versioning_process.get("semantic_versioning") or not versioning_process.get("deprecation_policy"):
                feedback.append("Versioning process missing key components")
                suggestions.append("Include semantic versioning rules and deprecation policy")
                score += 0.5
            else:
                feedback.append("Strategy includes comprehensive versioning process")
                score += 0.9
            
            # Check for backward compatibility considerations
            has_compatibility = "compatibility_matrix" in versioning or any("backward" in str(strategy).lower() for strategy in strategies)
            
            if not has_compatibility:
                feedback.append("Strategy lacks backward compatibility considerations")
                suggestions.append("Address backward compatibility concerns in the versioning strategy")
                score += 0.3
            else:
                feedback.append("Strategy addresses backward compatibility")
                score += 0.8
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Include client migration guidance for version transitions")
            suggestions.append("Add version sunset policy and communication plan")
            suggestions.append("Consider automated version compatibility testing")
            suggestions.append("Include version discovery mechanism for clients")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("standards_knowledge", min(1.0, self.performance_metrics.get("standards_knowledge", 0.5) + 0.05))
        self.update_metric("security_expertise", min(1.0, self.performance_metrics.get("security_expertise", 0.5) + 0.05))
        self.update_metric("implementation_feasibility", min(1.0, self.performance_metrics.get("implementation_feasibility", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)