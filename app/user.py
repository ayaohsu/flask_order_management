class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.id
    
    def get_user_by_id(self, id):
        if id == 1:
            self.id = 1
            self.username = 'admin'
            self.password = 'apass'
            return self
        elif id == 2:
            self.id = 2
            self.username = 'customer'
            self.password = 'bpass'
            return self
        else:
            return None
        