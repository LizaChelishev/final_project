from sqlalchemy.exc import OperationalError
from ApplicationLogger import Logger
from sqlalchemy import create_engine
import configparser
from sqlalchemy.orm import declarative_base, sessionmaker

logger = Logger.get_instance()
Base = declarative_base()

config = configparser.ConfigParser()
config.read("config.conf")

connection_string = 'postgresql+psycopg2://postgres:LooLi1709@localhost/Flights_Project'
#engine = create_engine(connection_string, echo=True)
engine = create_engine('postgresql+psycopg2://postgres:LooLi1709@localhost/Flights_Project')


def create_all_entities():
    try:
        Base.metadata.create_all(engine)
        logger.logger.debug('Created all sql tables.')
    except OperationalError:
        print('The database does not exist, please check the connection string')
        logger.logger.critical('The database does not exist, please check the connection string')


Session = sessionmaker()
local_session = Session(bind=engine)
