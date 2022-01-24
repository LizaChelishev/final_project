from Business_Logics.FacadeBase import FacadeBase
import logging
from ApplicationLogger import print_to_log

logger = logging.getLogger(__name__)


class CustomerFacade(FacadeBase):
    def update_customer(self, customer):
        print_to_log(logger, logging.INFO, f'Updating customer with id: {customer.id}')

    def add_ticket(self, ticket):
        print_to_log(logger, logging.INFO, f'Adding ticket with id:{ticket.id}')

    def remove_ticket(self, ticket):
        print_to_log(logger, logging.INFO, f'Removing ticket with id:{ticket.id}')

    def get_tickets_by_customer(self, customer):
        print_to_log(logger, logging.INFO, f'Getting all customer\'s {customer.id} tickets...')

