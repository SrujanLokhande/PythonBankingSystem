from datetime import datetime

class AdminLog:
    """
    A class representing an administrative action log entry.
    
    This class handles logging of all administrative actions for
    audit and tracking purposes.
    
    Attributes:
        admin_username (str): Username of admin who performed the action
        action (str): Description of the action performed
        details (str): Additional details about the action
        timestamp (str): When the action was performed
    """

    def __init__(self, admin_username, action, details, timestamp=None):
        """
        Initialize a new admin log entry.
        
        Args:
            admin_username (str): Username of the admin
            action (str): Action performed
            details (str): Additional action details
            timestamp (str, optional): Time of action. Defaults to current time
        """

        self.admin_username = admin_username
        self.action = action
        self.details = details
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """
        Convert log entry to a dictionary format for JSON storage.
        
        Returns:
            dict: Log entry in dictionary format
        """

        return {
            'admin_username': self.admin_username,
            'action': self.action,
            'details': self.details,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an AdminLog instance from dictionary data.
        
        Args:
            data (dict): Dictionary containing log information
            
        Returns:
            AdminLog: New instance of AdminLog
        """
        
        return cls(
            data['admin_username'],
            data['action'],
            data['details'],
            data['timestamp']
        )