import datetime
from Business_Logics.FacadeBase import FacadeBase
from Database.Airline_Companies import *
from Database.Countries import Countries
from Database.Flights import *
from datetime import datetime, timedelta
from custom_errors.NotLegalFlightTimesError import NotLegalFlightTimesError
from custom_errors.NoRemainingTicketsError import NoRemainingTicketsError
from custom_errors.WrongLoginTokenError import WrongLoginTokenError
from custom_errors.NotValidDataError import NotValidDataError


class AirlineFacade(FacadeBase):

    def __init__(self, login_token, repo):
        self.repo = repo
        super().__init__(self.repo)
        self._login_token = login_token

    def get_airline_flights(self):  # returns all the flight for the login token airline
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function get_airline_flights but his role is '
                f'not Airline Company.')
            raise WrongLoginTokenError
        return self.repo.get_by_condition(Flights, lambda query: query.filter(
            Flights.airline_company_id == self.login_token.id).all())

    def add_flight(self, flight):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but his role is not Airline Company.')
            raise WrongLoginTokenError
        if not isinstance(flight, Flights):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the flight "{flight}" '
                f'that was sent is not a Flight object.')
            raise NotValidDataError
        if not self.repo.get_by_condition(Countries,
                                          lambda query: query.filter(Countries.id == flight.origin_country_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the origin_country_id "{flight.origin_country_id}"'
                f'that was sent not exists in the db.')
            raise NotValidDataError
        if not self.repo.get_by_condition(Countries, lambda query: query.filter(
                Countries.id == flight.destination_country_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the destination_country_id "{flight.destination_country_id}"'
                f'that was sent not exists in the db.')
            raise NotValidDataError
        if not isinstance(flight.departure_time, datetime) or not isinstance(flight.landing_time, datetime):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but both departure_time "{flight.departure_time}" '
                f'and landing_time "{flight.landing_time}" must be a Datetime objects.')
            raise NotValidDataError
        if flight.departure_time + timedelta(hours=1) > flight.landing_time:  # checking the delta t
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but '
                f'the time delta between departure_time "{flight.departure_time}" and landing time "{flight.landing_time}" '
                f'is less than one hour.')
            raise NotLegalFlightTimesError
        if not isinstance(flight.remaining_tickets, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the remaining_tickets'
                f' "{flight.remaining_tickets}" that was sent is not an integer.')
            raise NotValidDataError
        if flight.remaining_tickets < 100:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_flight but the remaining_tickets'
                f' "{flight.remaining_tickets}" that was sent must be more or equal than 100.')
            raise NotValidDataError
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
            raise WrongLoginTokenError
        if not isinstance(flight_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_flight but the flight_id "{flight_id}" '
                f'that was sent is not an integer.')
            raise NotValidDataError
        if flight_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_flight but the flight_id "{flight_id}" '
                f'that was sent is not positive.')
            raise NotValidDataError
        flight = self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.id == flight_id).all())
        if not flight:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_flight but the flight_id "{flight_id}" '
                f'not exists in the db.')
            raise NotValidDataError
        if self.login_token.id != flight[0].airline_company_id:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_flight but the flight "{flight}" '
                f'not belongs to the login token airline company.')
            raise WrongLoginTokenError
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
            raise WrongLoginTokenError
        if not isinstance(airline, Airline_Companies):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_airline but the airline "{airline}" '
                f'that was sent is not an Airline Company object.')
            raise NotValidDataError
        airline_ = self.repo.get_by_condition(Airline_Companies, lambda query: query.filter(
            Airline_Companies.id == self.login_token.id).all())
        if not airline_:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_airline but the airline "{airline}" '
                f'not exists in the db.')
            raise NotValidDataError
        if self.repo.get_by_condition(Airline_Companies,
                                      lambda query: query.filter(Airline_Companies.name == airline.name).all()) \
                and self.repo.get_by_condition(Airline_Companies, lambda query: query.filter(
            Airline_Companies.name == airline.name).all()) != airline_:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_airline but the airline.name "{airline.name}" '
                f'already exists in the db.')
            raise NotValidDataError
        if not self.repo.get_by_condition(Countries,
                                          lambda query: query.filter(Countries.id == airline.country_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_airline but the airline.country_id "{airline.country_id}" '
                f'not exists in the db.')
            raise NotValidDataError
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function update_airline and updated to airline "{airline}"')
        self.repo.update_by_id(Airline_Companies, Airline_Companies.id, self.login_token.id,
                               {Airline_Companies.name: airline.name,
                                Airline_Companies.country_id: airline.country_id})
        return True

    def update_flight(self, flight):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but his role is '
                f'not Airline Company.')
            raise WrongLoginTokenError
        if not isinstance(flight, Flights):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but the flight "{flight}" '
                f'that was sent is not a Flight object.')
            raise NotValidDataError
        if not isinstance(flight.id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but the flight.id "{flight.id}" '
                f'that was sent is not an integer.')
            raise NotValidDataError
        if flight.id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but the flight.id "{flight.id}" '
                f'that was sent is not positive.')
            raise NotValidDataError
        flight_ = self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.id == flight.id).all())
        if not flight_:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but the flight.id "{flight.id}" '
                f'that was sent does not exists in the db.')
            raise NotValidDataError
        if flight_[0].airline_company_id != self.login_token.id:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but the flight with the flight.id "{flight.id}" '
                f'that was sent does not belong to the login token Airline Company.')
            raise WrongLoginTokenError
        if not isinstance(flight.origin_country_id, int) or not isinstance(flight.destination_country_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but both origin_country_id "{flight.origin_country_id}" '
                f'and destination_country_id "{flight.destination_country_id}" that was sent must be integers.')
            raise NotValidDataError
        if flight.origin_country_id <= 0 or flight.destination_country_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but both '
                f'origin_country_id "{flight.origin_country_id}" '
                f'and destination_country_id "{flight.destination_country_id}" that was sent must be positive.')
            raise NotValidDataError
        if not self.repo.get_by_condition(Countries,
                                          lambda query: query.filter(Countries.id == flight.origin_country_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but the origin_country_id "{flight.origin_country_id}" '
                f'that was sent does not exists in the db.')
            raise NotValidDataError
        if not self.repo.get_by_condition(Countries, lambda query: query.filter(
                Countries.id == flight.destination_country_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but the destination_country_id "{flight.destination_country_id}" '
                f'that was sent does not exists in the db.')
            raise NotValidDataError
        if not isinstance(flight.departure_time, datetime) or not isinstance(flight.landing_time, datetime):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but both departure_time "{flight.departure_time}" '
                f'and landing_time "{flight.landing_time}" must be a Datetime objects.')
            raise NotValidDataError
        if flight.departure_time + timedelta(hours=1) > flight.landing_time:  # checking the delta t
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but '
                f'the time delta between departure_time "{flight.departure_time}" and landing time "{flight.landing_time}" '
                f'is less than one hour.')
            raise NotLegalFlightTimesError
        if not isinstance(flight.remaining_tickets, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but the remaining_tickets'
                f' "{flight.remaining_tickets}" that was sent is not an integer.')
            raise NotValidDataError
        if flight.remaining_tickets < 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function update_flight but the remaining_tickets'
                f' "{flight.remaining_tickets}" that was sent must be more or equal than 100.')
            raise NoRemainingTicketsError
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function update_flight and updated the flight "{flight_[0]}" '
            f'to the flight "{flight}".')
        self.repo.update_by_id(Flights, Flights.id, flight.id, {Flights.origin_country_id: flight.origin_country_id,
                                                                Flights.destination_country_id: flight.destination_country_id,
                                                                Flights.departure_time: flight.departure_time,
                                                                Flights.landing_time: flight.landing_time,
                                                                Flights.remaining_tickets: flight.remaining_tickets})
        return True
