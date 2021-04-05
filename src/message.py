from data import data
from src.error import InputError, AccessError
import src.helper as helper

def message_send_v2(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id. 
    Note: Each message should have it's own unique ID. 
    I.E. No messages should share an ID with another message, 
    even if that other message is in a different channel.
    
    This function return the message_id 

    '''

    is_member = False
    u_id = helper.valid_token(token)

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            curr_channel = channel
            for member in channel['all_members']:
                if member['auth_user_id'] == u_id:
                    is_member = True
                    break
            break

    if is_member == False:
        raise AccessError("Authorised user is not a member of channel")
    
    if len(message) > 1000:
        raise InputError("Message is too long")

    msg = {}
    
    msg['message_id'] = helper.msg_counter
    helper.msg_counter += 1
    
    msg['auth_user_id'] = u_id

    msg['message'] = message

    curr_channel['messages'].insert(0,msg)

    return {
        'message_id': msg['message_id']
    }
    '''
    return {
        'message_id': 1,
    }
    '''

def message_remove_v1(token, message_id):

    u_id = helper.valid_token(token)

    valid_msg_id = False
    valid_owner = False

    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                chan_id = channel['channel_id']
                valid_msg_id = True
                if message['auth_user_id'] == u_id:
                    valid_owner = True
                    break

    if valid_msg_id == False:
        raise InputError("Message no longer exists!")

    if valid_owner == False:
        raise AccessError("Not Authorised User!")

    for channel in data['channels']:
        if channel['channel_id'] == chan_id:
            curr_chan = channel

    for message in curr_chan['messages']:
        if message['message_id'] == message_id:
            curr_chan['messages'].remove(message)

    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    u_id = helper.valid_token(token)

    valid_msg_id = False
    valid_owner = False

    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                chan_id = channel['channel_id']
                valid_msg_id = True
                if message['auth_user_id'] == u_id:
                    valid_owner = True
                    break

    if valid_msg_id == False:
        raise InputError("Message no longer exists!")
    if len(message) > 1000:
        raise InputError("Message too long!")

    if valid_owner == False:
        raise AccessError("Not Authorised User!")

    if message == "":
        message_remove_v1(token, message_id)
        return {}

    else:
        for channel in data['channels']:
            if channel['channel_id'] == chan_id:
                curr_chan = channel
                break

        for msg in curr_chan['messages']:
            if msg['message_id'] == message_id:
                msg['message'] = message
                break

    
    return {
    }