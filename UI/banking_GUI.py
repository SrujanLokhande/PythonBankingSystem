import tkinter as tk
from tkinter import messagebox, ttk

class BankingGUI:
    def __init__(self, root, banking_system, show_user_type_screen):
        self.root = root
        self.bank = banking_system
        self.show_user_type_screen = show_user_type_screen
        self.current_account = None
        
        self.create_login_frame()
        self.create_register_frame()
        self.create_main_frame()

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.root, padding="20")
        
        ttk.Label(self.login_frame, text="Client Login", 
                 font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.login_frame, text="Account Number:").grid(row=1, column=0, pady=5)
        self.login_account_entry = ttk.Entry(self.login_frame)
        self.login_account_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=2, column=0, pady=5)
        self.login_password_entry = ttk.Entry(self.login_frame, show="*")
        self.login_password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(self.login_frame, text="Login", 
                  command=self.login).grid(row=3, column=0, pady=10)
        ttk.Button(self.login_frame, text="Register", 
                  command=self.show_register_frame).grid(row=3, column=1, pady=10)
        
        ttk.Button(self.login_frame, text="Back", 
                  command=self.show_user_type_screen).grid(row=4, column=0, columnspan=2)

    def create_register_frame(self):
        self.register_frame = ttk.Frame(self.root, padding="20")
        
        ttk.Label(self.register_frame, text="Register New Account", 
                 font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.register_frame, text="Name:").grid(row=1, column=0, pady=5)
        self.register_name_entry = ttk.Entry(self.register_frame)
        self.register_name_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.register_frame, text="Password:").grid(row=2, column=0, pady=5)
        self.register_password_entry = ttk.Entry(self.register_frame, show="*")
        self.register_password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(self.register_frame, text="Register", 
                  command=self.register).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.register_frame, text="Back to Login", 
                  command=self.show_login_frame).grid(row=4, column=0, columnspan=2)

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        
        self.balance_label = ttk.Label(self.main_frame, text="", 
                                     font=("Helvetica", 12, "bold"))
        self.balance_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.main_frame, text="Amount:").grid(row=1, column=0, pady=5)
        self.amount_entry = ttk.Entry(self.main_frame)
        self.amount_entry.grid(row=1, column=1, pady=5)
        
        ttk.Button(self.main_frame, text="Deposit", 
                  command=self.deposit).grid(row=2, column=0, pady=5, padx=5)
        ttk.Button(self.main_frame, text="Withdraw", 
                  command=self.withdraw).grid(row=2, column=1, pady=5, padx=5)
        
        # Transaction history
        ttk.Label(self.main_frame, text="Transaction History", 
                 font=("Helvetica", 11, "bold")).grid(row=3, column=0, columnspan=2, pady=5)
        
        self.transaction_tree = ttk.Treeview(
            self.main_frame, 
            columns=("Type", "Amount", "Date", "Balance"), 
            show="headings",
            height=10
        )
        self.transaction_tree.heading("Type", text="Type")
        self.transaction_tree.heading("Amount", text="Amount")
        self.transaction_tree.heading("Date", text="Date")
        self.transaction_tree.heading("Balance", text="Balance")
        
        # Configure column widths
        self.transaction_tree.column("Type", width=100)
        self.transaction_tree.column("Amount", width=100)
        self.transaction_tree.column("Date", width=150)
        self.transaction_tree.column("Balance", width=100)
        
        self.transaction_tree.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.transaction_tree.yview)
        scrollbar.grid(row=4, column=2, sticky="ns")
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        ttk.Button(self.main_frame, text="Logout", 
                  command=self.logout).grid(row=5, column=0, columnspan=2, pady=10)

    def show_login_frame(self):
        self.register_frame.grid_remove()
        self.main_frame.grid_remove()
        self.login_frame.grid()

    def show_register_frame(self):
        self.login_frame.grid_remove()
        self.main_frame.grid_remove()
        self.register_frame.grid()

    def show_main_frame(self):
        self.login_frame.grid_remove()
        self.register_frame.grid_remove()
        self.main_frame.grid()

    def update_balance_label(self):
        self.balance_label.config(
            text=f"Current Balance: ${self.current_account.balance:.2f}")

    def update_transaction_history(self):
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        for transaction in self.current_account.transactions:
            self.transaction_tree.insert("", "end", values=(
                transaction['type'],
                f"${transaction['amount']:.2f}",
                transaction['date'],
                f"${transaction['balance']:.2f}"
            ))

    def login(self):
        account_number = self.login_account_entry.get()
        password = self.login_password_entry.get()
        
        account = self.bank.login(account_number, password)
        if account:
            self.current_account = account
            self.update_balance_label()
            self.update_transaction_history()
            self.show_main_frame()
        else:
            messagebox.showerror("Error", "Invalid account number or password")

    def register(self):
        name = self.register_name_entry.get()
        password = self.register_password_entry.get()
        
        if name and password:
            account_number = self.bank.create_account(name, password)
            messagebox.showinfo(
                "Success", 
                f"Account created successfully!\nYour account number is: {account_number}"
            )
            self.show_login_frame()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
            
            if self.bank.deposit(self.current_account.account_number, amount):
                self.update_balance_label()
                self.update_transaction_history()
                self.amount_entry.delete(0, tk.END)
                messagebox.showinfo("Success", f"${amount:.2f} deposited successfully")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount")

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
            
            if self.bank.withdraw(self.current_account.account_number, amount):
                self.update_balance_label()
                self.update_transaction_history()
                self.amount_entry.delete(0, tk.END)
                messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully")
            else:
                messagebox.showerror("Error", "Insufficient balance")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount")

    def logout(self):
        self.current_account = None
        self.login_account_entry.delete(0, tk.END)
        self.login_password_entry.delete(0, tk.END)
        self.show_user_type_screen()