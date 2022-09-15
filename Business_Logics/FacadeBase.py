from datetime import datetime
from sqlalchemy import extract
from Database.Airline_Companies import Airline_Companies
from Database.Flights import Flights
from Database.Countries import Countries
from Database.Users import Users
from Database.User_Roles import User_Roles
from ApplicationLogger import Logger
from abc import ABC, abstractmethod
from Login_Token.LoginToken import LoginToken
from abc import ABC, abstractmethod
from datetime import datetime
from werkzeug.security import generate_password_hash

from custom_errors.NotValidDataError import NotValidDataError


class FacadeBase(ABC):

    @abstractmethod
    def __init__(self, repo, login_token=LoginToken(id_=None, name='Anonymous', role='Anonymous')):
        self.logger = Logger.get_instance()
        self.repo = repo
        self._login_token = login_token

    @property
    def login_token(self):
        return self._login_token

    def get_all_flights(self):
        return self.repo.get_all(Flights)

    def get_arrival_flights_by_delta_t(self, hours_num):
        if not isinstance(hours_num, int):
            raise NotValidDataError
        return self.repo.get_arrival_flights_by_delta_t(hours_num)

    def get_departure_flights_by_delta_t(self, hours_num):
        if not isinstance(hours_num, int):
            raise NotValidDataError
        return self.repo.get_departure_flights_by_delta_t(hours_num)

    def get_flight_by_id(self, id_):
        if not isinstance(id_, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_id '
                f'but the id "{id_}" that was sent is not an integer.')
            raise NotValidDataError
        if id_ <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_id but the id "{id_}" that was '
                f'sent is not positive.')
            raise NotValidDataError
        return self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.id == id_).all())

    def get_flights_by_airline_id(self, airline_id):
        if not isinstance(airline_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_airline_id but the airline_id '
                f'"{airline_id}" that was sent is not an integer.')
            raise NotValidDataError
        if airline_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_airline_id but the airline_id '
                f'"{airline_id}" that was sent is not positive.')
            raise NotValidDataError
        air_line_ = self.repo.get_by_condition(Airline_Companies, lambda query: query.filter(Airline_Companies.id == airline_id).all())
        if not air_line_:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_airline_id but the airline_id '
                f'"{airline_id}" that was sent is not exists in the db.')
            raise NotValidDataError
        return self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.airline_company_id == airline_id).all())

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        if not isinstance(origin_country_id, int) or not isinstance(destination_country_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_parameters but the county ids '
                f'"{origin_country_id}" and "{destination_country_id}" '
                f'that was sent must be integers')
            raise NotValidDataError
        if origin_country_id <= 0 or destination_country_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_parameters but the county ids '
                f'"{origin_country_id}" and "{destination_country_id}" '
                f'that was sent must be positive')
            raise NotValidDataError
        if not isinstance(date, datetime):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_parameters but the the date '
                f'"{date}" that was sent must be a Datetime object')
            raise NotValidDataError
        return self.repo.get_by_condition(Flights,
                                          lambda query: query.filter(Flights.origin_country_id == origin_country_id,
                                                                     Flights.destination_country_id == destination_country_id,
                                                                     extract('year', Flights.departure_time) == date.year,
                                                                     extract('month', Flights.departure_time) == date.month,
                                                                     extract('day', Flights.departure_time) == date.day).all())

    def get_all_airlines(self):
        return self.repo.get_all(Airline_Companies)

    def get_airline_by_id(self, id_):
        if not isinstance(id_, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_airline_by_id but the id "{id_}" '
                f'that was sent is not an integer.')
            raise NotValidDataError
        if id_ <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_airline_by_id but the id "{id_}" '
                f'that was sent is not positive.')
            raise NotValidDataError
        return self.repo.get_by_condition(Airline_Companies, lambda query: query.filter(Airline_Companies.id == id_).all())

    def create_user(self, user):
        if not isinstance(user, Users):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function create_user but the user "{user}" '
                f'that was sent must be instance if the class User.')
            raise NotValidDataError
        if self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == user.username).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function create_user but the user.username '
                f'"{user.username}" that was sent already exists in the db.')
            raise NotValidDataError
        if self.repo.get_by_condition(Users, lambda query: query.filter(Users.email == user.email).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function create_user but the user.email "{user.email}" '
                f'that was sent already exists in the db.')
            raise NotValidDataError
        if not self.repo.get_by_condition(User_Roles, lambda query: query.filter(User_Roles.id == user.user_role).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function create_user but the user.user_role '
                f'"{user.user_role}" that was sent does not exist in the db.')
            raise NotValidDataError
        user.password = generate_password_hash(user.password, method='sha256')
        user.id = None
        self.logger.logger.debug(f'The login token "{self.login_token}" used the function create_user and new user '
                                 f'"{user}" has ben added to the db.')
        self.repo.add(user)
        return True

    def get_all_countries(self):
        return self.repo.get_all(Countries)

    def get_country_by_id(self, id_):
        if not isinstance(id_, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_country_by_id but the id "{id_}" that was '
                f'sent is not an integer.')
            raise NotValidDataError
        if id_ <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_country_by_id but the id "{id_}" that was '
                f'sent is not positive.')
            raise NotValidDataError
        return self.repo.get_by_condition(Countries, lambda query: query.filter(Countries.id == id_).all())
