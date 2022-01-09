
class NoMoreTicketsForFlightsException(Exception):
    def __init__(self, airline_company, flight_id):
        self.airline_company = airline_company
        self.flight_id = flight_id
        self.message = f'We are so sorry but there are no more tickets for {airline_company} flight {flight_id}.'
        super().__init__(self.message)

    def __str__(self):
        return f'Error: {self.message}'
