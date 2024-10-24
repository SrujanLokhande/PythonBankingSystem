# create_admin.py (New file for initial admin setup)
import json
import os
from getpass import getpass
from utils.constants import ADMIN_FILE, DATA_DIR

def create_initial_admin():
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Check if admin file already exists
    if os.path.exists(ADMIN_FILE):
        print("Admin file already exists. Skipping initial admin creation.")
        return
    
    print("Creating initial admin account...")
    username = input("Enter admin username: ")
    password = getpass("Enter admin password: ")
    confirm_password = getpass("Confirm admin password: ")
    
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return
    
    admin_data = {
        username: {
            "username": username,
            "password": password
        }
    }
    
    with open(ADMIN_FILE, 'w') as file:
        json.dump(admin_data, file, indent=4)
    
    print("Admin account created successfully!")

if __name__ == "__main__":
    create_initial_admin()