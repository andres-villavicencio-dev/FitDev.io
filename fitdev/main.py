#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FitDev.io - Virtual Software Development Organization Generator

Main entry point for the FitDev.io application.
"""

import logging
import argparse
from dotenv import load_dotenv

from organization import Organization
from models.task import Task

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_sample_tasks(org: Organization) -> None:
    """Create sample tasks for the organization.
    
    Args:
        org: Organization to add tasks to
    """
    # Executive tasks
    
    # Project Planning Task
    planning_task = Task(
        title="Create Project Plan",
        description="Develop a comprehensive project plan for the new application",
        task_type="project_planning",
        priority=10
    )
    org.add_task(planning_task)
    
    # Architecture Design Task
    architecture_task = Task(
        title="Design System Architecture",
        description="Design the overall system architecture for the new application",
        task_type="architecture_design",
        priority=9
    )
    org.add_task(architecture_task)
    
    # Requirement Gathering Task
    requirements_task = Task(
        title="Gather Requirements",
        description="Gather and document project requirements from stakeholders",
        task_type="requirement_gathering",
        priority=8
    )
    org.add_task(requirements_task)
    
    # Development tasks
    
    # Frontend Component Implementation Task
    frontend_task = Task(
        title="Implement User Dashboard",
        description="Create a responsive dashboard component for the user interface",
        task_type="component_implementation",
        priority=7
    )
    org.add_task(frontend_task)
    
    # Backend API Development Task
    backend_task = Task(
        title="Develop User API",
        description="Create RESTful API endpoints for user management",
        task_type="api_development",
        priority=7
    )
    org.add_task(backend_task)
    
    # Full Stack Feature Implementation Task
    fullstack_task = Task(
        title="Implement Authentication System",
        description="Develop complete authentication feature with frontend and backend components",
        task_type="feature_implementation",
        priority=6
    )
    org.add_task(fullstack_task)
    
    # DevOps CI/CD Implementation Task
    devops_task = Task(
        title="Set Up CI/CD Pipeline",
        description="Create continuous integration and deployment pipeline for the project",
        task_type="ci_cd_implementation",
        priority=5
    )
    org.add_task(devops_task)


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description="FitDev.io Virtual Software Development Organization")
    parser.add_argument("--cycles", type=int, default=5, help="Number of organization cycles to run")
    args = parser.parse_args()
    
    logger.info("Starting FitDev.io Virtual Software Development Organization")
    
    # Initialize the organization
    org = Organization()
    
    # Create sample tasks
    create_sample_tasks(org)
    
    # Run the organization
    results = org.run_organization(max_cycles=args.cycles)
    
    # Display results
    logger.info("Organization run completed")
    logger.info(f"Organization: {results['name']}")
    logger.info(f"Agents: {results['agents']}")
    logger.info(f"Tasks completed: {results['tasks_completed']}")
    logger.info(f"Tasks pending: {results['tasks_pending']}")
    logger.info(f"Total compensation: {results['total_compensation']:.2f}")
    logger.info(f"Average performance: {results['average_performance']:.2f}")


if __name__ == "__main__":
    main()
