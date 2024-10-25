class BankAccount:
    """
    A class representing a bank account with basic banking operations.
    
    This class handles individual bank account data and operations including
    balance management and transaction history.
    
    Attributes:
        account_number (str): Unique identifier for the account
        name (str): Account holder's name
        password (str): Account password for authentication
        balance (float): Current balance in the account
        transactions (list): List of all transactions performed
    """
    def __init__(self, account_number, name, password, balance=0):
        """
        Initialize a new bank account.
        
        Args:
            account_number (str): Unique account identifier
            name (str): Account holder's name
            password (str): Account password
            balance (float, optional): Initial balance. Defaults to 0
        """
        self.account_number = account_number
        self.name = name
        self.password = password
        self.balance = balance
        self.transactions = []

    def to_dict(self):
        """
        Convert account information to a dictionary format for JSON storage.
        
        Returns:
            dict: Account information in dictionary format
        """

        return {
            'account_number': self.account_number,
            'name': self.name,
            'password': self.password,
            'balance': self.balance,
            'transactions': self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a BankAccount instance from dictionary data.
        
        Args:
            data (dict): Dictionary containing account information
            
        Returns:
            BankAccount: New instance of BankAccount
        """
        account = cls(
            data['account_number'],
            data['name'],
            data['password'],
            data['balance']
        )
        account.transactions = data['transactions']
        return account