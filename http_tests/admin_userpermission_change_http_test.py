'''
This file contains HTTP server tests for admin_user_permission_change in 
src.admin, testing that permissions are allowed to be changed, and the correct
input and access errors are called. 
'''
from src.config import url
from src.helper import generate_token
import json
import pytest
import requests

# Change the admin permission of a user and verify they have global owner status
# by calling add_owner
def test_admin_userpermission_change_validinput():
    # Clears the data and register two users in the auth_register/v2. Extract
    # the token from the first and token and auth_user_id from the second user
    requests.delete(f"{url}/clear/v1") 
    authorised_info1 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'z5555555@gmail.com', 
        'password': 'unswstudent', 
        'name_first': 'termone', 
        'name_last': 'student',
    })  
    payload = authorised_info1.json()
    authorised_token1 = payload['token']
    
    authorised_info2 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'z9999999@gmail.com', 
        'password': 'kensingtonstudent', 
        'name_first': 'student', 
        'name_last': 'kensington',
    })  
    payload = authorised_info2.json()
    auth_user_id2 = payload['auth_user_id']
    authorised_token2 = payload['token']
    
    # Create a channel using the first user's token and capture the channel id
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token1, 
        'name': 'Channel1', 
        'is_public': False,
    })     
    payload = request.json()
    channel_id = payload['channel_id']
   
    # Adjust the second user's permission id to an owner status and check the 
    # HTML request succeeded
    request = requests.post(f"{url}/admin/userpermission/change/v1", json = {
        'token': authorised_token1, 
        'u_id': auth_user_id2, 
        'permission_id': 1,
    })  
    assert request.status_code == 200 

    # Create a third student and extract their user_id
    authorised_info3 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'z7777777@gmail.com', 
        'password': 'student', 
        'name_first': 'unsw', 
        'name_last': 'campus',
    }) 
    payload = authorised_info2.json()
    auth_user_id3 = payload['auth_user_id']

    # Check that the second user was able to add the third user to the group
    # as an owner as they have global permissions
    request = requests.post(f"{url}/channel/addowner/v1", json = {
        'token': authorised_token2, 
        'channel_id': channel_id, 
        'u_id': auth_user_id3,
    })  
    assert request.status_code == 200 

# Test that an error will be raised for attempting to change the permission of 
# an invalid user permission [not in users]
def test_admin_userpermission_change_invalid_user():
    # Clear data 
    requests.delete(f"{url}/clear/v1") 
    # Register a user and extract their token 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'z5555555@gmail.com', 
        'password': 'unswstudent', 
        'name_first': 'termone', 
        'name_last': 'student',
    })  
    payload = authorised_info.json()
    authorised_token = payload['token']
    # Create an invalid token by adding one to their user id
    unauthorised_user = payload['auth_user_id'] + 1
    # Pass the valid token and invalid u_id into the userpermission/chnge
    request = requests.post(f"{url}/admin/userpermission/change/v1", json = {
        'token': authorised_token, 
        'u_id': unauthorised_user, 
        'permission_id': 2,
    })  
    # Verify a 400 status code is raised
    assert request.status_code == 400 

# Test that an invalid permission id (not an integer) raises an InputError
def test_admin_user_permission_change_noninteger_permission_id():
    requests.delete(f"{url}/clear/v1") 
    # After clearing data, extract token and user_id 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'z5555555@gmail.com', 
        'password': 'unswstudent', 
        'name_first': 'termone', 
        'name_last': 'student',
    }) 
    payload = authorised_info.json()
    authorised_token = payload['token']
    user_id = payload['auth_user_id']
    
    # Use the valid token and user as parameters for the function. Use a string
    # for the permission_id input and confirm an InputError is raised [400 code]
    request = requests.post(f"{url}/admin/userpermission/change/v1", json = {
        'token': authorised_token, 
        'u_id': user_id, 
        'permission_id': '2',
    })  
    assert request.status_code == 400 

# Test that an unauthorised token is prevented from changing permissions
def test_admin_userpermission_change_unauthorised_tokenuser():
    requests.delete(f"{url}/clear/v1") 
    # After clearing data, extract  user_id 
    authorised_info1 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'z5555555@gmail.com', 
        'password': 'unswstudent', 
        'name_first': 'termone', 
        'name_last': 'student',
    }) 
    payload = authorised_info1.json()
    user_id = payload['auth_user_id']
    # Adjust token by adding a string to the end of it to make it invalid and
    # use this token in the request
    unauthorised_id = user_id + 1
    unauthorised_token = generate_token(unauthorised_id)
    request = requests.post(f"{url}/admin/userpermission/change/v1", json = {
        'token': unauthorised_token, 
        'u_id': user_id, 
        'permission_id': '2',
    })  
    # Confirm an AccessError is raised with a 403 error code
    assert request.status_code == 403 
