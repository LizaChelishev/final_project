from Business_Logics.FacadeBase import FacadeBase
import logging
from ApplicationLogger import print_to_log

logger = logging.getLogger(__name__)


class CustomerFacade(FacadeBase):
    def update_customer(self, customer):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

    def add_ticket(self, ticket):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

    def remove_ticket(self, ticket):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

    def get_tickets_by_customer(self, customer):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

