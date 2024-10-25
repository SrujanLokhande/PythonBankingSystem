import os

"""
Configuration constants for the banking system.

This module defines constant values used throughout the application,
particularly file paths for data storage.
"""

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directory path
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# File paths for different data storage
DATA_FILE = os.path.join(DATA_DIR, 'bank_data.json')
ADMIN_FILE = os.path.join(DATA_DIR, 'admin_data.json')
ADMIN_LOG_FILE = os.path.join(DATA_DIR, 'admin_logs.json')