import json
import os
from datetime import datetime
from models.bank_account import BankAccount
from utils.constants import DATA_FILE

class BankingSystem:
    """
    Main banking system service handling all banking operations.
    
    This class manages all bank accounts and their operations, including
    creation, authentication, and transaction processing.
    
    Attributes:
        filename (str): Path to the JSON file storing account data
        accounts (dict): Dictionary of all bank accounts
    """

    def __init__(self):
        """Initialize the banking system and load existing account data."""
        self.filename = DATA_FILE
        self.accounts = {}
        self.load_data()

    def load_data(self):
        """
        Load account data from JSON file.
        
        Reads existing account data from the JSON file and creates
        BankAccount instances for each account.
        """

        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.accounts = {
                    acc_num: BankAccount.from_dict(acc_data)
                    for acc_num, acc_data in data.items()
                }

    def save_data(self):
        """
        Save all account data to JSON file.
        
        Converts all account instances to dictionary format and
        saves them to the JSON file.
        """

        data = {
            acc_num: account.to_dict()
            for acc_num, account in self.accounts.items()
        }
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def create_account(self, name, password):
        """
        Create a new bank account.
        
        Args:
            name (str): Account holder's name
            password (str): Account password
            
        Returns:
            str: New account number
        """

        account_number = self.generate_account_number()
        account = BankAccount(account_number, name, password)
        self.accounts[account_number] = account
        self.save_data()
        return account_number

    def generate_account_number(self):
        """
        Generate a unique account number.
        
        Returns:
            str: New unique account number
        """

        return str(len(self.accounts) + 1000)

    def login(self, account_number, password):
        """
        Authenticate user login.
        
        Args:
            account_number (str): Account number to authenticate
            password (str): Password to verify
            
        Returns:
            BankAccount: Account instance if authentication successful, None otherwise
        """

        account = self.accounts.get(account_number)
        if account and account.password == password:
            return account
        return None

    def deposit(self, account_number, amount):
        """
        Deposit money into an account.
        
        Args:
            account_number (str): Target account number
            amount (float): Amount to deposit
            
        Returns:
            bool: True if deposit successful, False otherwise
        """

        account = self.accounts.get(account_number)
        if account:
            account.balance += amount
            account.transactions.append({
                'type': 'deposit',
                'amount': amount,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'balance': account.balance
            })
            self.save_data()
            return True
        return False

    def withdraw(self, account_number, amount):
        """
        Withdraw money from an account.
        
        Args:
            account_number (str): Source account number
            amount (float): Amount to withdraw
            
        Returns:
            bool: True if withdrawal successful, False otherwise
        """
        
        account = self.accounts.get(account_number)
        if account and account.balance >= amount:
            account.balance -= amount
            account.transactions.append({
                'type': 'withdrawal',
                'amount': amount,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'balance': account.balance
            })
            self.save_data()
            return True
        return False