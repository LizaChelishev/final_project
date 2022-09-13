import pytest

from DataAccess import db_repo_pool
from Business_Logics.AnonymousFacade import AnonymousFacade
from datetime import datetime
from DataAccess.db_repo_pool import db_repo_pool


@pytest.fixture(scope='session')
def dao_connection_singleton():
    print('Setting up same DAO for all tests.')
    repool = db_repo_pool.get_instance()
    repo = repool.get_connection()
    return AnonymousFacade(repo)


@pytest.fixture(autouse=True)
def reset_db(dao_connection_singleton):
    dao_connection_singleton.repo.reset_test_db()
    return


def test_facade_base_get_all_flights(dao_connection_singleton):
    actual = dao_connection_singleton.get_all_flights()
    assert actual == [Flights(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                              departure_time=datetime(2022, 1, 30, 16, 0, 0),
                              landing_time=datetime(2022, 1, 30, 20, 0, 0),
                              remaining_tickets=200),
                      Flights(id=2, airline_company_id=2, origin_country_id=1, destination_country_id=2,
                              departure_time=datetime(2022, 1, 30, 16, 0, 0),
                              landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=0)]


@pytest.mark.parametrize('id_, expected',
                         [(1, Flights(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                      departure_time=datetime(2022, 1, 30, 16, 0, 0),
                                      landing_time=datetime(2022, 1, 30, 20, 0, 0),
                                      remaining_tickets=200)),
                          (2, Flights(id=2, airline_company_id=2, origin_country_id=1, destination_country_id=2,
                                      departure_time=datetime(2022, 1, 30, 16, 0, 0),
                                      landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=0))])
def test_facade_base_get_flight_by_id(dao_connection_singleton, id_, expected):
    actual = dao_connection_singleton.get_flight_by_id(id_)
    assert actual == [expected]


@pytest.mark.parametrize('ocountry_id, dcountry_id, date_, expected', [('f', 3, datetime(2022, 1, 30), None),
                                                                       (3, 'r', datetime(2022, 1, 30), None),
                                                                       (0, 4, datetime(2022, 1, 30), None),
                                                                       (1, 2, 4, None),
                                                                       (1, 2, datetime(2022, 1, 30), [
                                                                           Flights(id=1, airline_company_id=1,
                                                                                   origin_country_id=1,
                                                                                   destination_country_id=2,
                                                                                   departure_time=datetime(2022, 1, 30,
                                                                                                           16, 0, 0),
                                                                                   landing_time=datetime(2022, 1, 30,
                                                                                                         20, 0, 0),
                                                                                   remaining_tickets=200),
                                                                           Flights(id=2, airline_company_id=2,
                                                                                   origin_country_id=1,
                                                                                   destination_country_id=2,
                                                                                   departure_time=datetime(2022, 1, 30,
                                                                                                           16, 0, 0),
                                                                                   landing_time=datetime(2022, 1, 30,
                                                                                                         20, 0, 0),
                                                                                   remaining_tickets=0)]),
                                                                       (1, 1, datetime(2022, 1, 30), [])])
def test_facade_base_get_flights_by_parameters(dao_connection_singleton, ocountry_id, dcountry_id, date_, expected):
    actual = dao_connection_singleton.get_flights_by_parameters(ocountry_id, dcountry_id, date_)
    assert actual == expected


def test_facade_base_get_all_airlines(dao_connection_singleton):
    actual = dao_connection_singleton.get_all_airlines()
    assert actual == [Airline_Companies(id=1, name='Yoni', country_id=1, user_id=3),
                      Airline_Companies(id=2, name='Yishay', country_id=2, user_id=4)]


@pytest.mark.parametrize('id_, expected', [('h', None),
                                           (0, None),
                                           (3, []),
                                           (1, [Airline_Companies(id=1, name='Yoni', country_id=1, user_id=3)]),
                                           (2, [Airline_Companies(id=2, name='Yishay', country_id=2, user_id=4)])])
def test_facade_base_get_airline_by_id(dao_connection_singleton, id_, expected):
    actual = dao_connection_singleton.get_airline_by_id(id_)
    assert actual == expected


def test_facade_base_get_all_countries(dao_connection_singleton):
    actual = dao_connection_singleton.get_all_countries()
    assert actual == [Countries(id=1, name='Israel'), Countries(id=2, name='Germany')]


@pytest.mark.parametrize('id_, expected', [('6', None),
                                           (0, None),
                                           (3, []),
                                           (1, [Countries(id=1, name='Israel')]),
                                           (2, [Countries(id=2, name='Germany')])])
def test_facade_base_get_country_by_id(dao_connection_singleton, id_, expected):
    actual = dao_connection_singleton.get_country_by_id(id_)
    assert actual == expected


@pytest.mark.parametrize('user, expected', [('notuser', None),
                                            (
                                                    Users(username='Elad', password='123', email='eladi@gmail.com',
                                                          user_role=1),
                                                    None),
                                            (Users(username='Elados', password='123', email='elad@gmail.com',
                                                   user_role=2), None),
                                            (Users(username='Elados', password='123', email='eladi@gmail.com',
                                                   user_role=5), None),
                                            (Users(username='Elados', password='123', email='eladi@gmail.coom',
                                                   user_role=2), True)])
def test_facade_base_create_user(dao_connection_singleton, user, expected):
    actual = dao_connection_singleton.create_user(user)
    assert actual == expected


@pytest.mark.parametrize('airline_id, expected', [('not int', None),
                                                  (0, None),
                                                  (7, None),
                                                  (1, [Flights(id=1, airline_company_id=1, origin_country_id=1,
                                                              destination_country_id=2,
                                                              departure_time=datetime(2022, 1, 30, 16, 0, 0),
                                                              landing_time=datetime(2022, 1, 30, 20, 0, 0),
                                                              remaining_tickets=200)])])
def test_airline_facade_get_flights_by_airline(dao_connection_singleton, airline_id, expected):
    actual = dao_connection_singleton.get_flights_by_airline_id(airline_id)
    assert actual == expected
