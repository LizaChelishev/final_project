from Business_Logics.FacadeBase import FacadeBase
from DTO.FlightDto import FlightDto
from Exceptions.InvalidFlightException import InvalidFlightException
import logging
from ApplicationLogger import print_to_log
from Database.Flights import *

logger = logging.getLogger(__name__)


class AirlineFacade(FacadeBase):

    def get_flights_by_airline(self, airline_company_id):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')
        flight_dto_list = []
        flights = FacadeBase.repo.get_all_by_condition(Flights, Flights.airline_company_id, airline_company_id)
        for flight in flights:
            flight_dto = flight.get_dto()
            flight_dto_list.append(flight_dto)
        return flight_dto_list

    def update_airline(self, airline):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

    def update_flight(self, flight):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')
        if flight.get_remaining_tickets() < 0:
            print_to_log(logger, logging.ERROR, 'Invalid number of remaining tickets, cannot be negative.')
            raise InvalidFlightException(flight.get_airline_company_id(), flight.get_id())

        if flight.get_landing_time() <= flight.get_departure_time():
            print_to_log(logger, logging.ERROR, 'Invalid departure or landing time, '
                                                'make sure landing time is after departure time.')
            raise InvalidFlightException(flight.get_airline_company_id(), flight.get_id())

        if flight.get_origin_country_id() == flight.get_destination_country_id():
            print_to_log(logger, logging.ERROR, 'Destination country can not be the same as origin country.')
            raise InvalidFlightException(flight.get_airline_company_id(), flight.get_id())

        flight_dbo = FacadeBase.repo.get_by_id(Flights, flight.get_id())
        FacadeBase.repo.update(Flights, Flights.get_key(), flight.get_id(),
                               flight_dbo.get_dict(flight.get_airline_company_id(),
                                                   flight.get_origin_country_id(),
                                                   flight.get_destination_country_id(),
                                                   flight.get_departure_time(),
                                                   flight.get_landing_time(),
                                                   flight.get_remaining_tickets()))
