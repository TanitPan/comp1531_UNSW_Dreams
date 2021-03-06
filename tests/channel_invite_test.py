"""
This file contains test function for channel_invite function in channel.py
"""
import pytest
from src.channel import channel_invite_v1, channel_details_v1
from src.channels import channels_create_v1, channels_list_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from data import data



def test_channel_invite():
    """
    This function checks if the new user 
    detail added to the channel is correct.
    """
    
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_id2 = auth_register_v1("harrypotter@gmail.com", "555555", "harry", "potter")

    channel_id1 = channels_create_v1(auth_id1["auth_user_id"], "Chill Soc", True)

    channel_invite_v1(auth_id1["auth_user_id"], channel_id1["channel_id"], auth_id2["auth_user_id"])
   
    # Check if the new u_id is added to channel
    assert channels_list_v1(auth_id2["auth_user_id"]) == {
        'channels': [
        	{
        		'channel_id': 1, # channel id start at 1 or 0 is worth checking ?
        		'name': 'Chill Soc',
        	}
        ],
    }

    # Check if the new user detail added to the channel is correct
    assert data["channels"] == [{
        'channel_id' :  1,
        'name': 'Chill Soc',
        'owner_members': [
            { 
                'auth_user_id' : 0, 
         
            }
        ],
        'all_members': [
            { 
                'auth_user_id' : 0, 
              
            },
            {
                'auth_user_id': 1,
               
            }
        ],
        'ispublic' :  True,
    }
    ]


    
  

def test_channel_invite_except_channel():
    """
    This function tests error for invalid channel
    being used as an input.
    """

    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_id2 = auth_register_v1("harrypotter@gmail.com", "555555", "harry", "potter")

    channel_id1 = channels_create_v1(auth_id1["auth_user_id"], "Chill Soc", True)

    # Test error for invalid channel
    with pytest.raises(InputError):
        channel_invite_v1(auth_id1["auth_user_id"], 12, auth_id2["auth_user_id"])
       


def test_channel_invite_except_user():
    """
    This function tests error for invalid u_id
    being invited to the channel.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_id2 = auth_register_v1("harrypotter@gmail.com", "555555", "harry", "potter")

    channel_id1 = channels_create_v1(auth_id1["auth_user_id"], "Chill Soc", True)
    
    # Test error for invalid u_id
    with pytest.raises(InputError):
        channel_invite_v1(auth_id1["auth_user_id"], channel_id1["channel_id"], 2222)
        


def test_channel_invite_except_noaccess():
    """
    This function tests if  the auth_user_id
    is a member of the channel.
    """

    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_id2 = auth_register_v1("harrypotter@gmail.com", "555555", "harry", "potter")

    channel_id1 = channels_create_v1(auth_id1["auth_user_id"], "Chill Soc", True)
    
    # Auth_user_id not a member of channel
    with pytest.raises(AccessError):
        channel_invite_v1(auth_id2["auth_user_id"], channel_id1["channel_id"], auth_id2["auth_user_id"])
       



def test_channel_invite_except_invalid_auth():
    """
    This functions tests if the auth_user_id is 
    a valid id.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_id2 = auth_register_v1("harrypotter@gmail.com", "555555", "harry", "potter")

    channel_id1 = channels_create_v1(auth_id1["auth_user_id"], "Chill Soc", True)

    # Test invalid auth_user_id case
    with pytest.raises(AccessError):
        channel_invite_v1(222, channel_id1["channel_id"],  auth_id2["auth_user_id"])



def test_channel_invite_except_repetitive():
    """
    This functions tests if the auth_user_id is 
    inviting a user already in the channel.
    """
    # Clear the data structure
    clear_v1()
    # Call other functions to create the data and store in data structure
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "123456", "john", "smith")
    auth_id2 = auth_register_v1("harrypotter@gmail.com", "555555", "harry", "potter")

    channel_id1 = channels_create_v1(auth_id1["auth_user_id"], "Chill Soc", True)

    # Test invalid auth_user_id case
    with pytest.raises(AccessError):
        channel_invite_v1(auth_id1["auth_user_id"], channel_id1["channel_id"],  auth_id1["auth_user_id"])