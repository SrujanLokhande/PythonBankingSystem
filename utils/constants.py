import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

DATA_FILE = os.path.join(DATA_DIR, 'bank_data.json')
ADMIN_FILE = os.path.join(DATA_DIR, 'admin_data.json')
ADMIN_LOG_FILE = os.path.join(DATA_DIR, 'admin_logs.json')