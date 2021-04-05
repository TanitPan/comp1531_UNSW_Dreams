'''This file consists of Python tests for admin_user_permission_change_v2 in 
admin.py, testing for a valid input and for the errors '''

import pytest
from src.auth import auth_register_v2
from src.admin import admin_userpermission_change_v1
from src.channel import channel_addowner_v1, channel_removeowner_v1
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.helper import generate_token
from src.other import clear_v1

# Test the function by changing the admin permission of a user to owner and 
# verify they have global owner status
def test_admin_userpermission_change_valid():
    # Clear data and register three users
    clear_v1()
    authorised_dict1 = auth_register_v2('john.smith@gmail.com', 'password', 
                       'john', 'smith')
    authorised_dict2 = auth_register_v2('jane_doe@gmail.com', 'pass1234', 
                       'jane', 'doe')
    authorised_dict3 = auth_register_v2('matt_brown@gmail.com', '123456', 
                       'matt', 'brown')
    
    # Extract the token and user id of the first user and create a channel, 
    # making them both a global owner and the channel owner
    token1 = authorised_dict1['token']
    channel = channels_create_v2(token1, 'Channel_1', True)
    channel_id1 = channel['channel_id']
    
    # Extracting the second user's token and user id, make them a global owner
    token2 = authorised_dict2['token']
    user_id2 = authorised_dict2['auth_user_id']
    admin_userpermission_change_v1(token1, user_id2, 1) #owner = 1

    # Verify the second user can add the third user as an owner
    user_id3 = authorised_dict3['auth_user_id']
    token3 = authorised_dict3['token']
    channel_addowner_v1(token2, channel_id1, user_id3)
    
    # Verify that the second user can remove the third user as an owner, which 
    # is only possible if they are an owner of Dreams (not channel owner)

    channel_removeowner_v1(token2, channel_id1, user_id3) 
    # Make sure the third user cannot add themselves back as an owner, as they

    # are no longer an owner
    with pytest.raises(AccessError):
        channel_addowner_v1(token3, channel_id1, user_id3)

# Test that the permissions of an invalid user_id cannot be changed 
def test_admin_userpermission_change_invalid_user():
    clear_v1() # Clear
    # Register an user with a valid token, however, increase their user_id so 
    # it is invalid
    authorised_dict1 = auth_register_v2('john.smith@gmail.com', 'password', 
                       'john', 'smith')
    token = authorised_dict1['token']
    unauthorised_user = authorised_dict1['auth_user_id'] + 1
    # Confirm an InputError is raised when this invalid user id is passed in
    with pytest.raises(InputError): 
        admin_userpermission_change_v1(token, unauthorised_user, 2)   

# Test that the permission_id is an integer or else raise an InputError           
def test_admin_userpermission_change_invalid_permission():
    clear_v1() # clear
    # Extract the token and user id of a registered user
    authorised_dict = auth_register_v2('jane_doe@gmail.com', 'pass1234', 
                       'jane', 'smith')    
    token = authorised_dict['token']
    user_id = authorised_dict['auth_user_id']
    # Pass in non-integer type permission ids (string, list, dict) and
    # confirm an InputError is raised
    with pytest.raises(InputError): 
        admin_userpermission_change_v1(token, user_id, "!")   
    with pytest.raises(InputError): 
        admin_userpermission_change_v1(token, user_id, [1, 2, 3])
    with pytest.raises(InputError): 
        admin_userpermission_change_v1(token, user_id, {'key': 'value'})  

# Test that a non Dreams owner is prevented from changing the permission id
def test_admin_userpermission_change_unauthorised_user():            
    clear_v1()
    # After clearing, register 2 users (owner and member of Dreams respectively)
    authorised_dict1 = auth_register_v2('john.smith@gmail.com', 'password', 
                       'john', 'smith')
    authorised_dict2 = auth_register_v2('jane_doe@gmail.com', 'pass1234', 
                       'jane', 'smith') 
    # Using the user_id of the authorised user (the one whose token is passed 
    # in) and the token of the non-authorised user, test an error is raised
    user_id = authorised_dict1['auth_user_id']
    token = authorised_dict2['token']
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(token, user_id, 2)

