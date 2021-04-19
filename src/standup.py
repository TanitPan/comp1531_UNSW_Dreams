''' This file implements standup_start, standup_active and standup_send'''

from data import data
from src.error import InputError, AccessError
from src.helper import valid_token, save_data, valid_member, valid_channel, save_data
import time
from datetime import datetime, timedelta, timezone
import threading

# Global variable that contains all the messages in the buffered queue
message_queue = []

def standup_start_v1(token, channel_id, length):
    ''' 
    This function begins the standup process, where messsages, if they are 
    attempted to be sent, are buffered and delayed for a length of time. 
    In the meantime, they shall be added to the message queue.
    Arguments:
        token (string)   - an encoded token that signals a session has been
                           opened for a valid user who has logged in
        channel_id (int) - the unique identification number of a channel
        length (int)     - the length of time that a standup is active for
                                                  
    Exceptions:
        InputError  - Channel ID does not belong to a channel in the data list
                    - There is an attempt to start a standup when an already 
                      active standup is in use
        AccessError - Occurs when the token is invalid and it belongs to an
                      unauthorised user
                    - Occurs when the token belongs to an user who is not a 
                      member of the channel
    
    Return Value:
        Returns an integer (UNIX timestamp) by tracking the seconds since the 
        UTC standard
    '''
    # Checks for a valid token and channel_id and that the user is a member of 
    # the channel
    user_id = valid_token(token)
    valid_channel(channel_id)
    valid_member(user_id, channel_id)
    
    # Obtains the current time by calling datetime_now
    start_time = datetime.now()
    # Adds the inputted length to the start time to calculate the finish_time
    finish_time = start_time + timedelta(seconds = length)
    # Checks if a standup is currently running in the channel and, if so, raises
    # an error
    return_value = standup_active_v1(token, channel_id)
    if return_value["is_active"]:
        raise InputError("An active standup is currently running in this channel")   
    
    # Loops through the standups and it adds or edits the information of the 
    # length, starting and finishing times, having converted it to an isoformat. 
    # Otherwise, this information is appended to data list as a dictionary 
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["standups"]["length"] = length
            channel["standups"]["start_time"] = start_time.isoformat()
            channel["standups"]["finish_time"] = finish_time.isoformat()
    # Saves data
    save_data(data)
   
    # Returns the integer conversion of the timestamp, having converted it to an
    # UTC timestamp
    # Source: https://www.tutorialspoint.com/How-to-convert-Python-date-to-Unix-timestamp
    time_finish = int(finish_time.replace(tzinfo=timezone.utc).timestamp())
    return {"time_finish": time_finish}

def standup_active_v1(token, channel_id):
    '''
    This function checks if there is a currently running standup by looking at 
    the global variable and returns when the standup will finish. 
    Arguments:
        token (string)   - a code that a user will receive after logging into a
                           session
        channel_id (int) - a channel's unique identification code
                                                  
    Exceptions:
        InputError  - Occurs when the channel ID belongs to a channel not in the 
                      channels list in the data frame
        AccessError - Occurs when the token belongs to an user who is not 
                      unauthorised
                      
    Return Value:
        Returns a dictionary containing a Boolean is_active value, which checks 
        if the standup is active. If true, it returns an integer UTC timestamp. 
        If false, it returns None.
    '''
    # Confirm that the channel id and token are valid, and have been included
    # in the data frame
    valid_token(token)    
    channel_id = int(channel_id) # Convert to an integer
    valid_channel(channel_id)
    return_value = {} # empty dictionary to store values
    is_active = False # Flag

    # If a channel_id matches the channel_id passed in, check if the current time 
    # is more recent than the expected finish time. If so, change the is_active
    # value to True
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            # Firstly checks if the finish time has been added to the llist
            if "finish_time" in channel["standups"]:
                if datetime.now() < datetime.fromisoformat(
                channel["standups"]["finish_time"]):
                    is_active = True
                    finish_time = datetime.fromisoformat(
                        channel["standups"]["finish_time"])            
    
    # Add the is_active response to the dictionary as a key
    return_value["is_active"] = is_active
    # If is_active is true, the value of the finish time will be the converted
    # UTC timestamp. Else, it will be equal to None. Add it to the dictionary
    if return_value["is_active"]:
        return_value["time_finish"] = int(
            finish_time.replace(tzinfo=timezone.utc).timestamp())
    else:
        return_value["time_finish"] = None
    # Return the is_active and finish_time values in a dictionary
    return return_value

