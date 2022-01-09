from db_config import create_all_entities
from db_repo import DbRepo
from Airline_Companies import Airline_Companies
from Flights import Flights
from Tickets import Tickets
from Countries import Countries
from Customers import Customers
from Users import Users
from User_Roles import User_Roles
from Administrators import Administrators


class Flights_Management:
    def __init__(self):
        local_session = create_all_entities()
        repo = DbRepo(local_session)

        repo.reset_auto_inc(Airline_Companies)
        repo.reset_auto_inc(Flights)
        repo.reset_auto_inc(Tickets)
        repo.reset_auto_inc(Countries)
        repo.reset_auto_inc(Customers)
        repo.reset_auto_inc(Users)
        repo.reset_auto_inc(User_Roles)
        repo.reset_auto_inc(Administrators)

        user_roles_list = [User_Roles(role_name='Customer'), User_Roles(role_name='Airline_Company'),
                           User_Roles(role_name='Administrator')]
        repo.add_all(user_roles_list)