import pytest

from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.helper import generate_token
from src.other import clear_v1

'''This file consists of Python tests for channels_create_v2 in channels.py'''

# Test the type of the return value of channels_create to ensure it produces a
# dictionary (Specs 6.1.1)
def test_channels_create_type():
	# Clear at the beginning of all test functions to prevent information from
	# persisting
    clear_v1()
    # Created a valid user and extracted their authorised user id
    authorised_dict = auth_register_v2('john.smith@gmail.com', 'password', 
                       'john', 'smith')
    authorised_token = authorised_dict['token']
    # Used the above authorised user id to generate a channel_id
    channel_id =  channels_create_v2(authorised_token, "Channel0", True) 
    return_value = channel_id['channel_id']
    # Checked if the channel_id returned the expected output
    assert(return_value == 1)
    # Confirmed the type was a dict
    assert(isinstance(channel_id, dict) == True) 

# Test the key value of the return value (assuming it is a dictionary) to ensure 
# the channel_id is a integer value (Specs 6.1.1)
def test_channels_create_multiple_channels():
    clear_v1()
    authorised_dict = auth_register_v2('rujanair4@yahoo.com', 'ruja1nair',
                       'ruja', 'nair')
    authorised_token = authorised_dict['token']
    channel1_id = channels_create_v2(authorised_token, 'Channel1', True)

    # Created two channels, confirmed the channel_id was an integer and the 
    # format was correct
    channel1_key = channel1_id['channel_id']
    assert (isinstance(channel1_key, int) == True)
    assert (channel1_id == {'channel_id': 1})
    
    channel2_id = channels_create_v2(authorised_token, 'Channel2', True)
    channel2_key = channel2_id['channel_id']
    assert (isinstance(channel2_key, int) == True)
    assert (channel2_id == {'channel_id': 2})

# Test the complete structure of the return value to ensure the channel_id is 
# formatted properly  
def test_channels_create_firstvalue():
    clear_v1()
    # Extract a token and auth_user_id by calling auth_register_v1
    authorised_dict = auth_register_v2('annethomas@hotmail.com', 'pass1234', 
                       'anne', 'thomas')
    authorised_token = authorised_dict['token']
    # Create a new channel and obtained the id, confirming it is of the expected
    # format
    channel_id =  channels_create_v2(authorised_token, "Channel3", True)   
    assert (channel_id == {'channel_id': 1})

# Test the name value to see if the function raises an InputError for a name 
# with a length greater than 20 (Specs 6.2)
def test_channels_create_long_name():
    clear_v1()
    authorised_dict = auth_register_v2('jane.doe@me.com', 'janedoe2021',
                       'jane', 'doe')
    authorised_token = authorised_dict['token']
    # Checked if an InputError was raised for names greater than 20 characters
    with pytest.raises(InputError):   
        channels_create_v2(authorised_token, "longnamefortestchannel", True) 
    with pytest.raises(InputError):
        channels_create_v2(authorised_token, "123456789012345678901", False)
    with pytest.raises(InputError):
        channels_create_v2(authorised_token, "#!!!!!!!!!!!!!!!!!!!!#", True)
      
# Test multiple calls of channels_create_v1 to verify the dict has been updated
def test_channels_create_multiple():
    clear_v1()
    authorised_dict = auth_register_v2('comp1531student@email.com', 'comp15', 
                       'comp', 'student')
    authorised_token = authorised_dict['token']
    # Tested each element separately to ensure these have all increased in value
    channel_id1 =  channels_create_v2(authorised_token, "Channel4", True) 
    assert (channel_id1 == {'channel_id': 1})
    channel_id2 =  channels_create_v2(authorised_token, "Channel5", True) 
    assert (channel_id2 == {'channel_id': 2})
    channel_id3 =  channels_create_v2(authorised_token, "Channel6", True) 
    assert (channel_id3 == {'channel_id': 3})

 # Tests that the channels created by an unauthorised user is not listed 
def test_channels_create_unauthorised():
    clear_v1()
    authorised_dict = auth_register_v2('user1@yahoo.com', 'password1234', 
                       'anne', 'smith')
    authorised_token = authorised_dict['token']
    non_authorised_user = authorised_dict['auth_user_id'] + 1
    # Generated a new number, which was one higher than the authorised token
    # and tested if it would produce an AccessError when called as this was 
    # a non authorised user id
    non_authorised_token = generate_token(non_authorised_user)
    channels_create_v2(authorised_token, 'Channel0', True)
    with pytest.raises(AccessError):
        channels_create_v2(non_authorised_token, 'Channel1', True)

