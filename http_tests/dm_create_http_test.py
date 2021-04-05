"""
This file contain the test for dm_create_v1 HTTP implementation
"""
from src.config import url
from src.helper import generate_token
import pytest
import json
import requests

def test_dm_create_valid():
    """
    This function test the successful creation of dm.
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

    user3_data = {
        "email": "alexcactus@gmail.com",
        "password": "alex1234",
        "name_first": "alex",
        "name_last": "cactus",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    
    auth_id2 = payload["auth_user_id"]
    

    auth_user3_info = requests.post(f"{url}/auth/register/v2", json = user3_data)
    payload = auth_user3_info.json()
    
    auth_id3 = payload["auth_user_id"]
    
    u_ids = [auth_id2, auth_id3]

    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })

    # Check if the HTML request is successful
    assert dm_response.status_code == 200
    payload = dm_response.json()
    assert payload["dm_id"] == 1
    assert payload["dm_name"] == "alexcactus,johnsmith,michaelbush"

    u_ids = [auth_id3]

    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })

    # Check incrementation of dm_id
    payload = dm_response.json()
    assert payload["dm_id"] == 2
    assert payload["dm_name"] == "alexcactus,johnsmith"

def test_dm_create_invalid_uid():
    """
    This function test for invalid u_id in the input
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

    user3_data = {
        "email": "alexcactus@gmail.com",
        "password": "alex1234",
        "name_first": "alex",
        "name_last": "cactus",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    
    auth_id2 = payload["auth_user_id"]

    auth_user3_info = requests.post(f"{url}/auth/register/v2", json = user3_data)
    payload = auth_user3_info.json()
    

    invalid_user = 88
    u_ids = [auth_id2, invalid_user]

    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })

    # Test invalid u_id by checking if 400 status code is raised
    assert dm_response.status_code == 400

def test_dm_create_invalid_auth():
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

    user3_data = {
        "email": "alexcactus@gmail.com",
        "password": "alex1234",
        "name_first": "alex",
        "name_last": "cactus",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    
    auth_id2 = payload["auth_user_id"]
    

    auth_user3_info = requests.post(f"{url}/auth/register/v2", json = user3_data)
    payload = auth_user3_info.json()
    
    auth_id3 = payload["auth_user_id"]
   
    invalid_user = 88
    invalid_token = generate_token(invalid_user)
    u_ids = [auth_id2, auth_id3]

    dm_response = requests.post(f"{url}/dm/create/v1", json = {
        "token": invalid_token, 
        "u_ids": u_ids
    })

    # Test invalid token by checking if 403 status code is raised
    assert dm_response.status_code == 403