from src.error import InputError, AccessError
<<<<<<< HEAD
from data import data
from src.helper import (check_valid_user, valid_token, valid_channel, check_existing_owner, 
check_dreams_owner, save_data, update_user_stats, generate_token, search_user_data)
=======
from src.data import data
from src.helper import (check_valid_user, valid_token, valid_channel, 
check_existing_owner, check_dreams_owner, save_data, update_user_stats, generate_token)
>>>>>>> master

def channel_invite_v2(token, channel_id, u_id):
    """
    This function invites the user to given channel. 
    On success, add the user data to the channel.

    Arguments:
        token (string) - Input token which signify that an authorised and
                          valid user is requesting for this information
        channel_id (int) - the ID of the channel to invite a user to
        u_id (int) - the ID of the user being invited to the channel

    Exceptions:
        InputError - Occurs when u_id or channel_id is invalid.
        AccessError - Occurs when the authorised user is not a member of the channel
                      or the authorised user is invalid or the authorised user is 
                      inviting someone already in the channel.
    Return Value:
        Returns an empty dictionary on completeion
    """
    # Check token validity
    auth_user_id = valid_token(token)

    # Flags to check for invalid input or invalid access
    valid_channel = False
    valid_uid = False
    ismember = False

    new_member = {}
    # Loop to check if user id is valid and store that user info
    for user in data["users"]:
        if user["auth_user_id"] == u_id:
            valid_uid = True
            new_member["auth_user_id"] = user["auth_user_id"]
            break

    # Raise exception for invalid u_id
    if valid_uid == False:
        raise InputError(description = "u_id is not valid user")

    # Loop to check if channel id is valid
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel = True

            # Loop to check if auth_user_id is a member of channel
            for member in channel["all_members"]:
                if member["auth_user_id"] == auth_user_id:
                    ismember = True
                    break
            # Loop to check if u_id is already in channel
            for member in channel["all_members"]:
                if member["auth_user_id"] == u_id:
                    raise AccessError(description = "Repetitive invite! This u_id already in channel")

            break

    # Raise exception when detect invalid access/input
    if valid_channel == False:
        raise InputError(description = "channel_id is not a valid channel")
    if ismember == False:
        raise AccessError(description = "authorised user not a member of channel")

    # Loop over the target channel and add u_id into channel
    for channel in data["channels"]:
        if channel_id == channel["channel_id"]:
            channel["all_members"].append(new_member)

    myUserToken = generate_token(u_id)
    update_user_stats(myUserToken, 'channels_joined', 1) # update the user's stats

    # Writes data to file for persistence
    save_data(data)
        
    return {
    }

def channel_details_v2(token, channel_id):

    ''' 
    This function is to return the detail of a channel that includes
        channel name, the owners data and the all members data 
        
    Arguments:
        token () - the user ID of the members
        channel_id (int) - the ID of the channel

    Exceptions:
        InputError - Occurs when u_id or channel_id is invalid.
        AccessError - Occurs when the authorised user is not a member of the channel
                      or the authorised user is invalid or the authorised user is 
                      inviting someone already in the channel.
    Return Value:
        Returns a dictionary dictionary that includes channel name, 
        the owners data and the members data
    '''

    # Assign new variables to check
    valid_channel = False
    is_member = False

    # Assign new lists
    owners_list = []
    members_list = []

    # Assign new dictionary details
    channel_details = {}
    
    # Find the auth_user_id from input token
    auth_user_id = valid_token(token)

    # Loops to check if channel is in data file by looking from the channel_id
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            valid_channel = True
            # Assign the channel with the right channel_id into channel_data
            channel_data = channel
            # Loops to check if member is in data file by looking from the auth_user_id
            for member in channel['all_members']:
                print(channel)
                if member['auth_user_id'] == auth_user_id:
                    is_member = True
                    break
            break
    
    # Raise error message if channel is not valid or if user is not a member
    if valid_channel == False:
        raise InputError("Channel ID is not a valid channel")
    if is_member == False:
        raise AccessError("Authorised user is not a member of channel")
    
    # Assign the channel name into new dictionary channel_details
    channel_details['name'] = channel_data['name']
    
    channel_details['is_public'] = channel_data['is_public']

    # Loops through the owner_members in channel data
    # Calling the search_user_data to return the user data and assign it into owner
    # Append the user data into the list owners_list
    # Add the list owners_list into new dictionary channel_details
    for id_owner in channel_data["owner_members"]:
        owner = search_user_data(id_owner)
        owners_list.append(owner)
    channel_details['owner_members'] = owners_list

    # Loops through the all_members in channel data
    # Calling the search_user_data to return the user data and assign it into member
    # Append the user data into the list members_list
    # Add the list members_list into new dictionary channel_details
    for id_member in channel_data["all_members"]:
        member = search_user_data(id_member)
        members_list.append(member)
    channel_details['all_members'] = members_list

    # Writes data to file for persistence
    save_data(data)
    
    # return the new dictionary
    return(channel_details)
    
