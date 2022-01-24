from Business_Logics.FacadeBase import FacadeBase
import logging
from ApplicationLogger import print_to_log

logger = logging.getLogger(__name__)



class AdministratorFacade(FacadeBase):

    def get_all_customers(self):
        print_to_log(logger, logging.INFO, 'Getting all customers...')

    def add_airline(self, airline):
        print_to_log(logger, logging.INFO, f'Adding airline {airline.id}...')

    def add_customer(self, customer):
        print_to_log(logger, logging.INFO, f'Adding customer {customer.id}...')

    def add_administrator(self, administrator):
        print_to_log(logger, logging.INFO, f'Adding administrator {administrator.id}...')

    def remove_airline(self, airline):
        print_to_log(logger, logging.INFO, f'Removing airline {airline.id}...')

    def remove_customer(self, customer):
        print_to_log(logger, logging.INFO, f'Removing customer {customer.id}...')

    def remove_administrator(self, administrator):
        print_to_log(logger, logging.INFO, f'Removing administrator {administrator.id}...')