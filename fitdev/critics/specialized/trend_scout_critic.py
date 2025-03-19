#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trend Scout Critic for FitDev.io
"""

from typing import Dict, Any, List
from models.critic import BaseCritic


class TrendScoutCritic(BaseCritic):
    """Critic agent for evaluating Trend Scout's work."""
    
    def __init__(self, name: str = "Trend Scout Critic"):
        """Initialize the Trend Scout Critic agent.
        
        Args:
            name: Critic agent name (default: "Trend Scout Critic")
        """
        description = """Evaluates technology trend research, tool evaluations, and technology 
                      recommendations produced by the Trend Scout. Provides feedback on research 
                      thoroughness, trend relevance, and recommendation quality."""
        super().__init__(name, "Trend Scout", description)
        
        # Add evaluation criteria specific to Trend Scout
        self.add_evaluation_criterion("Research Thoroughness")
        self.add_evaluation_criterion("Trend Relevance")
        self.add_evaluation_criterion("Recommendation Quality")
        self.add_evaluation_criterion("Analysis Depth")
        self.add_evaluation_criterion("Source Diversity")
        
        # Critic-specific performance metrics
        self.update_metric("industry_knowledge", 0.5)
        self.update_metric("analytical_depth", 0.5)
        self.update_metric("future_prediction", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the Trend Scout.
        
        Args:
            work_output: Work output and metadata from the Trend Scout
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "trend_research":
            # Evaluate trend research output
            research = work_output.get("research", {})
            
            # Check trends
            trends = research.get("trends", [])
            if not trends:
                feedback.append("No trends identified in the research")
                suggestions.append("Expand research to identify relevant trends")
                score += 0.0
            elif len(trends) < 3:
                feedback.append("Limited number of trends identified")
                suggestions.append("Broaden research to discover more diverse trends")
                score += 0.3
            else:
                feedback.append(f"Research identified {len(trends)} trends")
                score += 0.8
            
            # Check technology areas coverage
            areas = research.get("technology_areas", [])
            if not areas:
                feedback.append("No specific technology areas defined")
                suggestions.append("Define clear technology areas for focused research")
                score += 0.2
            else:
                feedback.append(f"Research covers {len(areas)} technology areas")
                score += 0.7
            
            # Check insights
            insights = research.get("insights", [])
            if not insights:
                feedback.append("No industry insights provided")
                suggestions.append("Include broader industry insights and context")
                score += 0.0
            elif len(insights) < 2:
                feedback.append("Limited industry insights provided")
                suggestions.append("Expand industry insights to provide more context")
                score += 0.4
            else:
                feedback.append(f"Research includes {len(insights)} industry insights")
                score += 0.9
            
            # Check recommendations
            recommendations = research.get("recommendations", [])
            if not recommendations:
                feedback.append("No actionable recommendations provided")
                suggestions.append("Include specific, actionable recommendations based on trends")
                score += 0.0
            else:
                feedback.append(f"Research includes {len(recommendations)} recommendations")
                score += 0.8
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Include trend maturity analysis for better prioritization")
            suggestions.append("Add competitive analysis showing industry adoption rates")
            suggestions.append("Provide case studies of successful implementations")
            suggestions.append("Include risk assessment for each trend")
            
        elif task_type == "tool_evaluation":
            # Evaluate tool evaluation output
            evaluation = work_output.get("evaluation", {})
            
            # Check evaluation criteria
            criteria = evaluation.get("evaluation_criteria", [])
            if not criteria:
                feedback.append("No evaluation criteria defined")
                suggestions.append("Define clear evaluation criteria")
                score += 0.0
            elif len(criteria) < 5:
                feedback.append("Limited evaluation criteria")
                suggestions.append("Expand evaluation criteria for more comprehensive assessment")
                score += 0.4
            else:
                feedback.append(f"Evaluation uses {len(criteria)} criteria")
                score += 0.8
            
            # Check strengths and weaknesses
            strengths = evaluation.get("strengths", [])
            weaknesses = evaluation.get("weaknesses", [])
            
            if not strengths and not weaknesses:
                feedback.append("No strengths or weaknesses identified")
                suggestions.append("Provide balanced analysis of strengths and weaknesses")
                score += 0.0
            elif len(strengths) < 2 or len(weaknesses) < 1:
                feedback.append("Unbalanced analysis of strengths and weaknesses")
                suggestions.append("Ensure balanced assessment of both strengths and weaknesses")
                score += 0.4
            else:
                feedback.append(f"Evaluation identifies {len(strengths)} strengths and {len(weaknesses)} weaknesses")
                score += 0.9
            
            # Check alternatives
            alternatives = evaluation.get("alternatives", [])
            if not alternatives:
                feedback.append("No alternatives suggested")
                suggestions.append("Suggest alternative tools for comparison")
                score += 0.0
            else:
                feedback.append(f"Evaluation includes {len(alternatives)} alternative tools")
                score += 0.8
            
            # Check recommendation clarity
            has_recommendation = "recommendation" in evaluation and "reasoning" in evaluation
            if not has_recommendation:
                feedback.append("No clear recommendation or reasoning provided")
                suggestions.append("Provide clear recommendation with supporting reasoning")
                score += 0.0
            else:
                feedback.append("Evaluation includes clear recommendation and reasoning")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Include real-world case studies of tool usage")
            suggestions.append("Add benchmark comparisons with alternatives")
            suggestions.append("Provide implementation cost estimates")
            suggestions.append("Include adoption timeline recommendations")
            
        elif task_type == "technology_recommendations":
            # Evaluate technology recommendations output
            tech_recommendations = work_output.get("recommendations", {})
            
            # Check recommendations
            recommendations = tech_recommendations.get("recommendations", [])
            if not recommendations:
                feedback.append("No technology recommendations provided")
                suggestions.append("Provide specific technology recommendations")
                score += 0.0
            elif len(recommendations) < 2:
                feedback.append("Limited technology recommendations")
                suggestions.append("Expand recommendations to cover more project needs")
                score += 0.4
            else:
                feedback.append(f"Provided {len(recommendations)} technology recommendations")
                score += 0.8
            
            # Check project needs coverage
            needs = tech_recommendations.get("project_needs", [])
            needs_covered = set()
            for rec in recommendations:
                if "need" in rec:
                    needs_covered.add(rec["need"])
            
            if not needs:
                feedback.append("No project needs defined")
                suggestions.append("Clearly define project needs for targeted recommendations")
                score += 0.2
            elif len(needs_covered) < len(needs):
                feedback.append("Not all project needs are addressed by recommendations")
                suggestions.append("Ensure all project needs have corresponding recommendations")
                score += 0.5
            else:
                feedback.append("All project needs are addressed by recommendations")
                score += 0.9
            
            # Check consideration of constraints
            constraints = tech_recommendations.get("constraints", [])
            if not constraints:
                feedback.append("No project constraints considered")
                suggestions.append("Consider relevant project constraints in recommendations")
                score += 0.3
            else:
                feedback.append(f"Recommendations consider {len(constraints)} project constraints")
                score += 0.8
            
            # Check migration considerations
            migration = tech_recommendations.get("migration_considerations", [])
            if not migration and tech_recommendations.get("current_stack"):
                feedback.append("No migration considerations provided despite existing stack")
                suggestions.append("Include migration considerations for existing technology stack")
                score += 0.2
            elif migration:
                feedback.append("Recommendations include migration considerations")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Include adoption difficulty ratings for each recommendation")
            suggestions.append("Add implementation timeline estimates")
            suggestions.append("Consider team skill set in technology recommendations")
            suggestions.append("Provide proof-of-concept guidelines for evaluation")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("industry_knowledge", min(1.0, self.performance_metrics.get("industry_knowledge", 0.5) + 0.05))
        self.update_metric("analytical_depth", min(1.0, self.performance_metrics.get("analytical_depth", 0.5) + 0.05))
        self.update_metric("future_prediction", min(1.0, self.performance_metrics.get("future_prediction", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)