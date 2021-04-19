"""
This file contains test function for dm_details function in dm.py
"""
import pytest
from src.dm import dm_create_v1, dm_list_v1, dm_details_v1
from src.channels import channels_create_v2, channels_list_v2
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.helper import generate_token

def test_dm_details_valid():
    """
    This function test for valid case of dm_details_v1 function
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")


    auth_token1 = auth_dict1["token"]
    auth_id2 = auth_dict2["auth_user_id"]

    dm_dict = dm_create_v1(auth_token1, [auth_id2])
    dm_id = dm_dict["dm_id"]
    assert dm_details_v1(auth_token1, dm_id) == {
        "name": "harrypotter,johnsmith",
        "members": [
            {
                "auth_user_id": 0,
                "name_first": "john",
                "name_last": "smith",
                "handle_str": "johnsmith",
                "email": "johnsmith@gmail.com"
            },
            {
                "auth_user_id": 1,
                "name_first": "harry",
                "name_last": "potter",
                "handle_str": "harrypotter",
                "email": "harrypotter@gmail.com"
            }
        ]
                                        
    } 


def test_dm_details_invalid_dm():
    """
    This function test the invalid DM channel ID 
    case of dm_details_v1
    """

    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")


    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]
    auth_id2 = auth_dict2["auth_user_id"]

    dm_create_v1(auth_token1, [auth_id2])
    invalid_dm_id = 900
    with pytest.raises(InputError):
        dm_details_v1(auth_token2, invalid_dm_id)

def test_dm_details_invalid_member():
    """
    This function test if the auth user is not a member of 
    a DM channel dm_details_v1
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")


    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]

    dm_dict = dm_create_v1(auth_token1, [])
    dm_id = dm_dict["dm_id"]
    with pytest.raises(AccessError):
        dm_details_v1(auth_token2, dm_id)

def test_dm_details_invalid_auth():
    """
    This function test for invalid token
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_id2 = auth_dict2["auth_user_id"]
    invalid_user = 500
    invalid_token = generate_token(invalid_user)

    dm_dict = dm_create_v1(auth_token1, [auth_id2])
    dm_id = dm_dict["dm_id"]
    with pytest.raises(AccessError):
        dm_details_v1(invalid_token, dm_id)