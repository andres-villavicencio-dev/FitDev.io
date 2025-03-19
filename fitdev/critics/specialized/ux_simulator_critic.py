#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UX Simulator Critic for FitDev.io
"""

from typing import Dict, Any, List
from fitdev.models.critic import BaseCritic


class UXSimulatorCritic(BaseCritic):
    """Critic agent for evaluating UX Simulator's work."""
    
    def __init__(self, name: str = "UX Simulator Critic"):
        """Initialize the UX Simulator Critic agent.
        
        Args:
            name: Critic agent name (default: "UX Simulator Critic")
        """
        description = """Evaluates user personas, user flows, heuristic evaluations, and usability 
                      test results produced by the UX Simulator. Provides feedback on quality, 
                      depth, and actionability of UX deliverables."""
        super().__init__(name, "UX Simulator", description)
        
        # Add evaluation criteria specific to UX Simulator
        self.add_evaluation_criterion("Persona Realism")
        self.add_evaluation_criterion("User Flow Completeness")
        self.add_evaluation_criterion("Heuristic Evaluation Depth")
        self.add_evaluation_criterion("Usability Test Methodology")
        self.add_evaluation_criterion("Recommendation Actionability")
        
        # Critic-specific performance metrics
        self.update_metric("ux_domain_knowledge", 0.5)
        self.update_metric("evaluation_thoroughness", 0.5)
        self.update_metric("actionable_feedback", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the UX Simulator.
        
        Args:
            work_output: Work output and metadata from the UX Simulator
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "persona_creation":
            # Evaluate persona creation output
            personas_output = work_output.get("personas", {})
            
            # Check persona count
            personas = personas_output.get("personas", [])
            if not personas:
                feedback.append("No personas created")
                suggestions.append("Create multiple personas to cover target audience segments")
                score += 0.0
            elif len(personas) < 2:
                feedback.append("Only one persona created, limiting audience coverage")
                suggestions.append("Create additional personas to represent diverse user groups")
                score += 0.3
            else:
                feedback.append(f"Created {len(personas)} personas")
                score += 0.8
            
            # Check persona depth
            deep_personas = 0
            for persona in personas:
                # Count attributes that indicate depth
                depth_indicators = ["needs", "motivations", "pain_points", "scenarios", "behavioral_traits"]
                depth_count = sum(1 for indicator in depth_indicators if indicator in persona and persona[indicator])
                
                if depth_count >= 4:
                    deep_personas += 1
            
            if not deep_personas:
                feedback.append("Personas lack depth and essential attributes")
                suggestions.append("Enhance personas with needs, motivations, and scenarios")
                score += 0.0
            elif deep_personas < len(personas):
                feedback.append("Some personas lack sufficient depth")
                suggestions.append("Ensure all personas have comprehensive attributes")
                score += 0.5
            else:
                feedback.append("All personas have good depth with essential attributes")
                score += 0.9
            
            # Check target audience alignment
            target_audiences = personas_output.get("target_audiences", [])
            has_alignment = any("target_audience" in persona for persona in personas)
            
            if target_audiences and not has_alignment:
                feedback.append("Personas not aligned with specified target audiences")
                suggestions.append("Explicitly link personas to target audience segments")
                score += 0.2
            elif target_audiences and has_alignment:
                feedback.append("Personas aligned with target audience segments")
                score += 0.9
            
            # Normalize score
            score = score / 3.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Include specific quotations to bring personas to life")
            suggestions.append("Add technical proficiency indicators to inform UI complexity decisions")
            suggestions.append("Include accessibility needs in persona attributes")
            suggestions.append("Add quantitative data points to support persona characteristics")
            
        elif task_type == "user_flow_mapping":
            # Evaluate user flow mapping output
            flows_output = work_output.get("user_flows", {})
            
            # Check user flows count
            flows = flows_output.get("user_flows", [])
            if not flows:
                feedback.append("No user flows created")
                suggestions.append("Create user flows for key user journeys")
                score += 0.0
            elif len(flows) < 2:
                feedback.append("Limited user flows, not covering enough scenarios")
                suggestions.append("Create additional user flows for more key tasks")
                score += 0.4
            else:
                feedback.append(f"Created {len(flows)} user flows")
                score += 0.8
            
            # Check flow step detail
            detailed_flows = 0
            for flow in flows:
                steps = flow.get("steps", [])
                
                # Check if steps are detailed enough
                detailed_steps = 0
                for step in steps:
                    # Count attributes that indicate detail
                    detail_indicators = ["actions", "thoughts", "pain_points", "duration"]
                    detail_count = sum(1 for indicator in detail_indicators if indicator in step and step[indicator])
                    
                    if detail_count >= 3:
                        detailed_steps += 1
                
                if detailed_steps >= len(steps) * 0.7:  # 70% of steps are detailed
                    detailed_flows += 1
            
            if not detailed_flows:
                feedback.append("User flows lack necessary detail")
                suggestions.append("Add user thoughts, pain points, and timing to each step")
                score += 0.0
            elif detailed_flows < len(flows):
                feedback.append("Some user flows need more detailed steps")
                suggestions.append("Ensure all steps include actions, thoughts, and pain points")
                score += 0.5
            else:
                feedback.append("User flows have good step-by-step detail")
                score += 0.9
            
            # Check if flows include recommendations
            has_recommendations = "recommendations" in flows_output and flows_output["recommendations"]
            if not has_recommendations:
                feedback.append("User flows missing actionable recommendations")
                suggestions.append("Include specific recommendations based on flow analysis")
                score += 0.0
            else:
                feedback.append("User flows include improvement recommendations")
                score += 0.8
            
            # Normalize score
            score = score / 3.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Add decision points to represent user choices in the flow")
            suggestions.append("Include error paths to show recovery scenarios")
            suggestions.append("Link flows to specific persona motivations and goals")
            suggestions.append("Add expected emotions at each step of the flow")
            
        elif task_type == "heuristic_evaluation":
            # Evaluate heuristic evaluation output
            evaluation = work_output.get("evaluation", {})
            
            # Check element coverage
            elements = evaluation.get("elements_evaluated", [])
            if not elements:
                feedback.append("No interface elements evaluated")
                suggestions.append("Identify and evaluate key interface elements")
                score += 0.0
            elif len(elements) < 3:
                feedback.append("Limited interface element coverage")
                suggestions.append("Expand evaluation to include more interface elements")
                score += 0.4
            else:
                feedback.append(f"Evaluation covers {len(elements)} interface elements")
                score += 0.8
            
            # Check heuristic coverage
            heuristics = evaluation.get("heuristics_used", [])
            if not heuristics:
                feedback.append("No heuristics specified for evaluation")
                suggestions.append("Use established heuristics like Nielsen's 10 heuristics")
                score += 0.0
            elif len(heuristics) < 5:
                feedback.append("Limited heuristic coverage")
                suggestions.append("Expand evaluation to include more heuristics")
                score += 0.4
            else:
                feedback.append(f"Evaluation uses {len(heuristics)} heuristics")
                score += 0.9
            
            # Check issue specificity
            element_evaluations = evaluation.get("element_evaluations", [])
            specific_issues = 0
            total_issues = 0
            
            for element_eval in element_evaluations:
                issues = element_eval.get("issues", [])
                total_issues += len(issues)
                
                for issue in issues:
                    # Check if issue has specific description and recommendation
                    has_specific_description = "description" in issue and len(issue["description"]) > 20
                    has_recommendation = "recommendation" in issue and issue["recommendation"]
                    
                    if has_specific_description and has_recommendation:
                        specific_issues += 1
            
            if total_issues == 0:
                feedback.append("No usability issues identified")
                suggestions.append("Identify specific usability issues for each element")
                score += 0.0
            elif specific_issues < total_issues * 0.7:  # Less than 70% of issues are specific
                feedback.append("Many issues lack specific descriptions or recommendations")
                suggestions.append("Provide detailed descriptions and specific recommendations for each issue")
                score += 0.4
            else:
                feedback.append(f"Evaluation includes {specific_issues} specific issues with recommendations")
                score += 0.9
            
            # Normalize score
            score = score / 3.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Include severity ratings for all identified issues")
            suggestions.append("Prioritize issues based on user impact and implementation effort")
            suggestions.append("Include positive findings along with issues")
            suggestions.append("Add screenshots or mockups to illustrate issues")
            
        elif task_type == "usability_testing":
            # Evaluate usability testing output
            test_results = work_output.get("usability_test", {})
            
            # Check participant count
            participants = test_results.get("participants", [])
            if not participants:
                feedback.append("No test participants included")
                suggestions.append("Include at least 5 participants for reliable results")
                score += 0.0
            elif len(participants) < 3:
                feedback.append("Too few test participants for reliable results")
                suggestions.append("Increase participant count to at least 5")
                score += 0.3
            else:
                feedback.append(f"Test includes {len(participants)} participants")
                score += 0.8
            
            # Check scenario coverage
            scenarios = test_results.get("scenario_results", [])
            if not scenarios:
                feedback.append("No test scenarios defined")
                suggestions.append("Define specific scenarios for usability testing")
                score += 0.0
            elif len(scenarios) < 2:
                feedback.append("Limited test scenario coverage")
                suggestions.append("Include more scenarios to test different aspects of the interface")
                score += 0.4
            else:
                feedback.append(f"Test includes {len(scenarios)} scenarios")
                score += 0.8
            
            # Check metrics and findings
            detailed_metrics = 0
            for scenario in scenarios:
                metrics = scenario.get("metrics", {})
                common_issues = scenario.get("common_issues", [])
                
                # Check if metrics are comprehensive
                has_success_rate = "success_rate" in metrics
                has_time_metrics = "average_time_on_task" in metrics
                has_satisfaction = "average_satisfaction" in metrics
                
                if has_success_rate and has_time_metrics and has_satisfaction and common_issues:
                    detailed_metrics += 1
            
            if not scenarios or detailed_metrics < len(scenarios):
                feedback.append("Some test scenarios lack comprehensive metrics or findings")
                suggestions.append("Include success rates, time metrics, and identified issues for all scenarios")
                score += 0.3
            else:
                feedback.append("All test scenarios include comprehensive metrics and findings")
                score += 0.9
            
            # Check recommendations
            recommendations = test_results.get("recommendations", [])
            if not recommendations:
                feedback.append("No actionable recommendations from test results")
                suggestions.append("Provide specific recommendations based on test findings")
                score += 0.0
            elif len(recommendations) < 3:
                feedback.append("Limited recommendations from test results")
                suggestions.append("Expand recommendations to address all major findings")
                score += 0.5
            else:
                feedback.append(f"Test results include {len(recommendations)} actionable recommendations")
                score += 0.9
            
            # Normalize score
            score = score / 4.0  # Average of the aspects evaluated
            
            # Add specific suggestions
            suggestions.append("Include verbatim quotes from participants to support findings")
            suggestions.append("Add task completion paths to illustrate user behaviors")
            suggestions.append("Segment findings by user demographics or experience level")
            suggestions.append("Include comparison metrics with industry benchmarks if available")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("ux_domain_knowledge", min(1.0, self.performance_metrics.get("ux_domain_knowledge", 0.5) + 0.05))
        self.update_metric("evaluation_thoroughness", min(1.0, self.performance_metrics.get("evaluation_thoroughness", 0.5) + 0.05))
        self.update_metric("actionable_feedback", min(1.0, self.performance_metrics.get("actionable_feedback", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)