import uuid

class User:
    def __init__(self, username, password, role="staff", user_id=None):
        self.username = username
        self.password = password
        self.role = role
        self.user_id = user_id if user_id else uuid.uuid4().hex[:4]

    def to_dict(self):
        return {
            "user-id": self.user_id,
            "password": self.password,
            "role": self.role
        }

