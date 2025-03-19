#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API Specialist Agent for FitDev.io
"""

from typing import Dict, Any, List
from fitdev.models.agent import BaseAgent


class APISpecialistAgent(BaseAgent):
    """API Specialist agent responsible for API design, documentation, and evaluation."""
    
    def __init__(self, name: str = "API Specialist"):
        """Initialize the API Specialist agent.
        
        Args:
            name: Agent name (default: "API Specialist")
        """
        description = """Designs, evaluates, and documents APIs. Provides expertise on 
                      API architecture, standards, versioning, security, and best practices 
                      for creating developer-friendly interfaces."""
        super().__init__(name, "specialized", description)
        
        # Add API Specialist-specific skills
        self.add_skill("API Design")
        self.add_skill("REST Architecture")
        self.add_skill("GraphQL Schema Development")
        self.add_skill("API Documentation")
        self.add_skill("API Security")
        self.add_skill("API Versioning")
        
        # API Specialist-specific performance metrics
        self.update_metric("design_quality", 0.0)
        self.update_metric("documentation_clarity", 0.0)
        self.update_metric("security_implementation", 0.0)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task assigned to this agent.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results and metadata
        """
        # Task execution logic for the API Specialist agent
        task_type = task.get("type", "")
        results = {"status": "completed", "agent": self.name}
        
        if task_type == "api_design":
            # Logic for API design tasks
            results["api_design"] = self._design_api(task)
            
        elif task_type == "api_documentation":
            # Logic for API documentation tasks
            results["documentation"] = self._create_api_documentation(task)
            
        elif task_type == "api_security_review":
            # Logic for API security review tasks
            results["security_review"] = self._review_api_security(task)
            
        elif task_type == "api_versioning_strategy":
            # Logic for API versioning strategy tasks
            results["versioning_strategy"] = self._develop_versioning_strategy(task)
        
        # Update metrics based on task execution
        self._update_metrics_from_task(task)
        
        return results
    
    def evaluate_performance(self) -> float:
        """Evaluate API Specialist agent's performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        # Weight factors for different metrics
        weights = {
            "design_quality": 0.4,
            "documentation_clarity": 0.3,
            "security_implementation": 0.3
        }
        
        # Calculate weighted performance score
        score = 0.0
        for metric, weight in weights.items():
            if metric in self.performance_metrics:
                # Normalize metric value to 0.0-1.0 range if needed
                metric_value = min(1.0, max(0.0, self.performance_metrics[metric]))
                score += metric_value * weight
        
        return score
    
    def _design_api(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Design an API based on requirements.
        
        Args:
            task: Task containing API design requirements
            
        Returns:
            API design specification
        """
        api_name = task.get("api_name", "")
        api_type = task.get("api_type", "REST")  # Default to REST
        domain_entities = task.get("domain_entities", [])
        requirements = task.get("requirements", [])
        
        # Generate API design (placeholder implementation)
        endpoints = []
        schemas = []
        
        # Process domain entities
        for entity in domain_entities:
            # Create schema for this entity
            schema = {
                "name": entity,
                "properties": [
                    {"name": "id", "type": "string", "format": "uuid", "required": True, "description": f"Unique identifier for {entity}"},
                    {"name": "name", "type": "string", "required": True, "description": f"Name of the {entity}"},
                    {"name": "description", "type": "string", "required": False, "description": f"Description of the {entity}"},
                    {"name": "created_at", "type": "string", "format": "date-time", "required": True, "description": "Creation timestamp"},
                    {"name": "updated_at", "type": "string", "format": "date-time", "required": True, "description": "Last update timestamp"}
                ]
            }
            
            # Add entity-specific properties (simplified)
            if entity.lower() == "user":
                schema["properties"].extend([
                    {"name": "email", "type": "string", "format": "email", "required": True, "description": "User's email address"},
                    {"name": "role", "type": "string", "enum": ["admin", "user", "guest"], "required": True, "description": "User's role"}
                ])
            elif entity.lower() == "product":
                schema["properties"].extend([
                    {"name": "price", "type": "number", "format": "float", "required": True, "description": "Product price"},
                    {"name": "category", "type": "string", "required": True, "description": "Product category"},
                    {"name": "inventory_count", "type": "integer", "required": True, "description": "Current inventory count"}
                ])
            elif entity.lower() == "order":
                schema["properties"].extend([
                    {"name": "user_id", "type": "string", "format": "uuid", "required": True, "description": "ID of the user who placed the order"},
                    {"name": "items", "type": "array", "items": {"type": "object"}, "required": True, "description": "Order items"},
                    {"name": "total", "type": "number", "format": "float", "required": True, "description": "Order total"},
                    {"name": "status", "type": "string", "enum": ["pending", "processing", "shipped", "delivered"], "required": True, "description": "Order status"}
                ])
            
            schemas.append(schema)
            
            # Create endpoints for this entity
            if api_type == "REST":
                # REST Endpoints
                endpoints.extend([
                    {
                        "path": f"/{entity.lower()}s",
                        "method": "GET",
                        "description": f"List all {entity.lower()}s",
                        "query_params": [
                            {"name": "page", "type": "integer", "required": False, "description": "Page number for pagination"},
                            {"name": "limit", "type": "integer", "required": False, "description": "Items per page for pagination"}
                        ],
                        "responses": [
                            {"status": 200, "description": "Success", "schema": f"Array of {entity}"},
                            {"status": 400, "description": "Bad Request"},
                            {"status": 401, "description": "Unauthorized"}
                        ]
                    },
                    {
                        "path": f"/{entity.lower()}s/{{id}}",
                        "method": "GET",
                        "description": f"Get a specific {entity.lower()} by ID",
                        "path_params": [
                            {"name": "id", "type": "string", "required": True, "description": f"ID of the {entity.lower()}"}
                        ],
                        "responses": [
                            {"status": 200, "description": "Success", "schema": entity},
                            {"status": 404, "description": "Not Found"},
                            {"status": 401, "description": "Unauthorized"}
                        ]
                    },
                    {
                        "path": f"/{entity.lower()}s",
                        "method": "POST",
                        "description": f"Create a new {entity.lower()}",
                        "request_body": {"schema": entity},
                        "responses": [
                            {"status": 201, "description": "Created", "schema": entity},
                            {"status": 400, "description": "Bad Request"},
                            {"status": 401, "description": "Unauthorized"}
                        ]
                    },
                    {
                        "path": f"/{entity.lower()}s/{{id}}",
                        "method": "PUT",
                        "description": f"Update an existing {entity.lower()}",
                        "path_params": [
                            {"name": "id", "type": "string", "required": True, "description": f"ID of the {entity.lower()}"}
                        ],
                        "request_body": {"schema": entity},
                        "responses": [
                            {"status": 200, "description": "Success", "schema": entity},
                            {"status": 404, "description": "Not Found"},
                            {"status": 400, "description": "Bad Request"},
                            {"status": 401, "description": "Unauthorized"}
                        ]
                    },
                    {
                        "path": f"/{entity.lower()}s/{{id}}",
                        "method": "DELETE",
                        "description": f"Delete a {entity.lower()}",
                        "path_params": [
                            {"name": "id", "type": "string", "required": True, "description": f"ID of the {entity.lower()}"}
                        ],
                        "responses": [
                            {"status": 204, "description": "No Content"},
                            {"status": 404, "description": "Not Found"},
                            {"status": 401, "description": "Unauthorized"},
                            {"status": 403, "description": "Forbidden"}
                        ]
                    }
                ])
                
                # Add relationship endpoints if appropriate
                if entity.lower() == "user":
                    endpoints.append({
                        "path": f"/{entity.lower()}s/{{id}}/orders",
                        "method": "GET",
                        "description": f"Get orders for a specific user",
                        "path_params": [
                            {"name": "id", "type": "string", "required": True, "description": "ID of the user"}
                        ],
                        "responses": [
                            {"status": 200, "description": "Success", "schema": "Array of Order"},
                            {"status": 404, "description": "Not Found"},
                            {"status": 401, "description": "Unauthorized"}
                        ]
                    })
                
            elif api_type == "GraphQL":
                # Simplified GraphQL schemas and operations
                # For GraphQL, we'd create types and operations
                endpoints = [{
                    "type": "Query",
                    "operations": [
                        {
                            "name": f"get{entity}",
                            "description": f"Get a specific {entity.lower()} by ID",
                            "arguments": [
                                {"name": "id", "type": "ID!", "description": f"ID of the {entity.lower()}"}
                            ],
                            "return_type": entity
                        },
                        {
                            "name": f"list{entity}s",
                            "description": f"List all {entity.lower()}s",
                            "arguments": [
                                {"name": "page", "type": "Int", "description": "Page number for pagination"},
                                {"name": "limit", "type": "Int", "description": "Items per page for pagination"}
                            ],
                            "return_type": f"[{entity}]"
                        }
                    ]
                },
                {
                    "type": "Mutation",
                    "operations": [
                        {
                            "name": f"create{entity}",
                            "description": f"Create a new {entity.lower()}",
                            "arguments": [
                                {"name": "input", "type": f"{entity}Input!", "description": f"Input for creating a {entity.lower()}"}
                            ],
                            "return_type": entity
                        },
                        {
                            "name": f"update{entity}",
                            "description": f"Update an existing {entity.lower()}",
                            "arguments": [
                                {"name": "id", "type": "ID!", "description": f"ID of the {entity.lower()}"},
                                {"name": "input", "type": f"{entity}Input!", "description": f"Input for updating a {entity.lower()}"}
                            ],
                            "return_type": entity
                        },
                        {
                            "name": f"delete{entity}",
                            "description": f"Delete a {entity.lower()}",
                            "arguments": [
                                {"name": "id", "type": "ID!", "description": f"ID of the {entity.lower()}"}
                            ],
                            "return_type": "Boolean"
                        }
                    ]
                }]
        
        # Authentication endpoints if required
        if any("authentication" in req.lower() for req in requirements):
            if api_type == "REST":
                endpoints.extend([
                    {
                        "path": "/auth/login",
                        "method": "POST",
                        "description": "Authenticate user and get access token",
                        "request_body": {
                            "schema": "LoginRequest",
                            "properties": [
                                {"name": "email", "type": "string", "required": True, "description": "User's email"},
                                {"name": "password", "type": "string", "required": True, "description": "User's password"}
                            ]
                        },
                        "responses": [
                            {"status": 200, "description": "Success", "schema": "AuthResponse"},
                            {"status": 401, "description": "Unauthorized"}
                        ]
                    },
                    {
                        "path": "/auth/refresh",
                        "method": "POST",
                        "description": "Refresh access token",
                        "request_body": {
                            "schema": "RefreshRequest",
                            "properties": [
                                {"name": "refresh_token", "type": "string", "required": True, "description": "Refresh token"}
                            ]
                        },
                        "responses": [
                            {"status": 200, "description": "Success", "schema": "AuthResponse"},
                            {"status": 401, "description": "Unauthorized"}
                        ]
                    }
                ])
                
                schemas.extend([
                    {
                        "name": "LoginRequest",
                        "properties": [
                            {"name": "email", "type": "string", "format": "email", "required": True, "description": "User's email"},
                            {"name": "password", "type": "string", "required": True, "description": "User's password"}
                        ]
                    },
                    {
                        "name": "AuthResponse",
                        "properties": [
                            {"name": "access_token", "type": "string", "required": True, "description": "JWT access token"},
                            {"name": "refresh_token", "type": "string", "required": True, "description": "JWT refresh token"},
                            {"name": "expires_in", "type": "integer", "required": True, "description": "Token expiration time in seconds"}
                        ]
                    }
                ])
        
        # Generate API principles based on requirements
        principles = [
            "Use consistent naming conventions",
            "Follow HTTP status code standards",
            "Implement proper error handling and error responses",
            "Use pagination for list endpoints",
            "Implement proper authentication and authorization",
            "Version the API appropriately"
        ]
        
        # Add security principles if security is mentioned in requirements
        if any("security" in req.lower() for req in requirements):
            principles.extend([
                "Use HTTPS for all endpoints",
                "Implement rate limiting to prevent abuse",
                "Validate all input data to prevent injection attacks",
                "Use OAuth 2.0 for authentication when appropriate",
                "Include appropriate CORS headers"
            ])
        
        return {
            "api_name": api_name,
            "api_type": api_type,
            "version": "1.0.0",
            "base_path": "/api/v1",
            "schemas": schemas,
            "endpoints": endpoints,
            "principles": principles,
            "authentication": any("authentication" in req.lower() for req in requirements),
            "authorization": any("authorization" in req.lower() for req in requirements),
            "rate_limiting": any("rate" in req.lower() and "limit" in req.lower() for req in requirements)
        }
    
    def _create_api_documentation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create API documentation.
        
        Args:
            task: Task containing API documentation requirements
            
        Returns:
            API documentation
        """
        api_name = task.get("api_name", "")
        api_design = task.get("api_design", {})
        audience = task.get("audience", "developers")
        format = task.get("format", "OpenAPI")
        
        # Generate API documentation (placeholder implementation)
        schemas = api_design.get("schemas", [])
        endpoints = api_design.get("endpoints", [])
        api_type = api_design.get("api_type", "REST")
        
        # Generate documentation structure
        documentation = {
            "info": {
                "title": api_name,
                "description": f"API documentation for {api_name}",
                "version": api_design.get("version", "1.0.0"),
                "contact": {
                    "name": "API Support",
                    "email": "api-support@example.com",
                    "url": "https://example.com/support"
                },
                "license": {
                    "name": "MIT",
                    "url": "https://opensource.org/licenses/MIT"
                }
            },
            "servers": [
                {
                    "url": "https://api.example.com/v1",
                    "description": "Production server"
                },
                {
                    "url": "https://staging-api.example.com/v1",
                    "description": "Staging server"
                }
            ]
        }
        
        # Generate sections based on API type and audience
        sections = []
        
        # Introduction section
        sections.append({
            "title": "Introduction",
            "content": f"""
