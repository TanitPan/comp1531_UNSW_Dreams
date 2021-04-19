"""
This file contains test function for dm_remove function in dm.py
"""
import pytest
from src.dm import dm_create_v1, dm_list_v1, dm_details_v1, dm_remove_v1
from src.channels import channels_create_v2, channels_list_v2
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.helper import generate_token

def test_dm_remove_valid():
    """
    This function test the valid case of dm_remove_v1
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")


    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]
    auth_id1 = auth_dict1["auth_user_id"]
   

    dm_dict = dm_create_v1(auth_token2, [auth_id1])
    dm_id = dm_dict["dm_id"]
    dm_remove_v1(auth_token2, dm_id)
    dm_dict = dm_list_v1(auth_token2) 
    assert dm_dict["dms"] == []

    dm_dict = dm_create_v1(auth_token2, [auth_id1])
    dm_id = dm_dict["dm_id"]
    dm_remove_v1(auth_token1, dm_id)
    dm_dict = dm_list_v1(auth_token1) 
    assert dm_dict["dms"] == []

def test_dm_remove_invalid_dm():
    """
    This function test the invalid DM channel ID case
    """
   
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")


    auth_token2 = auth_dict2["token"]
    auth_id1 = auth_dict1["auth_user_id"]
    auth_dict2["auth_user_id"]

    dm_create_v1(auth_token2, [auth_id1])
    invalid_dm = 900
    with pytest.raises(InputError):
        dm_remove_v1(auth_token2, invalid_dm)

def test_dm_remove_not_owner():
    """
    This function test the invalid DM channel ID case
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]
    auth_id1 = auth_dict1["auth_user_id"]
    auth_dict2["auth_user_id"]

    dm_dict = dm_create_v1(auth_token1, [auth_id1])
    dm_id = dm_dict["dm_id"]

    with pytest.raises(AccessError):
        dm_remove_v1(auth_token2, dm_id)


def test_dm_remove_invalid_auth():
    """
    This function test the invalid token case
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_id1 = auth_dict1["auth_user_id"]
    invalid_user = 800
    invalid_token = generate_token(invalid_user)

    dm_dict = dm_create_v1(auth_token1, [auth_id1])
    dm_id = dm_dict["dm_id"]

    with pytest.raises(AccessError):
        dm_remove_v1(invalid_token, dm_id)