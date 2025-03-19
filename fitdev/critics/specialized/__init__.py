#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Specialized Critics for FitDev.io
"""

from fitdev.critics.specialized.knowledge_management_critic import KnowledgeManagementCritic
from fitdev.critics.specialized.trend_scout_critic import TrendScoutCritic
from fitdev.critics.specialized.ux_simulator_critic import UXSimulatorCritic
from fitdev.critics.specialized.api_specialist_critic import APISpecialistCritic
from fitdev.critics.specialized.tech_debt_manager_critic import TechDebtManagerCritic

__all__ = [
    'KnowledgeManagementCritic',
    'TrendScoutCritic',
    'UXSimulatorCritic',
    'APISpecialistCritic',
    'TechDebtManagerCritic'
]