def channel_messages_v2(token, channel_id, start):

    ''' 
    This function is to return the upto 50 messages between start and end  
        
    Arguments:
        auth_user_id (int) - the user ID of the members
        channel_id (int) - the ID of the channel
        start (int) - the start of an index

    Exceptions:
        InputError - Occurs when u_id or channel_id is invalid.
        InputEror - Occurs when the start index is greater than the total number of messages
        AccessError - Occurs when the authorised user is not a member of the channel
                      or the authorised user is invalid or the authorised user is 
                      inviting someone already in the channel.

    Return Value:
        Returns a dictionary return_msg that includes the message details, index start and the index end
    '''

    # Assign new variables to check
    valid_channel = False
    is_member = False

    # Assign new list msg
    msg = []
    
    # Assign new variables
    end = start + 50
    count = 0
    msg_counter = 0

    # Find the auth_user_id from input token
    auth_user_id = valid_token(token)

    # Loops to check if channel is in data file by looking from the channel_id
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel = True
            # Assign the channel with the right channel_id into channel_data
            channel_data = channel
            # Loops to check if member is in data file by looking from the auth_user_id
            for member in channel["all_members"]:
                if member["auth_user_id"] == auth_user_id:
                    is_member = True
                    break
            break
            
    # Raise error message if channel is not valid or if user is not a member
    if valid_channel == False:
        raise InputError("Channel ID is not a valid channel")
    if is_member == False:
        raise AccessError("Authorised user is not a member of channel")

    # Return Error if start position is greater than messages in data
    if start > len(channel_data['messages']):
        raise InputError("Input Error! start > messages")

    # Length of the message in the channel
    len_message = len(channel['messages'])
    
    # Loops through the channel messages
    for message in channel['messages']:
        if count < end:
            msg.append(message)
            msg_counter += 1
        count += 1

    # Return -1 if the function returned the least recent message in the channel
    # to indicate there are no more messages to load after this return.
    if len_message == start + msg_counter:
        end = -1

    # Return the message, start, and end
    return_msg = {'messages':msg, 'start': start, 'end':end}
    
    # Writes data to file for persistence
    save_data(data)

    return(return_msg)

def channel_leave_v1(token, channel_id):
    '''
    This argument removes an user from a channel, stripping them of their member
    status and owner status. As the instructions do not specify, we assume that 
    the last member/owner of the channel can also leave
    Arguments:
        token (string) - an input token that validates a session
        channel_id (integer) - the id number of the channel the user, who is 
                               to be removed, belongs to          
    Exceptions:
        InputError  - Occurs if the channel ID is not of a valid channel

        AccessError - Occurs when the authorised user (the one who is inputting
                      the token) is not a member of the channel 
    
    Return Value:
        Returns an empty dictionary
    ''' 
    # Check if the token user and channel are both valid
    auth_user = valid_token(token)
    valid_channel(channel_id)
    
    # Check if the authorised user is a member of the channel and if so remove 
    # them. Assume that this user can be removed even if they are the last owner
    # or member 
    
    leaving_user = {"auth_user_id": auth_user}    
    for channel in data["channels"]:
        if channel_id == channel["channel_id"]:
            # Remove the user from the owner_members if they are an owner
            for owner in channel["owner_members"]:
                # If they are the only user, raise an InputError
                if leaving_user == owner:
                    channel['owner_members'].remove(leaving_user)
                    break
            # Remove the user from the all_members list
            member_valid = False
            for member in channel['all_members']:  
                if leaving_user == member: 
                    channel['all_members'].remove(leaving_user)
                    member_valid = True
                    break
    # Raise an AccessError if this user does not belong to the group 
    if member_valid == False:
        raise AccessError("Authorised user is not a member in the channel")
    # Decrease the number of channels joined by the user
    update_user_stats(token, 'channels_joined', -1) 
    # Save data for persistence
    save_data(data)
    return {
    }
    
def channel_join_v2(token, channel_id):
    """
    This function adds a auth_user_id to a
    channel_id provided.

    Arguments:
        token (string) - Input token which signify that an authorised and
                          valid user is requesting for this information
        channel_id (int) - the ID of the channel the user want to join

    Exceptions:
        InputError - Occurs when channel_id is invalid.
        AccessError - Occurs when the authorised user is not a valid ID or 
                      the authorised user is joining a private channel without
                      being a global DREAM owner or the authorised user is joining
                      a channel he is already in
    Return Value:
        Returns an empty dictionary on completeion
    """
    # Check token validity
    auth_user_id = valid_token(token)

    # Flags to check for invalid input or invalid access
    valid_channel = False
    new_user_info = {}

    # Loop to store user info
    for user in data["users"]:
        if user["auth_user_id"] == auth_user_id:
            global_permission = user["permission_id"]
            new_user_info["auth_user_id"] = user["auth_user_id"]
            break

    # Loop to check if channel id is valid and store channel privacy
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel = True
            channel_privacy = channel["is_public"]

            # Loop to check if member is already in channel 
            for member in channel["all_members"]:
                if member["auth_user_id"] == auth_user_id:
                    raise AccessError("Repetitive join! You are already a member of channel !")
            break

    # Raise excpetion when detect invalid channel
    if not valid_channel:
        raise InputError("invalid channel ID")

    # Check if the auth_user_id has permission to join channel
    if global_permission == 1 or channel_privacy:
        for channel in data["channels"]:
            if channel["channel_id"] == channel_id:
                channel["all_members"].append(new_user_info)
    else:
        raise AccessError("channel ID refer to a private channel")
    # Increase the number of channels joined by the user
    update_user_stats(token, 'channels_joined', 1)
    # Writes data to file for persistence
    save_data(data)

    return {
    }

