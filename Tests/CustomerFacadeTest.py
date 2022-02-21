import pytest
from Business_Logics.AnonymousFacade import AnonymousFacade
from Database.Customers import Customers
from Database.Tickets import Tickets
from Exceptions.NoMoreTicketsForFlightsException import NoMoreTicketsForFlightsException
from db_repo_pool import db_repo_pool


@pytest.fixture(scope='session')
def customer_facade_object():
    print('Setting up same DAO for all tests.')
    repool = db_repo_pool.get_instance()
    repo = repool.get_connection()
    anonfacade = AnonymousFacade(repo)
    return anonfacade.login('Uri', '123')


@pytest.fixture(autouse=True)
def reset_db(customer_facade_object):
    customer_facade_object.repo.reset_test_db()
    return


@pytest.mark.parametrize('customer, expected', [('not customer', None),
                                                (Customers(first_name='Liza', last_name='Dorven', address='New York',
                                                           phone_no='0544462111', credit_card_no='8520', user_id=2), None),
                                                (Customers(first_name='Ofek', last_name='Shimoni', address='Haroline 82',
                                                           phone_no='0544462112', credit_card_no='7411', user_id=2), None),
                                                (Customers(first_name='Pira', last_name='Ziva', address='Hess 70',
                                                           phone_no='0544462113', credit_card_no='9630', user_id=2), True)])
def test_customer_facade_update_customer(customer_facade_object, customer, expected):
    actual = customer_facade_object.update_customer(customer)
    assert actual == expected


@pytest.mark.parametrize('ticket, expected', [('not ticket', None),
                                              (Tickets(flight_id=3), None),
                                              (Tickets(flight_id=2), True)])
def test_customer_facade_remove_ticket(customer_facade_object, ticket, expected):
    actual = customer_facade_object.remove_ticket(ticket)
    assert actual == expected


def test_customer_facade_get_tickets_by_customer(customer_facade_object):
    actual = customer_facade_object.get_tickets_by_customer()
    assert actual == [Tickets(id=2, flight_id=2, customer_id=2)]


def test_customer_facade_add_ticket_raise_noremainingticketserror(customer_facade_object):
    with pytest.raises(NoMoreTicketsForFlightsException):
        customer_facade_object.add_ticket(Tickets(flight_id=2, customer_id=1))


@pytest.mark.parametrize('ticket, expected', [('not ticket', None),
                                              (Tickets(flight_id=4), None),
                                              (Tickets(flight_id=1), True)])
def test_customer_facade_add_ticket(customer_facade_object, ticket, expected):
    actual = customer_facade_object.add_ticket(ticket)
    assert actual == expected
