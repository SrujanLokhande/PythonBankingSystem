from datetime import datetime

class AdminLog:
    def __init__(self, admin_username, action, details, timestamp=None):
        self.admin_username = admin_username
        self.action = action
        self.details = details
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'admin_username': self.admin_username,
            'action': self.action,
            'details': self.details,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['admin_username'],
            data['action'],
            data['details'],
            data['timestamp']
        )