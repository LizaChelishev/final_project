from Business_Logics.FacadeBase import FacadeBase
import logging
from ApplicationLogger import print_to_log
from Database.Customers import Customers
from Database.Flights import Flights
from Database.Tickets import Tickets
from Exceptions.NoMoreTicketsForFlightsException import NoMoreTicketsForFlightsException

logger = logging.getLogger(__name__)


class CustomerFacade(FacadeBase):
    def __init__(self, login_token, repo):
        self.repo = repo
        super().__init__(self.repo)
        self._login_token = login_token

    def update_customer(self, customer):
        if self.login_token.role != 'customers':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function update_customer but his role is not Customer.')
            return
        if not isinstance(customer, Customers):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" sent to the function customer :"{customer}" update_customer '
                         f'but its not a Customer object.')
            return
        updated_customer = self.repo.get_by_condition(Customers, lambda query: query.filter(
            Customers.id == self.login_token.id).all())
        if not updated_customer:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function update_customer but his customer_id not '
                         f'exists in the db.')
            return
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(Customers.phone_no == customer.phone_no).all()) and \
                self.repo.get_by_condition(Customers, lambda query: query.filter(
                    Customers.phone_no == customer.phone_no).all()) != updated_customer:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function update_customer but the phone number "{customer.phone_no}" '
                         f'already exists in the db.')
            return
        if self.repo.get_by_condition(Customers, lambda query: query.filter(
                Customers.credit_card_no == customer.credit_card_no).all()) and \
                self.repo.get_by_condition(Customers, lambda query: query.filter(
                    Customers.credit_card_no == customer.credit_card_no).all()) != updated_customer:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" used the function update_customer but the credit card number "{customer.credit_card_no}" '
                         f'already exists in the db.')
            return
        print_to_log(logger, logging.DEBUG,
                     f'The login token "{self.login_token}" used the function update_customer and updated to "{customer}"')
        self.repo.update_by_id(Customers, Customers.id, self.login_token.id,
                               {Customers.first_name: customer.first_name, Customers.last_name: customer.last_name,
                                Customers.address: customer.address, Customers.phone_no: customer.phone_no,
                                Customers.credit_card_no: customer.credit_card_no})
        return True

    def add_ticket(self, ticket):
        if self.login_token.role != 'customers':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_ticket but his role is not Customer.')
            return
        if not isinstance(ticket, Tickets):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_ticket but the ticket "{ticket}" '
                         f'that was sent to the function is not a Ticket object.')
            return
        flight = self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.id == ticket.flight_id).all())
        if not flight:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_ticket but the flight.id "{ticket.flight_id}" '
                         f'that was sent to the function not exists in the db.')
            return
        if flight[0].remaining_tickets <= 0:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_ticket but the flight has no remaining tickets')
            raise NoMoreTicketsForFlightsException
        if self.repo.get_by_condition(Tickets, lambda query: query.filter(Tickets.customer_id == self.login_token.id,
                                                                          Tickets.flight_id == ticket.flight_id).all()):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function add_ticket but this customer already has a ticket for this flight')
            return
        self.repo.update_by_id(Flights, Flights.id, ticket.flight_id,  # updating the remaining tickets of the flight
                               {Flights.remaining_tickets: flight[0].remaining_tickets - 1})
        ticket.id = None
        ticket.customer_id = self.login_token.id
        print_to_log(logger, logging.DEBUG,
                     f'The login token "{self.login_token}" used the function add_ticket and added this ticket "{ticket}"')
        self.repo.add(ticket)
        return True

    def remove_ticket(self, ticket):
        if self.login_token.role != 'customers':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_ticket but his role is not Customer.')
            return
        if not isinstance(ticket, Tickets):
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_ticket but the ticket "{ticket}" '
                         f'that was sent is not a Ticket object.')
            return
        ticket_ = self.repo.get_by_condition(Tickets, lambda query: query.filter(Tickets.flight_id == ticket.flight_id,
                                                                                 Tickets.customer_id == self.login_token.id).all())
        if not ticket_:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_ticket but the ticket "{ticket}" '
                         f'that was sent not exist in the db.')
            return
        if ticket_[0].customer_id != self.login_token.id:
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function remove_ticket but the ticket.customer_id "{ticket.customer_id}" '
                         f'is not belong to the login_token.')
            return
        self.repo.update_by_id(Flights, Flights.id, ticket_[0].flight.id,
                               {Flights.remaining_tickets: ticket_[0].flight.remaining_tickets + 1})
        print_to_log(logger, logging.DEBUG,
                     f'The login token "{self.login_token}" used the function remove_ticket and removed the ticket "{ticket}"')
        self.repo.delete_by_id(Tickets, Tickets.id, ticket_[0].id)
        return True

    def get_my_tickets(self, customer):
        print_to_log(logger, logging.INFO, f'Getting all customer\'s {customer.id} tickets...')
        if self.login_token.role != 'customers':
            print_to_log(logger, logging.ERROR,
                         f'The login token "{self.login_token}" tried to use the function get_tickets_by_customer but his role is not Customer.')
            return
        return self.repo.get_by_condition(Tickets,
                                          lambda query: query.filter(Tickets.customer_id == self.login_token.id).all())
