from Business_Logics.FacadeBase import *
from Business_Logics.FacadeBase import FacadeBase
from Database import Airline_Companies, Tickets
from Database.Administrators import Administrators
from Database.Countries import Countries
from Database.Customers import Customers
from Database.Flights import Flights
from Database.Users import Users
from ApplicationLogger import *

logger = logging.getLogger(__name__)


class AdministratorFacade(FacadeBase):

    def __init__(self, login_token, repo):
        self.repo = repo
        super().__init__(self.repo)
        self._login_token = login_token

    def get_all_customers(self):
        if self.login_token.role != 'administrators':
            print_to_log(logger, logging.ERROR,
                         f'The function get_all is accessible to administrators only. The login token '
                         f'"{self.login_token}" tried to use this function.')
            return
        return self.repo.get_all(Customers)

    def add_administrator(self, user, administrator):
        if self.login_token.role != 'administrators':
            print_to_log(logger, logging.ERROR,
                         f'The function add_administrator is accessible to administrators only. The login token '
                         f'"{self.login_token}" tried to use this function.')
            return
        if not isinstance(user, Users):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_administrator but the user "{user}" '
                         f'that was sent is not a User object.')
            return
        if Users.user_role != 3:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_administrator but the user.user_role "{Users.user_role}" '
                         f'that was sent is not 3(Administrator).')
            return
        if not isinstance(administrator, Administrators):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_administrator but the administrator "{administrator}" '
                         f'that was sent is not an Administrator object.')
            return
        if self.create_user(user):
            administrator.id = None
            administrator.user_id = user.id
            print_to_log(logger, logging.DEBUG,
                         f'The login token "{self.login_token}" used the function add_administrator and added administrator "{administrator}" '
                         f'that connected to the user "{user}".')
            self.repo.add(administrator)
            return True
        else:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_administrator but the user "{user}" '
                         f'that was sent is not valid so the function failed.')
            return

    def remove_administrator(self, administrator_id):
        if self.login_token.role != 'administrators':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_administrator but his role is '
                         f'not Administrator.')
            return
        if not isinstance(administrator_id, int):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_administrator but the administrator_id "{administrator_id}" '
                         f'that was sent is not an integer.')
            return
        if administrator_id <= 0:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_administrator but the administrator_id "{administrator_id}" '
                         f'that was sent is not positive.')
            return
        admin = self.repo.get_by_condition(Administrators,
                                           lambda query: query.filter(Administrators.id == administrator_id).all())
        if not admin:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_administrator but the administrator_id "{administrator_id}" '
                         f'that was sent does not exist in the db.')
            return
        print_to_log(logger, logging.DEBUG,
                     f'The login token "{self.login_token}" used the function remove_administrator and removed the administrator "{admin}"')
        self.repo.delete_by_id(Users, Users.id, admin[0].user.id)
        return True

    def remove_airline(self, airline_id):
        if self.login_token.role != 'administrators':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_airline but his role is '
                         f'not Administrator.')
            return
        if not isinstance(airline_id, int):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline_id}" '
                         f'that was sent is not an integer.')
            return
        if airline_id <= 0:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline_id}" '
                         f'that was sent is not an positive.')
            return
        airline = self.repo.get_by_condition(Airline_Companies,
                                             lambda query: query.filter(Airline_Companies.id == airline_id).all())
        if not airline:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline_id}" '
                         f'that was sent does not exist in the db.')
            return
        print_to_log(logger, logging.DEBUG,
                     f'The login token "{self.login_token}" used the function remove_airline and removed the airline "{airline}"')
        self.repo.delete_by_id(Users, Users.id, airline[0].user.id)
        return True

    def remove_customer(self, customer_id):
        if self.login_token.role != 'administrators':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_customer but his role is '
                         f'not Administrator.')
            return
        if not isinstance(customer_id, int):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                         f'that was sent is not an integer.')
            return
        if customer_id <= 0:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                         f'that was sent is not positive.')
            return
        customer = self.repo.get_by_condition(Customers,
                                              lambda query: query.filter(Customers.id == customer_id).all())
        if not customer:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                         f'that was sent does not exist in the db.')
            return
        tickets = self.repo.get_by_condition(Tickets,
                                             lambda query: query.filter(Tickets.customer_id == customer_id).all())
        for ticket in tickets:
            self.repo.update_by_id(Flights, Flights.id, ticket.flight_id,
                                   # updating the remaining tickets of the flight
                                   {Flights.remaining_tickets: ticket.flight.remaining_tickets + 1})
        print_to_log(logger, logging.DEBUG,
                     f'The login token "{self.login_token}" used the function remove_customer and removed the customer "{customer}"')
        self.repo.delete_by_id(Users, Users.id, customer[0].user.id)
        return True

    def add_customer(self, user, customer):
        if self.login_token.role != 'administrators':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_customer but his role is '
                         f'not Administrator.')
        if not isinstance(user, Users):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_customer but user "{user}" '
                         f'that was sent is not a User instance.')
            return
        if user.user_role != 1:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_customer but the user.user_role "{user.user_role}" '
                         f'that was sent is not 1(Customer).')
            return
        if not isinstance(customer, Customers):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_customer but customer "{customer}" '
                         f'that was sent is not a Customer object.')
            return
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(Customers.phone_no == customer.phone_no).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_customer but customer.phone_no "{customer.phone_no}" '
                         f'that was sent already exists in the db.')
            return
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(
                                          Customers.credit_card_no == customer.credit_card_no).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_customer but customer.credit_card_no "{customer.credit_card_no}" '
                         f'that was sent already exists in the db.')
            return
        if self.create_user(user):
            customer.id = None
            customer.user_id = user.id
            print_to_log(logger, logging.DEBUG,
                         f'The login token "{self.login_token}" used the function add_customer and added the customer "{customer}" '
                         f'connected by the user "{user}".')
            self.repo.add(customer)
            return True
        else:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_customer but the user "{user}" '
                         f'that was sent is not valid so the function failed.')
            return

    def add_airline(self, user, airline):
        if self.login_token.role != 'administrators':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_airline but his role is '
                         f'not Administrator.')
            return
        if not isinstance(user, Users):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_airline but user "{user}" '
                         f'that was sent is not a User object.')
            return
        if Users.user_role != 2:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_airline but the Users.user_role "{Users.user_role}" '
                         f'that was sent is not 2(Airline).')
            return
        if not isinstance(airline, Airline_Companies):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_airline but airline "{airline}" '
                         f'that was sent is not an Airline Company object.')
            return
        if self.repo.get_by_condition(Airline_Companies,
                                      lambda query: query.filter(Airline_Companies.name == airline.name).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_airline but airline.name "{airline.name}" '
                         f'that was sent already exists in the db.')
            return
        if not self.repo.get_by_condition(Countries,
                                          lambda query: query.filter(Countries.id == airline.country_id).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_airline but airline.country_id "{Airline_Companies.country_id}" '
                         f'that was sent does not exist in the db.')
            return
        if self.create_user(user):
            Airline_Companies.id = None
            Airline_Companies.user_id = user.id
            print_to_log(logger, logging.DEBUG,
                         f'The login token "{self.login_token}" used the function add_airline and added airline "{airline}" '
                         f'that connected to the user "{user}".')
            self.repo.add(airline)
            return True
        else:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_airline but the user "{user}" '
                         f'that was sent is not valid so the function failed.')
