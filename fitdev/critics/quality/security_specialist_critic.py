#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Security Specialist Critic for FitDev.io
"""

from typing import Dict, Any, List
from models.critic import BaseCritic


class SecuritySpecialistCritic(BaseCritic):
    """Critic agent for evaluating Security Specialist's work."""
    
    def __init__(self, name: str = "Security Specialist Critic"):
        """Initialize the Security Specialist Critic agent.
        
        Args:
            name: Critic agent name (default: "Security Specialist Critic")
        """
        description = """Evaluates security assessments, code security reviews, and security 
                      implementations performed by the Security Specialist. Provides feedback 
                      on vulnerability detection, security best practices, and implementation quality."""
        super().__init__(name, "Security Specialist", description)
        
        # Add evaluation criteria specific to Security Specialist
        self.add_evaluation_criterion("Vulnerability Detection Thoroughness")
        self.add_evaluation_criterion("Risk Assessment Accuracy")
        self.add_evaluation_criterion("Secure Coding Practices")
        self.add_evaluation_criterion("Compliance with Security Standards")
        self.add_evaluation_criterion("Implementation Security")
        
        # Critic-specific performance metrics
        self.update_metric("security_expertise", 0.5)
        self.update_metric("implementation_review_quality", 0.5)
        self.update_metric("standards_knowledge", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the Security Specialist.
        
        Args:
            work_output: Work output and metadata from the Security Specialist
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "security_assessment":
            # Evaluate security assessment output
            assessment = work_output.get("assessment", {})
            
            # Check vulnerabilities
            vulnerabilities = assessment.get("vulnerabilities", [])
            if not vulnerabilities:
                feedback.append("No vulnerabilities identified in the assessment")
                suggestions.append("Use a more thorough approach to identify potential vulnerabilities")
                # No vulnerabilities could be legitimate, so neutral score
                score += 0.5
            else:
                feedback.append(f"Assessment identified {len(vulnerabilities)} vulnerabilities")
                score += 0.8
            
            # Check risk areas covered
            scope = assessment.get("scope", [])
            if not scope:
                feedback.append("Assessment lacks defined scope")
                suggestions.append("Clearly define the assessment scope")
                score += 0.2
            else:
                feedback.append(f"Assessment covers {len(scope)} areas in its scope")
                score += 0.7
            
            # Check recommendations
            recommendations = assessment.get("recommendations", [])
            if not recommendations:
                feedback.append("No security recommendations provided")
                suggestions.append("Always include specific security recommendations")
                score += 0.0
            elif len(recommendations) < 3:
                feedback.append("Limited security recommendations provided")
                suggestions.append("Provide more comprehensive security recommendations")
                score += 0.4
            else:
                feedback.append(f"Assessment includes {len(recommendations)} security recommendations")
                score += 0.9
            
            # Check overall risk level
            risk_level = assessment.get("overall_risk", "")
            if not risk_level:
                feedback.append("No overall risk level provided")
                suggestions.append("Include an overall risk assessment")
                score += 0.2
            else:
                feedback.append(f"Assessment provides overall risk level: {risk_level}")
                score += 0.8
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions for security assessment
            suggestions.append("Include threat modeling in the assessment")
            suggestions.append("Map vulnerabilities to OWASP Top 10 or other standards")
            suggestions.append("Add impact assessment for each vulnerability")
            suggestions.append("Prioritize recommendations based on risk level")
            
        elif task_type == "code_security_review":
            # Evaluate code security review output
            review = work_output.get("review", {})
            
            # Check findings
            findings = review.get("findings", [])
            # For code review, absence of findings could mean secure code
            files_reviewed = review.get("files_reviewed", 0)
            
            if files_reviewed <= 0:
                feedback.append("No files were reviewed")
                suggestions.append("Ensure files are properly reviewed")
                score += 0.0
            elif findings:
                feedback.append(f"Review identified {len(findings)} security issues across {files_reviewed} files")
                score += 0.8
            else:
                feedback.append(f"Review found no security issues in {files_reviewed} files")
                # Could be legitimate, but we should investigate further
                score += 0.6
                suggestions.append("Verify that no false negatives were missed")
            
            # Check for severity classifications
            has_severity = all("severity" in finding for finding in findings) if findings else False
            if findings and not has_severity:
                feedback.append("Security findings lack severity classifications")
                suggestions.append("Classify each finding by severity")
                score += 0.3
            elif findings:
                feedback.append("Security findings include severity classifications")
                score += 0.8
            
            # Check recommendations
            recommendations = review.get("recommendations", [])
            if not recommendations:
                feedback.append("No security recommendations provided")
                suggestions.append("Always include specific remediation recommendations")
                score += 0.0
            else:
                feedback.append(f"Review includes {len(recommendations)} security recommendations")
                score += 0.9
            
            # Normalize score
            score = score / 3.0  # Average of the aspects evaluated
            
            # Add specific suggestions for code security review
            suggestions.append("Include references to security standards")
            suggestions.append("Provide code examples for secure alternatives")
            suggestions.append("Add a summary of security debt in the codebase")
            suggestions.append("Suggest automated security scanning tools")
            
        elif task_type == "security_implementation":
            # Evaluate security implementation output
            implementation = work_output.get("implementation", {})
            
            # Check code
            code = implementation.get("code", "")
            if not code:
                feedback.append("No implementation code provided")
                suggestions.append("Provide actual implementation code")
                score += 0.0
            elif len(code.strip().split("\n")) < 10:
                feedback.append("Implementation code is minimal")
                suggestions.append("Develop more comprehensive security implementation")
                score += 0.3
            else:
                feedback.append("Implementation has a reasonable amount of code")
                score += 0.7
            
            # Check documentation
            docs = implementation.get("documentation", "")
            if not docs:
                feedback.append("No documentation provided for the security implementation")
                suggestions.append("Always document security implementations thoroughly")
                score += 0.0
            elif len(docs.strip().split("\n")) < 5:
                feedback.append("Limited documentation for security implementation")
                suggestions.append("Expand documentation with usage examples and security notes")
                score += 0.4
            else:
                feedback.append("Implementation includes good documentation")
                score += 0.9
            
            # Check compliance
            compliance = implementation.get("compliance", {})
            if not compliance:
                feedback.append("No compliance information provided")
                suggestions.append("Document compliance with security standards")
                score += 0.2
            else:
                standards = [standard for standard, compliant in compliance.items() if compliant]
                feedback.append(f"Implementation complies with {len(standards)} security standards")
                score += 0.8
            
            # Check feature type
            feature_type = implementation.get("feature_type", "")
            if not feature_type:
                feedback.append("Security feature type not specified")
                suggestions.append("Specify the type of security feature implemented")
                score += 0.3
            else:
                feedback.append(f"Implemented {feature_type} security feature")
                score += 0.7
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions for security implementation
            suggestions.append("Add unit tests for the security implementation")
            suggestions.append("Include edge case handling")
            suggestions.append("Consider rate limiting for authentication features")
            suggestions.append("Implement logging for security events")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("security_expertise", min(1.0, self.performance_metrics.get("security_expertise", 0.5) + 0.05))
        self.update_metric("implementation_review_quality", min(1.0, self.performance_metrics.get("implementation_review_quality", 0.5) + 0.05))
        self.update_metric("standards_knowledge", min(1.0, self.performance_metrics.get("standards_knowledge", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)