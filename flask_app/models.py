from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

    @staticmethod
    def get(username):
        return User(username)

    @staticmethod
    def get_by_id(user_id):
        return User(user_id)