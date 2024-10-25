class Admin:
    """
    A class representing an administrator account.
    
    This class handles administrator credentials and authentication
    for system administration purposes.
    
    Attributes:
        username (str): Administrator's username
        password (str): Administrator's password
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        """
        Convert admin information to a dictionary format for JSON storage.
        
        Returns:
            dict: Admin information in dictionary format
        """

        return {
            'username': self.username,
            'password': self.password
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an Admin instance from dictionary data.
        
        Args:
            data (dict): Dictionary containing admin information
            
        Returns:
            Admin: New instance of Admin
        """
        
        return cls(data['username'], data['password'])