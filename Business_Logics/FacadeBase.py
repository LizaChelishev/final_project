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



class FacadeBase:
    repo = None

    @staticmethod
    def init():
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

        airlines_list = [Airline_Companies(name='Air France', country_id=1), Airline_Companies(name='El Al', country_id=2),
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
        pass

    def get_flight_by_id(self, id):
        pass

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        pass

    def get_all_airlines(self):
        pass

    def get_airline_by_id(self, id):
        pass

    def add_customer(self, customer):
        pass

    def add_airline(self, airline):
        pass

    def get_all_countries(self):
        pass

    def get_country_by_id(self, id):
        pass
