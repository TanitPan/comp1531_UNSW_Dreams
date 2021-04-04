'''This file consists of HTTP server tests for search_v2 in other.py'''

from src.config import url
from src.helper import generate_token
import json
import pytest
import requests

def test_search_empty_messages():
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "a.andrews@gmail.com",
        "password": "password123",
        "name_first": "anne",
        "name_last": "andrews",
    })
    payload = authorised_info.json()
    token = payload["token"]
    
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'channel1', 
        'is_public': True
    })
    payload = request.json()
    channel_id = payload["channel_id"]   
    request = requests.get(f"{url}/search/v2", 
        params= {"token": token, "query_str": "Good morning"})
    assert request.status_code == 200 
    payload = request.json()
    assert (payload == [])
    
def test_search_overlimit_querystr():
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "a.andrews@gmail.com",
        "password": "password123",
        "name_first": "anne",
        "name_last": "andrews",
    })
    payload = authorised_info.json()
    token = payload["token"]
    query_str = "12345" * 201
    request = requests.get(f"{url}/search/v2", 
        params= {"token": token, "query_str": query_str})
    assert request.status_code == 400   
                       
def test_search_invalidtoken():
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "a.andrews@gmail.com",
        "password": "password123",
        "name_first": "anne",
        "name_last": "andrews",
    })
    payload = authorised_info.json()
    # Create an invalid user_id add by adding one to the existing user
    invalid_user_id = payload["auth_user_id"] + 1
    token2 = generate_token(invalid_user_id)  
    request = requests.get(f"{url}/search/v2", 
        params= {"token": token2, "query_str": "COMP1531"})
    assert request.status_code == 403   
    
