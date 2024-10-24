from tkinter import ttk

class UserTypeScreen:
    def __init__(self, root, show_admin_login, show_client_login):
        self.root = root
        self.show_admin_login = show_admin_login
        self.show_client_login = show_client_login
        
        self.frame = ttk.Frame(root, padding="20")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Welcome to the Banking System", 
                 font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(self.frame, text="Please select your user type:").grid(
            row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.frame, text="Administrator", 
                  command=self.show_admin_login).grid(row=2, column=0, padx=10, pady=10)
        
        ttk.Button(self.frame, text="Client", 
                  command=self.show_client_login).grid(row=2, column=1, padx=10, pady=10)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()