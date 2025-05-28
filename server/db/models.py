from datetime import datetime

class User:
    def __init__(self, user_id: int, username: str, password_hash: str, email: str, created_at: datetime, profile_image: str = None):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = created_at
        self.profile_picture = profile_image  # Placeholder for profile picture URL or path
    
    def __repr__(self):
        return f"User(id: {self.user_id}, name: {self.username}, password: {self.password_hash}, email: {self.email}, created at: {self.created_at})"
    

class Group:
    def __init__(self, group_id: int, group_name: str, creator_id: int,group_code: str, created_at: datetime):
        self.group_id = group_id
        self.group_name = group_name
        self.creator_id = creator_id
        self.group_code = group_code  # Unique code for the group
        self.created_at = created_at
        

class GroupMember:
    def __init__(self, group_id: int, user_id: int, is_admin: bool):
        self.group_id = group_id
        self.user_id = user_id
        self.is_admin = is_admin


class Message:
    def __init__(self, message_id: int, content: str, sender_id: int, group_id: int, recipient_id: int, timestamp: datetime, message_type: str, file_name: str):
        self.message_id = message_id
        self.content = content
        self.sender_id = sender_id
        self.group_id = group_id
        self.recipient_id = recipient_id
        self.timestamp = timestamp
        self.message_type = message_type
        self.file_name = file_name 
