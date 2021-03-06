"""
This file contains test functions for channel_join function
in channel.py.
"""
import pytest
from data import data
from src.other import clear_v1
from src.error import InputError, AccessError
from src.channel import channel_join_v1, channel_details_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1

def test_channel_join():
    """
    This function checks if the user is successfully
    added to the channel and store in the data structure.
    """

    # Clear the data structure
    clear_v1()
   

    # Call other functions to create the data and store in data structure
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_id2 = auth_register_v1("harrypotter@gmail.com", "555555", "harry", "potter")

    channel_id1 = channels_create_v1(auth_id1["auth_user_id"], "Chill Soc", True)
    # print(channel_id1)
    
    channel_join_v1(auth_id2["auth_user_id"], channel_id1["channel_id"])

    # Black box testing version in waiting
    # Check if the user is successfully added to the channel data frame
    assert channels_list_v1(auth_id2["auth_user_id"]) = {
        'channels': [
        	{
        		'channel_id': 1, # channel id start at 1 or 0 is worth checking ?
        		'name': 'Chill Soc',
        	}
        ],
    }

    # assert channel_details_v1(auth_id2["auth_user_id"], channel_id1["channel_id"]) == {
    #     'name': 'Chill Soc',
    #     'owner_members': [
    #         { 
    #             'auth_user_id' : 0, 
    #             'name_first' : 'john',
    #             'name_last' : 'smith', 
    #         }
    #     ],
    #     'all_members': [
    #         { 
    #             'auth_user_id' : 0, 
    #             'name_first' : 'john',
    #             'name_last' : 'smith', 
    #         },
    #         {
    #             'auth_user_id': 1,
    #             'name_first': 'harry',
    #             'name_last': 'potter',
    #         }
    #     ],
    # }


def test_channel_join_except_channel():
    """
    This function tests if channel ID is
    a valid channel.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_id2 = auth_register_v1("harrypotter@gmail.com", "555555", "harry", "potter")

    channel_id1 = channels_create_v1(auth_id1["auth_user_id"], "Chill Soc", True)

    
    with pytest.raises(InputError):
        channel_join_v1(auth_id2["auth_user_id"], 50)


def test_channel_join_except_invalid_auth():
    """
    This function tests if auth_user_id is valid
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_id2 = auth_register_v1("harrypotter@gmail.com", "555555", "harry", "potter")

    channel_id1 = channels_create_v1(auth_id1["auth_user_id"], "Chill Soc", True)

    
    with pytest.raises(InputError):
        channel_join_v1(999, channel_id1["channel_id"])

    
def test_channel_join_except_private():
    """
    This function tests if the channel status
    is private and user is not global owner.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_id2 = auth_register_v1("harrypotter@gmail.com", "555555", "harry", "potter")

    channel_id1 = channels_create_v1(auth_id1["auth_user_id"], "Chill Soc", False)

    
    with pytest.raises(InputError):
        channel_join_v1(auth_id2["auth_user_id"], channel_id1["channel_id"])