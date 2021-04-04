'''This file consists of Python tests for channels_addowner_v1 in channel.py'''

import pytest

from src.channel import channel_addowner_v1, channel_removeowner_v1
from src.channels import channels_create_v2, channels_list_v2
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.other import clear_v1

# Test that the added owner is now a member of the channel by looking at the 
# channels_list function 
def test_channel_addowner_valid_inputs():
    clear_v1() # Clear
    # Register a valid user, who is the Dreams owner, and create a channel
    authorised_info = auth_register_v2("f.chopin@unsw.com", "nocturne", 
                      "frederic", "chopin")
    token = authorised_info["token"]
    channel_id = channels_create_v2(token, "Channel_1", True) 
    # Register a new user and obtain their user_id and token
    authorised_info = auth_register_v2("l.beethoven@gmail.com", "symphony", 
                      "ludwig", "beethoven") 
    new_user_id = authorised_info["auth_user_id"]
    new_token = authorised_info["token"]
    # Using the first user's token, who is an owner of both Dreams and the 
    # channel, add the second user as an owner of the newly created channel 
    channel_addowner_v1(token, channel_id, new_user_id)
    # Check if the function works by seeing if the user has joined the channel 
    # through the joined channels through channels_list
    joined_channels = channels_list_v2(new_token)
    assert (joined_channels == {'channels': [{'channel_id': 1, 
            'name': 'Channel_1'},]})

# Test that the newly added owner can now remove other owners 
def test_channel_addowner_removeowners():
    # Clear and register a valid owner of Dreams and a member of dreams 
    clear_v1() # Clear
    authorised_info1 = auth_register_v2("a.mozart@yahoo.com", "figaro", 
                      "amadeus", "mozart")
    authorised_info2 = auth_register_v2("anna.mozart@ymail.com", "nannerl", 
                      "anna", "mozart") 
    # Use the token of the first user to create a channel
    token1 = authorised_info1["token"]
    auth_user_id1 = authorised_info1["auth_user_id"]
    channel_id = channels_create_v2(token1, "Channel_2", True) 
    # Obtained the second user_id and token of the authorised user
    new_user_id2 = authorised_info2["auth_user_id"]
    new_token2 = authorised_info2["token"]
    # Add the second user as an owner of the newly created channel 
    channel_addowner_v1(token, channel_id, new_user_id2)
    # Verify that the newly added owner can remove the first user and confirm
    # this by looking at the list of joined channels
    channel_removeowner_v1(new_token2, channel_id, new_user_id2)
    joined_channels = channels_list_v2(token1)
    assert (joined_channels == {'channels': []})

# Test that an InputError is raised when an invalid channel id is passed in 
def test_channel_addowner_invalid_channel():
    clear_v1() # Clear
    # Register an user, extracting their token and user id 
    authorised_info = auth_register_v2("j.bach@gmail.com", "sebastian", 
                      "johann", "bach")
    token = authorised_info["token"]
    auth_user_id = authorised_info["auth_user_id"]
    # Create an invalid channel by incrementing one to an existing channel id
    invalid_channel = channels_create_v2(token, "Channel_3", False) + 1
    # Test that an InputError is raised for the invalid channel id
    with pytest.raises(InputError): 
        channel_addowner_v1(token, invalid_channel, auth_user_id)

# Test that an InputError is raised when someone tries to add an user_id who is 
# an already existing owner 
def test_channel_addowner_existingowner():
    # Clear and register an user, storing their token and user_id
    clear_v1() 
    authorised_info = auth_register_v2("c.debussey@gmail.com", "clairdelune", 
                      "claude", "debussey")
    token = authorised_info["token"]
    auth_user_id = authorised_info["auth_user_id"]
    # Create an channel, making the user the default owner of the channel
    channel_id = channels_create_v2(token, "Channel_4", True) 
    # Test that an InputError is raised for the attempt to add an existing owner
    with pytest.raises(InputError): 
        channel_addowner_v1(token, channel_id, auth_user_id)

# Test an AccessError is raised for an invalid token ID
def test_channel_addowner_invalidtoken():
    # Clear previous data and register two users
    clear_v1() 
    authorised_info1 = auth_register_v2("c.saintsaens@gmail.com", "carnival1", 
                      "camille", "saintsaens")
    auth_user_id = authorised_info1["auth_user_id"] # extract user id
    authorised_info2 = auth_register_v2("j.williams@outlook.com", "jurassic", 
                      "john", "williams")
    token1 = authorised_info2["token"] # extract token
    # Using the token of the second user, create a channel
    channel_id = channels_create_v2(token1, "Channel_5", False)               
    # Create a fake token and pass it into the add owner function, with the
    # expected result an AccessError
    token2 = "abc" 
    with pytest.raises(AccessError): 
        channel_addowner_v1(token2, channel_id, auth_user_id)
        
# Test an AccessError is raised if the authorised token user isn't an owner 
# of Dreams or the channel 
def test_channel_addowner_nonowner_token():
    # After clearing data, register an user and make them create a channel 
    clear_v1() 
    authorised_info1 = auth_register_v2("r.wagner@hotmail.com", "thering", 
                      "richard", "wagner")
    token1 = authorised_info1["token"]
    channel_id = channels_create_v2(token1, "Channel_6", True)                

    # Create two new users, neither of whom have been added to the channel, 
    # and pass in the second user's token and third user's auth_user_id
    authorised_info2 = auth_register_v2("j.haydn@outlook.com", "concerto", 
                      "joseph", "haydn")
    token2 = authorised_info2["token"]   

    authorised_info3 = auth_register_v2("i.tchaikovsky@gmail.com", "ballet", 
                      "ilyich", "tchaikovsky")
    auth_user_id = authorised_info3["auth_user_id"]   
    # Test if an AccessError is raised
    with pytest.raises(AccessError): 
        channel_addowner_v1(token2, channel_id, auth_user_id)


