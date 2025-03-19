#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Organization Class for FitDev.io
"""

from typing import Dict, List, Any, Optional, Type
import logging
from pathlib import Path

from models.agent import BaseAgent
from models.task import Task, TaskStatus
from models.compensation import CompensationSystem
from config.config import load_config

# Import agent implementations
from agents.executive.ceo import CEOAgent
from agents.executive.cto import CTOAgent
from agents.executive.product_owner import ProductOwnerAgent
from agents.development.frontend import FrontendDeveloperAgent
from agents.development.backend import BackendDeveloperAgent
from agents.development.fullstack import FullStackDeveloperAgent
from agents.development.devops import DevOpsEngineerAgent
from agents.quality.qa_engineer import QAEngineerAgent
from agents.quality.security_specialist import SecuritySpecialistAgent
from agents.quality.technical_writer import TechnicalWriterAgent
from agents.specialized.knowledge_management import KnowledgeManagementAgent
from agents.specialized.trend_scout import TrendScoutAgent
from agents.specialized.ux_simulator import UXSimulatorAgent
from agents.specialized.api_specialist import APISpecialistAgent
from agents.specialized.tech_debt_manager import TechDebtManagerAgent

# Import critic implementations
from critics.executive.ceo_critic import CEOCritic
from critics.executive.cto_critic import CTOCritic
from critics.executive.product_owner_critic import ProductOwnerCritic
from critics.development.frontend_critic import FrontendDeveloperCritic
from critics.development.backend_critic import BackendDeveloperCritic
from critics.development.fullstack_critic import FullStackDeveloperCritic
from critics.development.devops_critic import DevOpsEngineerCritic
from critics.quality.qa_engineer_critic import QAEngineerCritic
from critics.quality.security_specialist_critic import SecuritySpecialistCritic
from critics.quality.technical_writer_critic import TechnicalWriterCritic
from critics.specialized.knowledge_management_critic import KnowledgeManagementCritic
from critics.specialized.trend_scout_critic import TrendScoutCritic
from critics.specialized.ux_simulator_critic import UXSimulatorCritic
from critics.specialized.api_specialist_critic import APISpecialistCritic
from critics.specialized.tech_debt_manager_critic import TechDebtManagerCritic

logger = logging.getLogger(__name__)


class Organization:
    """Main organization class that manages agents, critics, tasks, and compensation."""
    
    def __init__(self, name: str = "FitDev.io"):
        """Initialize the organization.
        
        Args:
            name: Organization name
        """
        self.name = name
        self.config = load_config()
        self.agents: Dict[str, BaseAgent] = {}
        self.critics: Dict[str, BaseCritic] = {}
        self.agent_critic_pairs: Dict[str, str] = {}  # Maps agent_id -> critic_id
        self.tasks: Dict[str, Task] = {}
        self.completed_tasks: List[str] = []
        self.evaluations: Dict[str, List[Dict[str, Any]]] = {}  # Maps agent_id -> list of evaluations
        
        # Initialize compensation system
        self.compensation_system = CompensationSystem(
            base_rates=self.config["compensation"]["base_rates"],
            performance_multiplier=self.config["compensation"]["performance_multiplier"]
        )
        
        # Initialize default agents and critics
        self._initialize_default_agents()
    
    def _initialize_default_agents(self) -> None:
        """Initialize default agents and critics for the organization."""
        # Executive agents and critics
        self.add_agent_with_critic(CEOAgent(), CEOCritic())
        self.add_agent_with_critic(CTOAgent(), CTOCritic())
        self.add_agent_with_critic(ProductOwnerAgent(), ProductOwnerCritic())
        
        # Development agents and critics
        self.add_agent_with_critic(FrontendDeveloperAgent(), FrontendDeveloperCritic())
        self.add_agent_with_critic(BackendDeveloperAgent(), BackendDeveloperCritic())
        self.add_agent_with_critic(FullStackDeveloperAgent(), FullStackDeveloperCritic())
        self.add_agent_with_critic(DevOpsEngineerAgent(), DevOpsEngineerCritic())
        
        # Quality agents and critics
        self.add_agent_with_critic(QAEngineerAgent(), QAEngineerCritic())
        self.add_agent_with_critic(SecuritySpecialistAgent(), SecuritySpecialistCritic())
        self.add_agent_with_critic(TechnicalWriterAgent(), TechnicalWriterCritic())
        
        # Specialized agents and critics
        self.add_agent_with_critic(KnowledgeManagementAgent(), KnowledgeManagementCritic())
        self.add_agent_with_critic(TrendScoutAgent(), TrendScoutCritic())
        self.add_agent_with_critic(UXSimulatorAgent(), UXSimulatorCritic())
        self.add_agent_with_critic(APISpecialistAgent(), APISpecialistCritic())
        self.add_agent_with_critic(TechDebtManagerAgent(), TechDebtManagerCritic())
    
    def add_agent(self, agent: BaseAgent) -> str:
        """Add an agent to the organization.
        
        Args:
            agent: Agent to add
            
        Returns:
            Agent ID
        """
        self.agents[agent.id] = agent
        self.evaluations[agent.id] = []
        logger.info(f"Added agent: {agent.name} ({agent.role})")
        return agent.id
        
    def add_critic(self, critic: BaseCritic) -> str:
        """Add a critic to the organization.
        
        Args:
            critic: Critic to add
            
        Returns:
            Critic ID
        """
        self.critics[critic.id] = critic
        logger.info(f"Added critic: {critic.name} for {critic.target_role}")
        return critic.id
    
    def add_agent_with_critic(self, agent: BaseAgent, critic: BaseCritic) -> tuple:
        """Add an agent and its corresponding critic to the organization.
        
        Args:
            agent: Agent to add
            critic: Critic for the agent
            
        Returns:
            Tuple of (agent_id, critic_id)
        """
        agent_id = self.add_agent(agent)
        critic_id = self.add_critic(critic)
        self.agent_critic_pairs[agent_id] = critic_id
        logger.info(f"Paired agent {agent.name} with critic {critic.name}")
        return agent_id, critic_id
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an agent by ID.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent if found, None otherwise
        """
        return self.agents.get(agent_id)
    
    def get_agents_by_role(self, role: str) -> List[BaseAgent]:
        """Get all agents with a specific role.
        
        Args:
            role: Role to filter by
            
        Returns:
            List of agents with the specified role
        """
        return [agent for agent in self.agents.values() if agent.role == role]
    
    def add_task(self, task: Task) -> None:
        """Add a task to the organization.
        
        Args:
            task: Task to add
        """
        self.tasks[task.id] = task
        logger.info(f"Added task: {task.title}")
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task if found, None otherwise
        """
        return self.tasks.get(task_id)
    
    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign a task to an agent.
        
        Args:
            task_id: Task ID
            agent_id: Agent ID
            
        Returns:
            True if task was assigned successfully, False otherwise
        """
        task = self.get_task(task_id)
        agent = self.get_agent(agent_id)
        
        if not task or not agent:
            return False
        
        task.assigned_to = agent_id
        task.update_status(TaskStatus.IN_PROGRESS)
        logger.info(f"Assigned task '{task.title}' to {agent.name}")
        
        return True
    
    def complete_task(self, task_id: str, results: Dict[str, Any]) -> bool:
        """Mark a task as completed and request critic evaluation.
        
        Args:
            task_id: Task ID
            results: Task results
            
        Returns:
            True if task was completed successfully, False otherwise
        """
        task = self.get_task(task_id)
        
        if not task:
            return False
        
        # Add results to task
        for key, value in results.items():
            task.add_result(key, value)
        
        # Update task status
        task.update_status(TaskStatus.COMPLETED)
        self.completed_tasks.append(task_id)
        
        # Update agent's performance metrics and get critic evaluation
        if task.assigned_to and task.assigned_to in self.agents:
            agent = self.agents[task.assigned_to]
            agent_id = task.assigned_to
            
            # Get critic evaluation if a critic is paired with this agent
            if agent_id in self.agent_critic_pairs:
                critic_id = self.agent_critic_pairs[agent_id]
                if critic_id in self.critics:
                    critic = self.critics[critic_id]
                    
                    # Prepare work output for evaluation
                    work_output = {
                        "type": task.task_type,
                        "title": task.title,
                        "description": task.description,
                        "results": task.results,
                        "agent": agent.name,
                        "agent_role": agent.role
                    }
                    
                    # Get evaluation from critic
                    evaluation = critic.evaluate_work(work_output)
                    
                    # Add evaluation to agent's evaluations
                    self.evaluations[agent_id].append(evaluation)
                    
                    # Update agent's performance metrics based on evaluation
                    evaluation_score = evaluation.get("score", 0.5)
                    
                    # Update different metrics based on task type
                    if task.task_type in ["component_implementation", "styling", "frontend_integration"]:
                        agent.update_metric("code_quality", evaluation_score)
                    elif task.task_type in ["test_planning", "test_automation", "bug_verification"]:
                        agent.update_metric("test_coverage", evaluation_score)
                    elif task.task_type in ["security_assessment", "code_security_review"]:
                        agent.update_metric("vulnerability_detection", evaluation_score)
                    elif task.task_type in ["api_documentation", "user_guide", "developer_documentation"]:
                        agent.update_metric("documentation_clarity", evaluation_score)
                    # Specialized agent task types
                    elif task.task_type in ["persona_creation", "user_flow_mapping", "heuristic_evaluation", "usability_testing"]:
                        agent.update_metric("ux_expertise", evaluation_score)
                    elif task.task_type in ["api_design", "api_documentation", "api_security_review", "api_versioning_strategy"]:
                        agent.update_metric("api_quality", evaluation_score)
                    elif task.task_type in ["tech_debt_assessment", "refactoring_plan", "debt_prioritization", "architecture_evaluation"]:
                        agent.update_metric("architecture_quality", evaluation_score)
                    # Add more task type mappings as needed
                    
                    logger.info(f"Critic {critic.name} evaluated {agent.name}'s work with score {evaluation_score:.2f}")
                    
                else:
                    logger.warning(f"Critic {critic_id} not found for agent {agent_id}")
            else:
                logger.info(f"No critic paired with agent {agent_id}")
        
        logger.info(f"Completed task: {task.title}")
        
        return True
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks.
        
        Returns:
            List of pending tasks
        """
        return [task for task in self.tasks.values() 
                if task.status == TaskStatus.PENDING]
    
    def get_available_tasks(self) -> List[Task]:
        """Get all tasks that can be started based on dependencies.
        
        Returns:
            List of available tasks
        """
        return [task for task in self.get_pending_tasks() 
                if task.can_start(self.completed_tasks)]
    
    def get_agent_evaluations(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all evaluations for a specific agent.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            List of evaluations for the agent
        """
        if agent_id not in self.evaluations:
            return []
            
        return self.evaluations[agent_id]
    
    def get_agent_average_evaluation_score(self, agent_id: str) -> float:
        """Calculate the average evaluation score for an agent.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Average evaluation score (0.0 to 1.0)
        """
        evaluations = self.get_agent_evaluations(agent_id)
        
        if not evaluations:
            return 0.5  # Default score if no evaluations
        
        total_score = sum(eval.get("score", 0.5) for eval in evaluations)
        return total_score / len(evaluations)
    
    def calculate_compensation(self) -> Dict[str, float]:
        """Calculate compensation for all agents.
        
        Returns:
            Dictionary mapping agent IDs to compensation amounts
        """
        results = {}
        
        for agent_id, agent in self.agents.items():
            # Use both self-evaluation and critic evaluations
            self_score = agent.evaluate_performance()
            critic_score = self.get_agent_average_evaluation_score(agent_id)
            
            # Combined score with more weight on critic evaluation
            combined_score = (self_score * 0.4) + (critic_score * 0.6)
            
            compensation = self.compensation_system.calculate_compensation(
                agent_id, agent.role, combined_score
            )
            results[agent_id] = compensation
            
            logger.info(f"Calculated compensation for {agent.name}: {compensation:.2f} " +
                        f"(self: {self_score:.2f}, critic: {critic_score:.2f})")
            
        return results
    
    def select_agent_for_task(self, task: Task) -> Optional[str]:
        """Select the most appropriate agent for a task based on task type and agent skills.
        
        Args:
            task: Task to assign
            
        Returns:
            ID of the selected agent, or None if no suitable agent found
        """
        task_type = task.task_type
        
        # Map task types to appropriate agent roles
        role_mapping = {
            # Development task types
            "component_implementation": "development",
            "styling": "development",
            "frontend_integration": "development",
            "backend_development": "development",
            "api_development": "development",
            "devops_task": "development",
            
            # Quality task types
            "test_planning": "quality",
            "test_automation": "quality",
            "bug_verification": "quality",
            "security_assessment": "quality",
            "code_security_review": "quality",
            "security_implementation": "quality",
            "api_documentation": "quality",
            "user_guide": "quality",
            "developer_documentation": "quality",
            
            # Executive task types
            "project_planning": "executive",
            "product_strategy": "executive",
            "resource_allocation": "executive",
            "roadmap_planning": "executive",
            
            # Specialized task types
            "knowledge_base_creation": "specialized",
            "information_architecture": "specialized",
            "knowledge_transfer": "specialized",
            "trend_research": "specialized",
            "tool_evaluation": "specialized",
            "technology_recommendations": "specialized",
            "persona_creation": "specialized",
            "user_flow_mapping": "specialized",
            "heuristic_evaluation": "specialized",
            "usability_testing": "specialized",
            "api_design": "specialized",
            "api_documentation": "specialized",
            "api_security_review": "specialized",
            "api_versioning_strategy": "specialized",
            "tech_debt_assessment": "specialized",
            "refactoring_plan": "specialized",
            "debt_prioritization": "specialized",
            "architecture_evaluation": "specialized"
        }
        
        # Get the appropriate role for this task
        role = role_mapping.get(task_type, "executive")  # Default to executive if unknown
        
        # More specific agent selection within the role
        if role == "development":
            if task_type in ["component_implementation", "styling", "frontend_integration"]:
                # Frontend tasks
                frontend_agents = [agent for agent in self.agents.values() 
                                  if agent.role == "development" and "Frontend" in agent.name]
                if frontend_agents:
                    return frontend_agents[0].id
            
            elif task_type in ["backend_development", "api_development"]:
                # Backend tasks
                backend_agents = [agent for agent in self.agents.values() 
                                 if agent.role == "development" and "Backend" in agent.name]
                if backend_agents:
                    return backend_agents[0].id
            
            elif task_type in ["devops_task"]:
                # DevOps tasks
                devops_agents = [agent for agent in self.agents.values() 
                                if agent.role == "development" and "DevOps" in agent.name]
                if devops_agents:
                    return devops_agents[0].id
        
        elif role == "quality":
            if task_type in ["test_planning", "test_automation", "bug_verification"]:
                # QA tasks
                qa_agents = [agent for agent in self.agents.values() 
                            if agent.role == "quality" and "QA" in agent.name]
                if qa_agents:
                    return qa_agents[0].id
            
            elif task_type in ["security_assessment", "code_security_review", "security_implementation"]:
                # Security tasks
                security_agents = [agent for agent in self.agents.values() 
                                 if agent.role == "quality" and "Security" in agent.name]
                if security_agents:
                    return security_agents[0].id
            
            elif task_type in ["api_documentation", "user_guide", "developer_documentation"]:
                # Documentation tasks
                writer_agents = [agent for agent in self.agents.values() 
                               if agent.role == "quality" and "Writer" in agent.name]
                if writer_agents:
                    return writer_agents[0].id
        
        elif role == "executive":
            if task_type in ["project_planning", "resource_allocation"]:
                # CTO tasks
                cto_agents = [agent for agent in self.agents.values() 
                             if agent.role == "executive" and "CTO" in agent.name]
                if cto_agents:
                    return cto_agents[0].id
            
            elif task_type in ["product_strategy", "roadmap_planning"]:
                # Product Owner tasks
                po_agents = [agent for agent in self.agents.values() 
                            if agent.role == "executive" and "Product" in agent.name]
                if po_agents:
                    return po_agents[0].id
        
        elif role == "specialized":
            if task_type in ["knowledge_base_creation", "information_architecture", "knowledge_transfer"]:
                # Knowledge Management tasks
                km_agents = [agent for agent in self.agents.values() 
                           if agent.role == "specialized" and "Knowledge Management" in agent.name]
                if km_agents:
                    return km_agents[0].id
            
            elif task_type in ["trend_research", "tool_evaluation", "technology_recommendations"]:
                # Trend Scout tasks
                trend_agents = [agent for agent in self.agents.values() 
                               if agent.role == "specialized" and "Trend Scout" in agent.name]
                if trend_agents:
                    return trend_agents[0].id
            
            elif task_type in ["persona_creation", "user_flow_mapping", "heuristic_evaluation", "usability_testing"]:
                # UX Simulator tasks
                ux_agents = [agent for agent in self.agents.values() 
                            if agent.role == "specialized" and "UX Simulator" in agent.name]
                if ux_agents:
                    return ux_agents[0].id
            
            elif task_type in ["api_design", "api_documentation", "api_security_review", "api_versioning_strategy"]:
                # API Specialist tasks
                api_agents = [agent for agent in self.agents.values() 
                             if agent.role == "specialized" and "API Specialist" in agent.name]
                if api_agents:
                    return api_agents[0].id
            
            elif task_type in ["tech_debt_assessment", "refactoring_plan", "debt_prioritization", "architecture_evaluation"]:
                # Tech Debt Manager tasks
                debt_agents = [agent for agent in self.agents.values() 
                              if agent.role == "specialized" and "Tech Debt Manager" in agent.name]
                if debt_agents:
                    return debt_agents[0].id
        
        # If no specific agent found, fall back to role-based selection
        agents = self.get_agents_by_role(role)
        if agents:
            return agents[0].id
        
        # If still no agent found, return any agent
        if self.agents:
            return next(iter(self.agents.keys()))
        
        return None
    
    def run_organization(self, max_cycles: int = 10) -> Dict[str, Any]:
        """Run the organization for a number of cycles.
        
        Args:
            max_cycles: Maximum number of cycles to run
            
        Returns:
            Organization status and metrics
        """
        logger.info(f"Starting {self.name} for {max_cycles} cycles")
        
        for cycle in range(max_cycles):
            logger.info(f"Cycle {cycle + 1}/{max_cycles}")
            
            # Get available tasks
            available_tasks = self.get_available_tasks()
            
            if not available_tasks:
                logger.info("No available tasks")
                break
            
            # Assign and execute tasks
            for task in available_tasks:
                # Find appropriate agent for task using the new selection logic
                agent_id = self.select_agent_for_task(task)
                
                if not agent_id or agent_id not in self.agents:
                    logger.warning(f"No suitable agent found for task: {task.title}")
                    continue
                
                agent = self.agents[agent_id]
                self.assign_task(task.id, agent.id)
                
                # Execute task
                task_data = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "type": task.task_type,
                    # Add more task data as needed
                }
                
                results = agent.execute_task(task_data)
                self.complete_task(task.id, results)
            
            # Calculate compensation at the end of the cycle
            if cycle == max_cycles - 1 or not self.get_pending_tasks():
                self.calculate_compensation()
        
        # Compile organization status and metrics
        total_evaluations = sum(len(evals) for evals in self.evaluations.values())
        
        return {
            "name": self.name,
            "agents": len(self.agents),
            "tasks_completed": len(self.completed_tasks),
            "tasks_pending": len(self.get_pending_tasks()),
            "total_evaluations": total_evaluations,
            "total_compensation": self.compensation_system.get_total_compensation(),
            "average_performance": self.compensation_system.get_average_performance()
        }