"""
This file contains test functions for channel_join function
in channel.py.
"""
import pytest
from data import data
from src.other import clear_v1
from src.error import InputError, AccessError
from src.channel import channel_join_v2
from src.auth import auth_register_v2
from src.channels import channels_create_v2, channels_list_v2
from src.helper import generate_token

def test_channel_join():
    """
    This function checks if the user is successfully
    added to the channel and store in the data structure.
    """

    # Clear the data structure
    clear_v1()
   

    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]

    channel_id1 = channels_create_v2(auth_token1, "Chill Soc", True)
    
    
    channel_join_v2(auth_token2, channel_id1["channel_id"])

    # Black box testing version in waiting
    # Check if the user is successfully added to the channel data frame
    assert channels_list_v2(auth_token2) == {
        'channels': [
        	{
        		'channel_id': 1, # channel id start at 1 or 0 is worth checking ? It's currently start at 1.
        		'name': 'Chill Soc',
        	}
        ],
    }


def test_channel_join_except_channel():
    """
    This function tests if channel ID is
    a valid channel.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]

    channels_create_v2(auth_token1, "Chill Soc", True)
    invalid_channel = 50
    
    with pytest.raises(InputError):
        channel_join_v2(auth_token2, invalid_channel)


def test_channel_join_except_invalid_auth():
    """
    This function tests if token is valid
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]

    channel_id1 = channels_create_v2(auth_token1, "Chill Soc", True)

    # Create invalid token for the test
    invalid_user = 999
    invalid_token = generate_token(invalid_user)

    with pytest.raises(AccessError):
        channel_join_v2(invalid_token, channel_id1["channel_id"])

    
def test_channel_join_except_private():
    """
    This function tests if the channel status
    is private and user is not global owner.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]

    channel_id1 = channels_create_v2(auth_token1, "Chill Soc", False)
    
    with pytest.raises(AccessError):
        channel_join_v2(auth_token2, channel_id1["channel_id"])

def test_channel_join_private_global():
    """
    This function tests if the channel status
    is private and user is global DREAM owner.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_dict1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token1 = auth_dict1["token"]
    auth_token2 = auth_dict2["token"]

    channel_id1 = channels_create_v2(auth_token2, "Chill Soc", False)


    # Global DREAM owner attempt to join a private channel  
    channel_join_v2(auth_token1, channel_id1["channel_id"])

    # Check if the global owner successfully join private channel
    assert channels_list_v2(auth_token1) == {
        'channels': [
        	{
        		'channel_id': 1, # channel id start at 1 or 0 is worth checking ? It's currently start at 1.
        		'name': 'Chill Soc',
        	}
        ],
    }



def test_channel_join_except_repetitive():
    """
    This function tests if the user is already
    a member in that channel.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_dict2 = auth_register_v2("harrypotter@gmail.com", "555555", "harry", "potter")

    auth_token2 = auth_dict2["token"]

    channel_id1 = channels_create_v2(auth_token2, "Chill Soc", True)


    
    with pytest.raises(AccessError):
        channel_join_v2(auth_token2, channel_id1["channel_id"])
