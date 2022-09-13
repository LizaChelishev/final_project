class NoRemainingTicketsError(Exception):
    def __init__(self, msg="No remaining tickets for this flight."):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.msg}'