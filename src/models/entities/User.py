from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username

    @classmethod
    def verify_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