def channel_addowner_v1(token, channel_id, u_id):
    '''
    With the arguments of a token, channel_id and u_id, this function adds a
    new owner to a channel if the authorised user is a Dreams/channel owner
    Arguments:
        token (string) - an input token that suggests that a session is open
        channel_id (integer) - an integer id that tracks the channel that data
                               is being adjusted in  
        u_id (integer) - authorised user id of a second user [will be added]                            
    Exceptions:
        InputError  - Occurs if the channel ID is not of a valid channel
                    - Occurs if the u_id that the function is trying to add 
                      belongs to an existing owner  
        AccessError - Occurs when the token is invalid and doesn't belong to the
                      group
                    - Occurs when the authorised user (the one who is inputting
                     the token) is not an owner of Dreams or the channel 
    
    Return Value:
        Returns an empty dictionary
    ''' 
    # Check if the token and channel are both valid
    auth_user = valid_token(token)
    valid_channel(channel_id)
    # If the user is already an owner, raise an InputError
    if check_existing_owner(u_id, channel_id):
        raise InputError("The user is already an owner of the channel.")
    # Confirms that the authorised user is an owner of Dreams and/or the channel 
    if check_existing_owner(auth_user, channel_id) == False:
         check_dreams_owner(auth_user)
	
	# If the above errors are not raised, add the details of the user into the
	# owner members list
    new_owner = {"auth_user_id": u_id}    
    for channel in data['channels']:	
        if channel["channel_id"] == channel_id:
            channel['owner_members'].append(new_owner)
            break
            
    # Check if the user is not already a member. If they haven't been added to 
    # the members list (flag is false), append them to the list
    member_valid = False # Flag
    for member in channel['all_members']:
        if u_id == member['auth_user_id']: 
            member_valid = True	
            break 	
	
    if member_valid == False:
        channel['all_members'].append(new_owner)
        # if they aren't already a member, update their user stats to reflect
        # another channel joined
        update_user_stats(token, 'channels_joined', 1) # update the user's stats 
           
    # Save data for persistence
    save_data(data)    
    # Return an empty dictionary
    return {
    }

def channel_removeowner_v1(token, channel_id, u_id):
    '''
    With the arguments of a token, channel_id and u_id, this function removes an
    owner from a channel if the authorised user is a Dreams/channel owner
    Arguments:
        token (string) - input token which gives users access to use a session
        channel_id (integer) - id for the channel that information is being 
                               removed from
        u_id (integer) - authorised user id of the user who will be removed  
    Exceptions:
        InputError  - Occurs if the channel ID is not of a valid channel
                    - Occurs if the u_id does not belong to an already existing                   
                      owner
                    - Occurs if the u_id is the only owner of the channel 
        AccessError - Occurs when the token is invalid and doesn't belong to the
                      authorised tokens
                    - Occurs when the authorised user (the one who is inputting
                     the token) is not an owner of Dreams or the channel 
    
    Return Value:
        Returns an empty dictionary
    ''' 

    # Confirm the token and channel are both valid
    auth_user = valid_token(token)
    valid_channel(channel_id)
    # Checks that the u_id belongs to an owner of the channel 
    if check_existing_owner(u_id, channel_id) == False:
        raise InputError("The user is not an owner of the channel.")
    # Confirms that the authorised user is an owner of Dreams and/or the channel 
    if check_existing_owner(auth_user, channel_id) == False:
         check_dreams_owner(auth_user)
    
    # Loop through the channels and if the channel_id matches, remove the owner
    # from the channel. 
    removed_owner = {"auth_user_id": u_id}    
    for channel in data["channels"]:
        if channel_id == channel["channel_id"]:
            for owner in channel["owner_members"]:
                # If they are the only user, raise an InputError
                if owner["auth_user_id"] == u_id and len(channel["owner_members"]) == 1:
                    raise InputError("The owner is the only channel owner")
                elif removed_owner == owner:
                    channel['owner_members'].remove(removed_owner)
                    break
    # Save data for persistence
    save_data(data)
    
    # Return an empty dictionary
    return {
    }
