from Business_Logics.FacadeBase import FacadeBase
import logging
from ApplicationLogger import print_to_log

logger = logging.getLogger(__name__)

class AnonymousFacade(FacadeBase):
    def login(self, username, password):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')

    def create_new_user(self, user):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')
