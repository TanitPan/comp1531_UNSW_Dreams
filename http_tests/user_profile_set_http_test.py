'''
This file contains the tests for the HTTP server of user/profile/setname,
user/profile/setemail, user/profile/sethandle routes
'''

import pytest
import requests
import json
from src.config import url

@pytest.fixture
def register_user():
    global url
    requests.delete(f"{url}/clear/v1") # Clear the data
    requests.post(f"{url}/auth/register/v2", json={
        "email": "batman@gmail.com",
        "password": "123456",
        "name_first": "bat",
        "name_last": "man",
    })
    user = requests.post(f"{url}/auth/register/v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "john",
        "name_last": "smith",
    })
    payload = user.json()
    return payload

"""
TESTS FOR user/profile/setname/v2 ROUTE
"""
def test_valid_setname(register_user):
    global url
    user = register_user
    token = user['token']
    newFirstName = "Jason"
    newLastName = "Bourne"
    requests.put(f"{url}/user/profile/setname/v2", json={
        'token': token,
        'name_first': newFirstName,
        'name_last': newLastName,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert (payload['name_first'] == newFirstName and payload['name_last'] == newLastName)

def test_short_first_name(register_user):
    global url
    user = register_user
    token = user['token']
    newFirstName = ""
    newLastName = "Bourne"
    requests.put(f"{url}/user/profile/setname/v2", json={
        'token': token,
        'name_first': newFirstName,
        'name_last': newLastName,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_long_first_name(register_user):
    global url
    user = register_user
    token = user['token']
    newFirstName = "a"*51
    newLastName = "Bourne"
    requests.put(f"{url}/user/profile/setname/v2", json={
        'token': token,
        'name_first': newFirstName,
        'name_last': newLastName,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_short_last_name(register_user):
    global url
    user = register_user
    token = user['token']
    newFirstName = "Jason"
    newLastName = ""
    requests.put(f"{url}/user/profile/setname/v2", json={
        'token': token,
        'name_first': newFirstName,
        'name_last': newLastName,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_long_last_name(register_user):
    global url
    user = register_user
    token = user['token']
    newFirstName = "Jason"
    newLastName = "a"*51
    requests.put(f"{url}/user/profile/setname/v2", json={
        'token': token,
        'name_first': newFirstName,
        'name_last': newLastName,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['code'] == 400 # InputError

"""
TESTS FOR user/profile/setemail/v2 ROUTE
"""

def test_valid_email(register_user):
    global url
    user = register_user
    token = user['token']
    newEmail = "newemail@gmail.com"
    requests.put(f"{url}/user/profile/setemail/v2", json={
        'token': token,
        'email': newEmail,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['email'] == newEmail

def test_invalid_email(register_user):
    global url
    user = register_user
    token = user['token']
    newEmail = "invalid"
    requests.put(f"{url}/user/profile/setemail/v2", json={
        'token': token,
        'email': newEmail,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['code'] == 400 #InputError

def test_taken_email(register_user):
    global url
    user = register_user

    token = user['token']
    newEmail = "batman@gmail.com"
    requests.put(f"{url}/user/profile/setemail/v2", json={
        'token': token,
        'email': newEmail,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['code'] == 400 #InputError

"""
TESTS FOR user/profile/sethandle/v1 ROUTE
"""

def test_valid_handle(register_user):
    user = register_user

    token = user['token']
    newHandle = 'jasonbourne'
    requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': token,
        'handle_str': newHandle,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['handle_str'] == newHandle

def test_invalid_handle(register_user):
    user = register_user

    token = user['token']
    newHandle = 'jasonbourne'*5 # invalid string length
    requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': token,
        'handle_str': newHandle,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['code'] == 400 #InputError

def test_taken_handle(register_user):
    user = register_user

    token = user['token']
    newHandle = 'batman' # handle is taken by another user
    requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': token,
        'handle_str': newHandle,
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['code'] == 400 #InputError