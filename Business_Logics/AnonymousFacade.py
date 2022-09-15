from Business_Logics.AdministratorFacade import AdministratorFacade
from Business_Logics.AirlineFacade import AirlineFacade
from Business_Logics.CustomerFacade import CustomerFacade
from Business_Logics.FacadeBase import FacadeBase
from Database.Customers import Customers
from Database.Users import Users
from Login_Token import LoginToken
from custom_errors.UserRoleTableError import UserRoleTableError
from custom_errors.WrongLoginDataError import WrongLoginDataError
from custom_errors.NotValidDataError import NotValidDataError
from werkzeug.security import check_password_hash


class AnonymousFacade(FacadeBase):

    facade_dic = {1: lambda login_token, repo: CustomerFacade(login_token, repo), 2: lambda login_token, repo: AirlineFacade(login_token, repo),
                  3: lambda login_token, repo: AdministratorFacade(login_token, repo)}

    user_backref_and_name_column_dic = {1: ['customers', 'first_name'], 2: ['airline_companies', 'name'],
                                        3: ['administrators', 'first_name']}

    def __init__(self, repo):
        self.repo = repo
        super().__init__(self.repo)

    def login(self, username, pw):

        user = self.repo.get_by_condition(Users, lambda query: query.filter(Users.username == username).first())
        if not user:
            self.logger.logger.info(
                f'Wrong username {username} has been entered to the login function.')
            raise WrongLoginDataError
        if not check_password_hash(user.password, pw):
            self.logger.logger.info(
                f'Wrong password {pw} has been entered to the login function.')
            raise WrongLoginDataError
        try:
            name = eval(f'user.{AnonymousFacade.user_backref_and_name_column_dic[user.user_role][0]}.'
                        f'{AnonymousFacade.user_backref_and_name_column_dic[user.user_role][1]}')
            id_ = eval(f'user.{AnonymousFacade.user_backref_and_name_column_dic[user.user_role][0]}.id')
            role = AnonymousFacade.user_backref_and_name_column_dic[user.user_role][0]
            login_token = LoginToken(id_, name, role)

            self.logger.logger.debug(f'{login_token} logged in to the system.')
            return AnonymousFacade.facade_dic[user.user_role](login_token, self.repo)

        except KeyError:
            self.logger.logger.error(
                f'User Roles table contains more than 3 user roles. Please check it ASAP.')
            raise UserRoleTableError

    def add_customer(self, user, customer):
        if not isinstance(user, Users):
            self.logger.logger.error(f'the user "{user}" that was sent to the function add_customer is not a User instance.')
            raise NotValidDataError
        if user.user_role != 1:
            self.logger.logger.error(f'the user.user_role "{user.user_role}" is not 1(Customer).')
            raise NotValidDataError
        if not isinstance(customer, Customers):
            self.logger.logger.error(
                f'the customer "{customer}" that was sent to the function add_customer is not a Customer instance.')
            raise NotValidDataError
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(Customers.phone_no == customer.phone_no).all()):
            self.logger.logger.error(
                f'the customer.phone_no "{customer.phone_no}" that was sent the function add_customer is already exists in the db.')
            raise NotValidDataError
        if self.repo.get_by_condition(Customers,
                                      lambda query: query.filter(
                                          Customers.credit_card_no == customer.credit_card_no).all()):
            self.logger.logger.error(
                f'the customer.credit_card_no "{customer.credit_card_no}" that was sent the function add_customer is already exists in the db.')
            raise NotValidDataError
        if self.create_user(user):
            customer.id = None
            customer.user_id = user.id
            self.logger.logger.debug(f'A Customer "{customer}" connected by the User "{user}" has been added to the db.')
            self.repo.add(customer)
            return True
        else:
            self.logger.logger.error(f'The function add_customer failed - the User "{user} "that was sent is not valid.')
            raise NotValidDataError