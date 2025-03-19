#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Security Specialist Agent for FitDev.io
"""

from typing import Dict, Any, List
from models.agent import BaseAgent


class SecuritySpecialistAgent(BaseAgent):
    """Security Specialist agent responsible for security assessment and implementation."""
    
    def __init__(self, name: str = "Security Specialist"):
        """Initialize the Security Specialist agent.
        
        Args:
            name: Agent name (default: "Security Specialist")
        """
        description = """Performs security assessments, code reviews from a security perspective, 
                      identifies vulnerabilities, and recommends security improvements. Ensures
                      application follows security best practices."""
        super().__init__(name, "quality", description)
        
        # Add Security Specialist-specific skills
        self.add_skill("Vulnerability Assessment")
        self.add_skill("Secure Coding Practices")
        self.add_skill("Authentication & Authorization")
        self.add_skill("Data Protection")
        self.add_skill("Penetration Testing")
        
        # Security Specialist-specific performance metrics
        self.update_metric("vulnerability_detection", 0.0)
        self.update_metric("security_implementation", 0.0)
        self.update_metric("threat_modeling", 0.0)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task assigned to this agent.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results and metadata
        """
        # Task execution logic for the Security Specialist agent
        task_type = task.get("type", "")
        results = {"status": "completed", "agent": self.name}
        
        if task_type == "security_assessment":
            # Logic for security assessment tasks
            results["assessment"] = self._perform_security_assessment(task)
            
        elif task_type == "code_security_review":
            # Logic for code security review tasks
            results["review"] = self._review_code_security(task)
            
        elif task_type == "security_implementation":
            # Logic for security implementation tasks
            results["implementation"] = self._implement_security_feature(task)
        
        # Update metrics based on task execution
        self._update_metrics_from_task(task)
        
        return results
    
    def evaluate_performance(self) -> float:
        """Evaluate Security Specialist agent's performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        # Weight factors for different metrics
        weights = {
            "vulnerability_detection": 0.4,
            "security_implementation": 0.3,
            "threat_modeling": 0.3
        }
        
        # Calculate weighted performance score
        score = 0.0
        for metric, weight in weights.items():
            if metric in self.performance_metrics:
                # Normalize metric value to 0.0-1.0 range if needed
                metric_value = min(1.0, max(0.0, self.performance_metrics[metric]))
                score += metric_value * weight
        
        return score
    
    def _perform_security_assessment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a security assessment of an application or feature.
        
        Args:
            task: Task containing security assessment requirements
            
        Returns:
            Security assessment results
        """
        target = task.get("target", "")
        scope = task.get("scope", [])
        requirements = task.get("requirements", [])
        
        # Generate vulnerabilities (placeholder implementation)
        vulnerabilities = []
        risk_areas = ["Authentication", "Authorization", "Data Validation", 
                     "Encryption", "Session Management", "API Security"]
        
        for area in risk_areas:
            # Simulate finding vulnerabilities in each risk area
            import random
            if random.random() > 0.7:  # 30% chance of finding a vulnerability
                vulnerabilities.append({
                    "id": f"VULN-{len(vulnerabilities) + 1}",
                    "area": area,
                    "description": f"Potential security issue in {area.lower()}",
                    "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                    "recommendations": [f"Implement proper {area.lower()} controls"]
                })
        
        # Generate security recommendations
        recommendations = [
            "Implement input validation for all user inputs",
            "Use parameterized queries to prevent SQL injection",
            "Apply the principle of least privilege",
            "Implement multi-factor authentication for sensitive operations",
            "Use HTTPS for all communications",
            "Implement proper error handling that doesn't leak sensitive information"
        ]
        
        return {
            "target": target,
            "scope": scope,
            "vulnerabilities": vulnerabilities,
            "vulnerability_count": len(vulnerabilities),
            "recommendations": recommendations,
            "overall_risk": self._calculate_risk_level(vulnerabilities)
        }
    
    def _review_code_security(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Review code for security vulnerabilities.
        
        Args:
            task: Task containing code review requirements
            
        Returns:
            Code security review results
        """
        code_files = task.get("files", [])
        language = task.get("language", "")
        
        # Mock code review findings (placeholder implementation)
        findings = []
        common_issues = [
            {"pattern": "exec(", "issue": "Potential code injection", "severity": "High"},
            {"pattern": "eval(", "issue": "Potential code injection", "severity": "High"},
            {"pattern": "getElementById", "issue": "Potential DOM manipulation without sanitization", "severity": "Medium"},
            {"pattern": "password", "issue": "Hardcoded credential", "severity": "High"},
            {"pattern": "SELECT * FROM", "issue": "SQL query without parameterization", "severity": "High"},
            {"pattern": ".innerHTML", "issue": "Potential XSS vulnerability", "severity": "Medium"}
        ]
        
        # Simulate finding issues in the files
        for file in code_files:
            # In a real implementation, this would parse and analyze the actual file
            filename = file.get("name", "")
            # Simulate finding 0-2 issues per file
            import random
            num_issues = random.randint(0, 2)
            for _ in range(num_issues):
                issue = random.choice(common_issues)
                findings.append({
                    "file": filename,
                    "line": random.randint(1, 100),
                    "issue": issue["issue"],
                    "severity": issue["severity"],
                    "recommendation": f"Replace with secure alternative for {issue['pattern']}"
                })
        
        return {
            "files_reviewed": len(code_files),
            "language": language,
            "findings": findings,
            "issues_count": len(findings),
            "pass": len(findings) == 0,
            "recommendations": [
                "Implement input validation",
                "Use parameterized queries",
                "Sanitize user input before using in DOM manipulation",
                "Use secure coding patterns"
            ]
        }
    
    def _implement_security_feature(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Implement a security feature.
        
        Args:
            task: Task containing security implementation requirements
            
        Returns:
            Security implementation details
        """
        feature_type = task.get("feature_type", "")
        requirements = task.get("requirements", [])
        language = task.get("language", "")
        
        # Generate implementation code based on feature type (placeholder implementation)
        code_snippet = ""
        docs = ""
        
        if feature_type == "authentication":
            code_snippet = """
            import bcrypt
            
            def hash_password(password: str) -> str:
                # Generate a salt and hash the password
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
                return hashed.decode('utf-8')
            
            def verify_password(password: str, hashed: str) -> bool:
                # Verify that the password matches the hash
                return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
            """
            docs = """
            # Password Security Implementation
            
            This module provides secure password hashing and verification using bcrypt.
            
            ## Usage
            
            ```python
            # Hash a password
            hashed_password = hash_password(user_password)
            
            # Verify a password
            is_valid = verify_password(input_password, stored_hash)
            ```
            
            ## Security Notes
            
            - Passwords are never stored in plaintext
            - bcrypt automatically includes the salt in the hash
            - Work factor is set to industry standard
            """
            
        elif feature_type == "authorization":
            code_snippet = """
            from typing import Dict, List, Any
            
            class RoleBasedAccessControl:
                def __init__(self):
                    self.roles: Dict[str, List[str]] = {}
                    self.user_roles: Dict[str, List[str]] = {}
                
                def add_role(self, role: str, permissions: List[str]) -> None:
                    self.roles[role] = permissions
                
                def assign_role_to_user(self, user_id: str, role: str) -> None:
                    if role not in self.roles:
                        raise ValueError(f"Role {role} does not exist")
                    
                    if user_id not in self.user_roles:
                        self.user_roles[user_id] = []
                    
                    if role not in self.user_roles[user_id]:
                        self.user_roles[user_id].append(role)
                
                def check_permission(self, user_id: str, permission: str) -> bool:
                    if user_id not in self.user_roles:
                        return False
                    
                    for role in self.user_roles[user_id]:
                        if permission in self.roles[role]:
                            return True
                    
                    return False
            """
            docs = """
            # Role-Based Access Control Implementation
            
            This module provides a simple RBAC system for authorization control.
            
            ## Usage
            
            ```python
            # Initialize the RBAC system
            rbac = RoleBasedAccessControl()
            
            # Define roles and their permissions
            rbac.add_role("admin", ["read", "write", "delete"])
            rbac.add_role("editor", ["read", "write"])
            rbac.add_role("viewer", ["read"])
            
            # Assign roles to users
            rbac.assign_role_to_user("user123", "editor")
            
            # Check permissions
            can_delete = rbac.check_permission("user123", "delete")  # False
            can_read = rbac.check_permission("user123", "read")  # True
            ```
            
            ## Security Notes
            
            - Implements the principle of least privilege
            - Roles can be easily modified without changing code
            - Permissions are checked explicitly, defaulting to deny
            """
            
        elif feature_type == "encryption":
            code_snippet = """
            from cryptography.fernet import Fernet
            
            class DataEncryption:
                def __init__(self, key=None):
                    self.key = key if key else Fernet.generate_key()
                    self.cipher = Fernet(self.key)
                
                def encrypt(self, data: str) -> bytes:
                    return self.cipher.encrypt(data.encode('utf-8'))
                
                def decrypt(self, encrypted_data: bytes) -> str:
                    return self.cipher.decrypt(encrypted_data).decode('utf-8')
                
                def get_key(self) -> bytes:
                    return self.key
            """
            docs = """
            # Data Encryption Implementation
            
            This module provides symmetric encryption for sensitive data.
            
            ## Usage
            
            ```python
            # Initialize encryption with a new key
            encryptor = DataEncryption()
            
            # Or with an existing key
            # encryptor = DataEncryption(existing_key)
            
            # Encrypt data
            encrypted = encryptor.encrypt("sensitive data")
            
            # Decrypt data
            decrypted = encryptor.decrypt(encrypted)
            
            # Get the key for storage in a secure location
            key = encryptor.get_key()
            ```
            
            ## Security Notes
            
            - Uses Fernet (AES-128 in CBC mode with PKCS7 padding)
            - Includes authentication to prevent tampering
            - Keys should be stored securely, not in code
            """
            
        return {
            "feature_type": feature_type,
            "language": language,
            "code": code_snippet,
            "documentation": docs,
            "compliance": {
                "owasp_top_10": True,
                "app_sec_verification_standard": True
            }
        }
    
    def _calculate_risk_level(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        """Calculate overall risk level based on vulnerabilities.
        
        Args:
            vulnerabilities: List of identified vulnerabilities
            
        Returns:
            Overall risk level (Low, Medium, High, Critical)
        """
        if not vulnerabilities:
            return "Low"
            
        # Count vulnerabilities by severity
        severity_counts = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0
        }
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "Low")
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        # Determine overall risk level
        if severity_counts["Critical"] > 0:
            return "Critical"
        elif severity_counts["High"] > 0:
            return "High"
        elif severity_counts["Medium"] > 0:
            return "Medium"
        else:
            return "Low"
    
    def _update_metrics_from_task(self, task: Dict[str, Any]) -> None:
        """Update agent's performance metrics based on task execution.
        
        Args:
            task: Completed task
        """
        task_type = task.get("type", "")
        
        if task_type == "security_assessment":
            # Update metrics related to security assessment
            current = self.performance_metrics.get("vulnerability_detection", 0.0)
            self.update_metric("vulnerability_detection", min(1.0, current + 0.1))
            
            current = self.performance_metrics.get("threat_modeling", 0.0)
            self.update_metric("threat_modeling", min(1.0, current + 0.1))
            
        elif task_type == "code_security_review":
            # Update metrics related to code security review
            current = self.performance_metrics.get("vulnerability_detection", 0.0)
            self.update_metric("vulnerability_detection", min(1.0, current + 0.1))
            
        elif task_type == "security_implementation":
            # Update metrics related to security implementation
            current = self.performance_metrics.get("security_implementation", 0.0)
            self.update_metric("security_implementation", min(1.0, current + 0.1))