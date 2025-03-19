#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UX Simulator Agent for FitDev.io
"""

from typing import Dict, Any, List
from fitdev.models.agent import BaseAgent


class UXSimulatorAgent(BaseAgent):
    """UX Simulator agent responsible for simulating and evaluating user experiences."""
    
    def __init__(self, name: str = "UX Simulator"):
        """Initialize the UX Simulator agent.
        
        Args:
            name: Agent name (default: "UX Simulator")
        """
        description = """Simulates user interactions, evaluates user experiences, and provides 
                      recommendations for UX improvements. Creates user personas, user flows, 
                      and conducts heuristic evaluations."""
        super().__init__(name, "specialized", description)
        
        # Add UX Simulator-specific skills
        self.add_skill("User Persona Creation")
        self.add_skill("User Flow Mapping")
        self.add_skill("Heuristic Evaluation")
        self.add_skill("Usability Testing")
        self.add_skill("Interaction Design Assessment")
        
        # UX Simulator-specific performance metrics
        self.update_metric("persona_quality", 0.0)
        self.update_metric("usability_assessment", 0.0)
        self.update_metric("ux_recommendations", 0.0)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task assigned to this agent.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results and metadata
        """
        # Task execution logic for the UX Simulator agent
        task_type = task.get("type", "")
        results = {"status": "completed", "agent": self.name}
        
        if task_type == "persona_creation":
            # Logic for creating user personas
            results["personas"] = self._create_personas(task)
            
        elif task_type == "user_flow_mapping":
            # Logic for mapping user flows
            results["user_flows"] = self._map_user_flows(task)
            
        elif task_type == "heuristic_evaluation":
            # Logic for conducting heuristic evaluations
            results["evaluation"] = self._conduct_heuristic_evaluation(task)
            
        elif task_type == "usability_testing":
            # Logic for simulating usability tests
            results["usability_test"] = self._simulate_usability_test(task)
        
        # Update metrics based on task execution
        self._update_metrics_from_task(task)
        
        return results
    
    def evaluate_performance(self) -> float:
        """Evaluate UX Simulator agent's performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        # Weight factors for different metrics
        weights = {
            "persona_quality": 0.3,
            "usability_assessment": 0.4,
            "ux_recommendations": 0.3
        }
        
        # Calculate weighted performance score
        score = 0.0
        for metric, weight in weights.items():
            if metric in self.performance_metrics:
                # Normalize metric value to 0.0-1.0 range if needed
                metric_value = min(1.0, max(0.0, self.performance_metrics[metric]))
                score += metric_value * weight
        
        return score
    
    def _create_personas(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create user personas.
        
        Args:
            task: Task containing persona creation requirements
            
        Returns:
            User personas
        """
        product_type = task.get("product_type", "")
        target_audiences = task.get("target_audiences", [])
        persona_count = task.get("persona_count", 3)
        
        # Generate user personas (placeholder implementation)
        personas = []
        
        # Generic persona templates that can be adapted to different product types
        persona_templates = [
            {
                "name": "Tech-Savvy Professional",
                "age_range": "25-35",
                "technical_proficiency": "High",
                "usage_frequency": "Daily",
                "primary_goals": ["Efficiency", "Advanced features", "Integration with other tools"],
                "pain_points": ["Complex workflows", "Performance issues", "Limited customization"],
                "behavioral_traits": ["Early adopter", "Feature explorer", "Power user"]
            },
            {
                "name": "Busy Manager",
                "age_range": "35-45",
                "technical_proficiency": "Medium",
                "usage_frequency": "Daily",
                "primary_goals": ["Overview and insights", "Team coordination", "Time efficiency"],
                "pain_points": ["Information overload", "Complex interfaces", "Learning curve"],
                "behavioral_traits": ["Goal-oriented", "Delegator", "Values simplicity"]
            },
            {
                "name": "Occasional User",
                "age_range": "20-60",
                "technical_proficiency": "Low to Medium",
                "usage_frequency": "Weekly or less",
                "primary_goals": ["Completing specific tasks", "Minimum effort", "Clear guidance"],
                "pain_points": ["Forgetting how to use", "Complex terminology", "Hidden features"],
                "behavioral_traits": ["Cautious", "Follows instructions", "Avoids exploration"]
            },
            {
                "name": "Student/Learner",
                "age_range": "18-25",
                "technical_proficiency": "Medium",
                "usage_frequency": "Variable",
                "primary_goals": ["Learning", "Affordability", "Collaboration"],
                "pain_points": ["Cost barriers", "Complex setup", "Limited guidance"],
                "behavioral_traits": ["Curious", "Budget-conscious", "Social learner"]
            },
            {
                "name": "Senior User",
                "age_range": "60+",
                "technical_proficiency": "Low",
                "usage_frequency": "Variable",
                "primary_goals": ["Simplicity", "Reliability", "Accessibility"],
                "pain_points": ["Small text", "Complex navigation", "Technical jargon"],
                "behavioral_traits": ["Careful", "Routine-oriented", "Prefers stability"]
            }
        ]
        
        # Select and customize personas based on target audience and product type
        import random
        selected_templates = random.sample(persona_templates, min(persona_count, len(persona_templates)))
        
        for i, template in enumerate(selected_templates):
            # Customize the persona based on product type and target audience
            persona = template.copy()
            
            # Assign a target audience if available
            if target_audiences and i < len(target_audiences):
                persona["target_audience"] = target_audiences[i]
            
            # Add scenario specific to the product type
            if product_type == "mobile_app":
                persona["scenarios"] = [
                    f"Using the app while commuting",
                    f"Quick check during a meeting",
                    f"Using the app in poor network conditions"
                ]
            elif product_type == "web_application":
                persona["scenarios"] = [
                    f"Extended work session using multiple features",
                    f"Collaborating with team members",
                    f"Accessing from different devices and browsers"
                ]
            elif product_type == "enterprise_software":
                persona["scenarios"] = [
                    f"Integrating with other business systems",
                    f"Creating reports for management",
                    f"Training new team members"
                ]
            else:
                persona["scenarios"] = [
                    f"First-time use experience",
                    f"Regular usage pattern",
                    f"Troubleshooting a problem"
                ]
            
            # Add needs and motivations
            persona["needs"] = [
                f"Need 1 for {persona['name']}",
                f"Need 2 for {persona['name']}",
                f"Need 3 for {persona['name']}"
            ]
            
            persona["motivations"] = [
                f"Motivation 1 for {persona['name']}",
                f"Motivation 2 for {persona['name']}",
                f"Motivation 3 for {persona['name']}"
            ]
            
            personas.append(persona)
        
        return {
            "product_type": product_type,
            "personas": personas,
            "persona_count": len(personas),
            "target_audiences": target_audiences,
            "usage_notes": "These personas should be used to inform design decisions and usability testing."
        }
    
    def _map_user_flows(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Map user flows for key user journeys.
        
        Args:
            task: Task containing user flow requirements
            
        Returns:
            User flow maps
        """
        product_name = task.get("product_name", "")
        key_tasks = task.get("key_tasks", [])
        persona_names = task.get("persona_names", [])
        
        # Generate user flows (placeholder implementation)
        user_flows = []
        
        for i, task_name in enumerate(key_tasks):
            # Determine persona for this flow
            persona = persona_names[i % len(persona_names)] if persona_names else f"Generic User {i+1}"
            
            # Generate steps for this flow
            steps = []
            
            # Generic flow pattern: entry -> actions -> outcome
            steps.append({
                "step_number": 1,
                "description": f"User navigates to {product_name}",
                "screen": "Landing/Home Screen",
                "actions": ["Load application", "View initial options"],
                "thoughts": ["Where do I find the feature I need?", "What are my options?"],
                "pain_points": ["Navigation not clear", "Too many options"],
                "duration": "5-10 seconds"
            })
            
            # Middle steps depend on the task
            steps.append({
                "step_number": 2,
                "description": f"User looks for {task_name} functionality",
                "screen": "Navigation/Menu",
                "actions": ["Scan menu items", "Click on relevant section"],
                "thoughts": ["Where is the feature located?", "What category would it be under?"],
                "pain_points": ["Menu organization not intuitive", "Feature buried in submenus"],
                "duration": "5-15 seconds"
            })
            
            steps.append({
                "step_number": 3,
                "description": f"User interacts with {task_name} feature",
                "screen": f"{task_name.title()} Screen",
                "actions": ["Input required information", "Configure options"],
                "thoughts": ["How do I use this feature?", "What information is required?"],
                "pain_points": ["Unclear input requirements", "Complex form"],
                "duration": "20-60 seconds"
            })
            
            steps.append({
                "step_number": 4,
                "description": f"User completes {task_name}",
                "screen": "Confirmation Screen",
                "actions": ["Submit or confirm action", "Review results"],
                "thoughts": ["Did it work?", "What happens next?"],
                "pain_points": ["Unclear confirmation", "Next steps not provided"],
                "duration": "5-10 seconds"
            })
            
            # Add flow to the collection
            user_flows.append({
                "task_name": task_name,
                "persona": persona,
                "entry_point": "Home Screen",
                "exit_point": "Confirmation Screen",
                "steps": steps,
                "total_steps": len(steps),
                "estimated_duration": "35-95 seconds",
                "success_criteria": [
                    f"User successfully completes {task_name}",
                    "User understands the outcome",
                    "User can navigate back or to next task"
                ]
            })
        
        return {
            "product_name": product_name,
            "user_flows": user_flows,
            "total_flows": len(user_flows),
            "key_findings": [
                "Users may struggle to find features in the navigation",
                "Confirmation screens should provide clear next steps",
                "Input requirements should be clearly communicated"
            ],
            "recommendations": [
                "Simplify navigation structure",
                "Improve confirmation messaging",
                "Provide inline help for complex inputs"
            ]
        }
    
    def _conduct_heuristic_evaluation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct a heuristic evaluation.
        
        Args:
            task: Task containing heuristic evaluation requirements
            
        Returns:
            Heuristic evaluation results
        """
        product_name = task.get("product_name", "")
        interface_elements = task.get("interface_elements", [])
        heuristics = task.get("heuristics", [])
        
        # If no specific heuristics provided, use Nielsen's 10 heuristics
        if not heuristics:
            heuristics = [
                "Visibility of system status",
                "Match between system and real world",
                "User control and freedom",
                "Consistency and standards",
                "Error prevention",
                "Recognition rather than recall",
                "Flexibility and efficiency of use",
                "Aesthetic and minimalist design",
                "Help users recognize, diagnose, and recover from errors",
                "Help and documentation"
            ]
        
        # If no interface elements specified, use generic ones
        if not interface_elements:
            interface_elements = [
                "Navigation menu",
                "Search functionality",
                "Forms and inputs",
                "Confirmation dialogs",
                "Error messages",
                "User dashboard"
            ]
        
        # Generate heuristic evaluation (placeholder implementation)
        evaluation_results = []
        
        # Severity ratings for issues
        severity_levels = ["Low", "Medium", "High", "Critical"]
        
        # For each interface element, evaluate against each heuristic
        for element in interface_elements:
            issues = []
            
            # Generate 1-3 issues for each element across different heuristics
            import random
            num_issues = random.randint(1, 3)
            selected_heuristics = random.sample(heuristics, num_issues)
            
            for heuristic in selected_heuristics:
                # Generate a specific issue for this heuristic and element
                severity = random.choice(severity_levels)
                
                issue = {
                    "heuristic": heuristic,
                    "description": f"Issue with {element} related to {heuristic}",
                    "severity": severity,
                    "example": f"When using {element}, users may encounter problems with {heuristic.lower()}",
                    "impact": f"This affects user efficiency and satisfaction when using {element}",
                    "recommendation": f"Improve {element} by addressing {heuristic.lower()}"
                }
                
                issues.append(issue)
            
            # Add element evaluation to results
            evaluation_results.append({
                "element": element,
                "issues": issues,
                "issue_count": len(issues)
            })
        
        # Summarize findings
        total_issues = sum(len(result["issues"]) for result in evaluation_results)
        critical_issues = sum(1 for result in evaluation_results 
                             for issue in result["issues"] 
                             if issue["severity"] == "Critical")
        high_issues = sum(1 for result in evaluation_results 
                         for issue in result["issues"] 
                         if issue["severity"] == "High")
        
        # Generate priority recommendations based on critical and high issues
        priority_recommendations = []
        for result in evaluation_results:
            for issue in result["issues"]:
                if issue["severity"] in ["Critical", "High"]:
                    priority_recommendations.append({
                        "element": result["element"],
                        "heuristic": issue["heuristic"],
                        "recommendation": issue["recommendation"]
                    })
        
        return {
            "product_name": product_name,
            "evaluation_date": "",  # Could be filled with actual date
            "heuristics_used": heuristics,
            "elements_evaluated": interface_elements,
            "element_evaluations": evaluation_results,
            "summary": {
                "total_issues": total_issues,
                "critical_issues": critical_issues,
                "high_issues": high_issues,
                "medium_issues": total_issues - critical_issues - high_issues
            },
            "priority_recommendations": priority_recommendations[:5],  # Top 5 recommendations
            "overall_usability_rating": self._calculate_usability_rating(total_issues, len(interface_elements))
        }
    
    def _simulate_usability_test(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate a usability test.
        
        Args:
            task: Task containing usability test requirements
            
        Returns:
            Usability test results
        """
        product_name = task.get("product_name", "")
        test_scenarios = task.get("test_scenarios", [])
        participant_count = task.get("participant_count", 5)
        
        # Generate usability test results (placeholder implementation)
        participants = []
        
        # Generate participants
        for i in range(participant_count):
            participants.append({
                "id": f"P{i+1}",
                "demographic": f"Participant demographic {i+1}",
                "technical_proficiency": ["Low", "Medium", "High"][i % 3]
            })
        
        # Generate test results for each scenario
        scenario_results = []
        
        for scenario in test_scenarios:
            participant_results = []
            
            # For each participant, generate results for this scenario
            for participant in participants:
                # Randomize success and metrics for realism
                import random
                success = random.choice([True, True, True, False, False])  # 60% success rate
                time_on_task = random.randint(30, 180)  # seconds
                error_count = random.randint(0, 5)
                
                observations = []
                if not success:
                    observations.append(f"Participant struggled to complete the task")
                if error_count > 2:
                    observations.append(f"Participant made {error_count} errors")
                if time_on_task > 120:
                    observations.append(f"Task took longer than expected ({time_on_task} seconds)")
                
                # Add random observations
                potential_observations = [
                    "Expressed confusion about navigation",
                    "Didn't notice key UI elements",
                    "Had trouble understanding terminology",
                    "Looked for help documentation",
                    "Expressed frustration during the task",
                    "Tried to use search functionality",
                    "Mentioned expectations from similar products",
                    "Navigated confidently through the interface",
                    "Completed task efficiently with no hesitation"
                ]
                
                # Add 1-3 random observations
                num_obs = random.randint(1, 3)
                for _ in range(num_obs):
                    obs = random.choice(potential_observations)
                    if obs not in observations:
                        observations.append(obs)
                
                participant_results.append({
                    "participant_id": participant["id"],
                    "success": success,
                    "time_on_task": time_on_task,
                    "error_count": error_count,
                    "observations": observations,
                    "quotes": [f"Example quote from {participant['id']} about {scenario}"],
                    "satisfaction_rating": random.randint(1, 5)  # 1-5 scale
                })
            
            # Calculate scenario metrics
            success_rate = sum(1 for r in participant_results if r["success"]) / len(participant_results)
            avg_time = sum(r["time_on_task"] for r in participant_results) / len(participant_results)
            avg_errors = sum(r["error_count"] for r in participant_results) / len(participant_results)
            avg_satisfaction = sum(r["satisfaction_rating"] for r in participant_results) / len(participant_results)
            
            # Identify common issues
            all_observations = [obs for r in participant_results for obs in r["observations"]]
            from collections import Counter
            observation_counts = Counter(all_observations)
            common_issues = [issue for issue, count in observation_counts.items() 
                           if count > len(participant_results) * 0.3]  # Issues observed by >30% of participants
            
            scenario_results.append({
                "scenario": scenario,
                "metrics": {
                    "success_rate": success_rate,
                    "average_time_on_task": avg_time,
                    "average_error_count": avg_errors,
                    "average_satisfaction": avg_satisfaction
                },
                "common_issues": common_issues,
                "participant_results": participant_results
            })
        
        # Generate recommendations based on test results
        recommendations = []
        for result in scenario_results:
            if result["metrics"]["success_rate"] < 0.7:
                recommendations.append(f"Improve task flow for {result['scenario']}")
            if result["metrics"]["average_satisfaction"] < 3.0:
                recommendations.append(f"Address satisfaction issues with {result['scenario']}")
            for issue in result["common_issues"]:
                recommendations.append(f"Fix common issue: {issue}")
        
        # De-duplicate recommendations
        recommendations = list(set(recommendations))
        
        return {
            "product_name": product_name,
            "test_date": "",  # Could be filled with actual date
            "participants": participants,
            "scenario_results": scenario_results,
            "overall_metrics": {
                "average_success_rate": sum(r["metrics"]["success_rate"] for r in scenario_results) / len(scenario_results),
                "average_satisfaction": sum(r["metrics"]["average_satisfaction"] for r in scenario_results) / len(scenario_results)
            },
            "recommendations": recommendations,
            "priority_issues": [r["common_issues"][0] for r in scenario_results if r["common_issues"]][:3]  # Top 3 issues
        }
    
    def _calculate_usability_rating(self, total_issues: int, element_count: int) -> str:
        """Calculate an overall usability rating based on issues found.
        
        Args:
            total_issues: Total number of issues found
            element_count: Number of interface elements evaluated
            
        Returns:
            Usability rating (Excellent, Good, Fair, Poor)
        """
        # Calculate issues per element
        if element_count == 0:
            return "Unknown"
            
        issues_per_element = total_issues / element_count
        
        if issues_per_element < 1:
            return "Excellent"
        elif issues_per_element < 2:
            return "Good"
        elif issues_per_element < 3:
            return "Fair"
        else:
            return "Poor"
    
    def _update_metrics_from_task(self, task: Dict[str, Any]) -> None:
        """Update agent's performance metrics based on task execution.
        
        Args:
            task: Completed task
        """
        task_type = task.get("type", "")
        
        if task_type == "persona_creation":
            # Update metrics related to persona creation
            current = self.performance_metrics.get("persona_quality", 0.0)
            self.update_metric("persona_quality", min(1.0, current + 0.1))
            
        elif task_type == "user_flow_mapping" or task_type == "heuristic_evaluation":
            # Update metrics related to usability assessment
            current = self.performance_metrics.get("usability_assessment", 0.0)
            self.update_metric("usability_assessment", min(1.0, current + 0.1))
            
        elif task_type == "usability_testing":
            # Update metrics related to UX recommendations
            current = self.performance_metrics.get("ux_recommendations", 0.0)
            self.update_metric("ux_recommendations", min(1.0, current + 0.1))