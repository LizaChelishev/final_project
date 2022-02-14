import datetime
from sqlalchemy import asc, extract, desc, text

from Database.Administrators import Administrators
from Database.Airline_Companies import Airline_Companies
from Database.Countries import Countries
from Database.Customers import Customers
from Database.Flights import Flights
from Database.Tickets import Tickets
from Database.User_Roles import User_Roles
from Database.Users import Users
from sqlalchemy.exc import OperationalError, IntegrityError


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session

    def reset_auto_inc(self, table_class):
        try:
            self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')
            self.local_session.commit()
            self.logger.logger.debug(f'Reset auto inc in {table_class} table')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_by_id(self, table_class, id):
        return self.local_session.query(table_class).get(id)

    def get_all(self, table_class):
        try:
            return self.local_session.query(table_class).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_all_limit(self, table_class, limit_num):
        try:
            return self.local_session.query(table_class).limit(limit_num).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_all_order_by(self, table_class, column_name, direction=asc):
        try:
            return self.local_session.query(table_class).order_by(direction(column_name)).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_by_column_value(self, table_class, column_value, value):
        try:
            return self.local_session.query(table_class).filter(column_value == value).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_by_condition(self, table_class, condition):  # condition is a lambda expression of a filter
        try:
            return condition(self.local_session.query(table_class))
        except OperationalError as e:
            self.logger.logger.critical(e)

    def add(self, one_row):
        try:
            self.local_session.add(one_row)
            self.local_session.commit()
            self.logger.logger.debug(f'{one_row} has been added to the db')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def add_all(self, rows_list):
        try:
            self.local_session.add_all(rows_list)
            self.local_session.commit()
            self.logger.logger.debug(f'{rows_list} have been added to the db')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def delete_by_id(self, table_class, id_column_name, id):
        try:
            self.local_session.query(table_class).filter(id_column_name == id).delete(synchronize_session=False)
            self.local_session.commit()
            self.logger.logger.debug(f'A row with the id {id} has been deleted from {table_class}')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def update_by_id(self, table_class, id_column_name, id,
                     data):  # data is a dictionary of all the new columns and values
        try:
            self.local_session.query(table_class).filter(id_column_name == id).update(data)
            self.local_session.commit()
            self.logger.logger.debug(
                f'A row with the id {id} has been updated from {table_class}. the updated data is  {data}.')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_airlines_by_country(self, country_id):
        try:
            return self.local_session.query(Airline_Companies).filter(Airline_Companies.country_id == country_id).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_flights_by_destination_country_id(self, country_id):
        try:
            return self.local_session.query(Flights).filter(Flights.destination_country_id == country_id).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_flights_by_origin_country_id(self, country_id):
        try:
            return self.local_session.query(Flights).filter(Flights.origin_country_id == country_id).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_flights_by_departure_date(self, departure_date):
        try:
            return self.local_session.query(Flights).filter(
                extract('year', Flights.departure_date) == departure_date.year,
                extract('month', Flights.departure_date) == departure_date.month,
                extract('day', Flights.departure_date) == departure_date.day).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_flights_by_landing_date(self, landing_date):
        try:
            return self.local_session.query(Flights).filter(
                extract('year', Flights.departure_date) == landing_date.year,
                extract('month',
                        Flights.departure_date) == landing_date.month,
                extract('day',
                        Flights.departure_date) == landing_date.day).all()
        except OperationalError as e:
            self.logger.logger.critical(e)

    def get_flights_by_customer(self, customer_id):
        try:
            flights_ls = []
            tickets = self.local_session.query(Tickets).filter(Tickets.customer_id == customer_id).all()
            for ticket in tickets:
                flights_ls.append(ticket.flight)
            return flights_ls
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_airline_by_username(self, _username):
        try:
            stmt = text('select * from sp_get_airline_by_username(:username)').bindparams(username=_username)
            airline_cursor = self.local_session.execute(stmt)
            airline = [air1 for air1 in airline_cursor][0]
            return airline
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_customer_by_username(self, _username):
        try:
            stmt = text('select * from sp_get_customer_by_username(:username)').bindparams(username=_username)
            customer_cursor = self.local_session.execute(stmt)
            customer = [cus1 for cus1 in customer_cursor][0]
            return customer
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_user_by_username(self, _username):
        try:
            stmt = text('select * from sp_get_user_by_username(:username)').bindparams(username=_username)
            user_cursor = self.local_session.execute(stmt)
            user = [us1 for us1 in user_cursor][0]
            return user
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_flights_by_airline_id(self, _airline_id):
        try:
            stmt = text('select * from sp_get_flights_by_airline_id(:airline_id)').bindparams(airline_id=_airline_id)
            flights_cursor = self.local_session.execute(stmt)
            flights = [flight for flight in flights_cursor]
            return flights
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_tickets_by_customer_id(self, _customer_id):
        try:
            stmt = text('select * from sp_get_tickets_by_customer_id(:customer_id)').bindparams(
                customer_id=_customer_id)
            tickets_cursor = self.local_session.execute(stmt)
            tickets = [ticket for ticket in tickets_cursor]
            return tickets
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_arrival_flights(self,
                               _country_id):  # returns all the flights that arrive to the country_id in the next 12 hours
        try:
            stmt = text('select * from sp_get_arrival_flights(:country_id)').bindparams(country_id=_country_id)
            flights_cursor = self.local_session.execute(stmt)
            flights = [flight for flight in flights_cursor]
            return flights
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_departure_flights(self,
                                 _country_id):  # returns all the flights that departure to the country_id in the next 12 hours
        try:
            stmt = text('select * from sp_get_departure_flights(:country_id)').bindparams(country_id=_country_id)
            flights_cursor = self.local_session.execute(stmt)
            flights = [flight for flight in flights_cursor]
            return flights
        except OperationalError as e:
            self.logger.logger.critical(e)

    def sp_get_flights_by_parameters(self, _origin_country_id, _destination_country_id, _date):
        try:
            stmt = text(
                'select * from sp_get_flights_by_parameters(:origin_country_id, :destination_country_id, :date)') \
                .bindparams(origin_country_id=_origin_country_id, destination_country_id=_destination_country_id,
                            date=_date)
            flights_cursor = self.local_session.execute(stmt)
            flights = [flight for flight in flights_cursor]
            return flights
        except OperationalError as e:
            self.logger.logger.critical(e)

    def create_all_sp(self, file):
        try:
            try:
                with open(file, 'r') as sp_file:
                    queries = sp_file.read().split('|||')
                for query in queries:
                    self.local_session.execute(query)
                self.local_session.commit()
                self.logger.logger.debug(f'all sp from {file} were created.')
            except FileNotFoundError:
                self.logger.logger.critical(f'Tried to create all sp from the the file "{file}" but file was not found')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def drop_all_tables(self):
        try:
            self.local_session.execute('DROP TABLE users CASCADE')
            self.local_session.execute('DROP TABLE user_roles CASCADE')
            self.local_session.execute('DROP TABLE tickets CASCADE')
            self.local_session.execute('DROP TABLE flights CASCADE')
            self.local_session.execute('DROP TABLE customers CASCADE')
            self.local_session.execute('DROP TABLE countries CASCADE')
            self.local_session.execute('DROP TABLE airline_companies CASCADE')
            self.local_session.execute('DROP TABLE administrators CASCADE')
            self.local_session.commit()
            self.logger.logger.debug(f'All tables Dropped.')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def reset_test_db(self):
        try:
            # resetting auto increment for all tables
            self.reset_auto_inc(Countries)
            self.reset_auto_inc(User_Roles)
            self.reset_auto_inc(Users)
            self.reset_auto_inc(Administrators)
            self.reset_auto_inc(Airline_Companies)
            self.reset_auto_inc(Customers)
            self.reset_auto_inc(Flights)
            self.reset_auto_inc(Tickets)
            # county
            israel = Countries(name='Israel')
            self.add(israel)
            self.add(Countries(name='Germany'))
            # user role
            self.add(User_Roles(role_name='Customer'))
            self.add(User_Roles(role_name='Airline Company'))
            self.add(User_Roles(role_name='Administrator'))
            self.add(User_Roles(role_name='Not Legal'))
            # user
            self.add(Users(username='Elad', password='123', email='elad@gmail.com', user_role=1))
            self.add(Users(username='Uri', password='123', email='uri@gmail.com', user_role=1))
            self.add(Users(username='Yoni', password='123', email='yoni@gmail.com', user_role=2))
            self.add(Users(username='Yishay', password='123', email='yishay@gmail.com', user_role=2))
            self.add(Users(username='Tomer', password='123', email='tomer@gmail.com', user_role=3))
            self.add(Users(username='Boris', password='123', email='boris@gmail.com', user_role=3))
            self.add(Users(username='not legal', password='123', email='notlegal@gmail.com', user_role=4))
            # administrator
            self.add(Administrators(first_name='Tomer', last_name='Tome', user_id=5))
            self.add(Administrators(first_name='Boris', last_name='Bori', user_id=6))
            # airline company
            self.add(Airline_Companies(name='Yoni', country_id=1, user_id=3))
            self.add(Airline_Companies(name='Yishay', country_id=2, user_id=4))
            # customer
            self.add(Customers(first_name='Elad', last_name='Gunders', address='Sokolov 11',
                               phone_no='0545557007', credit_card_no='0000', user_id=1))
            self.add(Customers(first_name='Uri', last_name='Goldshmid', address='Helsinki 16',
                               phone_no='0527588331', credit_card_no='0001', user_id=2))
            # flight
            self.add(Flights(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                             departure_time=datetime(2022, 1, 30, 16, 0, 0),
                             landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200))
            self.add(Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2,
                             departure_time=datetime(2022, 1, 30, 16, 0, 0),
                             landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=0))
            # ticket
            self.add(Tickets(flight_id=1, customer_id=1))
            self.add(Tickets(flight_id=2, customer_id=2))
            self.logger.logger.debug(f'Reset flights_db_tests')
        except OperationalError as e:
            self.logger.logger.critical(e)

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

    def update(self, table_class, id_column_name, id, data_dict):
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
