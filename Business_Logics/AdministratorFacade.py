from Business_Logics.FacadeBase import FacadeBase
import logging
from ApplicationLogger import print_to_log

logger = logging.getLogger(__name__)



class AdministratorFacade(FacadeBase):

    def get_all_customers(self):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

    def add_airline(self, airline):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

    def add_customer(self, customer):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

    def add_administrator(self, administrator):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

    def remove_airline(self, airline):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

    def remove_customer(self, customer):
        pass

    def remove_administrator(self, administrator):
        pass