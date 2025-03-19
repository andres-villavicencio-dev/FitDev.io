#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Specialized Agents for FitDev.io
"""

from fitdev.agents.specialized.knowledge_management import KnowledgeManagementAgent
from fitdev.agents.specialized.trend_scout import TrendScoutAgent
from fitdev.agents.specialized.ux_simulator import UXSimulatorAgent
from fitdev.agents.specialized.api_specialist import APISpecialistAgent
from fitdev.agents.specialized.tech_debt_manager import TechDebtManagerAgent

__all__ = [
    'KnowledgeManagementAgent',
    'TrendScoutAgent',
    'UXSimulatorAgent',
    'APISpecialistAgent',
    'TechDebtManagerAgent'
]
