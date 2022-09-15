from Business_Logics.FacadeBase import FacadeBase
from Database.Customers import Customers
from Database.Users import Users
from Database.Flights import Flights
from Database.Tickets import Tickets
from Database.Airline_Companies import Airline_Companies
from Database.Administrators import Administrators
from Database.Countries import Countries
from custom_errors.WrongLoginTokenError import WrongLoginTokenError
from custom_errors.NotValidDataError import NotValidDataError


class AdministratorFacade(FacadeBase):

    def __init__(self, login_token, repo):
        self.repo = repo
        super().__init__(self.repo)
        self._login_token = login_token

    def get_all_customers(self):
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function get_all_customers but his role is '
                f'not Administrator.')
            raise WrongLoginTokenError
        return self.repo.get_all(Customers)

    def add_administrator(self, user, administrator):
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_administrator but his role is '
                f'not Administrator.')
            raise WrongLoginTokenError
        if not isinstance(user, Users):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_administrator but the user "{user}" '
                f'that was sent is not a User object.')
            raise NotValidDataError
        if user.user_role != 3:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_administrator but the user.user_role "{user.user_role}" '
                f'that was sent is not 3(Administrator).')
            raise NotValidDataError
        if not isinstance(administrator, Administrators):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_administrator but the administrator "{administrator}" '
                f'that was sent is not an Administrator object.')
            raise NotValidDataError
        if self.create_user(user):
            administrator.id = None
            administrator.user_id = user.id
            self.logger.logger.debug(
                f'The login token "{self.login_token}" used the function add_administrator and added administrator "{administrator}" '
                f'that connected to the user "{user}".')
            self.repo.add(administrator)
            return True
        else:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_administrator but the user "{user}" '
                f'that was sent is not valid so the function failed.')
            raise NotValidDataError

    def remove_administrator(self, administrator_id):
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_administrator but his role is '
                f'not Administrator.')
            raise WrongLoginTokenError
        if not isinstance(administrator_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_administrator but the administrator_id "{administrator_id}" '
                f'that was sent is not an integer.')
            raise NotValidDataError
        if administrator_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_administrator but the administrator_id "{administrator_id}" '
                f'that was sent is not positive.')
            raise NotValidDataError
        admin = self.repo.get_by_condition(Administrators,
                                           lambda query: query.filter(Administrators.id == administrator_id).all())
        if not admin:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_administrator but the administrator_id "{administrator_id}" '
                f'that was sent does not exist in the db.')
            raise NotValidDataError
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function remove_administrator and removed the administrator "{admin}"')
        self.repo.delete_by_id(Users, Users.id, admin[0].user.id)
        return True

    def remove_airline(self, airline_id):
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but his role is '
                f'not Administrator.')
            raise WrongLoginTokenError
        if not isinstance(airline_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline_id}" '
                f'that was sent is not an integer.')
            raise NotValidDataError
        if airline_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline_id}" '
                f'that was sent is not an positive.')
            raise NotValidDataError
        airline = self.repo.get_by_condition(Airline_Companies,
                                             lambda query: query.filter(Airline_Companies.id == airline_id).all())
        if not airline:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_airline but the airline_id "{airline_id}" '
                f'that was sent does not exist in the db.')
            raise NotValidDataError
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function remove_airline and removed the airline "{airline}"')
        self.repo.delete_by_id(Users, Users.id, airline[0].user.id)
        return True

    def remove_customer(self, customer_id):
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but his role is '
                f'not Administrator.')
            raise WrongLoginTokenError
        if not isinstance(customer_id, int):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                f'that was sent is not an integer.')
            raise NotValidDataError
        if customer_id <= 0:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                f'that was sent is not positive.')
            raise NotValidDataError
        customer = self.repo.get_by_condition(Customers,
                                              lambda query: query.filter(Customers.id == customer_id).all())
        if not customer:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function remove_customer but the customer_id "{customer_id}" '
                f'that was sent does not exist in the db.')
            raise NotValidDataError
        tickets = self.repo.get_by_condition(Tickets,
                                             lambda query: query.filter(Tickets.customer_id == customer_id).all())
        for ticket in tickets:
            self.repo.update_by_id(Flights, Flights.id, ticket.flight_id,
                                   # updating the remaining tickets of the flight
                                   {Flights.remaining_tickets: ticket.flight.remaining_tickets + 1})
        self.logger.logger.debug(
            f'The login token "{self.login_token}" used the function remove_customer and removed the customer "{customer}"')
        self.repo.delete_by_id(Users, Users.id, customer[0].user.id)
        return True

    def add_customer(self, user, customer):
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but his role is '
                f'not Administrator.')
            raise WrongLoginTokenError
        if not isinstance(user, Users):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but user "{user}" '
                f'that was sent is not a User instance.')
            raise NotValidDataError
        if user.user_role != 1:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but the user.user_role "{user.user_role}" '
                f'that was sent is not 1(Customer).')
            raise NotValidDataError
        if not isinstance(customer, Customers):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but customer "{customer}" '
                f'that was sent is not a Customer object.')
            raise NotValidDataError
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(Customers.phone_no == customer.phone_no).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but customer.phone_no "{customer.phone_no}" '
                f'that was sent already exists in the db.')
            raise NotValidDataError
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(
                                          Customers.credit_card_no == customer.credit_card_no).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_customer but customer.credit_card_no "{customer.credit_card_no}" '
                f'that was sent already exists in the db.')
            raise NotValidDataError
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
            raise NotValidDataError

    def add_airline(self, user, airline):
        if self.login_token.role != 'administrators':
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but his role is '
                f'not Administrator.')
            raise WrongLoginTokenError
        if not isinstance(user, Users):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but user "{user}" '
                f'that was sent is not a User object.')
            raise NotValidDataError
        if user.user_role != 2:
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but the user.user_role "{user.user_role}" '
                f'that was sent is not 2(Airline).')
            raise NotValidDataError
        if not isinstance(airline, Airline_Companies):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but airline "{airline}" '
                f'that was sent is not an Airline Company object.')
            raise NotValidDataError
        if self.repo.get_by_condition(Airline_Companies,
                                      lambda query: query.filter(Airline_Companies.name == airline.name).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but airline.name "{airline.name}" '
                f'that was sent already exists in the db.')
            raise NotValidDataError
        if not self.repo.get_by_condition(Countries,
                                          lambda query: query.filter(Countries.id == airline.country_id).all()):
            self.logger.logger.error(
                f'The login token "{self.login_token}" tried to use the function add_airline but airline.country_id "{airline.country_id}" '
                f'that was sent does not exist in the db.')
            raise NotValidDataError
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
            raise NotValidDataError
