class FlightDto:
    def __init__(self):
        self.id = None
        self.airline_company_id = None
        self.origin_country_id = None
        self.destination_country_id = None
        self.departure_time = None
        self.landing_time = None
        self.remaining_tickets = None

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_airline_company_id(self):
        return self.airline_company_id

    def set_airline_company_id(self, airline_company_id):
        self.airline_company_id = airline_company_id

    def get_origin_country_id(self):
        return self.origin_country_id

    def set_origin_country_id(self, origin_country_id):
        self.origin_country_id = origin_country_id

    def get_destination_country_id(self):
        return self.destination_country_id

    def set_destination_country_id(self, destination_country_id):
        self.destination_country_id = destination_country_id

    def get_departure_time(self):
        return self.departure_time

    def set_departure_time(self, departure_time):
        self.departure_time = departure_time

    def get_landing_time(self):
        return self.landing_time

    def set_landing_time(self, landing_time):
        self.landing_time = landing_time

    def get_remaining_tickets(self):
        return self.remaining_tickets

    def set_remaining_tickets(self, remaining_tickets):
        self.remaining_tickets = remaining_tickets

    def __str__(self):
        return f'<Flight> id:{self.id} airline_company_id:{self.airline_company_id}' \
               f' origin_country_id:{self.origin_country_id} destination_country_id:{self.destination_country_id}\n'

    def __repr__(self):
        return f'<Flight> id:{self.id} airline_company_id:{self.airline_company_id}' \
               f' origin_country_id:{self.origin_country_id} destination_country_id:{self.destination_country_id}\n'
