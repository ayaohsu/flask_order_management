from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "name"
        self.password = "password"
        
    def __repr__(self):
        return f"User[id={self.id}][name={self.name}]"

def get_user_by_id(id):
    return User(id)