# {api_name} API Documentation

This documentation provides information about the {api_name} API, including endpoints, 
request/response formats, and authentication requirements.

## Base URL

All API endpoints are relative to the base URL:

```
{documentation['servers'][0]['url']}
```

## Authentication

{self._generate_auth_docs(api_design)}
            """
        })
        
        # Getting Started section
        sections.append({
            "title": "Getting Started",
            "content": f"""
# Getting Started

Follow these steps to begin using the {api_name} API:

1. **Create an Account**: Sign up for an API account at our [Developer Portal](https://example.com/developers).
2. **Get API Keys**: Generate API keys from your developer dashboard.
3. **Make Your First Request**: Try a simple request to verify your setup.

## Example Request

```bash
curl -X GET "{documentation['servers'][0]['url']}/status" \\
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Response Format

All responses are returned in JSON format.

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request.
            """
        })
        
        # Reference section with endpoints
        endpoints_content = ""
        
        if api_type == "REST":
            # Group endpoints by resource
            endpoints_by_resource = {}
            for endpoint in endpoints:
                path_parts = endpoint.get("path", "").split("/")
                resource = path_parts[1] if len(path_parts) > 1 else "general"
                
                if resource not in endpoints_by_resource:
                    endpoints_by_resource[resource] = []
                
                endpoints_by_resource[resource].append(endpoint)
            
            # Generate documentation for each resource
            for resource, resource_endpoints in endpoints_by_resource.items():
                endpoints_content += f"\n## {resource.title()}\n\n"
                
                for endpoint in resource_endpoints:
                    method = endpoint.get("method", "")
                    path = endpoint.get("path", "")
                    description = endpoint.get("description", "")
                    
                    endpoints_content += f"### {method} {path}\n\n"
                    endpoints_content += f"{description}\n\n"
                    
                    # Path parameters
                    path_params = endpoint.get("path_params", [])
                    if path_params:
                        endpoints_content += "#### Path Parameters\n\n"
                        endpoints_content += "| Name | Type | Required | Description |\n"
                        endpoints_content += "|------|------|----------|-------------|\n"
                        
                        for param in path_params:
                            endpoints_content += f"| {param.get('name', '')} | {param.get('type', '')} | {param.get('required', False)} | {param.get('description', '')} |\n"
                        
                        endpoints_content += "\n"
                    
                    # Query parameters
                    query_params = endpoint.get("query_params", [])
                    if query_params:
                        endpoints_content += "#### Query Parameters\n\n"
                        endpoints_content += "| Name | Type | Required | Description |\n"
                        endpoints_content += "|------|------|----------|-------------|\n"
                        
                        for param in query_params:
                            endpoints_content += f"| {param.get('name', '')} | {param.get('type', '')} | {param.get('required', False)} | {param.get('description', '')} |\n"
                        
                        endpoints_content += "\n"
                    
                    # Request body
                    request_body = endpoint.get("request_body", {})
                    if request_body:
                        endpoints_content += "#### Request Body\n\n"
                        schema_name = request_body.get("schema", "")
                        
                        if schema_name:
                            endpoints_content += f"Schema: {schema_name}\n\n"
                            
                            # Find the schema
                            schema = next((s for s in schemas if s.get("name") == schema_name), None)
                            
                            if schema:
                                properties = schema.get("properties", [])
                                
                                endpoints_content += "| Property | Type | Required | Description |\n"
                                endpoints_content += "|----------|------|----------|-------------|\n"
                                
                                for prop in properties:
                                    endpoints_content += f"| {prop.get('name', '')} | {prop.get('type', '')} | {prop.get('required', False)} | {prop.get('description', '')} |\n"
                                
                                endpoints_content += "\n"
                        
                    # Responses
                    responses = endpoint.get("responses", [])
                    if responses:
                        endpoints_content += "#### Responses\n\n"
                        endpoints_content += "| Status | Description | Schema |\n"
                        endpoints_content += "|--------|-------------|--------|\n"
                        
                        for response in responses:
                            endpoints_content += f"| {response.get('status', '')} | {response.get('description', '')} | {response.get('schema', '')} |\n"
                        
                        endpoints_content += "\n"
                    
                    # Example request
                    endpoints_content += "#### Example Request\n\n"
                    endpoints_content += "```bash\n"
                    
                    if method == "GET":
                        endpoints_content += f'curl -X GET "{documentation["servers"][0]["url"]}{path}" \\\n  -H "Authorization: Bearer YOUR_API_KEY"\n'
                    else:
                        endpoints_content += f'curl -X {method} "{documentation["servers"][0]["url"]}{path}" \\\n  -H "Content-Type: application/json" \\\n  -H "Authorization: Bearer YOUR_API_KEY" \\\n  -d \'{{"example": "data"}}\'\n'
                    
                    endpoints_content += "```\n\n"
                    
                    # Example response
                    endpoints_content += "#### Example Response\n\n"
                    endpoints_content += "```json\n"
                    endpoints_content += "{\n  \"example\": \"response\",\n  \"id\": \"12345\"\n}\n"
                    endpoints_content += "```\n\n"
        
        elif api_type == "GraphQL":
            # GraphQL documentation
            endpoints_content += "\n## Schema\n\n"
            
            # Types
            endpoints_content += "### Types\n\n"
            for schema in schemas:
                name = schema.get("name", "")
                endpoints_content += f"#### {name}\n\n"
                
                properties = schema.get("properties", [])
                if properties:
                    endpoints_content += "| Field | Type | Description |\n"
                    endpoints_content += "|-------|------|-------------|\n"
                    
                    for prop in properties:
                        required = "!" if prop.get("required", False) else ""
                        endpoints_content += f"| {prop.get('name', '')} | {prop.get('type', '')}{required} | {prop.get('description', '')} |\n"
                    
                    endpoints_content += "\n"
            
            # Queries and Mutations
            for endpoint in endpoints:
                type_name = endpoint.get("type", "")
                operations = endpoint.get("operations", [])
                
                endpoints_content += f"\n### {type_name}\n\n"
                
                for operation in operations:
                    name = operation.get("name", "")
                    return_type = operation.get("return_type", "")
                    description = operation.get("description", "")
                    
                    endpoints_content += f"#### {name}: {return_type}\n\n"
                    endpoints_content += f"{description}\n\n"
                    
                    # Arguments
                    arguments = operation.get("arguments", [])
                    if arguments:
                        endpoints_content += "##### Arguments\n\n"
                        endpoints_content += "| Name | Type | Description |\n"
                        endpoints_content += "|------|------|-------------|\n"
                        
                        for arg in arguments:
                            endpoints_content += f"| {arg.get('name', '')} | {arg.get('type', '')} | {arg.get('description', '')} |\n"
                        
                        endpoints_content += "\n"
                    
                    # Example query/mutation
                    endpoints_content += "##### Example\n\n"
                    endpoints_content += "```graphql\n"
                    
                    if type_name == "Query":
                        args_str = ", ".join([f"{arg.get('name', '')}: \"value\"" for arg in arguments])
                        endpoints_content += f"{type_name.lower()} {{\n  {name}({args_str}) {{\n    id\n    name\n    # other fields\n  }}\n}}\n"
                    else:
                        args_str = ", ".join([f"{arg.get('name', '')}: \"value\"" for arg in arguments])
                        endpoints_content += f"mutation {{\n  {name}({args_str}) {{\n    id\n    name\n    # other fields\n  }}\n}}\n"
                    
                    endpoints_content += "```\n\n"
        
        sections.append({
            "title": "API Reference",
            "content": f"""
# API Reference

{endpoints_content}
            """
        })
        
        # Add schemas/models section
        models_content = ""
        
        for schema in schemas:
            name = schema.get("name", "")
            properties = schema.get("properties", [])
            
            models_content += f"\n## {name}\n\n"
            
            if properties:
                models_content += "| Property | Type | Required | Description |\n"
                models_content += "|----------|------|----------|-------------|\n"
                
                for prop in properties:
                    models_content += f"| {prop.get('name', '')} | {prop.get('type', '')} | {prop.get('required', False)} | {prop.get('description', '')} |\n"
                
                models_content += "\n"
        
        sections.append({
            "title": "Data Models",
            "content": f"""
# Data Models

{models_content}
            """
        })
        
        # Generate API documentation output format
        documentation_output = ""
        
        if format == "OpenAPI":
            # Summary of what the OpenAPI spec would look like
            documentation_output = "OpenAPI 3.0 specification (JSON or YAML format)"
        elif format == "Markdown":
            # Combine all markdown sections
            documentation_output = "\n\n".join([section["content"] for section in sections])
        elif format == "HTML":
            # Summary of HTML documentation
            documentation_output = "HTML documentation with interactive examples"
        
        return {
            "api_name": api_name,
            "format": format,
            "info": documentation["info"],
            "servers": documentation["servers"],
            "sections": sections,
            "schemas_count": len(schemas),
            "endpoints_count": len(endpoints),
            "documentation_output": documentation_output
        }
    
    def _review_api_security(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Review API security.
        
        Args:
            task: Task containing API security review requirements
            
        Returns:
            API security review results
        """
        api_name = task.get("api_name", "")
        api_design = task.get("api_design", {})
        security_requirements = task.get("security_requirements", [])
        
        # Generate API security review (placeholder implementation)
        authentication = api_design.get("authentication", False)
        authorization = api_design.get("authorization", False)
        rate_limiting = api_design.get("rate_limiting", False)
        
        # Check security issues
        issues = []
        recommendations = []
        
        # Authentication checks
        if not authentication:
            issues.append({
                "category": "Authentication",
                "severity": "High",
                "description": "API does not implement authentication",
                "impact": "Unauthorized access to API resources"
            })
            recommendations.append("Implement OAuth 2.0 or JWT-based authentication")
        
        # Authorization checks
        if not authorization:
            issues.append({
                "category": "Authorization",
                "severity": "High",
                "description": "API does not implement authorization",
                "impact": "Users may access resources they should not have access to"
            })
            recommendations.append("Implement role-based access control (RBAC)")
        
        # Rate limiting checks
        if not rate_limiting:
            issues.append({
                "category": "Rate Limiting",
                "severity": "Medium",
                "description": "API does not implement rate limiting",
                "impact": "Vulnerability to DoS attacks and excessive usage"
            })
            recommendations.append("Implement rate limiting based on API key or IP address")
        
        # HTTPS checks
        servers = api_design.get("servers", [])
        https_enforced = all("https://" in server.get("url", "") for server in servers) if servers else False
        
        if not https_enforced:
            issues.append({
                "category": "Transport Security",
                "severity": "High",
                "description": "API does not enforce HTTPS",
                "impact": "Data transmitted in plaintext may be intercepted"
            })
            recommendations.append("Enforce HTTPS for all API endpoints")
        
        # Input validation checks
        endpoints = api_design.get("endpoints", [])
        has_input_validation = any("validation" in str(endpoint).lower() for endpoint in endpoints)
        
        if not has_input_validation:
            issues.append({
                "category": "Input Validation",
                "severity": "High",
                "description": "No evidence of input validation in API design",
                "impact": "Vulnerability to injection attacks"
            })
            recommendations.append("Implement comprehensive input validation for all endpoints")
        
        # Error handling checks
        has_error_responses = all(any("error" in str(response).lower() for response in endpoint.get("responses", [])) 
                                for endpoint in endpoints if endpoint.get("responses"))
        
        if not has_error_responses:
            issues.append({
                "category": "Error Handling",
                "severity": "Medium",
                "description": "Incomplete error response definitions",
                "impact": "May leak sensitive information in error messages"
            })
            recommendations.append("Define standardized error responses with appropriate detail levels")
        
        # CORS checks
        has_cors = any("cors" in str(endpoint).lower() for endpoint in endpoints)
        
        if not has_cors:
            issues.append({
                "category": "CORS",
                "severity": "Medium",
                "description": "No evidence of CORS configuration",
                "impact": "May be vulnerable to cross-origin attacks or block legitimate clients"
            })
            recommendations.append("Configure appropriate CORS headers")
        
        # Security headers
        has_security_headers = any("security" in str(endpoint).lower() and "header" in str(endpoint).lower() 
                                 for endpoint in endpoints)
        
        if not has_security_headers:
            issues.append({
                "category": "Security Headers",
                "severity": "Medium",
                "description": "No evidence of security headers",
                "impact": "Missing protection from common web vulnerabilities"
            })
            recommendations.append("Implement security headers (Content-Security-Policy, X-Content-Type-Options, etc.)")
        
        # Add more security checks based on specific requirements
        for requirement in security_requirements:
            if "audit" in requirement.lower() and not any("audit" in str(endpoint).lower() for endpoint in endpoints):
                issues.append({
                    "category": "Auditing",
                    "severity": "Medium",
                    "description": "No evidence of audit logging",
                    "impact": "Inability to track security events and user actions"
                })
                recommendations.append("Implement comprehensive audit logging")
            
            if "sensitive" in requirement.lower() and not any("pii" in str(endpoint).lower() or "sensitive" in str(endpoint).lower() for endpoint in endpoints):
                issues.append({
                    "category": "Data Classification",
                    "severity": "High",
                    "description": "No evidence of sensitive data handling",
                    "impact": "May expose sensitive data inappropriately"
                })
                recommendations.append("Implement data classification and appropriate handling for sensitive data")
        
        # Calculate overall security score
        total_issues = len(issues)
        high_severity = sum(1 for issue in issues if issue["severity"] == "High")
        medium_severity = sum(1 for issue in issues if issue["severity"] == "Medium")
        
        # Score calculation (simplified)
        # More weight to high severity issues
        max_score = 100
        high_penalty = 15  # Per high severity issue
        medium_penalty = 7  # Per medium severity issue
        
        score = max(0, max_score - (high_severity * high_penalty + medium_severity * medium_penalty))
        
        return {
            "api_name": api_name,
            "review_date": "",  # Could be filled with actual date
            "security_score": score,
            "issues": issues,
            "total_issues": total_issues,
            "high_severity_issues": high_severity,
            "medium_severity_issues": medium_severity,
            "recommendations": recommendations,
            "compliance": {
                "oauth2": authentication,
                "https": https_enforced,
                "input_validation": has_input_validation,
                "rate_limiting": rate_limiting,
                "error_handling": has_error_responses,
                "cors": has_cors,
                "security_headers": has_security_headers
            }
        }
    
    def _develop_versioning_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Develop an API versioning strategy.
        
        Args:
            task: Task containing API versioning requirements
            
        Returns:
            API versioning strategy
        """
        api_name = task.get("api_name", "")
        api_type = task.get("api_type", "REST")
        current_version = task.get("current_version", "1.0.0")
        versioning_requirements = task.get("versioning_requirements", [])
        
        # Generate API versioning strategy (placeholder implementation)
        strategies = [
            {
                "name": "URL Path Versioning",
                "description": "Include version number in the URL path",
                "example": "/api/v1/resources",
                "pros": [
                    "Simple and intuitive",
                    "Clear and visible",
                    "Easy to implement",
                    "Works with caching mechanisms"
                ],
                "cons": [
                    "Requires changing URLs for each version",
                    "Can lead to code duplication"
                ]
            },
            {
                "name": "Query Parameter Versioning",
                "description": "Specify version in query parameter",
                "example": "/api/resources?version=1",
                "pros": [
                    "Backward compatible URLs",
                    "Easy to implement",
                    "Optional (can have a default version)"
                ],
                "cons": [
                    "Less visible",
                    "May interfere with other query parameters",
                    "Less elegant"
                ]
            },
            {
                "name": "Header Versioning",
                "description": "Specify version in HTTP header",
                "example": "Accept: application/vnd.company.resource.v1+json",
                "pros": [
                    "Clean URLs",
                    "Doesn't affect URL structure",
                    "More flexible content negotiation"
                ],
                "cons": [
                    "Less visible, harder to test",
                    "Harder to use directly in browser",
                    "More complex implementation"
                ]
            },
            {
                "name": "Content Type Versioning",
                "description": "Specify version in content type header",
                "example": "Content-Type: application/vnd.company.resource.v1+json",
                "pros": [
                    "Follows HTTP content negotiation pattern",
                    "Clean URLs",
                    "Specific to content format"
                ],
                "cons": [
                    "Complex implementation",
                    "Harder to test and debug",
                    "Only works for content-negotiated requests"
                ]
            }
        ]
        
        # Select recommended strategy based on API type and requirements
        recommended_strategy = None
        
        if api_type == "REST":
            # For REST APIs, URL path versioning is often simplest
            recommended_strategy = strategies[0]
            
            # But check if specific requirements suggest other approaches
            if any("header" in req.lower() for req in versioning_requirements):
                recommended_strategy = strategies[2]
            elif any("content" in req.lower() for req in versioning_requirements):
                recommended_strategy = strategies[3]
        elif api_type == "GraphQL":
            # For GraphQL, don't use URL versioning
            recommended_strategy = {
                "name": "Schema Evolution",
                "description": "Add new fields/types and deprecate old ones without removing them",
                "example": """type User {
  id: ID!
  name: String!
  email: String!
  phone: String @deprecated(reason: "Use phoneNumber instead")
  phoneNumber: String
}""",
                "pros": [
                    "No need for explicit versioning",
                    "Backwards compatible",
                    "Clients can choose what they need"
                ],
                "cons": [
                    "Schema can become complex over time",
                    "Must maintain deprecated fields",
                    "Breaking changes still need special handling"
                ]
            }
            
            # Add this GraphQL-specific strategy to the list
            strategies.append(recommended_strategy)
        
        # Generate version compatibility matrix
        versions = ["1.0.0", "1.1.0", "2.0.0"]
        if current_version not in versions:
            versions.append(current_version)
            
        compatibility_matrix = []
        for version in versions:
            entry = {
                "version": version,
                "supported": version == current_version or version < current_version,
                "end_of_life": version < current_version and float(version.split(".")[0]) < float(current_version.split(".")[0]),
                "breaking_changes": version.split(".")[0] != current_version.split(".")[0],
                "features": [f"Feature for version {version}"]
            }
            compatibility_matrix.append(entry)
        
        # Generate versioning process
        versioning_process = {
            "semantic_versioning": {
                "description": "Follow semantic versioning (MAJOR.MINOR.PATCH)",
                "rules": [
                    "MAJOR version when making incompatible API changes",
                    "MINOR version when adding functionality in a backward compatible manner",
                    "PATCH version when making backward compatible bug fixes"
                ]
            },
            "deprecation_policy": {
                "notice_period": "6 months",
                "communication_channels": [
                    "Email notifications",
                    "API status page",
                    "Developer documentation",
                    "Deprecation headers in responses"
                ],
                "steps": [
                    "Announce deprecation with timeline",
                    "Add deprecation notices in responses",
                    "Monitor usage of deprecated features",
                    "Send reminder notifications",
                    "Remove deprecated feature after notice period"
                ]
            },
            "migration_support": {
                "documentation": "Provide detailed migration guides for each major version",
                "tools": "Provide migration tools and sandboxes for testing",
                "support": "Offer support channels for migration assistance"
            }
        }
        
        return {
            "api_name": api_name,
            "current_version": current_version,
            "versioning_strategies": strategies,
            "recommended_strategy": recommended_strategy,
            "compatibility_matrix": compatibility_matrix,
            "versioning_process": versioning_process,
            "recommendations": [
                "Use semantic versioning for clear communication of changes",
                "Provide detailed documentation for each version",
                "Implement a deprecation policy with sufficient notice",
                "Ensure backward compatibility within major versions",
                "Consider long-term support for major versions used by critical clients"
            ]
        }
    
    def _generate_auth_docs(self, api_design: Dict[str, Any]) -> str:
        """Generate authentication documentation based on API design.
        
        Args:
            api_design: API design specification
            
        Returns:
            Authentication documentation markdown
        """
        authentication = api_design.get("authentication", False)
        
        if not authentication:
            return "This API does not require authentication."
        
        auth_docs = """
All API endpoints require authentication. The API supports the following authentication methods:

### API Key Authentication

Include your API key in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

### OAuth 2.0 Authentication

For secure client-server applications, use the OAuth 2.0 flow:

1. Redirect users to the authorization endpoint
2. Receive authorization code
3. Exchange code for access token
4. Use access token in API requests

Example token usage:

```
Authorization: Bearer YOUR_OAUTH_TOKEN
```

### Token Expiration and Refresh

Access tokens expire after 1 hour. Use the refresh token endpoint to get a new access token:

```
POST /auth/refresh
```
        """
        
        return auth_docs
    
    def _update_metrics_from_task(self, task: Dict[str, Any]) -> None:
        """Update agent's performance metrics based on task execution.
        
        Args:
            task: Completed task
        """
        task_type = task.get("type", "")
        
        if task_type == "api_design":
            # Update metrics related to API design
            current = self.performance_metrics.get("design_quality", 0.0)
            self.update_metric("design_quality", min(1.0, current + 0.1))
            
        elif task_type == "api_documentation":
            # Update metrics related to API documentation
            current = self.performance_metrics.get("documentation_clarity", 0.0)
            self.update_metric("documentation_clarity", min(1.0, current + 0.1))
            
        elif task_type == "api_security_review" or task_type == "api_versioning_strategy":
            # Update metrics related to API security and architecture
            current = self.performance_metrics.get("security_implementation", 0.0)
            self.update_metric("security_implementation", min(1.0, current + 0.1))