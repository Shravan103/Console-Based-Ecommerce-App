class User:

    def __init__(self, user_id=None, name=None, email=None, password=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    def get_role(self):
        return "USER"
