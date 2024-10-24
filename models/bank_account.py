class BankAccount:
    def __init__(self, account_number, name, password, balance=0):
        self.account_number = account_number
        self.name = name
        self.password = password
        self.balance = balance
        self.transactions = []

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'name': self.name,
            'password': self.password,
            'balance': self.balance,
            'transactions': self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(
            data['account_number'],
            data['name'],
            data['password'],
            data['balance']
        )
        account.transactions = data['transactions']
        return account