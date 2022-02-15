from Business_Logics.AdministratorFacade import AdministratorFacade
from Business_Logics.AirlineFacade import AirlineFacade
from Business_Logics.CustomerFacade import CustomerFacade
from Business_Logics.FacadeBase import FacadeBase
import logging
from ApplicationLogger import print_to_log
from Database.Customers import Customers
from Database.Users import Users
from LoginToken import LoginToken

logger = logging.getLogger(__name__)


class AnonymousFacade(FacadeBase):
    facade_dic = {1: lambda login_token, repo: CustomerFacade(login_token, repo),
                  2: lambda login_token, repo: AirlineFacade(login_token, repo),
                  3: lambda login_token, repo: AdministratorFacade(login_token, repo)}

    user_backref_and_name_column_dic = {1: ['customers', 'first_name'], 2: ['airline_companies', 'name'],
                                        3: ['administrators', 'first_name']}

    def __init__(self, repo):
        self.repo = repo
        super().__init__(self.repo)

    def login(self, username, password):
        print_to_log(logger, logging.INFO, 'Invalid number of remaining tickets, cannot be negative.')
        user = self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == username,
                                                                            Users.password == password).first())
        if not user:
            print_to_log(logger, logging.INFO,
                         f'Wrong username {username} or password {password} has been entered to the login function.')
            return
        try:
            name = eval(f'user.{AnonymousFacade.user_backref_and_name_column_dic[user.user_role][0]}.'
                        f'{AnonymousFacade.user_backref_and_name_column_dic[user.user_role][1]}')
            id_ = eval(f'user.{AnonymousFacade.user_backref_and_name_column_dic[user.user_role][0]}.id')
            role = AnonymousFacade.user_backref_and_name_column_dic[user.user_role][0]
            login_token = LoginToken(id_, name, role)

            print_to_log(logger, logging.DEBUG, f'{login_token} logged in to the system.')
            return AnonymousFacade.facade_dic[user.user_role](login_token, self.repo)

        except KeyError:
            print_to_log(logger, logging.ERROR,
                         f'User Roles table contains more than 3 user roles. Please check it ASAP.')
            raise UserRoleTableError

    def add_customer(self, user, customer):
        if not isinstance(user, Users):
            print_to_log(logger, logging.ERROR,
                         f'the user "{user}" that was sent to the function add_customer is not a User instance.')
            return
        if user.user_role != 1:
            print_to_log(logger, logging.ERROR, f'the user.user_role "{user.user_role}" is not 1(Customer).')
            return
        if not isinstance(customer, Customers):
            print_to_log(logger, logging.ERROR,
                         f'the customer "{customer}" that was sent to the function add_customer is not a Customer instance.')
            return
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(Customers.phone_no == customer.phone_no).all()):
            print_to_log(logger, logging.ERROR,
                         f'the customer.phone_no "{customer.phone_no}" that was sent the function add_customer is already exists in the db.')
            return
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(
                                          Customers.credit_card_no == customer.credit_card_no).all()):
            print_to_log(logger, logging.ERROR,
                         f'the customer.credit_card_no "{customer.credit_card_no}" that was sent the function add_customer is already exists in the db.')
            return
        if self.create_user(user):
            customer.id = None
            customer.user_id = user.id
            print_to_log(logger, logging.DEBUG,
                         f'A Customer "{customer}" connected by the User "{user}" has been added to the db.')
            self.repo.add(customer)
            return True
        else:
            print_to_log(logger, logging.ERROR,
                         f'The function add_customer failed - the User "{user} "that was sent is not valid.')
            return
