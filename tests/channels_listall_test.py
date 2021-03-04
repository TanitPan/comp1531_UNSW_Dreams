from src.channels import channels_create_v1, channels_listall_v1
from src.channel import channel_join_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1

# Test the type of the return value of channels_listall to ensure it produces a
# dictionary (Specs 6.1.1)
def test_channels_listall_channeltype():
    clear_v1()
    authorised_token = auth_register_v1('janedoe@hotmail.com', '1234567', 
                       'jane', 'doe')
    dict_channel = channels_listall_v1(authorised_token)
    list_channel = dict_channel.values()
    for channel in list_channel:
        assert(isinstance(channel, list) == True)  

# Tests the contents of the return value to ensure it meets the specs of being a
# list (Specs 6.1.1)        
def test_channels_listall_type():
    clear_v1()
    authorised_token = auth_register_v1('johnsmith@email.com', 'password', 
                       'john', 'smith')
    dict_channel = channels_listall_v1(authorised_token)
    for element in dict_channel['channels']:
        assert(isinstance(element, dict) == True) 
        
# Tests the function to make sure an InputError arises when there's no input
def channels_listall_empty_test():
    with pytest.raises(InputError):
        assert channels_listall_v1()

# Tests the number of lists are added to the channel once the channels_create 
# function is called twice 
def test_channels_listall_multiplechannel_length():
    clear_v1()
    authorised_token = auth_register_v1('user1@yahoo.com', 'password1234', 
                       'anne', 'smith')
    channel_id1 = channels_create_v1(authorised_token, 'Channel0', True)
    channel_id2 = channels_create_v1(authorised_token, 'Channel1', True)
    assert len(channels_listall_v1(authorised_token)) == 2


