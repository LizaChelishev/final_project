import pytest
from AnonymousFacade import AnonymousFacade
from CustomerFacade import CustomerFacade
from AirlineFacade import AirlineFacade
from AdministratorFacade import AdministratorFacade
from UserRoleTableError import UserRoleTableError
from User import User
from DbRepoPool import DbRepoPool


@pytest.fixture(scope='session')
def anonymous_facade_object():
    print('Setting up same DAO for all tests.')
    repool = DbRepoPool.get_instance()
    repo = repool.get_connection()
    return AnonymousFacade(repo)


@pytest.fixture(autouse=True)
def reset_db(anonymous_facade_object):
    anonymous_facade_object.repo.reset_test_db()
    return


@pytest.mark.parametrize('username, password, expected', [('Elad', '123', CustomerFacade),
                                                          ('Yoni', '123', AirlineFacade),
                                                          ('Boris', '123', AdministratorFacade),
                                                          ('hh', '123', None)])
def test_anonymous_facade_log_in(anonymous_facade_object, username, password, expected):
    actual = anonymous_facade_object.login(username, password)
    if expected is None:
        assert actual == expected
    else:
        assert isinstance(actual, expected)


def test_anonymous_facade_log_in_raise_userroletableerror(anonymous_facade_object):
    with pytest.raises(UserRoleTableError):
        anonymous_facade_object.login('not legal', '123')