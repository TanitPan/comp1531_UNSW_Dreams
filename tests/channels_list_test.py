from data import data 

from src.channels import channels_create_v2, channels_list_v2
from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.other import clear_v1

# Test the function's return value to ensure it produces the right type (dict)
def test_channels_list_returntype():
    # Clear all the functions at the start
    clear_v1()
    authorised_dict = auth_register_v2('smithjack@outlook.com', 'newpassword', 
                       'jack', 'smith') #Registers a dummy account
    authorised_token = authorised_dict['token'] # Obtain token
    channels_create_v2(authorised_token, 'Channel0', True)
    # Check if created channel is stored in the return value
    dict_channel = channels_list_v2(authorised_token)
    #  Check if the type of the dict_channel is a dictionary 
    assert(isinstance(dict_channel, dict) == True) 
    
# Tested the channels returned by a function to ensure they were a list of 
# dictionaries
def test_channels_list_channeltype():
    clear_v1()
    # Extracts an auth_user_id by calling the auth_register_v1 function and 
    # extracting its value
    authorised_dict = auth_register_v2('comp1531@student.com', 'newpassword', 
                      'john', 'smith')
    authorised_token = authorised_dict['token']
    channels_create_v2(authorised_token, 'Channel1', True)
    dict_channel = channels_list_v2(authorised_token)   
    # Looks at the channels key and makes sure its value is a list
    channels_value = dict_channel['channels']
    assert(isinstance(channels_value, list) == True)
    # Then inspects each element to ensure it generates a dictionary
    for element in channels_value:
        assert(isinstance(element, dict) == True)
        
# Tested channels structure to ensure it was returning the correct format
def test_channels_list_format():
    clear_v1()
    authorised_dict = auth_register_v2('zidnumber@unsw.com', 'unswstudent', 
                      'randwick', 'kensington')
    authorised_token = authorised_dict['token']
    channels_create_v2(authorised_token, 'Channel2', True)
    dict_channel = channels_list_v2(authorised_token)
    # Confirms format of the channel to be a dictionary containing a list of 
    # dictionaries
    assert (dict_channel == {'channels': [{'channel_id': 1, 'name': 'Channel2'}]})
        
# Tests how many channels have been created
def test_channels_list_total_channels():	
    clear_v1()
    authorised_dict = auth_register_v2('student1@email.com', 'student1', 
                      'lily', 'thomas')
    authorised_token = authorised_dict['token']
    channels_create_v2(authorised_token, 'Channel3', True)
    channels_create_v2(authorised_token, 'Channel4', True) #create two channels
    dict_channel = channels_list_v2(authorised_token)
    # Firstly check the length to ensure two channels have been created
    assert(len(dict_channel['channels']) == 2)    
    # Check if the format of multiple is appropriate as per the specs
    assert (dict_channel == {'channels': [{'channel_id': 1, 'name': 'Channel3'}, 
            {'channel_id': 2, 'name': 'Channel4'}]})
   
# Tests that the channels called by an unauthorised user is not listed 
def test_channels_list_multiplechannel_length():
    clear_v1()
    # Have two authorised users make a channel
    authorised_dict1 = auth_register_v2('user1@yahoo.com', 'password1234', 
                       'anne', 'smith')
    authorised_token1 = authorised_dict1['token']
    authorised_dict2 = auth_register_v2('user2@yahoo.com', 'password1234', 
                       'anna', 'smiths')
    authorised_token2 = authorised_dict2['token']
    channels_create_v2(authorised_token1, 'Channel5', True)
    channels_create_v2(authorised_token2, 'Channel6', True)
    # Call for the channel_list function for only the first user
    dict_channel = channels_list_v2(authorised_token1)
    # Confirm only one channel (created by the first user) has been called
    assert(len(dict_channel['channels']) == 1)    



