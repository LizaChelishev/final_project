from db_config import create_all_entities
from db_repo import DbRepo
from Database.Airline_Companies import Airline_Companies
from Database.Flights import Flights
from Database.Tickets import Tickets
from Database.Countries import Countries
from Database.Customers import Customers
from Database.Users import Users
from Database.User_Roles import User_Roles
from Database.Administrators import Administrators
import logging
from ApplicationLogger import print_to_log
from abc import ABC, abstractmethod
from LoginToken import LoginToken

logger = logging.getLogger(__name__)


class FacadeBase(ABC):
    repo = None

    @abstractmethod
    def init(self):
#        print('init')
#       if FacadeBase.repo is None:
            print('creating DB repo')
            local_session = create_all_entities()
            FacadeBase.repo = DbRepo(local_session)

            FacadeBase.repo.reset_auto_inc(Airline_Companies)
            FacadeBase.repo.reset_auto_inc(Flights)
            FacadeBase.repo.reset_auto_inc(Tickets)
            FacadeBase.repo.reset_auto_inc(Countries)
            FacadeBase.repo.reset_auto_inc(Customers)
            FacadeBase.repo.reset_auto_inc(Users)
            FacadeBase.repo.reset_auto_inc(User_Roles)
            FacadeBase.repo.reset_auto_inc(Administrators)

            user_roles_list = [User_Roles(role_name='Customer'), User_Roles(role_name='Airline_Company'),
                               User_Roles(role_name='Administrator')]
            FacadeBase.repo.add_all(user_roles_list)
            FacadeBase.init_sample_data()

    def __init__(self):
        FacadeBase.init()

    @staticmethod
    def init_sample_data():
        countries_list = [Countries(name='France'), Countries(name='Israel'),
                          Countries(name='United Kingdom')]
        FacadeBase.repo.add_all(countries_list)

        airlines_list = [Airline_Companies(name='Air France', country_id=1),
                         Airline_Companies(name='El Al', country_id=2),
                         Airline_Companies(name='British Airways', country_id=3)]
        FacadeBase.repo.add_all(airlines_list)

        flights_list = [Flights(airline_company_id=1,
                                origin_country_id=1,
                                destination_country_id=2,
                                departure_time='2022-01-08 04:05:06',
                                landing_time='2022-01-08 08:00:00',
                                remaining_tickets=10)]
        FacadeBase.repo.add_all(flights_list)

    @property
    def login_token(self):
        return self._login_token

    def get_all_flights(self):
        print_to_log(logger, logging.INFO, 'Getting all flights...')
        return self.repo.get_all(Flights)

    def get_flight_by_id(self, flight_id):
        if not isinstance(id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_id '
                f'but the id "{id}" that was sent is not an integer.')
            return
        if id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_id but the id "{id}" that was '
                f'sent is not positive.')
            return self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.id == id).all())

        else:
            print_to_log(logger, logging.INFO, f'Getting flight id {flight_id}...')
            flight_dbo = FacadeBase.repo.get_by_id(Flights, flight_id)
            flight_dto = flight_dbo.get_dto()
            return flight_dto

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        print_to_log(logger, logging.INFO, f'Getting flight with origin country id:{origin_country_id},'
                                           f' destinations country id:{destination_country_id}, date: {date}.')
        if not isinstance(origin_country_id, int) or not isinstance(destination_country_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_parameters but the county ids '
                f'"{origin_country_id}" and "{destination_country_id}" '
                f'that was sent must be integers')
            return
        if origin_country_id <= 0 or destination_country_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_flights_by_parameters but the county ids '
                f'"{origin_country_id}" and "{destination_country_id}" '
                f'that was sent must be positive')
            return
        if not isinstance(date, datetime):
            self.logger.logger.error(
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
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_airline_by_id but the id "{id}" '
                f'that was sent is not an integer.')
            return
        if id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_airline_by_id but the id "{id}" '
                f'that was sent is not positive.')
            return
        return self.repo.get_by_condition(Airline_Companies, lambda query: query.filter(Airline_Companies.id == id_).all())

    def create_user(self, user):
        if not isinstance(user, Users):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function create_user but the user "{user}" '
                f'that was sent must be instance if the class User.')
            return
        if self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == user.username).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function create_user but the user.username '
                f'"{user.username}" that was sent already exists in the db.')
            return
        if self.repo.get_by_condition(Users, lambda query: query.filter(Users.email == user.email).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function create_user but the user.email "{user.email}" '
                f'that was sent already exists in the db.')
            return
        if not self.repo.get_by_condition(User_Roles, lambda query: query.filter(User_Roles.id == user.user_role).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function create_user but the user.user_role '
                f'"{user.user_role}" that was sent does not exist in the db.')
            return
        user.id = None
        self.logger.logger.debug(f'The login token "{self.login_token}" used the function create_user and new user '
                                 f'"{user}" has ben added to the db.')
        self.repo.add(user)
        return True

    def get_airline_by_parameter(self, name, country_id, user_id):
        print_to_log(logger, logging.INFO, f'Getting airline company with name {name}...')

    def add_customer(self, customer):
        print_to_log(logger, logging.INFO, f'Adding customer {customer.id}')

    def add_airline(self, airline):
        print_to_log(logger, logging.INFO, f'Adding airline {airline.id}')

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
        if id_ <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" used the function get_country_by_id but the id "{id}" that was '
                f'sent is not positive.')
            return
        return self.repo.get_by_condition(Countries, lambda query: query.filter(Countries.id == id).all())
