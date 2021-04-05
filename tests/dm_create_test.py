"""
This file contains test function for dm_create function in dm.py
"""
import pytest
from src.dm import dm_create_v1, dm_list_v1
from src.channels import channels_create_v2, channels_list_v2
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.helper import generate_token


def test_dm_create_valid():
    """
    This function checks valid case where dm channel
    is created successfully.
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")
    auth_dict3 = auth_register_v2("alexcactus@gmail.com", "alex1234", "alex", "cactus")

    auth_token1 = auth_dict1["token"]
    auth_id2 = auth_dict2["auth_user_id"]
    auth_id3 = auth_dict3["auth_user_id"]

    dm_dict = dm_create_v1(auth_token1, [auth_id2])
    assert dm_dict["dm_id"] == 1
    assert dm_dict["dm_name"] == "harrypotter,johnsmith"
   
    dm_dict = dm_create_v1(auth_token1, [auth_id2, auth_id3])
    assert dm_dict["dm_id"] == 2
    assert dm_dict["dm_name"] == "alexcactus,harrypotter,johnsmith"

def test_dm_create_invalid_uid():
    """
    This function test for invalid u_id in the input
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_id2 = auth_dict2["auth_user_id"]
    invalid_user = 500
    with pytest.raises(InputError):
        dm_create_v1(auth_token1, [auth_id2, invalid_user])

def test_dm_create_invalid_auth():
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_id2 = auth_dict2["auth_user_id"]
    invalid_user = 500
    invalid_token = generate_token(invalid_user)
    with pytest.raises(AccessError):
        dm_create_v1(invalid_token, [auth_id2])