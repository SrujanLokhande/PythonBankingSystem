from tkinter import ttk

class UserTypeScreen:
    """
    Initial screen for user type selection.
    
    This class creates and manages the initial screen where users
    choose between admin and client login options.
    
    Attributes:
        root (tk.Tk): Main window of the application
        show_admin_login (function): Callback to show admin login screen
        show_client_login (function): Callback to show client login screen
        frame (ttk.Frame): Main frame containing the UI elements
    """

    def __init__(self, root, show_admin_login, show_client_login):
        """
        Initialize the user type selection screen.
        
        Args:
            root (tk.Tk): Main window of the application
            show_admin_login (function): Callback for admin login
            show_client_login (function): Callback for client login
        """
        self.root = root
        self.show_admin_login = show_admin_login
        self.show_client_login = show_client_login
        
        self.frame = ttk.Frame(root, padding="20")
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all UI elements for the selection screen."""
        # Title label
        ttk.Label(self.frame, text="Welcome to the Banking System", 
                 font=("Helvetica", 14, "bold")).grid(
                     row=0, column=0, columnspan=2, pady=20)
        
        # Selection prompt
        ttk.Label(self.frame, text="Please select your user type:").grid(
            row=1, column=0, columnspan=2, pady=10)
        
        # Admin button
        ttk.Button(self.frame, text="Administrator", 
                  command=self.show_admin_login).grid(
                      row=2, column=0, padx=10, pady=10)
        
        # Client button
        ttk.Button(self.frame, text="Client", 
                  command=self.show_client_login).grid(
                      row=2, column=1, padx=10, pady=10)

    def show(self):
        """Display the user type selection screen."""
        self.frame.grid()

    def hide(self):
        """Hide the user type selection screen."""
        self.frame.grid_remove()