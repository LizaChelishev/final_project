import datetime

from sqlalchemy import asc

from Database.Flights import Flights
from Database.Tickets import Tickets
from Database.Users import Users


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session

    def reset_auto_inc(self, table_class):
        self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')

    def get_by_id(self, table_class, id):
        return self.local_session.query(table_class).get(id)

    def get_all(self, table_class):
        return self.local_session.query(table_class).all()

    def get_all_by_condition(self, table_class, filter_column, filter_value):
        return self.local_session.query(table_class).filter(filter_column == filter_value)

    def get_all_limit(self, table_class, limit_num):
        return self.local_session.query(table_class).limit(limit_num).all()

    def get_all_order_by(self, table_class, column_name, direction=asc):
        return self.local_session.query(table_class).order_by(direction(column_name)).all()

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()

    def add(self, table_class, object):
        self.local_session.add(table_class, object)
        self.local_session.commit()

    def update(self, table_class, id_column_name,  id, data_dict):
        self.local_session.query(table_class).filter(id_column_name == id).update(data_dict)
        self.local_session.commit()

    def remove(self, table_class, id):
        self.local_session.remove(table_class, id)
        self.local_session.commit()

    def get_airline_by_username(self, username):
        return self.local_session.execute(
            f'SELECT NAME FROM AIRLINE_COMPANIES, USERS WHERE USERNAME=={username}'
            f' AND AIRLINE_COMPANIES.USER_ID=USERS.ID')

    def get_customer_by_username(self, username):
        return self.local_session.execute(
            f'SELECT NAME FROM CUSTOMERS, USERS WHERE USERNAME=={username} AND CUSTOMER.USER_ID=USERS.ID')

    def get_user_by_username(self, username):
        return self.local_session.query(Users).get(username)

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, flight_date):
        return self.local_session.query(Flights).get(origin_country_id, destination_country_id,
                                                     flight_date)

    def get_flights_by_airline_id(self, airline_id):
        return self.local_session.query(Flights).get(airline_id)

    def get_arrival_flights(self, country_id):
        return self.local_session.query(Flights).filter(country_id in range(datetime.datetime.now(),
                                                                              datetime.timedelta(hours=12))).all()

    def get_departure_flights(self, country_id):
        return self.local_session.query(Flights).filter(country_id in range(datetime.datetime.now(),
                                                                            datetime.timedelta(hours=12))).all()

    def get_tickets_by_customer(self, customer_id):
        return self.local_session.query(Tickets).filter(customer_id).all()

    def getAirlinesByCountry(self, country_id):
        pass

    def getFlightsByOriginCountryId(self, country_id):
        pass

    def getFlightsByDestinationCountryId(self, country_id):
        pass

    def getFlightsByDepartureDate(self, departure_date):
        pass

    def getFlightsByLandingDate(self, landing_date):
        pass

    def getFlightsByCustomer(self, customer):
        pass

