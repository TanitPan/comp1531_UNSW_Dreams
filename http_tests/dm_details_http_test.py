"""
This file contais the test for dm_details_v1 HTTP implementation
"""
from src.config import url
from src.helper import generate_token
import pytest
import requests
import json

def test_dm_details_valid():
    """
    This function test the valid case of dm_details_v1
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
    dm_response = requests.get(f"{url}/dm/details/v1", params = {"token": token2, "dm_id":dm_id})

    # Check if the HTML request is successful
    assert dm_response.status_code == 200
    payload = dm_response.json()
    res_name = payload["name"]
    res_members = payload["members"]
    
    assert res_name == "johnsmith,michaelbush"
    assert res_members == [
        {
            "auth_user_id": 0,
            "name_first": "john",
            "name_last": "smith",
            "handle_str": "johnsmith",
            "email": "johnsmith@gmail.com"
        },
        {
            "auth_user_id": 1,
            "name_first": "michael",
            "name_last": "bush",
            "handle_str": "michaelbush",
            "email": "michaelbush@gmail.com"
        }
    ]

def test_dm_details_invalid_dm():
    """
    This function test the invalid DM channel ID 
    case of dm_details_v1
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
    
    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    auth_id2 = payload["auth_user_id"]
    token2 = payload["token"]

    u_ids = [auth_id2]
    requests.post(f"{url}/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })
    
    invalid_dm_id = 888
    dm_response = requests.get(f"{url}/dm/details/v1", params = {"token": token2, "dm_id": invalid_dm_id})

    # Test invalid dm_id by checking if 400 status code is raised
    assert dm_response.status_code == 400

def test_dm_details_invalid_member():
    """
    This function test if the auth user is not a member of 
    a DM channel dm_details_v1
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
    
    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    auth_id2 = payload["auth_user_id"]
    token2 = payload["token"]

    u_ids = []
    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })

    payload = dm_response.json()
    dm_id = payload["dm_id"]
    dm_response = requests.get(f"{url}/dm/details/v1", params = {"token": token2, "dm_id":dm_id})

    # Test if the user is member of channel. If not, 403 status code is raised
    assert dm_response.status_code == 403


def test_dm_details_invalid_auth():
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
    
    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    auth_id2 = payload["auth_user_id"]
    
    invalid_user = 95
    invalid_token = generate_token(invalid_user)

    u_ids = [auth_id2]
    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })

    payload = dm_response.json()
    dm_id = payload["dm_id"]
    dm_response = requests.get(f"{url}/dm/details/v1", params = {"token": invalid_token, "dm_id":dm_id})

    # Test if the token is valid. If not, 403 status code is raised
    assert dm_response.status_code == 403


