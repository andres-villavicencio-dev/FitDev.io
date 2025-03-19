#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DevOps Engineer Critic for FitDev.io
"""

from typing import Dict, Any, List
from models.critic import BaseCritic


class DevOpsEngineerCritic(BaseCritic):
    """Critic agent for evaluating DevOps Engineer's work."""
    
    def __init__(self, name: str = "DevOps Engineer Critic"):
        """Initialize the DevOps Engineer Critic agent.
        
        Args:
            name: Critic agent name (default: "DevOps Engineer Critic")
        """
        description = """Evaluates infrastructure setup, CI/CD pipelines, and monitoring 
                        configuration by the DevOps Engineer. Provides feedback on 
                        infrastructure quality, deployment reliability, and automation 
                        coverage."""
        super().__init__(name, "DevOps Engineer", description)
        
        # Add evaluation criteria specific to DevOps Engineer
        self.add_evaluation_criterion("Infrastructure as Code Quality")
        self.add_evaluation_criterion("CI/CD Pipeline Completeness")
        self.add_evaluation_criterion("Security Configuration")
        self.add_evaluation_criterion("Monitoring Coverage")
        self.add_evaluation_criterion("Automation Efficiency")
        
        # Critic-specific performance metrics
        self.update_metric("infrastructure_review_quality", 0.5)
        self.update_metric("devops_best_practices", 0.5)
        self.update_metric("security_insight", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the DevOps Engineer.
        
        Args:
            work_output: Work output and metadata from the DevOps Engineer
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "infrastructure_setup":
            # Evaluate infrastructure setup output
            infrastructure = work_output.get("infrastructure", {})
            
            # Check code
            code = infrastructure.get("code", "")
            if not code:
                feedback.append("No infrastructure code provided")
                suggestions.append("Implement infrastructure as code")
                score += 0.0
            elif len(code.strip().split("\n")) < 20:
                feedback.append("Infrastructure implementation is minimal")
                suggestions.append("Develop more comprehensive infrastructure code")
                score += 0.3
            else:
                feedback.append("Infrastructure has a reasonable implementation")
                score += 0.7
            
            # Check cloud provider
            cloud_provider = infrastructure.get("cloud_provider", "")
            if not cloud_provider:
                feedback.append("Cloud provider not specified")
                suggestions.append("Specify which cloud provider is being used")
                score += 0.2
            else:
                feedback.append(f"Infrastructure uses {cloud_provider}")
                score += 0.8
            
            # Check IaC tool
            iac_tool = infrastructure.get("iac_tool", "")
            if not iac_tool:
                feedback.append("Infrastructure as Code tool not specified")
                suggestions.append("Specify which IaC tool is being used (Terraform, CloudFormation, etc.)")
                score += 0.2
            else:
                feedback.append(f"Infrastructure uses {iac_tool} for provisioning")
                score += 0.8
            
            # Check resources created
            resources = infrastructure.get("resources_created", 0)
            if resources <= 0:
                feedback.append("No resources defined in the infrastructure")
                suggestions.append("Define the necessary cloud resources")
                score += 0.0
            elif resources < 3:
                feedback.append("Limited resource definition")
                suggestions.append("Add more resource definitions for a complete environment")
                score += 0.4
            else:
                feedback.append(f"Infrastructure defines {resources} resources")
                score += 0.8
            
            # Check security compliance
            security_compliant = infrastructure.get("security_compliant", False)
            if not security_compliant:
                feedback.append("Infrastructure lacks security considerations")
                suggestions.append("Add security configurations and compliance measures")
                score += 0.0
            else:
                feedback.append("Infrastructure includes security compliance measures")
                score += 0.9
            
            # Normalize score
            score = score / 5.0  # Average of the five aspects
            
            # Add more specific suggestions
            suggestions.append("Use variables for environment-specific configurations")
            suggestions.append("Add output values for important resource identifiers")
            suggestions.append("Consider implementing a modular infrastructure design")
            suggestions.append("Add tagging strategy for resource management")
            
        elif task_type == "ci_cd_implementation":
            # Evaluate CI/CD implementation output
            pipeline = work_output.get("pipeline", {})
            
            # Check code
            code = pipeline.get("code", "")
            if not code:
                feedback.append("No CI/CD pipeline code provided")
                suggestions.append("Implement CI/CD pipeline configuration")
                score += 0.0
            elif len(code.strip().split("\n")) < 30:
                feedback.append("CI/CD implementation is minimal")
                suggestions.append("Develop more comprehensive pipeline configuration")
                score += 0.3
            else:
                feedback.append("CI/CD pipeline has a reasonable implementation")
                score += 0.7
            
            # Check CI tool
            ci_tool = pipeline.get("ci_tool", "")
            if not ci_tool:
                feedback.append("CI/CD tool not specified")
                suggestions.append("Specify which CI/CD tool is being used")
                score += 0.2
            else:
                feedback.append(f"Pipeline uses {ci_tool}")
                score += 0.8
            
            # Check pipeline stages
            stages = pipeline.get("stages", 0)
            if stages <= 0:
                feedback.append("No pipeline stages defined")
                suggestions.append("Define stages for the CI/CD pipeline")
                score += 0.0
            elif stages < 3:
                feedback.append("Pipeline has minimal stages")
                suggestions.append("Add more stages for comprehensive CI/CD")
                score += 0.4
            else:
                feedback.append(f"Pipeline includes {stages} stages")
                score += 0.9
            
            # Check deployment environments
            environments = pipeline.get("environments", 0)
            if environments <= 0:
                feedback.append("No deployment environments defined")
                suggestions.append("Define target environments for deployment")
                score += 0.0
            elif environments < 2:
                feedback.append("Pipeline only targets a single environment")
                suggestions.append("Add more environments (e.g., dev, staging, prod)")
                score += 0.5
            else:
                feedback.append(f"Pipeline targets {environments} environments")
                score += 0.9
            
            # Check automated tests
            automated_tests = pipeline.get("automated_tests", False)
            if not automated_tests:
                feedback.append("Pipeline lacks automated tests")
                suggestions.append("Add automated testing to the pipeline")
                score += 0.0
            else:
                feedback.append("Pipeline includes automated testing")
                score += 0.9
            
            # Normalize score
            score = score / 5.0  # Average of the five aspects
            
            # Add more specific suggestions
            suggestions.append("Implement branch-specific pipeline behaviors")
            suggestions.append("Add quality checks (linting, security scanning)")
            suggestions.append("Consider implementing deployment approvals for production")
            suggestions.append("Add post-deployment verification steps")
            
        elif task_type == "monitoring_setup":
            # Evaluate monitoring setup output
            monitoring = work_output.get("monitoring", {})
            
            # Check config code
            config_code = monitoring.get("config_code", "")
            if not config_code:
                feedback.append("No monitoring configuration provided")
                suggestions.append("Implement monitoring configuration")
                score += 0.0
            elif len(config_code.strip().split("\n")) < 15:
                feedback.append("Monitoring configuration is minimal")
                suggestions.append("Develop more comprehensive monitoring configuration")
                score += 0.3
            else:
                feedback.append("Monitoring has a reasonable configuration")
                score += 0.7
            
            # Check alert code
            alert_code = monitoring.get("alert_code", "")
            if not alert_code:
                feedback.append("No alerting configuration provided")
                suggestions.append("Implement alerting rules")
                score += 0.0
            elif len(alert_code.strip().split("\n")) < 15:
                feedback.append("Alerting configuration is minimal")
                suggestions.append("Develop more comprehensive alerting rules")
                score += 0.3
            else:
                feedback.append("Alerting has a reasonable configuration")
                score += 0.7
            
            # Check monitoring tool
            monitoring_tool = monitoring.get("monitoring_tool", "")
            if not monitoring_tool:
                feedback.append("Monitoring tool not specified")
                suggestions.append("Specify which monitoring tool is being used")
                score += 0.2
            else:
                feedback.append(f"Monitoring uses {monitoring_tool}")
                score += 0.8
            
            # Check metrics monitored
            metrics = monitoring.get("metrics_monitored", 0)
            if metrics <= 0:
                feedback.append("No metrics defined for monitoring")
                suggestions.append("Define specific metrics to monitor")
                score += 0.0
            elif metrics < 5:
                feedback.append("Limited metrics monitored")
                suggestions.append("Add more metrics for comprehensive monitoring")
                score += 0.4
            else:
                feedback.append(f"Monitoring covers {metrics} metrics")
                score += 0.9
            
            # Check alert channels
            alert_channels = monitoring.get("alert_channels", 0)
            if alert_channels <= 0:
                feedback.append("No alert notification channels defined")
                suggestions.append("Configure alert notification channels")
                score += 0.0
            else:
                feedback.append(f"Alerting is configured with {alert_channels} notification channels")
                score += 0.8
            
            # Normalize score
            score = score / 5.0  # Average of the five aspects
            
            # Add more specific suggestions
            suggestions.append("Add dashboards for key metrics visualization")
            suggestions.append("Implement alert severity levels")
            suggestions.append("Consider adding SLO/SLI monitoring")
            suggestions.append("Add log aggregation and analysis")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("infrastructure_review_quality", min(1.0, self.performance_metrics.get("infrastructure_review_quality", 0.5) + 0.05))
        self.update_metric("devops_best_practices", min(1.0, self.performance_metrics.get("devops_best_practices", 0.5) + 0.05))
        self.update_metric("security_insight", min(1.0, self.performance_metrics.get("security_insight", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)
