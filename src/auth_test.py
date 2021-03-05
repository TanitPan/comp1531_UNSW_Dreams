'''
This file contains the test functions for the auth.py functions
'''
import pytest

from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError

def test_register():
    '''
    This is a function which tests the auth_regiser_v1 function from auth.py,
    mostly checks for InputError for invalid inputs when registering.
    '''
    # clear the dataframe first
    clear_v1()

    # test that two users do not have the same auth_user_id
    auth_user_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_user_id2 = auth_register_v1("johndoe@gmail.com", "password", "john", "doe")
    assert(auth_user_id1 != auth_user_id2)
    
    # test that a user cannot be registered with an invalid email
    with pytest.raises(InputError):
        auth_register_v1("qwerty", "qwerty", "qwer", "ty")
    
    # flag InputError when an email is already registered
    auth_register_v1("ebubekirclark@gmail.com", "123456", "ebubekir", "clark")
    with pytest.raises(InputError):
        auth_register_v1("ebubekirclark@gmail.com", "123456", "ebubekir", "clark")

    # flag InputError when a password is less than 6 characters
    with pytest.raises(InputError):
        auth_register_v1("spiderman@gmail.com", "123", "spider", "man")

    # flag InputError when name_first is less than 1 character
    with pytest.raises(InputError):
        auth_register_v1("aquaman@gmail.com", "password", "", "man")

    # flag InputError when name_first is more than 50 characters
    with pytest.raises(InputError):
        auth_register_v1("superman@gmail.com", "password123", "SUPERMAN" * 7, "man")

    # flag InputError when name_last is less than 1 character
    with pytest.raises(InputError):
        auth_register_v1("catgirl@gmail.com", "passwordcat", "catgirl", "")
        
    # flag InputError when name_last is more than 50 characters
    with pytest.raises(InputError):
        auth_register_v1("batman@gmail.com", "gothamcity", "batman", "na" * 26)

'''
def test_login():
    '''
    #This is a function which tests the auth_login_v1 function from auth.py, makes
    #sure InputErrors are correctly raised by the implementation
    '''
    # Start with a fresh dataframe
    clear_v1()

    # Register a dummy user
    auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")

    # flag InputError when attempting to login with an invalid email
    with pytest.raises(InputError):
        auth_login_v1("invalidemailatgmailcom", "123456")

    # flag InputError when email doesn't belong to user
    with pytest.raises(InputError):
        auth_login_v1("nonexistentuser@gmail.com", "123456")
    
    # flag InputError when password is incorrect
    with pytest.raises(InputError):
        auth_login_v1("johnsmith@gmail.com", "654321")

'''