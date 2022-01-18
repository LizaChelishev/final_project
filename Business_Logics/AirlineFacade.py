from Business_Logics.FacadeBase import FacadeBase
from DTO.FlightDto import FlightDto
from Exceptions.InvalidFlightException import InvalidFlightException
import logging
from ApplicationLogger import print_to_log
from Database.Flights import *

logger = logging.getLogger(__name__)


class AirlineFacade(FacadeBase):

    def get_flights_by_airline(self, airline_company_id):
        flight_dto_list = []
        flights = FacadeBase.repo.get_all_by_filter(Flights, Flights.airline_company_id, airline_company_id)
        return flight_dto_list

    def update_airline(self, airline):
        pass

    def update_flight(self, flight):
        if flight.get_remaining_tickets() < 0:
            print_to_log(logger, logging.ERROR, 'Invalid number of remaining tickets, cannot be negative.')
            raise InvalidFlightException(flight.get_airline_company_id(), flight.get_id())

        if flight.landing_time() <= flight.departure_time():
            print_to_log(logger, logging.ERROR, 'Invalid departure or landing time, '
                                                'make sure landing time is after departure time.')
            raise InvalidFlightException(flight.get_airline_company_id(), flight.get_id())

        if flight.origin_country_id() == flight.destination_country_id():
            print_to_log(logger, logging.ERROR, 'Destination country can not be the same as origin country.')
            raise InvalidFlightException(flight.get_airline_company_id(), flight.get_id())

        flight_dbo = Flights()
        FacadeBase.repo.update(Flights, flight_dbo.get_key(), flight.get_id(),
                               flight_dbo.get_dict(flight.get_airline_company_id(),
                                                   flight.get_origin_country_id(),
                                                   flight.get_destination_country_id(),
                                                   flight.get_departure_time(),
                                                   flight.get_landing_time(),
                                                   flight.get_remaining_tickets()))
