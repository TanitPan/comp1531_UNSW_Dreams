'''
This file contains the tests for the HTTP server of user/profile/setname,
user/profile/setemail, user/profile/sethandle routes.
'''

import pytest
import requests
import json
import urllib
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
    res = requests.put(f"{url}/user/profile/setname/v2", json={
        'token': token,
        'name_first': newFirstName,
        'name_last': newLastName,
    })
    payload = res.json()
    assert payload == {}

def test_short_first_name(register_user):
    global url
    user = register_user
    token = user['token']
    newFirstName = ""
    newLastName = "Bourne"
    res = requests.put(f"{url}/user/profile/setname/v2", json={
        'token': token,
        'name_first': newFirstName,
        'name_last': newLastName,
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_long_first_name(register_user):
    global url
    user = register_user
    token = user['token']
    newFirstName = "a"*51
    newLastName = "Bourne"
    res = requests.put(f"{url}/user/profile/setname/v2", json={
        'token': token,
        'name_first': newFirstName,
        'name_last': newLastName,
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_short_last_name(register_user):
    global url
    user = register_user
    token = user['token']
    newFirstName = "Jason"
    newLastName = ""
    res = requests.put(f"{url}/user/profile/setname/v2", json={
        'token': token,
        'name_first': newFirstName,
        'name_last': newLastName,
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_long_last_name(register_user):
    global url
    user = register_user
    token = user['token']
    newFirstName = "Jason"
    newLastName = "a"*51
    res = requests.put(f"{url}/user/profile/setname/v2", json={
        'token': token,
        'name_first': newFirstName,
        'name_last': newLastName,
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

"""
TESTS FOR user/profile/setemail/v2 ROUTE
"""
def test_valid_setemail(register_user):
    global url
    user = register_user
    token = user['token']
    newEmail = "jasonbourne@gmail.com"
    res = requests.put(f"{url}/user/profile/setemail/v2", json={
        'token': token,
        'email': newEmail,
    })
    payload = res.json()
    assert payload == {}

def test_invalid_email(register_user):
    global url
    user = register_user
    token = user['token']
    newEmail = "invalid"
    res = requests.put(f"{url}/user/profile/setemail/v2", json={
        'token': token,
        'email': newEmail,
    })
    payload = res.json()
    assert payload['code'] == 400 #InputError

def test_taken_email(register_user):
    global url
    user = register_user
    token = user['token']
    newEmail = "batman@gmail.com"
    res = requests.put(f"{url}/user/profile/setemail/v2", json={
        'token': token,
        'email': newEmail,
    })
    payload = res.json()
    assert payload['code'] == 400 #InputError

"""
TESTS FOR user/profile/sethandle/v1 ROUTE
"""
def test_valid_sethandle(register_user):
    global url
    user = register_user
    token = user['token']
    newHandle = "jasonbourne"
    res = requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': token,
        'handle_str': newHandle,
    })
    payload = res.json()
    assert payload == {}

def test_invalid_handle(register_user):
    global url
    user = register_user
    token = user['token']
    newHandle = 'jasonbourne'*5 # invalid string length
    res = requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': token,
        'handle_str': newHandle,
    })
    payload = res.json()
    assert payload['code'] == 400 #InputError

def test_taken_handle(register_user):
    global url
    user = register_user
    token = user['token']
    newHandle = 'batman' # handle is taken by another user
    res = requests.put(f"{url}/user/profile/sethandle/v1", json={
        'token': token,
        'handle_str': newHandle,
    })
    payload = res.json()
    assert payload['code'] == 400 #InputError
