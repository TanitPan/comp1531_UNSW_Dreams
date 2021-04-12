''' This file implements standup_start, standup_active and standup_send'''

from data import data
from src.error import InputError, AccessError
from src.helper import valid_token, save_data, valid_member, valid_channel
import time
from datetime import datetime, timedelta, timezone

# Created a global list, which would keep a list of the standups 
standups = []

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
    global standups     # Calls the global variable 
    # Checks if a standup is currently running in the channel and, if so, raises
    # an error
    return_value = standup_active_v1(token, channel_id)
    if return_value["is_active"]:
        raise InputError("An active standup is currently running in this channel")   
    
    updated_standup = False # Flag
    # Loops through the standups and if a standup exists for this channel, it 
    # edits the information of the length, starting and finishing times. 
    # Otherwise, this information is appended to the standup as a dictionary 
    for standup in standups:
        if standup["channel_id"] == channel_id:
            standup["length"] = length
            standup["start_time"] = start_time
            standup["finish_time"] = finish_time
            updated_standup = True
    if not updated_standup:
        standup = {"length": length, "channel_id": channel_id,
            "start_time": start_time, "finish_time": finish_time}
        standups.append(standup)
    
    # Returns the integer conversion of the timestamp, having converted it to an
    # UTC timestamp
    # Source: https://www.tutorialspoint.com/How-to-convert-Python-date-to-Unix-timestamp
    time_finish = int(finish_time.replace(tzinfo=timezone.utc).timestamp())
    return {time_finish}

def standup_active_v1(token, channel_id):
    ''' 
    This function checks if there is a currently running standup by looking at 
    the global variable and returns when the standup will finish. 
    Arguments:
        token (string)   - a code that a user will receive aafter logging into a
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
    valid_channel(channel_id)
    global standups # Call the global variable
    return_value = {} # empty dictionary to store values
    is_active = False # Flag

    # If a standup matches the channel_id passed in, check if the current time 
    # is more recent than the expected finish time. If so, change the is_active
    # value to True
    for standup in standups:
        if standup["channel_id"] == channel_id:
            if datetime.now() < standup["finish_time"]:
                is_active = True
                finish_time = standup["finish_time"]
    # Add the is_active response to the dictionary as a key
    return_value["is_active"] = is_active
    # If is_active is true, the value of the finish time will be the converted
    # UTC timestamp. Else, it will be equal to None. Add it to the dictionary
    if return_value["is_active"]:
        return_value["finish_time"] = int(
            finish_time.replace(tzinfo=timezone.utc).timestamp())
    else:
        return_value["finish_time"] = None
    # Return the is_active and finish_time values in a dictionary
    return return_value