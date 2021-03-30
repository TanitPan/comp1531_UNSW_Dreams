'''
This file contains the tests for the HTTP server of the functions auth_register
'''

import src.auth as auth
from src.helper import generate_token

import pytest
import requests
import json
from src.config import url

def test_input_valid(url):
    requests.delete(f"{url}/clear_v1") # clear the data first
    res = requests.post(f"{url}/auth/register_v2", json={
        "email": "johnsmith@gmail.com", # valid email
        "password": "123456",
        "name_first": "john",
        "name_last": "smith",
    })
    auth_user_id = 0
    token = generate_token(auth_user_id)
    payload = res.json()
    assert payload == {
        'token': token,
        'auth_user_id': auth_user_id
    }
def test_email_invalid(url):
    requests.delete(f"{url}/clear_v1") # clear the data first
    res = requests.post(f"{url}/auth/register_v2", json={
        "email": "john", # invalid email
        "password": "123456",
        "name_first": "john",
        "name_last": "smith",
    })
    auth_user_id = 0
    token = generate_token(auth_user_id)
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_email_taken(url):
    requests.delete(f"{url}/clear_v1") # clear the data first
    requests.post(f"{url}/auth/register_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "john",
        "name_last": "smith",
    })
    res = requests.post(f"{url}/auth/register_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "654321",
        "name_first": "johnny",
        "name_last": "smithson",
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_password_invalid(url):
    requests.delete(f"{url}/clear_v1") # clear the data first
    res = requests.post(f"{url}/auth/register_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123", #invalid password
        "name_first": "john",
        "name_last": "smith",
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_name_first_invalid(url):
    requests.delete(f"{url}/clear_v1") # clear the data first
    res = requests.post(f"{url}/auth/register_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "", # invalid first name, too short
        "name_last": "smith",
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

    requests.delete(f"{url}/clear_v1") # clear the data first
    res = requests.post(f"{url}/auth/register_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "a"*51, # invalid first name, too long
        "name_last": "smith",
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_name_last_invalid(url):
    requests.delete(f"{url}/clear_v1") # clear the data first
    res = requests.post(f"{url}/auth/register_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "john",
        "name_last": "", # invalid last name, too short
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

    requests.delete(f"{url}/clear_v1") # clear the data first
    res = requests.post(f"{url}/auth/register_v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "john", 
        "name_last": "a"*51, # invalid last name, too long
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError