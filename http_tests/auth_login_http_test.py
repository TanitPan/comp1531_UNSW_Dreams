"""
This file contains the tests for the HTTP implementation of auth_login_v2
"""

import src.auth as auth
from src.helper import generate_token

import pytest
import requests
import json
from src.config import url

def test_valid_login():
    global url
    requests.delete(f"{url}/clear_v1") # clear the data first
    requests.post(f"{url}/auth/register_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "john",
        "name_last": "smith",
    })
    requests.post(f"{url}/auth/login_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
    })

def test_email_invalid():
    global url
    requests.delete(f"{url}/clear_v1") # clear the data first
    res = requests.post(f"{url}/auth/login_v2", json={
        "email": "john", # invalid email
        "password": "123456",
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError
    

def test_email_unregistered():
    global url
    requests.delete(f"{url}/clear_v1") # clear the data first
    res = requests.post(f"{url}/auth/login_v2", json={
        "email": "johnsmith@gmail.com", # unregistered email
        "password": "123456",
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_password_invalid():
    global url
    requests.delete(f"{url}/clear_v1") # clear the data first
    requests.post(f"{url}/auth/register_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "john",
        "name_last": "smith",
    })
    res = requests.post(f"{url}/auth/login_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "password", # invalid password
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError
