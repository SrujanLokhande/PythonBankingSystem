import tkinter as tk
from UI.user_type_screen import UserTypeScreen
from UI.banking_GUI import BankingGUI
from UI.admin_GUI import AdminGUI
from services.banking_system import BankingSystem
from services.admin_service import AdminService

class BankingApplication:
    def __init__(self):
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
        self.admin_gui.login_frame.grid_remove()
        self.admin_gui.main_frame.grid_remove()
        self.banking_gui.login_frame.grid_remove()
        self.banking_gui.register_frame.grid_remove()
        self.banking_gui.main_frame.grid_remove()
        self.user_type_screen.show()

    def show_admin_login(self):
        self.user_type_screen.hide()
        self.admin_gui.show_login_frame()

    def show_client_login(self):
        self.user_type_screen.hide()
        self.banking_gui.show_login_frame()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BankingApplication()
    app.run()