class UserRoleSettingException(Exception):
    def __init__(self):
        self.message = "More than 3 roles in the user_roles table."
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
