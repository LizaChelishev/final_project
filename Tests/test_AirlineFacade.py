from Business_Logics.AirlineFacade import AirlineFacade

class TestAirlineFacade:
    def test_update_flight(self):
        airline_facade = AirlineFacade()
        flight_list = airline_facade.get_flights_by_airline(1)
        flight = flight_list[0]
        flight.origin_country_id = 3
        airline_facade.update_flight(flight)

        print(f'Checking the origin country id of flight id {flight.get_id()}')
        flight = airline_facade.get_flight_by_id(flight.get_id())
        print(f'retrieved flight_id {flight.get_id()}: {flight}')
        assert (flight.get_origin_country_id() == 3)

