#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Specialized Critics for FitDev.io
"""

from critics.specialized.knowledge_management_critic import KnowledgeManagementCritic
from critics.specialized.trend_scout_critic import TrendScoutCritic
from critics.specialized.ux_simulator_critic import UXSimulatorCritic
from critics.specialized.api_specialist_critic import APISpecialistCritic
from critics.specialized.tech_debt_manager_critic import TechDebtManagerCritic

__all__ = [
    'KnowledgeManagementCritic',
    'TrendScoutCritic',
    'UXSimulatorCritic',
    'APISpecialistCritic',
    'TechDebtManagerCritic'
]
