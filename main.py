from datetime import datetime
from Airline_Companies import Airline_companies
from db_config import local_session, create_all_entities

create_all_entities()
repo = Airline_companies_Repository(local_session)

all_airline_companies = repo.get_all()
print(all_airline_companies)