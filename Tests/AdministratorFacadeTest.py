import pytest
from Database.Administrators import Administrators
from Database.Airline_Companies import Airline_Companies
from Database.Customers import Customers
from Database.Users import Users
from DataAccess.db_repo_pool import db_repo_pool
from Business_Logics.AnonymousFacade import AnonymousFacade


@pytest.fixture(scope='session')
def administrator_facade_object():
    print('Setting up same DAO for all tests.')
    repool = db_repo_pool.get_instance()
    repo = repool.get_connection()
    anonfacade = AnonymousFacade(repo)
    return anonfacade.login('Tomer', '123')


@pytest.fixture(autouse=True)
def reset_db(administrator_facade_object):
    administrator_facade_object.repo.reset_test_db()
    return


@pytest.mark.parametrize('user, administrator, expected', [('not user', 2, None),
                                                           (Users(username='Test', password='123',
                                                                  email='lizachelishev@gmail.com', user_role=9), 2,
                                                            None),
                                                           (Users(username='Oren', password='123',
                                                                  email='lizachelishev@gmail.com', user_role=3), 2,
                                                            None),
                                                           (Users(username='Liza', password='123',
                                                                  email='lizachelishev@gmail.com', user_role=3), 'a',
                                                            None),
                                                           (Users(username='Pypo', password='123',
                                                                  email='lizachelishev@gmail.com', user_role=3),
                                                            Administrators(first_name='Liza', last_name='Chelishev',
                                                                           user_id=6), True)])
def test_administrator_facade_add_administrator(administrator_facade_object, user, administrator, expected):
    actual = administrator_facade_object.add_administrator(user, administrator)
    assert actual == expected


def test_administrator_facade_get_all_customers(administrator_facade_object):
    actual = administrator_facade_object.get_all_customers()
    expected = [Customers(id=1, first_name='Tibi', last_name='Oren', address='Tel Aviv',
                          phone_no='0544462114', credit_card_no='0000', user_id=1),
                Customers(id=2, first_name='Yael', last_name='Icon', address='Hess 9',
                          phone_no='0544462115', credit_card_no='0001', user_id=2)]
    assert actual == expected


@pytest.mark.parametrize('admin_id, expected', [('not int', None),
                                                (-1, None),
                                                (3, None),
                                                (1, True)])
def test_administrator_facade_remove_administrator(administrator_facade_object, admin_id, expected):
    actual = administrator_facade_object.remove_administrator(admin_id)
    assert actual == expected


@pytest.mark.parametrize('customer_id, expected', [('f', None),
                                                   (0, None),
                                                   (3, None),
                                                   (1, True),
                                                   (2, True)])
def test_administrator_facade_remove_customer(administrator_facade_object, customer_id, expected):
    actual = administrator_facade_object.remove_customer(customer_id)
    assert actual == expected


@pytest.mark.parametrize('airline_id, expected', [('f', None),
                                                  (-1, None),
                                                  (4, None),
                                                  (1, True)])
def test_administrator_facade_remove_airline(administrator_facade_object, airline_id, expected):
    actual = administrator_facade_object.remove_airline(airline_id)
    assert actual == expected


@pytest.mark.parametrize('user, customer, expected',
                         [(1, 1, None), (Users(username='Elad', password='123', email='eladi@gmail.com', user_role=2),
                                         Customers(first_name='kk', last_name='lk', address='Sokolov 1',
                                                   phone_no='0545557000', credit_card_no='0099', user_id=1), None),
                          (Users(username='Elados', password='123', email='eladi@gmail.coom', user_role=2),
                           Customers(first_name='kk', last_name='lk', address='Sokolov 1',
                                     phone_no='0545557000', credit_card_no='0099', user_id=1), None),
                          (Users(username='Elad', password='123', email='eladi@gmail.com', user_role=1),
                           Customers(first_name='kk', last_name='lk', address='Sokolov 1',
                                     phone_no='0545557000', credit_card_no='0099', user_id=1), None),
                          (Users(username='Elados', password='123', email='eladi@gmail.coom', user_role=2),
                           'g', None),
                          (Users(username='Elados', password='123', email='eladii@gmail.com', user_role=1),
                           Customers(first_name='kk', last_name='lk', address='Sokolov 1',
                                     phone_no='0545557007', credit_card_no='0099', user_id=1), None),
                          (Users(username='Elados', password='123', email='eladii@gmail.com', user_role=1),
                           Customers(first_name='kk', last_name='lk', address='Sokolov 1',
                                     phone_no='0545557004', credit_card_no='0000', user_id=1), None),
                          (Users(username='Elados', password='123', email='eladii@gmail.com', user_role=1),
                           Customers(first_name='kk', last_name='lk', address='Sokolov 1',
                                     phone_no='0545557004', credit_card_no='0055', user_id=8), True)
                          ])
def test_administrator_facade_add_customer(administrator_facade_object, user, customer, expected):
    actual = administrator_facade_object.add_customer(user, customer)
    assert actual == expected


@pytest.mark.parametrize('user, airline, expected', [(1, 1, None),
                                                     (Users(username='Elad', password='123', email='eladi@gmail.com',
                                                            user_role=1), 1, None),
                                                     (Users(username='Eladi', password='123', email='eladi@gmail.com',
                                                            user_role=2), 1, None),
                                                     (Users(username='Eladi', password='123', email='eladi@gmail.com',
                                                            user_role=2),
                                                      Airline_Companies(name='Yoni', country_id=1, user_id=3), None),
                                                     (Users(username='Eladi', password='123', email='eladi@gmail.com',
                                                            user_role=2),
                                                      Airline_Companies(name='Yonchkin', country_id=3, user_id=3),
                                                      None),
                                                     (Users(username='Eladi', password='123', email='eladi@gmail.com',
                                                            user_role=2),
                                                      Airline_Companies(name='Yonchkin', country_id=1, user_id=8),
                                                      True)])
def test_administrator_facade_add_airline(administrator_facade_object, user, airline, expected):
    actual = administrator_facade_object.add_airline(user, airline)
    assert actual == expected
