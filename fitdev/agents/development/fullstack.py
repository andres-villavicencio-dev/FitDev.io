#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Full Stack Developer Agent for FitDev.io
"""

from typing import Dict, Any, List
from models.agent import BaseAgent


class FullStackDeveloperAgent(BaseAgent):
    """Full Stack Developer agent responsible for implementing complete features."""
    
    def __init__(self, name: str = "Full Stack Developer"):
        """Initialize the Full Stack Developer agent.
        
        Args:
            name: Agent name (default: "Full Stack Developer")
        """
        description = """Works across both frontend and backend systems to implement 
                        complete features. Connects user interfaces with backend services."""
        super().__init__(name, "development", description)
        
        # Add Full Stack Developer-specific skills
        self.add_skill("Frontend Development")
        self.add_skill("Backend Development")
        self.add_skill("API Integration")
        self.add_skill("Full Feature Implementation")
        self.add_skill("End-to-End Testing")
        
        # Full Stack Developer-specific performance metrics
        self.update_metric("feature_completeness", 0.0)
        self.update_metric("integration_quality", 0.0)
        self.update_metric("code_quality", 0.0)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task assigned to this agent.
        
        Args:
            task: Task definition and parameters
            
        Returns:
            Task results and metadata
        """
        # Task execution logic for the Full Stack Developer agent
        task_type = task.get("type", "")
        results = {"status": "completed", "agent": self.name}
        
        if task_type == "feature_implementation":
            # Logic for complete feature implementation tasks
            results["feature"] = self._implement_feature(task)
            
        elif task_type == "system_integration":
            # Logic for system integration tasks
            results["integration"] = self._integrate_systems(task)
            
        elif task_type == "end_to_end_test":
            # Logic for end-to-end testing tasks
            results["test"] = self._create_end_to_end_test(task)
        
        # Update metrics based on task execution
        self._update_metrics_from_task(task)
        
        return results
    
    def evaluate_performance(self) -> float:
        """Evaluate Full Stack Developer agent's performance based on metrics.
        
        Returns:
            Performance score between 0.0 and 1.0
        """
        # Weight factors for different metrics
        weights = {
            "feature_completeness": 0.4,
            "integration_quality": 0.3,
            "code_quality": 0.3
        }
        
        # Calculate weighted performance score
        score = 0.0
        for metric, weight in weights.items():
            if metric in self.performance_metrics:
                # Normalize metric value to 0.0-1.0 range if needed
                metric_value = min(1.0, max(0.0, self.performance_metrics[metric]))
                score += metric_value * weight
        
        return score
    
    def _implement_feature(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Implement a complete feature spanning frontend and backend.
        
        Args:
            task: Task containing feature requirements
            
        Returns:
            Feature implementation details
        """
        feature_name = task.get("feature_name", "")
        requirements = task.get("requirements", [])
        
        # Simple feature implementation (placeholder implementation)
        frontend_code = """
        import React, { useState, useEffect } from 'react';
        import { fetchData, createItem } from '../api/itemApi';
        
        export const ItemList = () => {
          const [items, setItems] = useState([]);
          const [newItem, setNewItem] = useState('');
          
          useEffect(() => {
            loadItems();
          }, []);
          
          const loadItems = async () => {
            try {
              const data = await fetchData();
              setItems(data);
            } catch (error) {
              console.error('Error loading items:', error);
            }
          };
          
          const handleCreate = async () => {
            try {
              await createItem({ name: newItem });
              setNewItem('');
              loadItems();
            } catch (error) {
              console.error('Error creating item:', error);
            }
          };
          
          return (
            <div>
              <h2>Items</h2>
              <ul>
                {items.map(item => (
                  <li key={item.id}>{item.name}</li>
                ))}
              </ul>
              <div>
                <input 
                  value={newItem} 
                  onChange={e => setNewItem(e.target.value)} 
                />
                <button onClick={handleCreate}>Add Item</button>
              </div>
            </div>
          );
        };
        """
        
        backend_code = """
        @app.route('/api/items', methods=['GET'])
        def get_items():
            items = Item.query.all()
            return jsonify([item.to_dict() for item in items])
        
        @app.route('/api/items', methods=['POST'])
        def create_item():
            data = request.get_json()
            item = Item(name=data.get('name'))
            db.session.add(item)
            db.session.commit()
            return jsonify(item.to_dict()), 201
        """
        
        # TODO: Implement more sophisticated feature implementation logic
        
        return {
            "frontend_code": frontend_code,
            "backend_code": backend_code,
            "feature_name": feature_name,
            "requirements_met": len(requirements),
            "test_coverage": True
        }
    
    def _integrate_systems(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate different system components.
        
        Args:
            task: Task containing integration requirements
            
        Returns:
            Integration implementation details
        """
        components = task.get("components", [])
        interfaces = task.get("interfaces", [])
        
        # Simple integration implementation (placeholder implementation)
        integration_code = """
        // API client code
        export class ApiClient {
          constructor(baseUrl) {
            this.baseUrl = baseUrl || process.env.API_URL;
            this.headers = {
              'Content-Type': 'application/json',
            };
          }
          
          async setAuthToken(token) {
            this.headers['Authorization'] = `Bearer ${token}`;
          }
          
          async get(endpoint) {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
              method: 'GET',
              headers: this.headers,
            });
            
            if (!response.ok) {
              throw new Error(`API error: ${response.status}`);
            }
            
            return response.json();
          }
          
          async post(endpoint, data) {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
              method: 'POST',
              headers: this.headers,
              body: JSON.stringify(data),
            });
            
            if (!response.ok) {
              throw new Error(`API error: ${response.status}`);
            }
            
            return response.json();
          }
        }
        """
        
        # TODO: Implement more sophisticated integration logic
        
        return {
            "code": integration_code,
            "components_integrated": len(components),
            "interfaces_implemented": len(interfaces),
            "error_handling": True
        }
    
    def _create_end_to_end_test(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create end-to-end tests for a feature.
        
        Args:
            task: Task containing testing requirements
            
        Returns:
            Test implementation details
        """
        feature = task.get("feature", "")
        scenarios = task.get("scenarios", [])
        
        # Simple end-to-end test implementation (placeholder implementation)
        test_code = """
        describe('Item Management', () => {
          beforeEach(() => {
            cy.visit('/items');
          });
          
          it('should display items', () => {
            cy.get('ul li').should('have.length.at.least', 1);
          });
          
          it('should create a new item', () => {
            const newItemName = 'Test Item ' + Math.random().toString(36).substring(7);
            
            cy.get('input').type(newItemName);
            cy.get('button').contains('Add Item').click();
            
            cy.get('ul li').contains(newItemName).should('exist');
          });
        });
        """
        
        # TODO: Implement more sophisticated test generation logic
        
        return {
            "code": test_code,
            "feature": feature,
            "scenarios_covered": len(scenarios),
            "framework": "Cypress"
        }
    
    def _update_metrics_from_task(self, task: Dict[str, Any]) -> None:
        """Update agent's performance metrics based on task execution.
        
        Args:
            task: Completed task
        """
        task_type = task.get("type", "")
        
        if task_type == "feature_implementation":
            # Update metrics related to feature implementation
            current = self.performance_metrics.get("feature_completeness", 0.0)
            self.update_metric("feature_completeness", current + 0.1)
            
        elif task_type == "system_integration":
            # Update metrics related to system integration
            current = self.performance_metrics.get("integration_quality", 0.0)
            self.update_metric("integration_quality", current + 0.1)
            
        elif task_type == "end_to_end_test":
            # Update metrics related to end-to-end testing
            current = self.performance_metrics.get("code_quality", 0.0)
            self.update_metric("code_quality", current + 0.1)
