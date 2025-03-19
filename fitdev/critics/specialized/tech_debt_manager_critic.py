#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tech Debt Manager Critic for FitDev.io
"""

from typing import Dict, Any, List
from models.critic import BaseCritic


class TechDebtManagerCritic(BaseCritic):
    """Critic agent for evaluating Tech Debt Manager's work."""
    
    def __init__(self, name: str = "Tech Debt Manager Critic"):
        """Initialize the Tech Debt Manager Critic agent.
        
        Args:
            name: Critic agent name (default: "Tech Debt Manager Critic")
        """
        description = """Evaluates technical debt assessments, refactoring plans, debt prioritization, 
                      and architecture evaluations produced by the Tech Debt Manager. Provides feedback 
                      on thoroughness, actionability, and business alignment."""
        super().__init__(name, "Tech Debt Manager", description)
        
        # Add evaluation criteria specific to Tech Debt Manager
        self.add_evaluation_criterion("Assessment Completeness")
        self.add_evaluation_criterion("Prioritization Effectiveness")
        self.add_evaluation_criterion("Plan Feasibility")
        self.add_evaluation_criterion("Business Alignment")
        self.add_evaluation_criterion("Technical Accuracy")
        
        # Critic-specific performance metrics
        self.update_metric("technical_insight", 0.5)
        self.update_metric("pragmatic_approach", 0.5)
        self.update_metric("business_perspective", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the Tech Debt Manager.
        
        Args:
            work_output: Work output and metadata from the Tech Debt Manager
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "tech_debt_assessment":
            # Evaluate technical debt assessment output
            assessment = work_output.get("assessment", {})
            
            # Check assessment completeness
            findings_by_category = assessment.get("findings_by_category", {})
            recommendations = assessment.get("recommendations", [])
            
            # Evaluate category coverage
            essential_categories = ["Code Quality", "Architecture", "Test Coverage", "Documentation", "Dependency Management"]
            covered_categories = set(findings_by_category.keys())
            
            missing_categories = [cat for cat in essential_categories if cat not in covered_categories]
            
            if missing_categories:
                feedback.append(f"Assessment missing analysis in these areas: {', '.join(missing_categories)}")
                suggestions.append(f"Include analysis for missing categories: {', '.join(missing_categories)}")
                score += 0.3
            else:
                feedback.append("Assessment covers all essential technical debt categories")
                score += 0.9
            
            # Evaluate findings detail
            all_findings = []
            for category_findings in findings_by_category.values():
                all_findings.extend(category_findings)
            
            if not all_findings:
                feedback.append("Assessment contains no specific findings")
                suggestions.append("Include detailed findings with specific locations and severity")
                score += 0.0
            elif len(all_findings) < 5:
                feedback.append("Assessment contains minimal findings")
                suggestions.append("Expand assessment depth to uncover more technical debt items")
                score += 0.4
            else:
                feedback.append(f"Assessment includes {len(all_findings)} technical debt findings")
                score += 0.8
            
            # Check finding quality
            detailed_findings = 0
            for finding in all_findings:
                # Check if finding has key attributes
                has_location = "location" in finding
                has_severity = "severity" in finding
                has_remediation = "remediation" in finding
                
                if has_location and has_severity and has_remediation:
                    detailed_findings += 1
            
            if detailed_findings < len(all_findings) * 0.7:  # Less than 70% are detailed
                feedback.append("Many findings lack necessary details")
                suggestions.append("Ensure all findings include location, severity, and remediation guidance")
                score += 0.4
            else:
                feedback.append("Findings include good detail and remediation guidance")
                score += 0.9
            
            # Check recommendations
            if not recommendations:
                feedback.append("Assessment lacks actionable recommendations")
                suggestions.append("Include specific, actionable recommendations based on findings")
                score += 0.0
            elif len(recommendations) < 3:
                feedback.append("Limited recommendations provided")
                suggestions.append("Expand recommendations to cover more debt categories")
                score += 0.5
            else:
                feedback.append(f"Assessment includes {len(recommendations)} recommendations")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Include quantitative metrics like code coverage percentage")
            suggestions.append("Add trend analysis to show how debt is evolving over time")
            suggestions.append("Link findings to business impact for better prioritization")
            suggestions.append("Include estimation of remediation effort for each category")
            
        elif task_type == "refactoring_plan":
            # Evaluate refactoring plan output
            refactoring_plan = work_output.get("refactoring_plan", {})
            
            # Check plan components
            phases = refactoring_plan.get("phases", [])
            risks = refactoring_plan.get("risks_and_mitigations", [])
            
            # Evaluate phase structure
            if not phases:
                feedback.append("Refactoring plan contains no execution phases")
                suggestions.append("Define clear phases with timelines and specific tasks")
                score += 0.0
            elif len(phases) < 2:
                feedback.append("Refactoring plan lacks sufficient phase breakdown")
                suggestions.append("Break the refactoring into more granular phases")
                score += 0.4
            else:
                feedback.append(f"Plan includes {len(phases)} defined phases")
                score += 0.8
            
            # Evaluate phase detail
            detailed_phases = 0
            for phase in phases:
                # Check if phase has necessary details
                has_items = "items" in phase and phase.get("items")
                has_duration = "duration" in phase
                has_focus = "focus_areas" in phase and phase.get("focus_areas")
                
                if has_items and has_duration and has_focus:
                    detailed_phases += 1
            
            if not phases or detailed_phases < len(phases) * 0.7:  # Less than 70% are detailed
                feedback.append("Some phases lack necessary implementation details")
                suggestions.append("Ensure all phases include concrete tasks, durations, and focus areas")
                score += 0.4
            else:
                feedback.append("Phases include good implementation details")
                score += 0.9
            
            # Check feasibility
            coverage_percentage = refactoring_plan.get("coverage_percentage", 0)
            
            if coverage_percentage < 50:
                feedback.append(f"Plan only addresses {coverage_percentage:.1f}% of identified debt")
                suggestions.append("Expand plan to address more debt items or extend timeline")
                score += 0.3
            elif coverage_percentage < 80:
                feedback.append(f"Plan addresses {coverage_percentage:.1f}% of identified debt")
                suggestions.append("Consider strategies to address remaining debt items")
                score += 0.6
            else:
                feedback.append(f"Plan comprehensively addresses {coverage_percentage:.1f}% of debt")
                score += 0.9
            
            # Check risk assessment
            if not risks:
                feedback.append("Plan lacks risk assessment and mitigation strategies")
                suggestions.append("Add thorough risk assessment with mitigation strategies")
                score += 0.0
            elif len(risks) < 3:
                feedback.append("Limited risk assessment in the plan")
                suggestions.append("Expand risk assessment to cover more potential challenges")
                score += 0.5
            else:
                feedback.append(f"Plan includes {len(risks)} identified risks with mitigations")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Add go/no-go decision points between phases")
            suggestions.append("Include specific testing strategies for each refactoring phase")
            suggestions.append("Add rollback plans for high-risk refactorings")
            suggestions.append("Include communication plan for stakeholders during refactoring")
            
        elif task_type == "debt_prioritization":
            # Evaluate debt prioritization output
            prioritization = work_output.get("prioritization", {})
            
            # Check prioritization components
            prioritized_items = prioritization.get("prioritized_items", [])
            prioritization_criteria = prioritization.get("prioritization_criteria", {})
            items_by_tier = prioritization.get("items_by_tier", {})
            
            # Evaluate criteria comprehensiveness
            essential_criteria = ["business_impact", "risk", "effort"]
            covered_criteria = set(prioritization_criteria.keys())
            
            missing_criteria = [crit for crit in essential_criteria if crit not in covered_criteria]
            
            if missing_criteria:
                feedback.append(f"Prioritization missing these criteria: {', '.join(missing_criteria)}")
                suggestions.append(f"Include missing prioritization criteria: {', '.join(missing_criteria)}")
                score += 0.3
            else:
                feedback.append("Prioritization includes all essential criteria")
                score += 0.9
            
            # Evaluate prioritization detail
            if not prioritized_items:
                feedback.append("No items have been prioritized")
                suggestions.append("Include detailed prioritization of all debt items")
                score += 0.0
            elif not all("priority_score" in item for item in prioritized_items):
                feedback.append("Some items lack priority scores")
                suggestions.append("Ensure all items have numerical priority scores")
                score += 0.5
            else:
                feedback.append(f"Prioritization includes {len(prioritized_items)} scored items")
                score += 0.9
            
            # Evaluate tier distribution
            if not items_by_tier:
                feedback.append("Items not assigned to priority tiers")
                suggestions.append("Group items into priority tiers (P1, P2, P3) for clarity")
                score += 0.0
            elif any(len(items) == 0 for items in items_by_tier.values()):
                feedback.append("Unbalanced priority tier assignment")
                suggestions.append("Ensure balanced distribution across priority tiers")
                score += 0.5
            else:
                tier_counts = [f"{tier}: {len(items)}" for tier, items in items_by_tier.items()]
                feedback.append(f"Items well-distributed across priority tiers ({', '.join(tier_counts)})")
                score += 0.8
            
            # Check business alignment
            business_priorities = prioritization.get("business_priorities", [])
            
            if not business_priorities:
                feedback.append("Prioritization lacks business priorities context")
                suggestions.append("Include explicit business priorities to align technical debt work")
                score += 0.3
            else:
                feedback.append(f"Prioritization considers {len(business_priorities)} business priorities")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Add dependency analysis between debt items")
            suggestions.append("Include ROI calculation for addressing high-priority items")
            suggestions.append("Consider team capability/skill alignment in prioritization")
            suggestions.append("Add qualitative business stakeholder input to priorities")
            
        elif task_type == "architecture_evaluation":
            # Evaluate architecture evaluation output
            architecture_eval = work_output.get("architecture_evaluation", {})
            
            # Check evaluation components
            evaluations = architecture_eval.get("evaluations", {})
            architectural_debt = architecture_eval.get("architectural_debt", [])
            improvement_roadmap = architecture_eval.get("improvement_roadmap", [])
            
            # Evaluate aspect coverage
            essential_aspects = ["modularity", "coupling", "cohesion", "scalability", "maintainability"]
            covered_aspects = set(evaluations.keys())
            
            missing_aspects = [aspect for aspect in essential_aspects if aspect not in covered_aspects]
            
            if missing_aspects:
                feedback.append(f"Evaluation missing these aspects: {', '.join(missing_aspects)}")
                suggestions.append(f"Include analysis for missing aspects: {', '.join(missing_aspects)}")
                score += 0.3
            else:
                feedback.append("Evaluation covers all essential architectural aspects")
                score += 0.9
            
            # Evaluate aspect detail
            detailed_aspects = 0
            for aspect, evaluation in evaluations.items():
                # Check if evaluation has necessary details
                has_score = "score" in evaluation
                has_findings = "findings" in evaluation and evaluation.get("findings")
                has_strengths_weaknesses = "strengths" in evaluation and "weaknesses" in evaluation
                
                if has_score and has_findings and has_strengths_weaknesses:
                    detailed_aspects += 1
            
            if not evaluations or detailed_aspects < len(evaluations) * 0.7:  # Less than 70% are detailed
                feedback.append("Some aspects lack detailed evaluation")
                suggestions.append("Ensure all aspects include scores, findings, strengths, and weaknesses")
                score += 0.4
            else:
                feedback.append("Architectural aspects have detailed evaluations")
                score += 0.9
            
            # Check architectural debt items
            if not architectural_debt:
                feedback.append("No specific architectural debt items identified")
                suggestions.append("Identify specific architectural debt items with severity and recommendations")
                score += 0.0
            elif len(architectural_debt) < 3:
                feedback.append("Limited architectural debt items identified")
                suggestions.append("Expand analysis to identify more architectural debt items")
                score += 0.5
            else:
                feedback.append(f"Evaluation identified {len(architectural_debt)} architectural debt items")
                score += 0.9
            
            # Check improvement roadmap
            if not improvement_roadmap:
                feedback.append("No architectural improvement roadmap provided")
                suggestions.append("Include phased roadmap for architectural improvements")
                score += 0.0
            elif len(improvement_roadmap) < 2:
                feedback.append("Limited improvement roadmap")
                suggestions.append("Expand roadmap with more detailed phases and outcomes")
                score += 0.5
            else:
                feedback.append(f"Roadmap includes {len(improvement_roadmap)} improvement phases")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Include architectural diagrams to visualize current state")
            suggestions.append("Add ideal target architecture vision")
            suggestions.append("Include technology migration considerations")
            suggestions.append("Analyze operational impacts of architectural changes")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("technical_insight", min(1.0, self.performance_metrics.get("technical_insight", 0.5) + 0.05))
        self.update_metric("pragmatic_approach", min(1.0, self.performance_metrics.get("pragmatic_approach", 0.5) + 0.05))
        self.update_metric("business_perspective", min(1.0, self.performance_metrics.get("business_perspective", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)