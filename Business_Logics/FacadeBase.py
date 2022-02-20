from datetime import datetime
from sqlalchemy import extract
from Database.Airline_Companies import Airline_Companies
from Database.Flights import Flights
from Database.Countries import Countries
from Database.Users import Users
from Database.User_Roles import User_Roles
import logging
from ApplicationLogger import print_to_log
from abc import ABC, abstractmethod
from Login_Token import LoginToken

logger = logging.getLogger(__name__)


class FacadeBase(ABC):
    repo = None

    @abstractmethod
    def __init__(self, repo, login_token=LoginToken):
        self.logger = logging.Logger.get_instance()
        self.repo = repo
        self._login_token = login_token

    @property
    def login_token(self):
        return self._login_token

    def get_all_flights(self):
        print_to_log(logger, logging.INFO, 'Getting all flights...')
        return self.repo.get_all(Flights)

    def get_flight_by_id(self, flight_id):
        if not isinstance(id, int):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function get_flights_by_id '
                         f'but the id "{id}" that was sent is not an integer.')
            return
        if id <= 0:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function get_flights_by_id but the id "{id}" that was '
                         f'sent is not positive.')
            return self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.id == id).all())

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        print_to_log(logger, logging.INFO, f'Getting flight with origin country id:{origin_country_id},'
                                           f' destinations country id:{destination_country_id}, date: {date}.')
        if not isinstance(origin_country_id, int) or not isinstance(destination_country_id, int):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function get_flights_by_parameters but the county ids '
                         f'"{origin_country_id}" and "{destination_country_id}" '
                         f'that was sent must be integers')
            return
        if origin_country_id <= 0 or destination_country_id <= 0:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function get_flights_by_parameters but the county ids '
                         f'"{origin_country_id}" and "{destination_country_id}" '
                         f'that was sent must be positive')
            return
        if not isinstance(date, datetime):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function get_flights_by_parameters but the the date '
                         f'"{date}" that was sent must be a Datetime object')
            return
        return self.repo.get_by_condition(Flights,
                                          lambda query: query.filter(Flights.origin_country_id == origin_country_id,
                                                                     Flights.destination_country_id == destination_country_id,
                                                                     extract('year',
                                                                             Flights.departure_time) == date.year,
                                                                     extract('month',
                                                                             Flights.departure_time) == date.month,
                                                                     extract('day',
                                                                             Flights.departure_time) == date.day).all())

    def get_all_airlines(self):
        print_to_log(logger, logging.INFO, 'Getting all airlines...')
        return self.repo.get_all(Airline_Companies)

    def get_airline_by_id(self, id):
        print_to_log(logger, logging.INFO, f'Getting flight id {id}...')
        if not isinstance(id, int):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function get_airline_by_id but the id "{id}" '
                         f'that was sent is not an integer.')
            return
        if id <= 0:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function get_airline_by_id but the id "{id}" '
                         f'that was sent is not positive.')
            return
        return self.repo.get_by_condition(Airline_Companies,
                                          lambda query: query.filter(Airline_Companies.id == id).all())

    def get_airline_by_parameter(self, name, country_id, user_id):
        print_to_log(logger, logging.INFO, f'Getting airline company with name {name}...')

    def get_all_countries(self):
        print_to_log(logger, logging.INFO, 'Getting all countries...')
        return self.repo.get_all(Countries)

    def get_country_by_id(self, id):
        print_to_log(logger, logging.INFO, f'Getting country id {id}...')
        if not isinstance(id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_country_by_id but the id "{id}" that was '
                f'sent is not an integer.')
            return
        if id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_country_by_id but the id "{id}" that was '
                f'sent is not positive.')
            return
        return self.repo.get_by_condition(Countries, lambda query: query.filter(Countries.id == id).all())

    def create_user(self, user):
        if not isinstance(user, Users):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function create_user but the user "{user}" '
                         f'that was sent must be instance if the class User.')
            return
        if self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == user.username).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function create_user but the user.username '
                         f'"{user.username}" that was sent already exists in the db.')
            return
        if self.repo.get_by_condition(Users, lambda query: query.filter(Users.email == user.email).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function create_user but the user.email "{user.email}" '
                         f'that was sent already exists in the db.')
            return
        if not self.repo.get_by_condition(User_Roles,
                                          lambda query: query.filter(User_Roles.id == user.user_role).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function create_user but the user.user_role '
                         f'"{user.user_role}" that was sent does not exist in the db.')
            return
        user.id = None
        print_to_log(logger, logging.DEBUG,
                     (f'The login token "{self.login_token}" used the function create_user and new user '
                      f'"{user}" has ben added to the db.'))
        self.repo.add(user)
        return True
