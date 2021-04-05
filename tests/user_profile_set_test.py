import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.user import user_profile_setname_v2, user_profile_setemail_v2, user_profile_sethandle_v1
from src.other import clear_v1

@pytest.fixture
def register_user():
    clear_v1()
    auth_register_v2("superman@gmail.com", "123456", "super", "man")
    user = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    token = user['token']
    return token

"""
SETNAME TESTS
"""
def test_valid_setname(register_user):
    token = register_user
    res = user_profile_setname_v2(token, 'bat', 'man')
    assert res == {}

def test_short_first_name(register_user):
    token = register_user
    with pytest.raises(InputError):
        user_profile_setname_v2(token, '', 'man')

def test_long_first_name(register_user):
    token = register_user
    with pytest.raises(InputError):
        user_profile_setname_v2(token, 'a'*51, 'man')

def test_short_last_name(register_user):
    token = register_user
    with pytest.raises(InputError):
        user_profile_setname_v2(token, 'bat', '')

def test_long_last_name(register_user):
    token = register_user
    with pytest.raises(InputError):
        user_profile_setname_v2(token, 'bat', 'a'*51)


"""
SETEMAIL TESTS
"""

def test_valid_setemail(register_user):
    token = register_user
    res = user_profile_setemail_v2(token, "newemail@gmail.com")
    assert res == {}

def test_invalid_email(register_user):
    token = register_user
    with pytest.raises(InputError):
        user_profile_setemail_v2(token, "invalidemail")

def test_taken_email(register_user):
    token = register_user
    with pytest.raises(InputError):
        user_profile_setemail_v2(token, "superman@gmail.com")

"""
SETHANDLE TESTS
"""

def test_valid_sethandle(register_user):
    token = register_user
    res = user_profile_sethandle_v1(token, "newhandle")
    assert res == {}

def test_invalid_handle(register_user):
    token = register_user
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token, "a")
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token, "a"*22)

def test_taken_handle(register_user):
    token = register_user
    with pytest.raises(InputError):
        user_profile_sethandle_v1(token, "superman")