
class PasswordTooShortException(Exception):
    def __init__(self, password):
        self.password = password
        self.message = f'Sorry! password is too short.'
        super().__init__(self.message)

    def __str__(self):
        return f'Error: {self.message}'
