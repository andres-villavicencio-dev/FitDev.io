#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for reinforcement learning in FitDev.io
"""

import os
import sys
import logging
import random
import json
from dotenv import load_dotenv

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from fitdev
from fitdev.models.reinforcement import (
    ParameterLearningSystem,
    PromptEngineeringSystem,
    TaskStrategySystem
)
from fitdev.agents.development.frontend import FrontendDeveloperAgent
from fitdev.models.task import Task
from fitdev.organization import Organization

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def test_parameter_learning():
    """Test the parameter learning system."""
    logger.info("Testing parameter learning system...")
    
    # Create a parameter learning system
    agent_id = "test-agent-1"
    role = "frontend-developer"
    learning_system = ParameterLearningSystem(agent_id, role)
    
    # Print initial parameters
    logger.info("Initial parameters:")
    for param, value in learning_system.parameters.items():
        logger.info(f"  {param}: {value:.2f}")
    
    # Simulate multiple rounds of compensation feedback
    task_types = ["component_implementation", "styling", "frontend_integration"]
    
    for i in range(5):
        # Randomly choose a task type
        task_type = random.choice(task_types)
        
        # Simulate compensation - higher for later rounds to simulate improvement
        compensation = 50.0 + (i * 10.0) + random.uniform(-5.0, 5.0)
        
        # Update parameters based on compensation
        learning_system.update_from_compensation(compensation, task_type)
        
        logger.info(f"Round {i+1}: Task: {task_type}, Compensation: {compensation:.2f}")
        logger.info("Updated parameters:")
        for param, value in learning_system.parameters.items():
            logger.info(f"  {param}: {value:.2f}")
    
    # Get optimal parameters
    optimal_params = learning_system.get_optimal_parameters()
    logger.info("Optimal parameters:")
    for param, value in optimal_params.items():
        logger.info(f"  {param}: {value:.2f}")
    
    # Save and load test
    test_dir = "test_data/learning"
    os.makedirs(test_dir, exist_ok=True)
    test_file = f"{test_dir}/{agent_id}_{role}_parameters.json"
    
    try:
        learning_system.save_to_file(test_dir)
        logger.info(f"Saved parameters to {test_file}")
        
        loaded_system = ParameterLearningSystem.load_from_file(test_file)
        logger.info("Loaded parameters successfully")
        
        assert loaded_system.agent_id == agent_id
        assert loaded_system.role == role
        assert len(loaded_system.parameters) == len(learning_system.parameters)
        
        # Clean up
        os.remove(test_file)
    except Exception as e:
        logger.error(f"Error during save/load test: {e}")

def test_prompt_engineering():
    """Test the prompt engineering system."""
    logger.info("Testing prompt engineering system...")
    
    # Create a prompt engineering system
    agent_id = "test-agent-2"
    role = "frontend-developer"
    prompt_system = PromptEngineeringSystem(agent_id, role)
    
    # Print initial templates
    logger.info("Initial prompt templates:")
    for task_type, templates in prompt_system.prompt_templates.items():
        logger.info(f"  Task type: {task_type}")
        for i, template in enumerate(templates):
            logger.info(f"    Template {i+1}: {template[:50]}...")
    
    # Add a new template
    new_template = "As a {role}, implement a {component_type} component in {framework}. Requirements: {task_description}"
    prompt_system.add_template("component_implementation", new_template)
    logger.info(f"Added new template: {new_template}")
    
    # Test prompt generation
    task_types = ["component_implementation", "styling", "general"]
    context = {
        "role": "Frontend Developer",
        "component_type": "user profile",
        "framework": "React",
        "task_description": "Create a responsive user profile component"
    }
    
    for i in range(3):
        # Randomly choose a task type
        task_type = random.choice(task_types)
        
        # Generate a prompt
        prompt = prompt_system.get_prompt(task_type, context)
        logger.info(f"Generated prompt for {task_type}: {prompt}")
        
        # Record result with random compensation
        compensation = 50.0 + random.uniform(0.0, 50.0)
        prompt_system.record_result(task_type, prompt, compensation)
        logger.info(f"Recorded result with compensation: {compensation:.2f}")
    
    # Save and load test
    test_dir = "test_data/learning"
    os.makedirs(test_dir, exist_ok=True)
    test_file = f"{test_dir}/{agent_id}_{role}_prompts.json"
    
    try:
        prompt_system.save_to_file(test_dir)
        logger.info(f"Saved prompts to {test_file}")
        
        loaded_system = PromptEngineeringSystem.load_from_file(test_file)
        logger.info("Loaded prompts successfully")
        
        assert loaded_system.agent_id == agent_id
        assert loaded_system.role == role
        assert len(loaded_system.prompt_templates) == len(prompt_system.prompt_templates)
        
        # Clean up
        os.remove(test_file)
    except Exception as e:
        logger.error(f"Error during save/load test: {e}")

def test_task_strategy():
    """Test the task strategy system."""
    logger.info("Testing task strategy system...")
    
    # Create a task strategy system
    agent_id = "test-agent-3"
    role = "frontend-developer"
    strategy_system = TaskStrategySystem(agent_id, role)
    
    # Print initial strategies
    logger.info("Initial strategies:")
    for task_type, strategies in strategy_system.strategies.items():
        logger.info(f"  Task type: {task_type}")
        for i, strategy in enumerate(strategies):
            logger.info(f"    Strategy {i+1}: {strategy['name']} - {strategy['description']}")
    
    # Add a new strategy
    new_strategy = {
        "name": "Mobile-First Approach",
        "description": "Start with mobile layout and progressively enhance for larger screens",
        "steps": ["mobile_design", "implement_mobile", "adapt_for_desktop", "test_responsive"]
    }
    strategy_system.add_strategy("component_implementation", new_strategy)
    logger.info(f"Added new strategy: {new_strategy['name']}")
    
    # Test strategy selection
    task_types = ["component_implementation", "styling", "api_development", "general"]
    
    for i in range(5):
        # Randomly choose a task type
        task_type = random.choice(task_types)
        
        # Get a strategy
        strategy = strategy_system.get_strategy(task_type)
        logger.info(f"Selected strategy for {task_type}: {strategy['name']} - {strategy['description']}")
        
        # Record result with random compensation
        compensation = 50.0 + random.uniform(0.0, 50.0)
        strategy_system.record_result(task_type, strategy["name"], compensation)
        logger.info(f"Recorded result with compensation: {compensation:.2f}")
    
    # Get best strategy
    for task_type in task_types:
        best_strategy = strategy_system.get_best_strategy(task_type)
        if best_strategy:
            logger.info(f"Best strategy for {task_type}: {best_strategy['name']}")
    
    # Save and load test
    test_dir = "test_data/learning"
    os.makedirs(test_dir, exist_ok=True)
    test_file = f"{test_dir}/{agent_id}_{role}_strategies.json"
    
    try:
        strategy_system.save_to_file(test_dir)
        logger.info(f"Saved strategies to {test_file}")
        
        loaded_system = TaskStrategySystem.load_from_file(test_file)
        logger.info("Loaded strategies successfully")
        
        assert loaded_system.agent_id == agent_id
        assert loaded_system.role == role
        assert len(loaded_system.strategies) == len(strategy_system.strategies)
        
        # Clean up
        os.remove(test_file)
    except Exception as e:
        logger.error(f"Error during save/load test: {e}")

def test_agent_learning():
    """Test agent learning integration."""
    logger.info("Testing agent integration with learning systems...")
    
    # Enable learning for this test
    os.environ["ENABLE_LEARNING"] = "true"
    
    # Create a frontend developer agent
    frontend_dev = FrontendDeveloperAgent()
    
    # Create a task
    task = {
        "id": "task-123",
        "title": "Create User Profile Component",
        "description": "Implement a responsive user profile component with avatar, user details, and edit functionality",
        "type": "component_implementation",
        "component_type": "profile",
        "framework": "React"
    }
    
    # Execute the task
    logger.info(f"Executing task: {task['title']}...")
    
    # First execution
    try:
        result = frontend_dev.execute_task(task)
        logger.info(f"Task execution result status: {result.get('status', 'unknown')}")
        
        # Simulate compensation
        frontend_dev.calculate_compensation(85.0)
        logger.info(f"Calculated compensation: {frontend_dev.compensation:.2f}")
        
        # Get parameters and strategy for next execution
        if frontend_dev.learning_enabled and hasattr(frontend_dev, 'parameter_learning'):
            logger.info("Parameters after execution:")
            for param, value in frontend_dev.parameter_learning.parameters.items():
                logger.info(f"  {param}: {value:.2f}")
        
        # Get strategy
        if frontend_dev.learning_enabled and hasattr(frontend_dev, 'task_strategy'):
            strategy = frontend_dev.get_task_execution_strategy("component_implementation")
            logger.info(f"Strategy for next execution: {strategy['name']} - {strategy['description']}")
    except Exception as e:
        logger.error(f"Error during task execution: {e}")
    
    # Save learning data
    if frontend_dev.learning_enabled:
        try:
            frontend_dev.save_learning_data()
            logger.info("Saved agent learning data")
        except Exception as e:
            logger.error(f"Error saving learning data: {e}")
    
    # Clean up
    os.environ.pop("ENABLE_LEARNING", None)

def test_organization_learning():
    """Test organization with learning agents."""
    logger.info("Testing organization with learning agents...")
    
    # Enable learning for this test
    os.environ["ENABLE_LEARNING"] = "true"
    
    # Create organization
    org = Organization(name="FitDev.io Learning Test")
    
    # Create tasks
    tasks = [
        Task(
            title="Create User Profile Component",
            description="Implement a responsive user profile component with avatar and edit functionality",
            task_type="component_implementation",
            priority=8
        ),
        Task(
            title="Implement Theme System",
            description="Create a theme system with light and dark mode support",
            task_type="styling",
            priority=7
        )
    ]
    
    # Add tasks
    for task in tasks:
        org.add_task(task)
    
    # Run organization for 1 cycle
    try:
        results = org.run_organization(max_cycles=1)
        
        logger.info("Organization run completed")
        logger.info(f"Tasks completed: {results['tasks_completed']}")
        logger.info(f"Total compensation: {results['total_compensation']:.2f}")
        logger.info(f"Average performance: {results['average_performance']:.2f}")
    except Exception as e:
        logger.error(f"Error running organization: {e}")
    
    # Clean up
    os.environ.pop("ENABLE_LEARNING", None)

if __name__ == "__main__":
    logger.info("Starting reinforcement learning tests")
    
    # Test parameter learning
    test_parameter_learning()
    
    # Test prompt engineering
    test_prompt_engineering()
    
    # Test task strategy
    test_task_strategy()
    
    # Test agent learning integration
    test_agent_learning()
    
    # Test organization with learning
    test_organization_learning()
    
    logger.info("Reinforcement learning tests completed")