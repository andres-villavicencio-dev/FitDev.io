#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compensation System for FitDev.io
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid


class CompensationSystem:
    """Manages the virtual compensation for FitDev.io agents."""
    
    def __init__(self, base_rates: Dict[str, float], 
                performance_multiplier: float = 1.0):
        """Initialize the compensation system.
        
        Args:
            base_rates: Dictionary mapping role categories to base compensation rates
            performance_multiplier: Maximum multiplier for performance-based adjustments
        """
        self.base_rates = base_rates
        self.performance_multiplier = performance_multiplier
        self.payment_history: List[Dict[str, Any]] = []
    
    def get_base_rate(self, role: str) -> float:
        """Get the base compensation rate for a role.
        
        Args:
            role: Agent role category
            
        Returns:
            Base compensation rate for the role
        """
        return self.base_rates.get(role, self.base_rates.get("default", 50.0))
    
    def calculate_compensation(self, agent_id: str, role: str, 
                              performance_score: float) -> float:
        """Calculate compensation for an agent based on role and performance.
        
        Args:
            agent_id: ID of the agent
            role: Agent role category
            performance_score: Performance score between 0.0 and 1.0
            
        Returns:
            Calculated compensation amount
        """
        base_rate = self.get_base_rate(role)
        compensation = base_rate * (1.0 + performance_score * (self.performance_multiplier - 1.0))
        
        # Record the payment
        self.payment_history.append({
            "id": str(uuid.uuid4()),
            "agent_id": agent_id,
            "role": role,
            "base_rate": base_rate,
            "performance_score": performance_score,
            "compensation": compensation,
            "timestamp": datetime.now()
        })
        
        return compensation
    
    def get_agent_history(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get payment history for a specific agent.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            List of payment records for the agent
        """
        return [payment for payment in self.payment_history 
                if payment["agent_id"] == agent_id]
    
    def get_total_compensation(self, agent_id: Optional[str] = None) -> float:
        """Get total compensation paid.
        
        Args:
            agent_id: Optional agent ID to filter by
            
        Returns:
            Total compensation amount
        """
        if agent_id:
            return sum(payment["compensation"] for payment in self.payment_history 
                      if payment["agent_id"] == agent_id)
        else:
            return sum(payment["compensation"] for payment in self.payment_history)
    
    def get_average_performance(self, role: Optional[str] = None) -> float:
        """Get average performance score.
        
        Args:
            role: Optional role category to filter by
            
        Returns:
            Average performance score
        """
        if role:
            payments = [payment for payment in self.payment_history 
                       if payment["role"] == role]
        else:
            payments = self.payment_history
            
        if not payments:
            return 0.0
            
        return sum(payment["performance_score"] for payment in payments) / len(payments)
