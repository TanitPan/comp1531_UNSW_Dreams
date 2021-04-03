"""
This file contains test function for channel_invite function in channel.py
"""
import pytest
from src.channel import channel_invite_v2
from src.channels import channels_create_v2, channels_list_v2
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.helper import generate_token



def test_channel_invite():
    """
    This function checks if the new user 
    detail added to the channel is correct.
    """
    
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]
    auth_id2 = auth_dict2["auth_user_id"]

    channel_id1 = channels_create_v2(auth_token1, "Chill Soc", True)

    channel_invite_v2(auth_token1, channel_id1["channel_id"], auth_id2)
   
    # Check if the new u_id is added to channel
    assert channels_list_v2(auth_token2) == {
        'channels': [
        	{
        		'channel_id': 1, # channel id start at 1 or 0 is worth checking ?
        		'name': 'Chill Soc',
        	}
        ],
    }
  

def test_channel_invite_except_channel():
    """
    This function tests error for invalid channel
    being used as an input.
    """

    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_id2 = auth_dict2["auth_user_id"]

    channels_create_v2(auth_token1, "Chill Soc", True)
    invalid_channel = 55

    # Test error for invalid channel
    with pytest.raises(InputError):
        channel_invite_v2(auth_token1, invalid_channel, auth_id2)
       


def test_channel_invite_except_user():
    """
    This function tests error for invalid u_id
    being invited to the channel.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_id2 = auth_dict2["auth_user_id"]
    invalid_u_id = 2222

    channel_id1 = channels_create_v2(auth_token1, "Chill Soc", True)
    
    # Test error for invalid u_id
    with pytest.raises(InputError):
        channel_invite_v2(auth_token1, channel_id1["channel_id"], invalid_u_id)
        


def test_channel_invite_except_noaccess():
    """
    This function tests if the auth_user_id
    is a member of the channel.
    """

    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]
    auth_id2 = auth_dict2["auth_user_id"]

    channel_id1 = channels_create_v2(auth_token1, "Chill Soc", True)
    
    # Auth_user_id not a member of channel
    with pytest.raises(AccessError):
        channel_invite_v2(auth_token2, channel_id1["channel_id"], auth_id2)
       

def test_channel_invite_except_invalid_auth():
    """
    This function tests if the token is valid.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]
    auth_id2 = auth_dict2["auth_user_id"]

    # Create invalid token for the test
    invalid_user = 222
    invalid_token = generate_token(invalid_user)

    channel_id1 = channels_create_v2(auth_token1, "Chill Soc", True)

    # Test invalid auth_user_id case
    with pytest.raises(AccessError):
        channel_invite_v2(invalid_token, channel_id1["channel_id"], auth_id2 )


def test_channel_invite_except_repetitive():
    """
    This functions tests if the auth_user_id is 
    inviting a user already in the channel.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]
    auth_id1 = auth_dict1["auth_user_id"]

    channel_id1 = channels_create_v2(auth_token1, "Chill Soc", True)
    

    # Test invalid auth_user_id case
    with pytest.raises(AccessError):
        channel_invite_v2(auth_token1, channel_id1["channel_id"], auth_id1)