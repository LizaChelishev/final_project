import datetime

from Business_Logics.FacadeBase import FacadeBase
from DTO.FlightDto import FlightDto
from Database import Airline_Companies
from Database.Countries import Countries
from Exceptions.InvalidFlightException import InvalidFlightException
import logging
from ApplicationLogger import print_to_log
from Database.Flights import *

logger = logging.getLogger(__name__)


class AirlineFacade(FacadeBase):
    def __init__(self, login_token, repo):
        self.repo = repo
        super().__init__(self.repo)
        self._login_token = login_token

    def get_flights_by_airline(self, airline_company_id):
        print_to_log(logger, logging.INFO, f'Getting flights of airline: {airline_company_id}...')
        flight_dto_list = []
        flights = FacadeBase.repo.get_all_by_condition(Flights, Flights.airline_company_id, airline_company_id)
        for flight in flights:
            flight_dto = flight.get_dto()
            flight_dto_list.append(flight_dto)
        return flight_dto_list

        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function get_airline_flights but his role is '
                f'not Airline Company.')
            return
        return self.repo.get_by_condition(Flight, lambda query: query.filter(
            Flights.airline_company_id == self.login_token.id).all())

    def update_airline(self, airline):
        print_to_log(logger, logging.INFO, f'Updating airline {airline.id}...')

    def add_flight(self, flight):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but his role is not Airline Company.')
            return
        if not isinstance(flight, Flights):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the flight "{flight}" '
                f'that was sent is not a Flight object.')
            return
        if not self.repo.get_by_condition(Countries,
                                          lambda query: query.filter(Countries.id == flight.origin_country_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the origin_country_id "{flight.origin_country_id}"'
                f'that was sent not exists in the db.')
            return
        if not self.repo.get_by_condition(Countries, lambda query: query.filter(
                Countries.id == flight.destination_country_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the destination_country_id "{flight.destination_country_id}"'
                f'that was sent not exists in the db.')
            return
        if not isinstance(flight.departure_time, datetime) or not isinstance(flight.landing_time, datetime):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but both departure_time "{flight.departure_time}" '
                f'and landing_time "{flight.landing_time}" must be a Datetime objects.')
            return
        if flight.departure_time + datetime.timedelta(hours=1) > flight.landing_time:  # checking the delta t
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but '
                f'the time delta between departure_time "{flight.departure_time}" and landing time "{flight.landing_time}" '
                f'is less than one hour.')
            raise NotLegalFlightTimesError
        if not isinstance(flight.remaining_tickets, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the remaining_tickets'
                f' "{flight.remaining_tickets}" that was sent is not an integer.')
            return
        if flight.remaining_tickets < 100:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the remaining_tickets'
                f' "{flight.remaining_tickets}" that was sent must be more or equal than 100.')
            return
        flight.id = None
        flight.airline_company_id = self.login_token.id
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function add_flight and added the flight "{flight}" to the db.')
        self.repo.add(flight)
        return True

    def remove_flight(self, flight_id):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_flight but his role is '
                f'not Airline Company.')
            return
        if not isinstance(flight_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_flight but the flight_id "{flight_id}" '
                f'that was sent is not an integer.')
            return
        if flight_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_flight but the flight_id "{flight_id}" '
                f'that was sent is not positive.')
            return
        flight = self.repo.get_by_condition(Flights, lambda query: query.filter(Flight.id == flight_id).all())
        if not flight:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_flight but the flight_id "{flight_id}" '
                f'not exists in the db.')
            return
        if self.login_token.id != flight[0].airline_company_id:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_flight but the flight "{flight}" '
                f'not belongs to the login token airline company.')
            return
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function remove_flight and removed the flight "{flight}" '
            f'from the db.')
        self.repo.delete_by_id(Flights, Flights.id, flight_id)
        return True

    def update_airline(self, airline):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_airline but his role is '
                f'not Airline Company.')
            return
        if not isinstance(airline, Airline_Companies):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_airline but the airline "{airline}" '
                f'that was sent is not an Airline Company object.')
            return
        airline_ = self.repo.get_by_condition(Airline_Companies, lambda query: query.filter(
            Airline_Companies.id == self.login_token.id).all())
        if not airline_:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_airline but the airline "{airline}" '
                f'not exists in the db.')
            return
        if self.repo.get_by_condition(Airline_Companies,
                                      lambda query: query.filter(Airline_Companies.name == airline.name).all()) \
                and self.repo.get_by_condition(Airline_Companies, lambda query: query.filter(
            Airline_Companies.name == airline.name).all()) != airline_:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_airline but the airline.name "{airline.name}" '
                f'already exists in the db.')
            return
        if not self.repo.get_by_condition(Countries, lambda query: query.filter(Countries.id == airline.country_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_airline but the airline.country_id "{airline.country_id}" '
                f'not exists in the db.')
            return
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function update_airline and updated to airline "{airline}"')
        self.repo.update_by_id(Airline_Companies, Airline_Companies.id, self.login_token.id,
                               {Airline_Companies.name: airline.name,
                                Airline_Companies.country_id: airline.country_id})
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
