from db_config import local_session, create_all_entities
from Database.Flights import Flights
from Database.Countries import Countries
from Database.Tickets import Tickets
from Database.Airline_Companies import Airline_Companies
from Database.Customers import Customers
from Database.Users import Users
from Database.User_Roles import User_Roles
from Database.Administrators import Administrators
from Business_Logics.AnonymousFacade import AnonymousFacade
from db_repo import *


repo = DbRepo(local_session)
create_all_entities()  # create tables if not exist
repo.create_all_sp('sp_flights_db.sql')