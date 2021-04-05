"""
This file contain the test for dm_list_v1 HTTP implementation
"""
from src.config import url
from src.helper import generate_token
import pytest
import json
import requests

def test_dm_list_valid():
    """
    This function test the valid case of dm_list_v1
    """
     # Clear the data
    requests.delete(f"{url}/clear/v1")

    # Users information to be pass in as json
    user1_data = {
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first": "john",
        "name_last": "smith",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]

    u_ids = [auth_id2, auth_id3]

    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })

    dm_response = requests.get(f"{url}/dm/list/v1", params= {"token": token1})

    # Check if the HTML request is successful
    assert dm_response.status_code == 200

    payload = dm_response.json()
    assert payload["dms"] == [{"dm_id": 1, "name": "alexcactus,johnsmith,michaelbush"}]

def test_dm_invalid_auth():
    """
    This function test for invalid token
    """
    # Clear the data
    requests.delete(f"{url}/clear/v1")

    # Users information to be pass in as json
    user1_data = {
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first": "john",
        "name_last": "smith",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]

    invalid_user = 88
    invalid_token = generate_token(invalid_user)
    u_ids = [auth_id2, auth_id3]

    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })
    
    dm_response = requests.get(f"{url}/dm/list/v1", params= {"token": invalid_token})

    # Test invalid token by checking if 403 status code is raised
    assert dm_response.status_code == 403