def add_message_from_queue(channel_id):
    # Import global variable and make a copy of it      
    global message_queue
    message_list = message_queue.copy()
    # If the channel id associated with a message matches the inputted 
    # channel id, add this message to the channel using the following function and
    # remove it from the queue
    for message_value in message_list:
        if int(message_value["channel_id"]) == int(channel_id):
            add_message_to_channel(message_value)
            message_queue.remove(message_value)

def add_message_to_channel(arg):
    """ Function to add a message to a channel, and save it in the data list for
    persistence-> will replace with messages_send once it has been created"""
    # Extracts the message itself, user_id and channel_id
    message_text = arg["message"]
    user_id = arg["user_id"]
    channel_id = arg["channel_id"]
    # Loops through the code and checks all messages_id to ensure there are no
    # repetitions. Iteratively increases the current message id at the end to 
    # ensure it hasn't already been used to comply with the repo instructions
    message_id = 0
    for channel in data["channels"]:
        message_list = channel["messages"]
        if len(message_list) > 0:
            for message in message_list:
                if int(message["message_id"]) > int(message_id):
                    message_id = int(message["message_id"])
    message_id += 1
    # Adds the message at the end as a UTC timestamp 
    current_time = datetime.now()
    timestamp = int(current_time.replace(tzinfo=timezone.utc).timestamp())
    for channel in data["channels"]:
        if int(channel["channel_id"]) == int(channel_id):
            new_messages = {
                "message_id" : message_id, 
                "message" : message_text,
                "timestamp" : timestamp,
                "auth_user_id": user_id,
            }
            channel["messages"].append(new_messages)
    # Saves data to the data file and returns an empty dictionary
    save_data(data)
    return {}

def standup_send_v1(token, channel_id, message):
    '''
    If there is an active standup in a particular channel, this function queues 
    messages to be sent once the time has expired.
    Arguments:
        token (string)   - code received by the user in an active session
        channel_id (int) - the unique identifier of a channel
        message (string) - the new message the user wishes to send in the chat
                                                  
    Exceptions:
        InputError  - Occurs when the channel ID belongs to a channel not in the 
                      data frame
                    - Happens also when a message string is over 1000 characters
                      in length
                    - Could also be produced when a standup is not running in
                      the channel           
        AccessError - Occurs when the token belongs to an unauthorised user
                    - Occurs when the token is passed in by a user who is not a
                      member of the channel 
                      
    Return Value:
        Returns an empty dictionary '''
    # Test for valid inputs, by confirming the token is valid and belongs to
    # one person who is a member of the valid channel
    user_id = valid_token(token)
    valid_channel(channel_id)
    valid_member(user_id, channel_id)
    
    # Confirms that the standup is active, otherwise, raises an error
    return_value = standup_active_v1(token, channel_id)
    if not return_value["is_active"]:
        raise InputError("There is no active standup running in this channel")
    
    # Checks the length of the message string, raising an error if it exceeds
    # 1000 characters
    if len(message) > 1000:
        raise InputError("The message is more than 1000 characters in length")
    
    # To find the buffered length of time, loop through the channels and find
    # the one that matches the inputted channel_id. 
    length = 0
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            # Check the data time of the expected finish time and subtract the
            # time between the finish time and now, returning the length in
            # seconds          
            if datetime.now() < datetime.fromisoformat(channel["standups"]["finish_time"]):
                end_time = datetime.fromisoformat(channel["standups"]["finish_time"])
                time_difference = end_time - datetime.now()
                length = int(time_difference.total_seconds())
    
    # Finds the UTC timestamp and adds to the dictionary of message arguments,
    # along with user_id, channel_id and the message itself
    current_time = datetime.now()
    timestamp = int(current_time.replace(tzinfo=timezone.utc).timestamp())        
    messages_arguments = {
        "user_id": user_id, 
        "channel_id": channel_id, 
        "message": message, 
        "timestamp": timestamp}
    
    # Calls the global variable and checks if a message from the current channel
    # has already been added to it. If it has, the flag becomes False
    global message_queue
    start_thread = True # flag
    for queue in message_queue:
        if int(queue["channel_id"]) == int(channel_id):
            start_thread = False
            break
            
    # If the length of time is over 0, append the messages argument to the
    # global variable [this is done in both scenarios-> there is already a 
    # message in the queue belonging to this channel or not]
    if length > 0:
        message_queue.append(messages_arguments)
        # If nothing from the channel_list has been added to that queue, start 
        # the threading timer and pass this into the queue function above
        # Note, the threading process also indirectly captures anything sent to
        # the channel after the first message and will also publish it in time
        if start_thread:           
            t = threading.Timer(length, add_message_from_queue, [channel_id])
            t.start()    
    # Otherwise, directly add it to the queue
    else:
        add_message_to_channel(messages_arguments)
    # In both cases, 
    return {}
