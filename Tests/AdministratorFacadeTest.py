import pytest
from AnonymousFacade import AnonymousFacade
from User import User
from Administrator import Administrator
from Customer import Customer
from Airline_Company import Airline_Company
from DbRepoPool import DbRepoPool


@pytest.fixture(scope='session')
def administrator_facade_object():
    print('Setting up same DAO for all tests.')
    repool = DbRepoPool.get_instance()
    repo = repool.get_connection()
    anonfacade = AnonymousFacade(repo)
    return anonfacade.login('Tomer', '123')


@pytest.fixture(autouse=True)
def reset_db(administrator_facade_object):
    administrator_facade_object.repo.reset_test_db()
    return


@pytest.mark.parametrize('user, administrator, expected', [('not user', 2, None),
                                                           (User(username='Elad', password='123', email='elad@gmail.com', user_role=9), 2, None),
                                                           (User(username='Elad', password='123', email='elad@gmail.com', user_role=3), 2, None),
                                                           (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=3), 'k', None),
                                                           (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=3),
                                                            Administrator(first_name='Borissss', last_name='Boriiii', user_id=6), True)])
def test_administrator_facade_add_administrator(administrator_facade_object, user, administrator, expected):
    actual = administrator_facade_object.add_administrator(user, administrator)
    assert actual == expected


def test_administrator_facade_get_all_customers(administrator_facade_object):
    actual = administrator_facade_object.get_all_customers()
    expected = [Customer(id=1, first_name='Elad', last_name='Gunders', address='Sokolov 11',
                          phone_no='0545557007', credit_card_no='0000', user_id=1),
                Customer(id=2, first_name='Uri', last_name='Goldshmid', address='Helsinki 16',
                         phone_no='0527588331', credit_card_no='0001', user_id=2)]
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


@pytest.mark.parametrize('user, customer, expected', [(1, 1, None), (User(username='Elad', password='123', email='eladi@gmail.com', user_role=2),
                                                       Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                        phone_no='0545557000', credit_card_no='0099', user_id=1) , None),
                                                      (User(username='Elados', password='123', email='eladi@gmail.coom', user_role=2),
                                                       Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                                phone_no='0545557000', credit_card_no='0099', user_id=1), None),
                                                      (User(username='Elad', password='123', email='eladi@gmail.com', user_role=1),
                                                       Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                        phone_no='0545557000', credit_card_no='0099', user_id=1) , None),
                                                      (User(username='Elados', password='123', email='eladi@gmail.coom', user_role=2),
                                                       'g', None),
                                                      (User(username='Elados', password='123', email='eladii@gmail.com', user_role=1),
                                                       Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                        phone_no='0545557007', credit_card_no='0099', user_id=1) , None),
                                                      (User(username='Elados', password='123', email='eladii@gmail.com', user_role=1),
                                                       Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                        phone_no='0545557004', credit_card_no='0000', user_id=1) , None),
                                                      (User(username='Elados', password='123', email='eladii@gmail.com', user_role=1),
                                                       Customer(first_name='kk', last_name='lk', address='Sokolov 1',
                                                        phone_no='0545557004', credit_card_no='0055', user_id=8) , True)
                                                      ])
def test_administrator_facade_add_customer(administrator_facade_object, user, customer, expected):
    actual = administrator_facade_object.add_customer(user, customer)
    assert actual == expected


@pytest.mark.parametrize('user, airline, expected', [(1, 1, None),
                                                     (User(username='Elad', password='123', email='eladi@gmail.com', user_role=1), 1, None),
                                                     (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=2), 1, None),
                                                     (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=2),
                                                      Airline_Company(name='Yoni', country_id=1, user_id=3), None),
                                                     (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=2),
                                                      Airline_Company(name='Yonchkin', country_id=3, user_id=3), None),
                                                     (User(username='Eladi', password='123', email='eladi@gmail.com', user_role=2),
                                                      Airline_Company(name='Yonchkin', country_id=1, user_id=8), True)])
def test_administrator_facade_add_airline(administrator_facade_object, user, airline, expected):
    actual = administrator_facade_object.add_airline(user, airline)
    assert actual == expected