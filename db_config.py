from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

connection_string = 'postgresql+psyopg2://postgres:liza1709liza@localhost/flights_project'

Base = declarative_base()

Engine = create_engine(connection_string, echo=True)

def create_all_entities():