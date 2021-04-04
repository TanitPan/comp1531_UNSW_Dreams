''' This file contains tests for admin_user_remove in src.admin, testing for 
valid responses, access error (unauthorised token user), and input errors 
(invalid u_id, removed user is the only dreams owner)'''

import pytest
from src.admin import admin_user_remove_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.channel import (channel_addowner_v1, channel_removeowner_v1, 
channel_join_v2, channel_leave_v1, channel_messages_v2)
from src.channels import channels_create_v2
from src.message import message_send_v2
from src.other import clear_v1

''' Test that after the function is called, the necessary information is removed
regarding owners'''
def admin_user_remove_owners():
    # Clear and register a user to be the Dreams owner and a member
    clear_v1()
    user1 = auth_register_v2("smithj@outlook.com", "s1234", "john", "smith")
    token1 = user1['token']
    user2 = auth_register_v2("willpower@gmail.com", "tempest", "will", "power")
    user_id = user2['auth_user_id']
    token2 = user2['token']
    
    # Create a channel using the Dreams owner's token and allow the second user
    #to join as an owner
    channel_id = channels_create_v2(token1, "Channel_1", True)
    channel_addowner_v1(token2, channel_id['channel_id'], user_id) 
    # Remove details of the second user from the Dreams channel 
    admin_user_remove_v1(token2, user_id)
    # Confirm the function works by ensuring an InputError is raised for the
    # removal of this user as a owner [should have had their details cleared]
    with pytest.raises(InputError):
        channel_removeowner_v2(token1, channel_id, user_id)

''' Test that after the function is called, the necessary information is removed
regarding channel members'''
def admin_user_remove_members():
    # Clear data, registering two users
    clear_v1()
    user1 = auth_register_v2("j.smith@aol.com", "jjsmith", "john", "smith")
    token1 = user1['token']
    user2 = auth_register_v2("z1234567@unsw.com", "unsw", "unsw", "student")
    user_id = user2['auth_user_id']
    token2 = user2['token']
    # Create a channel using the first user's token 
    channel_id = channels_create_v2(token1, "Channel_1", True)
    # Ask the second user to join the channel and subsequently remove them 
    # from Dreams
    channel_join_v2(token2, channel_id['channel_id'])   
    admin_user_remove_v1(token2, user_id)
    # Confirm the function works by ensuring an AccessError is raised for the
    # this user attempting to leave [should have had their details removed]
    with pytest.raises(AccessError):
        channel_leave_v1(token2, channel_id)

''' Test that after the function is called, the necessary information is removed
regarding messages'''
def admin_user_remove_messages():
    # Clear data, registering two authorised users
    clear_v1()
    user1 = auth_register_v2("j.smith@aol.com", "jjsmith", "john", "smith")
    token1 = user1['token']
    user2 = auth_register_v2("z1234567@unsw.com", "unsw", "unsw", "student")
    user_id = user2['auth_user_id']
    token2 = user2['token']
    # Using the first user's token, create a channel and add the second user as
    # an owner 
    channel_id = channels_create_v2(token1, "Channel_1", True)
    channel_addowner_v2(token2, channel_id['channel_id'], user_id) 
    # Send a message using the second one's token and remove them from Dreams
    message_send_v2(token2, "Channel_1", "Hello")
    admin_user_remove_v1(token1, user_id)
    # Extract the messages and ensure the message contents have changed
    channel_messages = channel_messages_v2(token2, channel_id, 0)
    
    for message in channel_messages['messages']:
        assert message == [{'Removed user'}]

''' Test to ensure that an InputError is raised if the only owner of the Dreams
channel is removed'''        
def test_admin_user_remove_only_owner():
    clear_v1()
    # Create one user, extracting their token and user id and paassing it into
    # admin_user_remove_v1 
    user = auth_register_v2("john.smith@gmail.com", "pass2021", "john", "smith")
    token = user['token']
    u_id = user['auth_user_id']
    # Ensure an input error has been raised
    with pytest.raises(InputError):
        admin_user_remove_v1(token, u_id)

''' Test to verify an invalid user (not part of users) cannot be removed from
Dreams '''
def test_admin_user_remove_invalid_user():
    # Clear data and register an authorised user, preserving their token
    clear_v1()
    user = auth_register_v2("john.smith@yahoo.com", "passwd", "johnny", "smith")
    token = user['token']   
    # Create an unauthorised id by incrementing the authorised user's user id 
    unauthorised_user_id = user['auth_user_id'] + 1
    # Raise an InputError
    with pytest.raises(InputError):
        admin_user_remove_v1(token, unauthorised_user_id)
        
''' Test to check that a non-Dreams owner cannot remove other users'''
def test_admin_user_remove_unauthorised_user(): 
    # Clear and register a user to be the owner
    clear_v1()
    auth_register_v2("tom.smith@ymail.com", "tom00smith", "tom", "smith")
    # Extract the token from a new registration
    user1 = auth_register_v2("john.smith@yahoo.com", "passwd", "johnny", "smith")
    invalid_token = user1['token']
    # Take the user id from a third registration 
    user2 = auth_register_v2("kevin2000@yahoo.com", "kevin1", "kevin", "jones")   
    user_id = user2['auth_user_id']
    # Pass the details that are not from the Dreams owner and ensure an Access
    # Error is raised for an unauthorised token user passing in information
    with pytest.raises(AccessError):
        admin_user_remove_v1(invalid_token, user_id)


