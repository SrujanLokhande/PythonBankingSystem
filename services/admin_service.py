import json
import os
from models.admin import Admin
from models.admin_log import AdminLog
from utils.constants import ADMIN_FILE, ADMIN_LOG_FILE

class AdminService:
    """
    Service class handling all administrative operations.
    
    This class manages admin authentication, user management,
    and logging of administrative actions.
    
    Attributes:
        admin_file (str): Path to admin credentials file
        log_file (str): Path to admin logs file
        banking_system (BankingSystem): Reference to the banking system
        admins (dict): Dictionary of all admin accounts
        logs (list): List of all admin action logs
    """

    def __init__(self, banking_system):
        """
        Initialize the admin service.
        
        Args:
            banking_system (BankingSystem): Reference to the main banking system
        """

        self.admin_file = ADMIN_FILE
        self.log_file = ADMIN_LOG_FILE
        self.banking_system = banking_system
        self.admins = {}
        self.logs = []
        self.load_data()

    def load_data(self):
        """
        Load admin and log data from JSON files.
        
        Reads existing admin credentials and action logs from
        their respective JSON files.
        """
        # Load admin credentials
        if os.path.exists(self.admin_file):
            with open(self.admin_file, 'r') as file:
                data = json.load(file)
                self.admins = {
                    username: Admin.from_dict(admin_data)
                    for username, admin_data in data.items()
                }

        # Load admin logs
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                data = json.load(file)
                self.logs = [AdminLog.from_dict(log_data) for log_data in data]

    def save_admin_data(self):
        """Save admin credentials to JSON file."""
        data = {
            username: admin.to_dict()
            for username, admin in self.admins.items()
        }
        with open(self.admin_file, 'w') as file:
            json.dump(data, file, indent=4)

    def save_log_data(self):
        """Save admin logs to JSON file."""
        data = [log.to_dict() for log in self.logs]
        with open(self.log_file, 'w') as file:
            json.dump(data, file, indent=4)

    def login(self, username, password):
        """
        Authenticate admin login.
        
        Args:
            username (str): Admin username
            password (str): Admin password
            
        Returns:
            Admin: Admin instance if authentication successful, None otherwise
        """
        admin = self.admins.get(username)
        if admin and admin.password == password:
            self.log_action(username, "Login", "Admin logged into the system")
            return admin
        return None

    def log_action(self, admin_username, action, details):
        """
        Log an administrative action.
        
        Args:
            admin_username (str): Username of the admin performing the action
            action (str): Type of action performed
            details (str): Additional details about the action
        """
        log = AdminLog(admin_username, action, details)
        self.logs.append(log)
        self.save_log_data()

    def remove_user(self, admin_username, account_number):
        """
        Remove a user account from the system.
        
        Args:
            admin_username (str): Username of admin performing the removal
            account_number (str): Account number to remove
            
        Returns:
            bool: True if removal successful, False otherwise
        """
        try:
            account_number = str(account_number)
            if account_number in self.banking_system.accounts:
                user = self.banking_system.accounts[account_number]
                del self.banking_system.accounts[account_number]
                self.banking_system.save_data()
                self.log_action(
                    admin_username,
                    "Remove User",
                    f"Removed user account {account_number} ({user.name})"
                )
                return True
            return False
        except Exception as e:
            print(f"Error removing user: {e}")
            return False

    def get_user_transactions(self, account_number):
        """
        Get transaction history for a specific user.
        
        Args:
            account_number (str): Account number to get transactions for
            
        Returns:
            list: List of transactions for the account
        """
        try:
            account_number = str(account_number)
            account = self.banking_system.accounts.get(account_number)
            if account and hasattr(account, 'transactions'):
                return account.transactions
            return []
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []

    def get_all_users(self):
        """
        Get all user accounts in the system.
        
        Returns:
            dict: Dictionary of all user accounts
        """
        return self.banking_system.accounts

    def get_admin_logs(self):
        """
        Get all administrative action logs.
        
        Returns:
            list: List of all admin logs
        """
        return self.logs