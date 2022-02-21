import datetime
from Business_Logics.FacadeBase import FacadeBase
from Database.Airline_Companies import *
from Database.Countries import Countries
from Exceptions.InvalidFlightException import InvalidFlightException
import logging
from ApplicationLogger import print_to_log
from Database.Flights import *
from Exceptions.FlightTimesException import FlightTimesException

logger = logging.getLogger(__name__)


class AirlineFacade(FacadeBase):

    def __init__(self, login_token, repo):
        self.repo = repo
        super().__init__()
        self._login_token = login_token

        if self.login_token.role != 'airline_companies':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function get_airline_flights but his '
                         f'role is not Airline Company.')

    def update_airline(self, airline):
        print_to_log(logger, logging.INFO, f'Updating airline {airline.id}...')
        if self.login_token.role != 'airline_companies':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function update_airline but his role is '
                         f'not Airline Company.')
            return
        if not isinstance(airline, Airline_Companies):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function update_airline but the airline "{airline}" '
                         f'that was sent is not an Airline Company object.')
            return
        airline_ = self.repo.get_by_condition(Airline_Companies, lambda query: query.filter(
            Airline_Companies.id == self.login_token.id).all())
        if not airline_:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function update_airline but the airline "{airline}" '
                         f'not exists in the db.')
            return
        if self.repo.get_by_condition(Airline_Companies,
                                      lambda query: query.filter(Airline_Companies.name == airline.name).all()) \
                and self.repo.get_by_condition(Airline_Companies, lambda query: query.filter(
            Airline_Companies.name == airline.name).all()) != airline_:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function update_airline but the'
                         f' airline.name "{airline.name}" already exists in the db.')
            return
        if not self.repo.get_by_condition(Countries,
                                          lambda query: query.filter(Countries.id == airline.country_id).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function update_airline but the'
                         f' airline.country_id "{airline.country_id}" not exists in the db.')
            return
        print_to_log(logger, logging.DEBUG,
                     f'The login token "{self.login_token}" used the function update_airline and updated to'
                     f' airline "{airline}"')
        self.repo.update_by_id(Airline_Companies, Airline_Companies.id, self.login_token.id,
                               {Airline_Companies.name: airline.name,
                                Airline_Companies.country_id: airline.country_id})
        return True

    def add_flight(self, flight):
        if self.login_token.role != 'airline_companies':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_flight but his role'
                         f' is not Airline Company.')
            return
        if not isinstance(flight, Flights):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_flight but the flight '
                         f'"{flight}" that was sent is not a Flight object.')
            return
        if not self.repo.get_by_condition(Countries,
                                          lambda query: query.filter(Countries.id == flight.origin_country_id).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_flight but the'
                         f' origin_country_id "{Flights.origin_country_id}" that was sent not exists in the db.')
            return
        if not self.repo.get_by_condition(Countries, lambda query: query.filter(
                Countries.id == flight.destination_country_id).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_flight but the'
                         f' destination_country_id "{flight.destination_country_id}"that was sent not exists in the db.')
            return
        if not isinstance(flight.departure_time, datetime) or not isinstance(flight.landing_time, datetime):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_flight but both '
                         f'departure_time "{Flights.departure_time}" and landing_time "{Flights.landing_time}" '
                         f'must be a Datetime objects.')
            return
        if flight.departure_time + datetime.timedelta(hours=1) > flight.landing_time:  # checking the delta t
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_flight but '
                         f'the time delta between departure_time "{flight.departure_time}" and landing time "{flight.landing_time}" '
                         f'is less than one hour.')
            raise FlightTimesException
        if not isinstance(flight.remaining_tickets, int):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_flight'
                         f' but the remaining_tickets "{flight.remaining_tickets}" that was sent is not an integer.')
            return
        if flight.remaining_tickets < 100:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_flight but the'
                         f' remaining_tickets "{flight.remaining_tickets}" that was sent must be more or equal than 100.')
            return
        flight.id = None
        flight.airline_company_id = self.login_token.id
        print_to_log(logger, logging.DEBUG,
                     f'The login token "{self.login_token}" used the function add_flight and added the'
                     f' flight "{flight}" to the db.')
        self.repo.add(flight)
        return True

    def update_flight(self, flight):
        print_to_log(logger, logging.INFO, f'Updating flight {flight.id}...')
        if flight.get_remaining_tickets() < 0:
            print_to_log(logger, logging.ERROR, 'Invalid number of remaining tickets, cannot be negative.')
            raise InvalidFlightException(flight.get_airline_company_id(), flight.get_id())

        if flight.get_landing_time() <= flight.get_departure_time():
            print_to_log(logger, logging.ERROR, 'Invalid departure or landing time, '
                                                'make sure landing time is after departure time.')
            raise InvalidFlightException(flight.get_airline_company_id(), flight.get_id())

        if flight.get_origin_country_id() == flight.get_destination_country_id():
            print_to_log(logger, logging.ERROR, 'Destination country can not be the same as origin country.')
            raise InvalidFlightException(flight.get_airline_company_id(), flight.get_id())

        flight_dbo = FacadeBase.repo.get_by_id(Flights, flight.get_id())
        FacadeBase.repo.update(Flights, Flights.get_key(), flight.get_id(),
                               flight_dbo.get_dict(flight.get_airline_company_id(),
                                                   flight.get_origin_country_id(),
                                                   flight.get_destination_country_id(),
                                                   flight.get_departure_time(),
                                                   flight.get_landing_time(),
                                                   flight.get_remaining_tickets()))

    def remove_flight(self, flight_id):
        if self.login_token.role != 'airline_companies':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_flight but his role is '
                         f'not Airline Company.')
            return
        if not isinstance(flight_id, int):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_flight but the flight_id "{flight_id}" '
                         f'that was sent is not an integer.')
            return
        if flight_id <= 0:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_flight but the flight_id "{flight_id}" '
                         f'that was sent is not positive.')
            return
        flight = self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.id == flight_id).all())
        if not flight:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_flight but the flight_id "{flight_id}" '
                         f'not exists in the db.')
            return
        if self.login_token.id != flight[0].airline_company_id:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_flight but the flight "{flight}" '
                         f'not belongs to the login token airline company.')
            return
        print_to_log(logger, logging.DEBUG,
                     f'The login token "{self.login_token}" used the function remove_flight and removed the flight "{flight}" '
                     f'from the db.')
        self.repo.delete_by_id(Flights, Flights.id, flight_id)
        return True

    def get_my_flights(self):
        if self.login_token.role != 'airline_companies':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function get_airline_flights but his role is '
                         f'not Airline Company.')
            return
        return self.repo.get_by_condition(Flights, lambda query: query.filter(
            Flights.airline_company_id == self.login_token.id).all())
