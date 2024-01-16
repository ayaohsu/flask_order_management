from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return f'User[id={self.id}][username={self.username}]'

users = [
    User('1', 'admin01', b'$2b$12$PVAArPGy0TlBfpULT5cShO6X4NToEqHU5r44ehPfut8NWQLBqrc0.'), # 'p@ss'
    User('2', 'customer01', b'$2b$12$PQr/CiKJo8mt8uww4TxXmu1gP6gjPg61oGW81myWtJgVY5QgvKSMe') # 'w0rd'
]

def get_user_by_id(id):
    for user in users:
        if id == user.id:
            return user
    return None

def get_user_by_username(username):
    for user in users:
        if username == user.username:
            return user
    return None