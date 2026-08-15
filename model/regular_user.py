from model.user import User


class RegularUser(User):

    def __init__(self, user_id=None, name=None, email=None, password=None):
        super().__init__(
            user_id,
            name,
            email,
            password
        )

    def get_role(self):
        return "REGULAR_USER"
