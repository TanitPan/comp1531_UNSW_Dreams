from data import data
from src.error import InputError, AccessError
import src.helper as helper
from datetime import timezone, datetime

def message_send_v2(token, channel_id, message):

    ''' 
    This function is to return the message_id of a message and store the dictionary 'msg' that includes
    message_id, auth_user_id, message and time_created into channel['messages']
        
    Arguments:
        token - the user ID of the members
        channel_id (int) - the ID of the channel
        message - the input message

    Exceptions:
        InputError - Occurs when the length of the message exceed 1000.
        AccessError - Occurs when the the authorised user has not joined the channel they are trying to post to.

    Return Value:
        Returns a dictionary 'msg' that includes that includes
        message_id, auth_user_id, message and time_created
    '''

    # Assign empty dictionary 'msg'
    msg = {}

    # Assign new variables to check
    is_member = False

    # Get the user['auth_user_id']
    u_id = helper.valid_token(token)

    # Looped through the data['channels']
    # Find the channel['channel_id'] with the same input channel_id
    # Assign the channel to curr_channel
    # Looped through the channel['all_members']
    # Find the member['auth_user_id'] with the same u_id
    # If the member is part of the channel, assign is_member to True
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            curr_channel = channel
            for member in channel['all_members']:
                if member['auth_user_id'] == u_id:
                    is_member = True
                    break
            break
    
    # If the member is to part of the channel, it raise AccesError
    if is_member == False:
        raise AccessError("Authorised user is not a member of channel")
    
    # If the length of the message exceed 1000, it raise InputError
    if len(message) > 1000:
        raise InputError("Message is too long")

    
    # Generate the message_id and assign it into dictionary msg['message_id']
    # Added 1 to msg_counter
    msg['message_id'] = helper.msg_counter
    helper.msg_counter += 1
    
    # Assign the user['auth_user_id'] who send the message into msg['auth_user_id']
    msg['auth_user_id'] = u_id

    # Assign the message into msg['message']
    msg['message'] = message

    #
    dt = datetime.now(timezone.utc)
    timestamp = int(dt.replace(tzinfo = timezone.utc).timestamp())
    msg['time_created'] = timestamp 
    
    # Insert dictionary 'msg' into the channel['messages']
    curr_channel['messages'].insert(0,msg)

    # Return the message_id
    return {
        'message_id': msg['message_id']
    }
    '''
    return {
        'message_id': 1,
    }
    '''

def message_remove_v1(token, message_id):
    ''' 
    This function is to remove the specific message with the same message_id inside channel['messages'].
        
    Arguments:
        token - the user ID of the members
        message_id (int) - the ID of the message

    Exceptions:
        InputError - Occurs when the messages are not exists.
        AccessError - Occurs when the message's auth_user_id is not the same with the user's auth_user_id and 
                    - Occurs when the user who making this request are not the owner of the channel or the dream owner

    Return Value:
        None
    '''

    # Get the user['auth_user_id']
    u_id = helper.valid_token(token)

    # Assign new variables to check
    valid_msg_id = False
    valid_owner = False
    
    # Looped through the data['channels']
    # Looped through the channel['messages']
    # Find the message with the same message_id and the input message_id
    # Assign the channel['channel_id] into chan_id
    # If the message_id is exist, assign valid_msg_id to True
    # Find the message['auth_user_id] with the same user's auth_user_id
    # If the message's auth_user_id is the same with the user's auth_user_id, assign valid_owner to True
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                chan_id = channel['channel_id']
                valid_msg_id = True
                if message['auth_user_id'] == u_id:
                    valid_owner = True
                    break

    # If message_id is not exist, it raise InputError
    if valid_msg_id == False:
        raise InputError("Message no longer exists!")

    # If the owner of the message is not the same with the auth_user_id from input token,
    # It raise AccessError
    if valid_owner == False:
        raise AccessError("Not Authorised User!")

    # Looped through the data['channels']
    # Find the channel with the same channel_id
    # Assign the channel into curr_chan
    for channel in data['channels']:
        if channel['channel_id'] == chan_id:
            curr_chan = channel

    # Looped through the channel['messages']
    # Find the message with the same message_id
    # Remove the message
    for message in curr_chan['messages']:
        if message['message_id'] == message_id:
            curr_chan['messages'].remove(message)

    # Return None
    return {
    }

def message_edit_v1(token, message_id, message):
    ''' 
    This function is to modified the message inside channels['messages'] with the same input message_id.
        
    Arguments:
        token - the user ID of the members
        message_id (int) - the ID of the message
        message - the input message

    Exceptions:
        InputError  - Occurs when the length of the message exceed 1000.
                    - Occurs when the message_id is not exists
        AccessError - Occurs when the message's auth_user_id is not the same with the user's auth_user_id 
                    - Occurs when the user who making this request are not the owner of the channel or the dream owner

    Return Value:
        None
    '''
    # Get the user['auth_user_id']
    u_id = helper.valid_token(token)

    # Assign new variables to check
    valid_msg_id = False
    valid_owner = False

    # Looped through the data['channels']
    # Looped through the channel['messages']
    # Find the message with the same message_id and the input message_id
    # Assign the channel['channel_id] into chan_id
    # If the message_id is exist, assign valid_msg_id to True
    # Find the message['auth_user_id] with the same user's auth_user_id
    # If the message's auth_user_id is the same with the user's auth_user_id, assign valid_owner to True
    for channel in data['channels']:
        for msg in channel['messages']:
            if msg['message_id'] == message_id:
                chan_id = channel['channel_id']
                valid_msg_id = True
                if msg['auth_user_id'] == u_id:
                    valid_owner = True
                    break

    # Raise Input Error when:
    # - the message_id does not exists
    # - Length of the message exceed 1000
    if valid_msg_id == False:
        raise InputError("Message no longer exists!")
    if len(message) > 1000:
        raise InputError("Message too long!")

    # Raise AccessError when:
    # - the owner's auth_user_id of the message is not the same as the token's auth_user_id.
    if valid_owner == False:
        raise AccessError("Not Authorised User!")

    # If the message is empty, it remove the message
    if message == "":
        message_remove_v1(token, message_id)
        return {}

    # Else,
    # Looped through the data['channels']
    # Find the channel with the same channel_id
    # Assign the channel into curr_chan
    # Looped throught the curr_chan['message']
    # Find the msg with the same message_id
    # Assign the input message to msg['message']
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
