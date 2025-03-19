#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quality Critics for FitDev.io
"""

from critics.quality.qa_engineer_critic import QAEngineerCritic
from critics.quality.security_specialist_critic import SecuritySpecialistCritic
from critics.quality.technical_writer_critic import TechnicalWriterCritic

__all__ = [
    'QAEngineerCritic',
    'SecuritySpecialistCritic',
    'TechnicalWriterCritic'
]
