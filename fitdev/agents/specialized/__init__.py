#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Specialized Agents for FitDev.io
"""

from agents.specialized.knowledge_management import KnowledgeManagementAgent
from agents.specialized.trend_scout import TrendScoutAgent
from agents.specialized.ux_simulator import UXSimulatorAgent
from agents.specialized.api_specialist import APISpecialistAgent
from agents.specialized.tech_debt_manager import TechDebtManagerAgent

__all__ = [
    'KnowledgeManagementAgent',
    'TrendScoutAgent',
    'UXSimulatorAgent',
    'APISpecialistAgent',
    'TechDebtManagerAgent'
]
