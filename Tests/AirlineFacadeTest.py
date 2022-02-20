import pytest
from Business_Logics.AnonymousFacade import *
from Database.Flights import Flights
from datetime import datetime
from Database.Airline_Companies import *
from Exceptions.FlightTimesException import *
from Exceptions.NoMoreTicketsForFlightsException import *
from db_repo_pool import db_repo_pool


@pytest.fixture(scope='session')
def airline_facade_object():
    print('Setting up same DAO for all tests.')
    repool = db_repo_pool.get_instance()
    repo = repool.get_connection()
    anonfacade = AnonymousFacade(repo)
    return anonfacade.login('Yoni', '123')


@pytest.fixture(autouse=True)
def reset_db(airline_facade_object):
    airline_facade_object.repo.reset_test_db()
    return


def test_airline_facade_get_airline_flights(airline_facade_object):
    actual = airline_facade_object.get_airline_flights()
    assert actual == [Flights(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                             departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200)]


@pytest.mark.parametrize('flight, expected', [('not flight', None),
                                              (Flights(origin_country_id=3, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flights(origin_country_id=1, destination_country_id=3,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flights(origin_country_id=1, destination_country_id=2,
                        departure_time=1, landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flights(origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time='not datetime', remaining_tickets=200), None),
                                              (Flights(origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=100.7), None),
                                              (Flights(origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=99), None),
                                              (Flights(origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 21, 0, 0), remaining_tickets=100), True)])
def test_airline_facade_add_flight(airline_facade_object, flight, expected):
    actual = airline_facade_object.add_flight(flight)
    assert actual == expected


def test_airline_facade_add_flight_raise_notlegalflighttimeserror(airline_facade_object):
    with pytest.raises(FlightTimesException):
        airline_facade_object.add_flight(Flights(origin_country_id=1, destination_country_id=2,
                                                departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 17, 59, 0), remaining_tickets=100))


@pytest.mark.parametrize('airline, expected', [('not airline', None),
                                               (Airline_Companies(name='Yishay', country_id=1, user_id=3), None),
                                               (Airline_Companies(name='Yoni', country_id=3, user_id=3), None),
                                               (Airline_Companies(name='Yoniiiiii', country_id=2, user_id=3), True)])
def test_airline_facade_update_airline(airline_facade_object, airline, expected):
    actual = airline_facade_object.update_airline(airline)
    assert actual == expected


@pytest.mark.parametrize('flight, expected', [('not flight', None),
                                              (Flights(airline_company_id=3, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flights(airline_company_id=1, origin_country_id=3, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flights(airline_company_id=1, origin_country_id=1, destination_country_id=3,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flights(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=1, landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=200), None),
                                              (Flights(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time='not datetime', remaining_tickets=200), None),
                                              (Flights(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=100.7), None),
                                              (Flights(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=-2), None),
                                              (Flights(id=3, airline_company_id=1, origin_country_id=2, destination_country_id=1,
                        departure_time=datetime(2022, 1, 29, 17, 0, 0), landing_time=datetime(2022, 1, 30, 14, 0, 0), remaining_tickets=0), None),
                                              (Flights(id=2, airline_company_id=2, origin_country_id=2, destination_country_id=1,
                        departure_time=datetime(2022, 1, 29, 17, 0, 0), landing_time=datetime(2022, 1, 30, 14, 0, 0), remaining_tickets=0), None),
                                              (Flights(id=1, airline_company_id=1, origin_country_id=2, destination_country_id=1,
                        departure_time=datetime(2022, 1, 29, 17, 0, 0), landing_time=datetime(2022, 1, 30, 14, 0, 0), remaining_tickets=0), True)])
def test_airline_facade_update_flight(airline_facade_object, flight, expected):
    actual = airline_facade_object.update_flight(flight)
    assert actual == expected


def test_airline_facade_update_flight_raise_notlegalflighttimeserror(airline_facade_object):
    with pytest.raises(FlightTimesException):
        airline_facade_object.update_flight(Flights(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                                   departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 17, 59, 0), remaining_tickets=100))


def test_airline_facade_update_flight_raise_noremainingticketserror(airline_facade_object):
    with pytest.raises(NoMoreTicketsForFlightsException):
        airline_facade_object.update_flight(Flights(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                                   departure_time=datetime(2022, 1, 29, 00, 0, 0),
                                                   landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=-5))


@pytest.mark.parametrize('flight_id, expected', [('not_id', None),
                                                 (0, None),
                                                 (4, None),
                                                 (2, None),
                                                 (1, True)])
def test_airline_facade_remove_flight(airline_facade_object, flight_id, expected):
    actual = airline_facade_object.remove_flight(flight_id)
    assert actual == expected