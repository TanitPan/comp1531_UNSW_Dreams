"""
This file contais the test for dm_remove_v1 HTTP implementation
"""
from src.config import url
from src.helper import generate_token
import pytest
import requests
import json


def test_dm_remove_valid():
    """
    This function test the valid case of dm_remove_v1
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

    user2_data = {
        "email": "michaelbush@gmail.com",
        "password": "123456",
        "name_first": "michael",
        "name_last": "bush",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]
    auth_id1 = payload["auth_user_id"]
    
    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    auth_id2 = payload["auth_user_id"]
    token2 = payload["token"]

    u_ids = [auth_id1]
    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token2, 
        "u_ids": u_ids
    })

    payload = dm_response.json()
    dm_id = payload["dm_id"]

    dm_response = requests.delete(f"{url}/dm/remove/v1", json = {
        "token": token2,
        "dm_id": dm_id
    })

    assert dm_response.status_code == 200

def test_dm_remove_invalid_dm():
    """
    This function test the invalid DM channel ID case
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

    user2_data = {
        "email": "michaelbush@gmail.com",
        "password": "123456",
        "name_first": "michael",
        "name_last": "bush",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]
    auth_id1 = payload["auth_user_id"]
    
    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    auth_id2 = payload["auth_user_id"]
    token2 = payload["token"]

    u_ids = [auth_id1]
    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token2, 
        "u_ids": u_ids
    })

    payload = dm_response.json()
    dm_id = payload["dm_id"]
    invalid_dm = 900

    dm_response = requests.delete(f"{url}/dm/remove/v1", json = {
        "token": token2,
        "dm_id": invalid_dm
    })

    # Test invalid DM ID by checking if 400 status code is raised
    assert dm_response.status_code == 400

def test_dm_remove_not_owner():
    """
    This function test the invalid DM channel ID case
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

    user2_data = {
        "email": "michaelbush@gmail.com",
        "password": "123456",
        "name_first": "michael",
        "name_last": "bush",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]
    auth_id1 = payload["auth_user_id"]
    
    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    auth_id2 = payload["auth_user_id"]
    token2 = payload["token"]

    u_ids = [auth_id2]
    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })

    payload = dm_response.json()
    dm_id = payload["dm_id"]
   

    dm_response = requests.delete(f"{url}/dm/remove/v1", json = {
        "token": token2,
        "dm_id": dm_id
    })

    # Test invalid original owner by checking if 403 status code is raised
    assert dm_response.status_code == 403

def test_dm_remove_invalid_auth():
    """
    This function test the invalid token case
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

    user2_data = {
        "email": "michaelbush@gmail.com",
        "password": "123456",
        "name_first": "michael",
        "name_last": "bush",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]
    auth_id1 = payload["auth_user_id"]
    
    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    auth_id2 = payload["auth_user_id"]
    token2 = payload["token"]

    u_ids = [auth_id2]
    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })

    payload = dm_response.json()
    dm_id = payload["dm_id"]
    invalid_user = 900
    invalid_token = generate_token(invalid_user)
   

    dm_response = requests.delete(f"{url}/dm/remove/v1", json = {
        "token": invalid_token,
        "dm_id": dm_id
    })

    # Test invalid token by checking if 403 status code is raised
    assert dm_response.status_code == 403