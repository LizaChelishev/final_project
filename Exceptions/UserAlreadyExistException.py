
class UserAlreadyExistException(Exception):
    def __init__(self, username):
        self.username = username
        self.message = f'User {username} already exist'
        super().__init__(self.message)

    def __str__(self):
        return f'Error: {self.message}'
