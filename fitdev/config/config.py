#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration settings for FitDev.io
"""

import os
from pathlib import Path
from typing import Dict, Any

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"

# Default configuration
DEFAULT_CONFIG = {
    "organization": {
        "name": "FitDev.io",
        "description": "Virtual Software Development Organization"
    },
    "agents": {
        "default_model": "gpt-4",
        "browser_enabled": True,
        "memory_enabled": True
    },
    "compensation": {
        "base_rates": {
            "executive": 100,
            "development": 85,
            "quality": 80,
            "specialized": 90
        },
        "performance_multiplier": 1.5
    }
}


def load_config() -> Dict[str, Any]:
    """Load configuration from environment or default settings."""
    # TODO: Implement loading from config file
    # TODO: Override with environment variables
    return DEFAULT_CONFIG
