"""
This file contains the tests for the HTTP implementation of auth_logout_v1
"""

import src.auth as auth
from src.helper import generate_token

import pytest
import requests
import json
from src.config import url

def test_valid_logout():
    global url
    requests.delete(f"{url}/clear/v1") # clear the data first
    # Register a user and recieve their token
    user = requests.post(f"{url}/auth/register/v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "john",
        "name_last": "smith"
    })
    payload = user.json()
    token = payload['token']
    res = requests.post(f"{url}/auth/logout/v1", json={
        'token': token
    })
    payload = res.json()
    print("PAYLOAD IS: ", payload)
    assert payload == {'is_success': True}


def test_inactive_token():
    global url
    requests.delete(f"{url}/clear/v1") # clear the data first
    # Register a user
    token = generate_token(42) # random token
    res = requests.post(f"{url}/auth/logout/v1", json={
        'token': token
    })
    payload = res.json()
    assert payload == {'is_success': False}
