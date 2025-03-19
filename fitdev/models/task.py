#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Task Model for FitDev.io
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import uuid
from datetime import datetime


class TaskStatus(Enum):
    """Enum for task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class Task:
    """Represents a task in the FitDev.io system."""
    
    def __init__(self, title: str, description: str, task_type: str, 
                priority: int = 0, assigned_to: Optional[str] = None):
        """Initialize a task.
        
        Args:
            title: Task title
            description: Detailed task description
            task_type: Type of task (e.g., 'development', 'review')
            priority: Task priority (higher number = higher priority) 
            assigned_to: ID of the agent assigned to this task
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.task_type = task_type
        self.priority = priority
        self.assigned_to = assigned_to
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.completed_at = None
        self.dependencies: List[str] = []  # IDs of tasks this task depends on
        self.subtasks: List[str] = []  # IDs of subtasks
        self.parent_task: Optional[str] = None  # ID of parent task if this is a subtask
        self.tags: List[str] = []
        self.metadata: Dict[str, Any] = {}
        self.results: Dict[str, Any] = {}
    
    def update_status(self, status: TaskStatus) -> None:
        """Update the task status.
        
        Args:
            status: New status for the task
        """
        self.status = status
        self.updated_at = datetime.now()
        
        if status == TaskStatus.COMPLETED:
            self.completed_at = datetime.now()
    
    def add_dependency(self, task_id: str) -> None:
        """Add a dependency for this task.
        
        Args:
            task_id: ID of the task this task depends on
        """
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
            self.updated_at = datetime.now()
    
    def add_subtask(self, task_id: str) -> None:
        """Add a subtask to this task.
        
        Args:
            task_id: ID of the subtask
        """
        if task_id not in self.subtasks:
            self.subtasks.append(task_id)
            self.updated_at = datetime.now()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to this task.
        
        Args:
            tag: Tag to add
        """
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
    
    def add_result(self, key: str, value: Any) -> None:
        """Add a result to this task.
        
        Args:
            key: Result identifier
            value: Result value
        """
        self.results[key] = value
        self.updated_at = datetime.now()
    
    def can_start(self, completed_task_ids: List[str]) -> bool:
        """Check if this task can be started based on its dependencies.
        
        Args:
            completed_task_ids: List of IDs of completed tasks
            
        Returns:
            True if all dependencies are satisfied, False otherwise
        """
        return all(dep_id in completed_task_ids for dep_id in self.dependencies)
    
    def __repr__(self) -> str:
        """String representation of the task."""
        return f"{self.title} ({self.status.value})"
