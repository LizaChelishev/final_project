from Business_Logics.AdministratorFacade import AdministratorFacade
from Business_Logics.AirlineFacade import AirlineFacade
from Business_Logics.AnonymousFacade import AnonymousFacade
from Business_Logics.CustomerFacade import CustomerFacade
import logging
from ApplicationLogger import print_to_log
from ApplicationLogger import init_logger

init_logger()

logger = logging.getLogger(__name__)

print_to_log(logger, logging.INFO, "Starting the app...")

print_to_log(logger, logging.DEBUG, "Creating customer facade...")
customer_facade = CustomerFacade()

print_to_log(logger, logging.DEBUG, "Creating administrator facade...")
administrator_facade = AdministratorFacade()

print_to_log(logger, logging.DEBUG, "Creating anonymous facade...")
anonymous_facade = AnonymousFacade()

print_to_log(logger, logging.DEBUG, "Creating airline facade...")
airline_facade = AirlineFacade()

flight_dto_list = airline_facade.get_flights_by_airline(1)
print(flight_dto_list)
#airline_facade.update_flight(flight_dto_list[0])