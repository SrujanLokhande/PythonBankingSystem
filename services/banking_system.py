import json
import os
from datetime import datetime
from models.bank_account import BankAccount
from utils.constants import DATA_FILE

class BankingSystem:
    def __init__(self):
        self.filename = DATA_FILE
        self.accounts = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.accounts = {
                    acc_num: BankAccount.from_dict(acc_data)
                    for acc_num, acc_data in data.items()
                }

    def save_data(self):
        data = {
            acc_num: account.to_dict()
            for acc_num, account in self.accounts.items()
        }
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def create_account(self, name, password):
        account_number = self.generate_account_number()
        account = BankAccount(account_number, name, password)
        self.accounts[account_number] = account
        self.save_data()
        return account_number

    def generate_account_number(self):
        return str(len(self.accounts) + 1000)

    def login(self, account_number, password):
        account = self.accounts.get(account_number)
        if account and account.password == password:
            return account
        return None

    def deposit(self, account_number, amount):
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