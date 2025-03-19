#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for FitDev.io Virtual Software Development Organization
"""

import logging
from fitdev.organization import Organization
from fitdev.models.task import Task

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_test_tasks(org: Organization) -> None:
    """Create test tasks for the organization.
    
    Args:
        org: Organization to add tasks to
    """
    # Frontend task
    frontend_task = Task(
        title="Create User Profile Component",
        description="Implement a responsive user profile component with avatar, user details, and edit functionality",
        task_type="component_implementation",
        priority=8
    )
    org.add_task(frontend_task)
    
    # Backend task
    backend_task = Task(
        title="Create User API Endpoints",
        description="Develop RESTful API endpoints for user profile management",
        task_type="api_development",
        priority=7
    )
    org.add_task(backend_task)
    
    # Styling task
    styling_task = Task(
        title="Implement Theme System",
        description="Create a theme system supporting light and dark modes with consistent styling",
        task_type="styling",
        priority=6
    )
    org.add_task(styling_task)
    
    # Integration task
    integration_task = Task(
        title="Connect Profile Component to API",
        description="Integrate the user profile component with the backend API endpoints",
        task_type="frontend_integration",
        priority=5
    )
    org.add_task(integration_task)

def test_organization():
    """Test the FitDev.io organization execution."""
    logger.info("Starting FitDev.io test")
    
    # Initialize organization
    org = Organization(name="FitDev.io Test Instance")
    
    # Create test tasks
    create_test_tasks(org)
    
    # Run the organization for 3 cycles
    results = org.run_organization(max_cycles=3)
    
    # Display results
    logger.info("Organization test completed")
    logger.info(f"Organization: {results['name']}")
    logger.info(f"Agents: {results['agents']}")
    logger.info(f"Tasks completed: {results['tasks_completed']}")
    logger.info(f"Tasks pending: {results['tasks_pending']}")
    logger.info(f"Total compensation: {results['total_compensation']:.2f}")
    logger.info(f"Average performance: {results['average_performance']:.2f}")
    
    return results

if __name__ == "__main__":
    test_results = test_organization()
    print("\nTest Results Summary:")
    print("=====================")
    print(f"Organization: {test_results['name']}")
    print(f"Number of agents: {test_results['agents']}")
    print(f"Tasks completed: {test_results['tasks_completed']}")
    print(f"Tasks pending: {test_results['tasks_pending']}")
    print(f"Total compensation: ${test_results['total_compensation']:.2f}")
    print(f"Average performance: {test_results['average_performance']:.2f}")