import sys

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

sys.exit(0)


def get_flights_by_airline(self, airline_company_id):
    print_to_log(logger, logging.INFO, f'Getting flights of airline: {airline_company_id}...')
    flight_dto_list = []
    flights = FacadeBase.repo.get_all_by_condition(Flights, Flights.airline_company_id, airline_company_id)
    for flight in flights:
        flight_dto = flight.get_dto()
        flight_dto_list.append(flight_dto)
    return flight_dto_list

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

else:
print_to_log(logger, logging.INFO, f'Getting flight id {flight_id}...')
flight_dbo = FacadeBase.repo.get_by_id(Flights, flight_id)
flight_dto = flight_dbo.get_dto()
return flight_dto