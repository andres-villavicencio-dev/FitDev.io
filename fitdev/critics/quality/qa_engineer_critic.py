#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QA Engineer Critic for FitDev.io
"""

from typing import Dict, Any, List
from models.critic import BaseCritic


class QAEngineerCritic(BaseCritic):
    """Critic agent for evaluating QA Engineer's work."""
    
    def __init__(self, name: str = "QA Engineer Critic"):
        """Initialize the QA Engineer Critic agent.
        
        Args:
            name: Critic agent name (default: "QA Engineer Critic")
        """
        description = """Evaluates test plans, test automation code, and bug verification work 
                      performed by the QA Engineer. Provides feedback on test coverage,
                      test quality, and thoroughness of verification."""
        super().__init__(name, "QA Engineer", description)
        
        # Add evaluation criteria specific to QA Engineer
        self.add_evaluation_criterion("Test Coverage")
        self.add_evaluation_criterion("Test Case Quality")
        self.add_evaluation_criterion("Test Automation")
        self.add_evaluation_criterion("Bug Verification Thoroughness")
        self.add_evaluation_criterion("Test Reporting")
        
        # Critic-specific performance metrics
        self.update_metric("testing_expertise", 0.5)
        self.update_metric("automation_insight", 0.5)
        self.update_metric("bug_analysis_skill", 0.5)
    
    def evaluate_work(self, work_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate work output from the QA Engineer.
        
        Args:
            work_output: Work output and metadata from the QA Engineer
            
        Returns:
            Evaluation results with feedback and improvement suggestions
        """
        # Get the task type from the work output
        task_type = work_output.get("type", "")
        
        # Initialize evaluation variables
        score = 0.0
        feedback = []
        suggestions = []
        
        if task_type == "test_planning":
            # Evaluate test planning output
            test_plan = work_output.get("test_plan", {})
            
            # Check test cases
            test_cases = test_plan.get("test_cases", [])
            if not test_cases:
                feedback.append("No test cases provided in the test plan")
                suggestions.append("Create comprehensive test cases covering key functionality")
                score += 0.0
            elif len(test_cases) < 5:
                feedback.append("Limited number of test cases in the test plan")
                suggestions.append("Expand test coverage with more test cases")
                score += 0.3
            else:
                feedback.append(f"Test plan includes {len(test_cases)} test cases")
                score += 0.8
            
            # Check test levels
            test_levels = test_plan.get("test_levels", [])
            if not test_levels:
                feedback.append("Test plan doesn't specify test levels")
                suggestions.append("Define test levels (unit, integration, system, etc.)")
                score += 0.0
            elif len(test_levels) < 2:
                feedback.append("Test plan covers limited test levels")
                suggestions.append("Include more test levels for comprehensive testing")
                score += 0.4
            else:
                feedback.append(f"Test plan covers multiple test levels: {', '.join(test_levels)}")
                score += 0.9
            
            # Check time estimation
            estimated_time = test_plan.get("estimated_execution_time", 0)
            if estimated_time <= 0:
                feedback.append("No time estimation provided for test execution")
                suggestions.append("Include realistic time estimates for test execution")
                score += 0.0
            else:
                feedback.append(f"Test plan includes time estimation: {estimated_time} minutes")
                score += 0.8
            
            # Normalize score
            score = score / 3.0  # Average of the aspects evaluated
            
            # Add specific suggestions for test planning
            suggestions.append("Include risk assessment in the test plan")
            suggestions.append("Add traceability matrix linking tests to requirements")
            suggestions.append("Consider adding exploratory testing sessions")
            
        elif task_type == "test_automation":
            # Evaluate test automation output
            test_scripts = work_output.get("test_scripts", {})
            
            # Check code
            code = test_scripts.get("code", "")
            if not code:
                feedback.append("No test automation code provided")
                suggestions.append("Implement test automation scripts")
                score += 0.0
            elif len(code.strip().split("\n")) < 15:
                feedback.append("Test automation code is minimal")
                suggestions.append("Expand test automation coverage")
                score += 0.3
            else:
                feedback.append("Test automation has reasonable implementation")
                score += 0.7
            
            # Check framework usage
            framework = test_scripts.get("framework", "")
            if not framework:
                feedback.append("No test framework specified")
                suggestions.append("Specify which test framework is being used")
                score += 0.0
            else:
                feedback.append(f"Test automation uses {framework} framework")
                score += 0.8
            
            # Check test coverage
            coverage = test_scripts.get("coverage_percentage", 0)
            if coverage < 50:
                feedback.append(f"Low test coverage ({coverage}%)")
                suggestions.append("Increase test coverage to at least 80%")
                score += 0.2
            elif coverage < 80:
                feedback.append(f"Moderate test coverage ({coverage}%)")
                suggestions.append("Aim for higher test coverage")
                score += 0.6
            else:
                feedback.append(f"Good test coverage ({coverage}%)")
                score += 0.9
            
            # Normalize score
            score = score / 3.0  # Average of the aspects evaluated
            
            # Add specific suggestions for test automation
            suggestions.append("Add more assertions to verify expected behavior")
            suggestions.append("Include negative test cases and edge cases")
            suggestions.append("Implement data-driven testing")
            suggestions.append("Add proper error reporting for failed tests")
            
        elif task_type == "bug_verification":
            # Evaluate bug verification output
            verification = work_output.get("verification", {})
            
            # Check verification result
            verification_passed = verification.get("verification_passed", False)
            if verification_passed:
                feedback.append("Bug verification indicates the issue is fixed")
                score += 0.8
            else:
                feedback.append("Bug verification indicates the issue is not fixed")
                suggestions.append("Provide detailed reproduction steps for developers")
                score += 0.5  # Neutral score for negative verification
            
            # Check verification steps
            steps = verification.get("steps_performed", [])
            if not steps:
                feedback.append("No verification steps documented")
                suggestions.append("Document all steps taken to verify the fix")
                score += 0.0
            elif len(steps) < 3:
                feedback.append("Limited verification steps documented")
                suggestions.append("Perform more thorough verification")
                score += 0.4
            else:
                feedback.append(f"Verification includes {len(steps)} steps")
                score += 0.9
            
            # Check notes and recommendation
            notes = verification.get("notes", "")
            recommendation = verification.get("recommendation", "")
            if not notes or not recommendation:
                feedback.append("Missing notes or recommendation")
                suggestions.append("Always include detailed notes and clear recommendation")
                score += 0.2
            else:
                feedback.append("Verification includes notes and recommendation")
                score += 0.9
            
            # Normalize score
            score = score / 3.0  # Average of the aspects evaluated
            
            # Add specific suggestions for bug verification
            suggestions.append("Include screenshots or screen recordings for visual issues")
            suggestions.append("Verify the fix in multiple environments")
            suggestions.append("Check for regression issues introduced by the fix")
            suggestions.append("Consider adding automated tests to prevent regression")
        
        else:
            # Generic evaluation for unknown task types
            feedback.append(f"Received work output of unrecognized type: {task_type}")
            suggestions.append("Provide more specific task type for targeted evaluation")
            score = 0.5  # Neutral score for unknown tasks
        
        # Update critic's own performance metrics based on evaluation
        self.update_metric("testing_expertise", min(1.0, self.performance_metrics.get("testing_expertise", 0.5) + 0.05))
        self.update_metric("automation_insight", min(1.0, self.performance_metrics.get("automation_insight", 0.5) + 0.05))
        self.update_metric("bug_analysis_skill", min(1.0, self.performance_metrics.get("bug_analysis_skill", 0.5) + 0.05))
        
        # Return the evaluation report
        return self.get_evaluation_report(score, feedback, suggestions)