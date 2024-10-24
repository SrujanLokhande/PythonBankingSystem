import tkinter as tk
from tkinter import messagebox, ttk

class AdminGUI:
    def __init__(self, root, admin_service, show_user_type_screen):
        self.root = root
        self.admin_service = admin_service
        self.show_user_type_screen = show_user_type_screen
        self.current_admin = None
        
        self.create_login_frame()
        self.create_main_frame()

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.root, padding="20")
        
        ttk.Label(self.login_frame, text="Administrator Login", 
                 font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.login_frame, text="Username:").grid(row=1, column=0, pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=2, column=0, pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(self.login_frame, text="Login", 
                  command=self.login).grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.login_frame, text="Back", 
                  command=self.show_user_type_screen).grid(row=4, column=0, columnspan=2)

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        
        # User management section
        ttk.Label(self.main_frame, text="User Management", 
                 font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        self.users_tree = ttk.Treeview(self.main_frame, 
                                     columns=("Account", "Name", "Balance"), 
                                     show="headings")
        self.users_tree.heading("Account", text="Account")
        self.users_tree.heading("Name", text="Name")
        self.users_tree.heading("Balance", text="Balance")
        self.users_tree.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(self.main_frame, text="Remove Selected User", 
                  command=self.remove_user).grid(row=2, column=0, pady=5)
        ttk.Button(self.main_frame, text="View Transactions", 
                  command=self.view_transactions).grid(row=2, column=1, pady=5)
        
        # Admin logs section
        ttk.Label(self.main_frame, text="Admin Logs", 
                 font=("Helvetica", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=10)
        
        self.logs_tree = ttk.Treeview(self.main_frame, 
                                    columns=("Admin", "Action", "Details", "Timestamp"), 
                                    show="headings")
        self.logs_tree.heading("Admin", text="Admin")
        self.logs_tree.heading("Action", text="Action")
        self.logs_tree.heading("Details", text="Details")
        self.logs_tree.heading("Timestamp", text="Timestamp")
        self.logs_tree.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(self.main_frame, text="Refresh", 
                  command=self.refresh_data).grid(row=5, column=0, pady=5)
        ttk.Button(self.main_frame, text="Logout", 
                  command=self.logout).grid(row=5, column=1, pady=5)

    def show_login_frame(self):
        self.main_frame.grid_remove()
        self.login_frame.grid()

    def show_main_frame(self):
        self.login_frame.grid_remove()
        self.main_frame.grid()
        self.refresh_data()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        admin = self.admin_service.login(username, password)
        if admin:
            self.current_admin = admin
            self.show_main_frame()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def view_transactions(self):
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to view transactions")
            return
        
        # Get account number from selected item
        account_number = str(self.users_tree.item(selection[0])['values'][0])
        transactions = self.admin_service.get_user_transactions(account_number)
        
        if not transactions:
            messagebox.showinfo("Info", "No transactions found for this user")
            return
        
        # Create a new window to display transactions
        trans_window = tk.Toplevel(self.root)
        trans_window.title(f"Transactions - Account {account_number}")
        trans_window.geometry("600x400")
        
        # Create frame with padding
        frame = ttk.Frame(trans_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with scrollbar
        tree = ttk.Treeview(frame, 
                           columns=("Type", "Amount", "Date", "Balance"),
                           show="headings",
                           height=15)
        
        # Configure columns
        tree.heading("Type", text="Type")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")
        tree.heading("Balance", text="Balance")
        
        # Set column widths
        tree.column("Type", width=100)
        tree.column("Amount", width=100)
        tree.column("Date", width=200)
        tree.column("Balance", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        # Populate transactions
        for trans in transactions:
            tree.insert("", "end", values=(
                trans['type'],
                f"${trans['amount']:.2f}",
                trans['date'],
                f"${trans['balance']:.2f}"
            ))

    def remove_user(self):
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to remove")
            return
        
        account_number = str(self.users_tree.item(selection[0])['values'][0])
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this user?"):
            if self.admin_service.remove_user(self.current_admin.username, account_number):
                messagebox.showinfo("Success", "User removed successfully")
                self.refresh_data()
            else:
                messagebox.showerror("Error", "Failed to remove user")

    def refresh_data(self):
        # Clear and reload users
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        for account_number, account in self.admin_service.get_all_users().items():
            self.users_tree.insert("", "end", values=(
                account_number,
                account.name,
                f"${account.balance:.2f}"
            ))
        
        # Clear and reload logs
        for item in self.logs_tree.get_children():
            self.logs_tree.delete(item)
        
        for log in self.admin_service.get_admin_logs():
            self.logs_tree.insert("", "end", values=(
                log.admin_username,
                log.action,
                log.details,
                log.timestamp
            ))

    def logout(self):
        self.current_admin = None
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.show_user_type_screen()