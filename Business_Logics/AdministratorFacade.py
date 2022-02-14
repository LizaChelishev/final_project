from sqlalchemy.testing.pickleable import User
from Business_Logics.FacadeBase import FacadeBase
import logging
from ApplicationLogger import print_to_log
from Database import Airline_Companies
from Database.Countries import Countries
from Database.Customers import Customers
from Database.Flights import Flights
from Database.Users import Users

logger = logging.getLogger(__name__)



class AdministratorFacade(FacadeBase):

    def __init__(self, login_token, repo):
        self.repo = repo
        super().__init__(self.repo)
        self._login_token = login_token

    def get_all_customers(self):
        print_to_log(logger, logging.INFO, 'Getting all customers...')
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function get_all_customers but his role is '
                f'not Administrator.')
            return
        return self.repo.get_all(Customers)

    def add_airline(self, airline):
        print_to_log(logger, logging.INFO, f'Adding airline {airline.id}...')
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but his role is '
                f'not Administrator.')
            return
        if not isinstance(user, User):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but user "{user}" '
                f'that was sent is not a User object.')
            return
        if user.user_role != 2:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but the user.user_role "{user.user_role}" '
                f'that was sent is not 2(Airline).')
            return
        if not isinstance(airline, Airline_Companies):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but airline "{airline}" '
                f'that was sent is not an Airline Company object.')
            return
        if self.repo.get_by_condition(Airline_Companies,
                                      lambda query: query.filter(Airline_Companies.name == airline.name).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but airline.name "{airline.name}" '
                f'that was sent already exists in the db.')
            return
        if not self.repo.get_by_condition(Countries,
                                          lambda query: query.filter(Countries.id == airline.country_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but airline.country_id "{airline.country_id}" '
                f'that was sent does not exist in the db.')
            return
        if self.create_user(user):
            airline.id = None
            airline.user_id = user.id
            self.logger.logger.debug(
                f'The login token "{self.login_token}" used the function add_airline and added airline "{airline}" '
                f'that connected to the user "{user}".')
            self.repo.add(airline)
            return True
        else:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but the user "{user}" '
                f'that was sent is not valid so the function failed.')
            return

    def add_customer(self, customer):
        print_to_log(logger, logging.INFO, f'Adding customer {customer.id}...')
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but his role is '
                f'not Administrator.')
        if not isinstance(user, User):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but user "{user}" '
                f'that was sent is not a User instance.')
            return
        if user.user_role != 1:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but the user.user_role "{user.user_role}" '
                f'that was sent is not 1(Customer).')
            return
        if not isinstance(customer, Customers):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but customer "{customer}" '
                f'that was sent is not a Customer object.')
            return
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(Customers.phone_no == customer.phone_no).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but customer.phone_no "{customer.phone_no}" '
                f'that was sent already exists in the db.')
            return
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(
                                          Customers.credit_card_no == customer.credit_card_no).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but customer.credit_card_no "{customer.credit_card_no}" '
                f'that was sent already exists in the db.')
            return
        if self.create_user(user):
            customer.id = None
            customer.user_id = user.id
            self.logger.logger.debug(
                f'The login token "{self.login_token}" used the function add_customer and added the customer "{customer}" '
                f'connected by the user "{user}".')
            self.repo.add(customer)
            return True
        else:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but the user "{user}" '
                f'that was sent is not valid so the function failed.')
            return

    def add_administrator(self, administrator):
        print_to_log(logger, logging.INFO, f'Adding administrator {administrator.id}...')

    def remove_airline(self, airline):
        print_to_log(logger, logging.INFO, f'Removing airline {airline.id}...')
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but his role is '
                f'not Administrator.')
            return
        if not isinstance(airline.id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline.id}" '
                f'that was sent is not an integer.')
            return
        if airline.id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline.id}" '
                f'that was sent is not an positive.')
            return
        airline = self.repo.get_by_condition(Airline_Companies,
                                             lambda query: query.filter(Airline_Companies.id == airline.id).all())
        if not airline:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline.id}" '
                f'that was sent does not exist in the db.')
            return
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function remove_airline and removed the airline "{airline}"')
        self.repo.delete_by_id(Users, User.id, airline[0].user.id)
        return True

    def remove_customer(self, customer):
        print_to_log(logger, logging.INFO, f'Removing customer {customer.id}...')
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but his role is '
                f'not Administrator.')
            return
        if not isinstance(customer_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                f'that was sent is not an integer.')
            return
        if customer_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                f'that was sent is not positive.')
            return
        customer = self.repo.get_by_condition(Customers,
                                              lambda query: query.filter(Customers.id == customer_id).all())
        if not customer:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                f'that was sent does not exist in the db.')
            return
        tickets = self.repo.get_by_condition(Tickets,
                                             lambda query: query.filter(Tickets.customer_id == customer_id).all())
        for ticket in tickets:
            self.repo.update_by_id(Flights, Flights.id, ticket.flight_id,
                                   {Flights.remaining_tickets: ticket.flight.remaining_tickets + 1})
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function remove_customer and removed the customer "{customer}"')
        self.repo.delete_by_id(User, User.id, customer[0].user.id)
        return True

    def remove_administrator(self, administrator):
        print_to_log(logger, logging.INFO, f'Removing administrator {administrator.id}...')