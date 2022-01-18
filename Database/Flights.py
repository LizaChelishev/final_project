from sqlalchemy.orm import relationship, backref

from DTO.FlightDto import FlightDto
from db_config import Base
from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey


class Flights(Base):
    __tablename__ = 'flights'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger(), ForeignKey('airline_companies.id'))
    origin_country_id = Column(Integer(), ForeignKey('countries.id'))
    destination_country_id = Column(Integer(), ForeignKey('countries.id'))
    departure_time = Column(DateTime())
    landing_time = Column(DateTime())
    remaining_tickets = Column(Integer())

    tickets = relationship("Tickets", backref=backref("flights", uselist=True))
    destination_countries = relationship("Countries", foreign_keys=[destination_country_id])
    origin_countries = relationship("Countries", foreign_keys=[origin_country_id])

    def __str__(self):
        return f'<Flight> id:{self.id} airline_company_id:{self.airline_company_id}' \
               f' origin_country_id:{self.origin_country_id} destination_country_id:{self.destination_country_id}\n'

    def __repr__(self):
        return f'<Flight> id:{self.id} airline_company_id:{self.airline_company_id}' \
               f' origin_country_id:{self.origin_country_id} destination_country_id:{self.destination_country_id}\n'

    def get_dict(self, airline_company_id, origin_country_id, destination_country_id, departure_time
                 , landing_time, remaining_tickets):
        flight_dict = {self.airline_company_id: airline_company_id,
                       self.origin_country_id: origin_country_id,
                       self.destination_country_id: destination_country_id,
                       self.departure_time: departure_time,
                       self.landing_time: landing_time,
                       self.remaining_tickets: remaining_tickets}
        return flight_dict

    def get_key(self):
        return self.id

    def get_dto(self):
        flight_dto = FlightDto()
        flight_dto.set_id(self.id)
        flight_dto.set_airline_company_id(self.airline_company_id)
        flight_dto.set_origin_country_id(self.origin_country_id)
        flight_dto.set_destination_country_id(self.destination_country_id)
        flight_dto.set_departure_time(self.departure_time)
        flight_dto.set_landing_time(self.landing_time)
        flight_dto.set_remaining_tickets(self.remaining_tickets)
        return flight_dto
