#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Technical Writer Agent for FitDev.io
"""

from typing import Dict, Any, List
from fitdev.models.agent import BaseAgent


class TechnicalWriterAgent(BaseAgent):
    """Technical Writer agent responsible for documentation and technical communication."""
    
    def __init__(self, name: str = "Technical Writer"):
        """Initialize the Technical Writer agent.
        
        Args:
            name: Agent name (default: "Technical Writer")
        """
        description = """Creates clear, comprehensive technical documentation including 
                      API references, user guides, developer documentation, and tutorials.
                      Focuses on clarity, accuracy, and accessibility of information."""
        super().__init__(name, "quality", description)
        
        # Add Technical Writer-specific skills
        self.add_skill("API Documentation")
        self.add_skill("User Guide Creation")
        self.add_skill("Technical Writing")
        self.add_skill("Documentation Systems")
        self.add_skill("Information Architecture")
        
        # Technical Writer-specific performance metrics
        self.update_metric("documentation_clarity", 0.0)
        self.update_metric("technical_accuracy", 0.0)
        self.update_metric("content_organization", 0.0)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task assigned to this agent.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results and metadata
        """
        # Task execution logic for the Technical Writer agent
        task_type = task.get("type", "")
        results = {"status": "completed", "agent": self.name}
        
        if task_type == "api_documentation":
            # Logic for API documentation tasks
            results["documentation"] = self._create_api_documentation(task)
            
        elif task_type == "user_guide":
            # Logic for user guide tasks
            results["guide"] = self._create_user_guide(task)
            
        elif task_type == "developer_documentation":
            # Logic for developer documentation tasks
            results["documentation"] = self._create_developer_documentation(task)
        
        # Update metrics based on task execution
        self._update_metrics_from_task(task)
        
        return results
    
    def evaluate_performance(self) -> float:
        """Evaluate Technical Writer agent's performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        # Weight factors for different metrics
        weights = {
            "documentation_clarity": 0.4,
            "technical_accuracy": 0.4,
            "content_organization": 0.2
        }
        
        # Calculate weighted performance score
        score = 0.0
        for metric, weight in weights.items():
            if metric in self.performance_metrics:
                # Normalize metric value to 0.0-1.0 range if needed
                metric_value = min(1.0, max(0.0, self.performance_metrics[metric]))
                score += metric_value * weight
        
        return score
    
    def _create_api_documentation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create API documentation.
        
        Args:
            task: Task containing API documentation requirements
            
        Returns:
            API documentation
        """
        api_name = task.get("api_name", "")
        endpoints = task.get("endpoints", [])
        format_type = task.get("format", "markdown")
        
        # Generate documentation (placeholder implementation)
        doc_content = f"""# {api_name} API Documentation

## Overview

This documentation provides details on how to use the {api_name} API.

## Authentication

API requests require authentication using Bearer tokens.

### Example

```
Authorization: Bearer YOUR_API_TOKEN
```

## Endpoints
"""
        # Generate endpoint documentation
        for i, endpoint in enumerate(endpoints):
            endpoint_name = endpoint.get("name", f"Endpoint {i+1}")
            method = endpoint.get("method", "GET")
            path = endpoint.get("path", "/")
            description = endpoint.get("description", "No description provided.")
            
            doc_content += f"""
### {endpoint_name}

**{method}** `{path}`

{description}

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
"""
            
            # Add parameters
            params = endpoint.get("parameters", [])
            for param in params:
                param_name = param.get("name", "")
                param_type = param.get("type", "string")
                required = "Yes" if param.get("required", False) else "No"
                param_desc = param.get("description", "")
                
                doc_content += f"| {param_name} | {param_type} | {required} | {param_desc} |\n"
            
            # Add response examples
            doc_content += """
#### Response

```json
{
    "status": "success",
    "data": {
        // Response data
    }
}
```
"""
        
        # Add error codes section
        doc_content += """
## Error Codes

| Code | Description |
|------|-------------|
| 400  | Bad Request - The request was malformed |
| 401  | Unauthorized - Authentication required |
| 403  | Forbidden - Insufficient permissions |
| 404  | Not Found - Resource not found |
| 500  | Internal Server Error - Something went wrong on the server |
"""
        
        return {
            "title": f"{api_name} API Documentation",
            "content": doc_content,
            "format": format_type,
            "endpoints_documented": len(endpoints),
            "word_count": len(doc_content.split())
        }
    
    def _create_user_guide(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a user guide.
        
        Args:
            task: Task containing user guide requirements
            
        Returns:
            User guide documentation
        """
        product_name = task.get("product_name", "")
        features = task.get("features", [])
        audience = task.get("audience", "end users")
        format_type = task.get("format", "markdown")
        
        # Generate user guide (placeholder implementation)
        guide_content = f"""# {product_name} User Guide

## Introduction

Welcome to the {product_name} user guide. This document will help {audience} get started and make the most of {product_name}.

## Getting Started

### System Requirements

- Operating System: Windows 10+, macOS 10.14+, or Linux
- Memory: 4GB RAM minimum, 8GB recommended
- Disk Space: 500MB available space

### Installation

1. Download the installer from our website
2. Run the installer and follow the on-screen instructions
3. Launch the application after installation

## Features
"""
        
        # Generate feature documentation
        for i, feature in enumerate(features):
            feature_name = feature.get("name", f"Feature {i+1}")
            description = feature.get("description", "No description provided.")
            instructions = feature.get("instructions", [])
            
            guide_content += f"""
### {feature_name}

{description}

#### How to Use

"""
            
            # Add step-by-step instructions
            for j, step in enumerate(instructions):
                guide_content += f"{j+1}. {step}\n"
            
            # Add screenshots placeholder
            guide_content += """
#### Screenshots

[Screenshot 1: Description of what the screenshot shows]

"""
        
        # Add troubleshooting section
        guide_content += """
## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Application doesn't start | Verify system requirements and reinstall if necessary |
| Cannot save changes | Check permissions and available disk space |
| Feature X is not working | Restart the application and try again |

### Getting Support

If you encounter issues not covered in this guide, please contact our support team:

- Email: support@example.com
- Phone: (555) 123-4567
- Hours: Monday-Friday, 9AM-5PM EST
"""
        
        return {
            "title": f"{product_name} User Guide",
            "content": guide_content,
            "format": format_type,
            "features_documented": len(features),
            "target_audience": audience,
            "word_count": len(guide_content.split())
        }
    
    def _create_developer_documentation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create developer documentation.
        
        Args:
            task: Task containing developer documentation requirements
            
        Returns:
            Developer documentation
        """
        project_name = task.get("project_name", "")
        modules = task.get("modules", [])
        architecture = task.get("architecture", {})
        format_type = task.get("format", "markdown")
        
        # Generate developer documentation (placeholder implementation)
        doc_content = f"""# {project_name} Developer Documentation

## Overview

This documentation provides development information for {project_name}.

## Architecture

{architecture.get("description", "The system uses a modern, modular architecture.")}

### Components

"""
        
        # Add architecture components
        components = architecture.get("components", [])
        for component in components:
            component_name = component.get("name", "")
            role = component.get("role", "")
            
            doc_content += f"- **{component_name}**: {role}\n"
        
        # Add system diagram placeholder
        doc_content += """
### System Diagram

```
+---------------+       +---------------+
|  Component A  | ----> |  Component B  |
+---------------+       +---------------+
        |                       |
        v                       v
+---------------+       +---------------+
|  Component C  | <---- |  Component D  |
+---------------+       +---------------+
```

## Modules
"""
        
        # Generate module documentation
        for i, module in enumerate(modules):
            module_name = module.get("name", f"Module {i+1}")
            purpose = module.get("purpose", "No description provided.")
            classes = module.get("classes", [])
            
            doc_content += f"""
### {module_name}

{purpose}

#### Classes

"""
            
            # Add class documentation
            for cls in classes:
                class_name = cls.get("name", "")
                description = cls.get("description", "")
                methods = cls.get("methods", [])
                
                doc_content += f"""##### `{class_name}`

{description}

**Methods:**

"""
                
                # Add method documentation
                for method in methods:
                    method_name = method.get("name", "")
                    signature = method.get("signature", "")
                    method_desc = method.get("description", "")
                    
                    doc_content += f"- `{method_name}{signature}`: {method_desc}\n"
        
        # Add development setup section
        doc_content += """
## Development Setup

### Prerequisites

- Node.js 14+ or Python 3.8+
- Docker (for containerized development)
- Git

### Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/example/project.git
   ```

2. Install dependencies:
   ```
   npm install
   # or
   pip install -r requirements.txt
   ```

3. Run development server:
   ```
   npm run dev
   # or
   python manage.py runserver
   ```

### Testing

Run tests with:
```
npm test
# or
pytest
```

## Contributing

Please read our contributing guidelines before submitting pull requests.
"""
        
        return {
            "title": f"{project_name} Developer Documentation",
            "content": doc_content,
            "format": format_type,
            "modules_documented": len(modules),
            "word_count": len(doc_content.split())
        }
    
    def _update_metrics_from_task(self, task: Dict[str, Any]) -> None:
        """Update agent's performance metrics based on task execution.
        
        Args:
            task: Completed task
        """
        task_type = task.get("type", "")
        
        if task_type == "api_documentation":
            # Update metrics related to API documentation
            current = self.performance_metrics.get("technical_accuracy", 0.0)
            self.update_metric("technical_accuracy", min(1.0, current + 0.1))
            
            current = self.performance_metrics.get("content_organization", 0.0)
            self.update_metric("content_organization", min(1.0, current + 0.1))
            
        elif task_type == "user_guide":
            # Update metrics related to user guide creation
            current = self.performance_metrics.get("documentation_clarity", 0.0)
            self.update_metric("documentation_clarity", min(1.0, current + 0.1))
            
        elif task_type == "developer_documentation":
            # Update metrics related to developer documentation
            current = self.performance_metrics.get("technical_accuracy", 0.0)
            self.update_metric("technical_accuracy", min(1.0, current + 0.1))
            
            current = self.performance_metrics.get("documentation_clarity", 0.0)
            self.update_metric("documentation_clarity", min(1.0, current + 0.05))