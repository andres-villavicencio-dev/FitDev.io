#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Knowledge Management Specialist Critic for FitDev.io
"""

from typing import Dict, Any, List
from fitdev.models.critic import BaseCritic


class KnowledgeManagementCritic(BaseCritic):
    """Critic agent for evaluating Knowledge Management Specialist's work."""
    
    def __init__(self, name: str = "Knowledge Management Critic"):
        """Initialize the Knowledge Management Critic agent.
        
        Args:
            name: Critic agent name (default: "Knowledge Management Critic")
        """
        description = """Evaluates knowledge bases, information architectures, and knowledge 
                      transfer plans created by the Knowledge Management Specialist. Provides 
                      feedback on accessibility, structure, and information quality."""
        super().__init__(name, "Knowledge Management Specialist", description)
        
        # Add evaluation criteria specific to Knowledge Management
        self.add_evaluation_criterion("Information Accessibility")
        self.add_evaluation_criterion("Knowledge Structure")
        self.add_evaluation_criterion("Information Quality")
        self.add_evaluation_criterion("Search Effectiveness")
        self.add_evaluation_criterion("Knowledge Transfer Effectiveness")
        
        # Critic-specific performance metrics
        self.update_metric("knowledge_assessment", 0.5)
        self.update_metric("structure_analysis", 0.5)
        self.update_metric("user_perspective", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the Knowledge Management Specialist.
        
        Args:
            work_output: Work output and metadata from the Knowledge Management Specialist
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "knowledge_base_creation":
            # Evaluate knowledge base output
            knowledge_base = work_output.get("knowledge_base", {})
            
            # Check structure
            sections = knowledge_base.get("sections", [])
            if not sections:
                feedback.append("Knowledge base lacks sections")
                suggestions.append("Create comprehensive sections covering key topics")
                score += 0.0
            elif len(sections) < 3:
                feedback.append("Knowledge base has minimal sections")
                suggestions.append("Expand with more detailed sections")
                score += 0.3
            else:
                feedback.append(f"Knowledge base has {len(sections)} sections")
                score += 0.8
            
            # Check search index
            search_index = knowledge_base.get("search_index", {})
            if not search_index:
                feedback.append("Search index is missing")
                suggestions.append("Implement a comprehensive search index")
                score += 0.0
            elif len(search_index.get("indexed_fields", [])) < 2:
                feedback.append("Search index has limited field coverage")
                suggestions.append("Index more fields for better search results")
                score += 0.4
            else:
                feedback.append("Search index has good field coverage")
                score += 0.9
            
            # Check metadata
            metadata = knowledge_base.get("metadata", {})
            if not metadata:
                feedback.append("Knowledge base lacks metadata")
                suggestions.append("Add comprehensive metadata")
                score += 0.2
            else:
                feedback.append("Knowledge base includes metadata")
                score += 0.7
            
            # Normalize score
            score = score / 3.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Add content quality guidelines for contributors")
            suggestions.append("Implement version control for knowledge base sections")
            suggestions.append("Create relationships between related sections")
            suggestions.append("Add user feedback mechanism for each section")
            
        elif task_type == "information_architecture":
            # Evaluate information architecture output
            architecture = work_output.get("architecture", {})
            
            # Check content models
            content_models = architecture.get("content_models", [])
            if not content_models:
                feedback.append("No content models defined")
                suggestions.append("Define comprehensive content models")
                score += 0.0
            elif len(content_models) < 2:
                feedback.append("Limited content models defined")
                suggestions.append("Expand content models to cover more content types")
                score += 0.4
            else:
                feedback.append(f"Architecture includes {len(content_models)} content models")
                score += 0.8
            
            # Check navigation
            navigation = architecture.get("navigation", {})
            main_nav = navigation.get("main_navigation", [])
            if not main_nav:
                feedback.append("No navigation structure defined")
                suggestions.append("Create a comprehensive navigation structure")
                score += 0.0
            elif len(main_nav) < 3:
                feedback.append("Limited navigation structure")
                suggestions.append("Expand navigation to improve information findability")
                score += 0.3
            else:
                feedback.append(f"Navigation structure includes {len(main_nav)} main items")
                score += 0.9
            
            # Check permissions
            permissions = architecture.get("permissions", {})
            if not permissions:
                feedback.append("No permission structure defined")
                suggestions.append("Define comprehensive permission structure")
                score += 0.0
            else:
                feedback.append(f"Permission structure covers {len(permissions)} user roles")
                score += 0.8
            
            # Normalize score
            score = score / 3.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Implement breadcrumb navigation for deeper content")
            suggestions.append("Add content relationship model to connect related items")
            suggestions.append("Create tagging system for improved cross-referencing")
            suggestions.append("Define a content governance model")
            
        elif task_type == "knowledge_transfer":
            # Evaluate knowledge transfer output
            transfer = work_output.get("transfer", {})
            
            # Check transfer activities
            activities = transfer.get("transfer_activities", [])
            if not activities:
                feedback.append("No knowledge transfer activities defined")
                suggestions.append("Define comprehensive transfer activities")
                score += 0.0
            elif len(activities) < 2:
                feedback.append("Limited knowledge transfer activities")
                suggestions.append("Expand activities to cover more knowledge areas")
                score += 0.4
            else:
                feedback.append(f"Transfer plan includes activities for {len(activities)} knowledge areas")
                score += 0.8
            
            # Check success criteria
            criteria = transfer.get("success_criteria", [])
            if not criteria:
                feedback.append("No success criteria defined")
                suggestions.append("Define measurable success criteria")
                score += 0.0
            elif len(criteria) < activities:
                feedback.append("Success criteria don't cover all knowledge areas")
                suggestions.append("Define success criteria for each knowledge area")
                score += 0.5
            else:
                feedback.append("Success criteria defined for all knowledge areas")
                score += 0.9
            
            # Check overall plan completeness
            has_duration = "total_duration" in transfer
            has_source_target = "source" in transfer and "target" in transfer
            
            if not has_duration or not has_source_target:
                feedback.append("Transfer plan is missing key elements")
                suggestions.append("Include duration estimates and clearly identify source and target")
                score += 0.3
            else:
                feedback.append("Transfer plan includes all key elements")
                score += 0.8
            
            # Normalize score
            score = score / 3.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Add knowledge verification steps to ensure successful transfer")
            suggestions.append("Include documentation for each knowledge area")
            suggestions.append("Define support period after knowledge transfer completion")
            suggestions.append("Create knowledge retention strategy")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("knowledge_assessment", min(1.0, self.performance_metrics.get("knowledge_assessment", 0.5) + 0.05))
        self.update_metric("structure_analysis", min(1.0, self.performance_metrics.get("structure_analysis", 0.5) + 0.05))
        self.update_metric("user_perspective", min(1.0, self.performance_metrics.get("user_perspective", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)