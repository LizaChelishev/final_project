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

logger = logging.getLogger(__name__)


class FacadeBase(ABC):
    repo = None

    @abstractmethod
    def init(self):
        print('init')
        if FacadeBase.repo is None:
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

    def get_all_flights(self):
        print_to_log(logger, logging.INFO, 'Getting all flights...')

    def get_flight_by_id(self, flight_id):
        print_to_log(logger, logging.INFO, f'Getting flight id {flight_id}...')
        flight_dbo = FacadeBase.repo.get_by_id(Flights, flight_id)
        flight_dto = flight_dbo.get_dto()
        return flight_dto

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        print_to_log(logger, logging.INFO, f'Getting flight with origin country id:{origin_country_id},'
                                           f' destinations country id:{destination_country_id}, date: {date}.')

    def get_all_airlines(self):
        print_to_log(logger, logging.INFO, 'Getting all airlines...')

    def get_airline_by_id(self, id):
        print_to_log(logger, logging.INFO, f'Getting flight id {id}...')

    def add_customer(self, customer):
        print_to_log(logger, logging.INFO, f'Adding customer {customer.id}')

    def add_airline(self, airline):
        print_to_log(logger, logging.INFO, f'Adding airline {airline.id}')

    def get_all_countries(self):
        print_to_log(logger, logging.INFO, 'Getting all countries...')

    def get_country_by_id(self, id):
        print_to_log(logger, logging.INFO, f'Getting country id {id}...')
