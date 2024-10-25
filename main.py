import tkinter as tk
from UI.user_type_screen import UserTypeScreen
from UI.banking_GUI import BankingGUI
from UI.admin_GUI import AdminGUI
from services.banking_system import BankingSystem
from services.admin_service import AdminService

class BankingApplication:
    """
    Main application class coordinating all components of the banking system.
    
    This class initializes all necessary services and UI components,
    and manages navigation between different screens.
    
    Attributes:
        root (tk.Tk): Main window of the application
        banking_system (BankingSystem): Main banking system service
        admin_service (AdminService): Administrative service
        user_type_screen (UserTypeScreen): Initial user type selection screen
        admin_gui (AdminGUI): Administrator interface
        banking_gui (BankingGUI): Client banking interface
    """

    def __init__(self):
        """Initialize the banking application and all its components."""
        # Create main window
        self.root = tk.Tk()
        self.root.title("Banking System")
        self.root.geometry("800x600")
        
        # Initialize services
        self.banking_system = BankingSystem()
        self.admin_service = AdminService(self.banking_system)
        
        # Initialize UI components
        self.user_type_screen = UserTypeScreen(
            self.root,
            self.show_admin_login,
            self.show_client_login
        )
        
        self.admin_gui = AdminGUI(
            self.root,
            self.admin_service,
            self.show_user_type_screen
        )
        
        self.banking_gui = BankingGUI(
            self.root,
            self.banking_system,
            self.show_user_type_screen
        )
        
        # Show initial screen
        self.show_user_type_screen()

    def show_user_type_screen(self):
        """Display the initial user type selection screen."""

        # Hide all other frames
        self.admin_gui.login_frame.grid_remove()
        self.admin_gui.main_frame.grid_remove()
        self.banking_gui.login_frame.grid_remove()
        self.banking_gui.register_frame.grid_remove()
        self.banking_gui.main_frame.grid_remove()
        self.user_type_screen.show()

    def show_admin_login(self):
        """Switch to the administrator login screen."""
        self.user_type_screen.hide()
        self.admin_gui.show_login_frame()

    def show_client_login(self):
        """Switch to the client login screen."""
        self.user_type_screen.hide()
        self.banking_gui.show_login_frame()

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = BankingApplication()
    app.run()