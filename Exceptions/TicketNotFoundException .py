
class TicketNotFoundException (Exception):
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id
        self.message = f'Sorry, ticket id: {ticket_id} does not exist.'
        super().__init__(self.message)

    def __str__(self):
        return f'Error: {self.message}'
