class User:
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.id