import json
import os
from models.admin import Admin
from models.admin_log import AdminLog
from utils.constants import ADMIN_FILE, ADMIN_LOG_FILE

class AdminService:
    def __init__(self, banking_system):
        self.admin_file = ADMIN_FILE
        self.log_file = ADMIN_LOG_FILE
        self.banking_system = banking_system
        self.admins = {}
        self.logs = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.admin_file):
            with open(self.admin_file, 'r') as file:
                data = json.load(file)
                self.admins = {
                    username: Admin.from_dict(admin_data)
                    for username, admin_data in data.items()
                }

        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                data = json.load(file)
                self.logs = [AdminLog.from_dict(log_data) for log_data in data]

    def save_admin_data(self):
        data = {
            username: admin.to_dict()
            for username, admin in self.admins.items()
        }
        with open(self.admin_file, 'w') as file:
            json.dump(data, file, indent=4)

    def save_log_data(self):
        data = [log.to_dict() for log in self.logs]
        with open(self.log_file, 'w') as file:
            json.dump(data, file, indent=4)

    def login(self, username, password):
        admin = self.admins.get(username)
        if admin and admin.password == password:
            self.log_action(username, "Login", "Admin logged into the system")
            return admin
        return None

    def log_action(self, admin_username, action, details):
        log = AdminLog(admin_username, action, details)
        self.logs.append(log)
        self.save_log_data()

    def get_all_users(self):
        return self.banking_system.accounts

    def remove_user(self, admin_username, account_number):
        try:
            # Convert account_number to string if it's not already
            account_number = str(account_number)
            
            if account_number in self.banking_system.accounts:
                user = self.banking_system.accounts[account_number]
                del self.banking_system.accounts[account_number]
                self.banking_system.save_data()
                
                # Log the action
                self.log_action(
                    admin_username,
                    "Remove User",
                    f"Removed user account {account_number} ({user.name})"
                )
                return True
            return False
        except Exception as e:
            print(f"Error removing user: {e}")  # For debugging
            return False

    def get_user_transactions(self, account_number):
        try:
            # Convert account_number to string if it's not already
            account_number = str(account_number)
            
            account = self.banking_system.accounts.get(account_number)
            if account and hasattr(account, 'transactions'):
                return account.transactions
            return []
        except Exception as e:
            print(f"Error getting transactions: {e}")  # For debugging
            return []


    def get_admin_logs(self):
        return self.logs