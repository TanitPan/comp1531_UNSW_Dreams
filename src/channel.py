from src.error import InputError, AccessError

# channelData = {
#         "33":{'name': 'Hayden',
#             'owner_members': [
#                 {
#                     'u_id': 1,
#                     'name_first': 'Hayden',
#                     'name_last': 'Jacobs',
#                 }
#             ],
#             'all_members': [
#                 {
#                     'u_id': 1,
#                     'name_first': 'Hayden',
#                     'name_last': 'Jacobs',
#                 }
#             ],}
#         }

# users = [{"u_id":2, "name_first": "Mark", "name_last": "Smith"}]
data = { 

    'users' : [
    { 

	    'auth_user_id' : 1, 

	    'name_first' : 'john', 

	    'name_last' : 'smith', 

        'handle_str' : 'johnsmith??', 

	    'email': 'johnsmith@gmail.com', 

	    'password': 'pass123', 

        'permission_id'  : 1, #1 for owner, 2 for member 
    },
    { 

	    'auth_user_id' : 2, 

	    'name_first' : 'Mike', 

	    'name_last' : 'Potato', 

        'handle_str' : 'potatomike??', 

	    'email': 'potatomike@gmail.com', 

	    'password': 'pass123', 

        'permission_id'  : 2, #1 for owner, 2 for member 
    }

    ], 

    'channels' : [
    {      

		'channel_id' :  1, 

		'name' :  'channel0', 

		'owner_members' : [
            { 

                'auth_user_id' : 1, 

                'name_first' : 'john', 

                'name_last' : 'smith', 

                'handle_str' : 'johnsmith??', 

                'email': 'johnsmith@gmail.com', 

                'password': 'pass123', 

                'permission_id' : 1, #1 for owner, 2 for member 
            }

        ], 

        'all_members' : [
            { 

                'auth_user_id' : 1, 

                'name_first' : 'john', 

                'name_last' : 'smith', 

                'handle_str' : 'johnsmith??', 

                'email': 'johnsmith@gmail.com', 

                'password': 'pass123', 

                'permission_id'  : 1, #1 for owner, 2 for member 
            }
            
        ], 

        'is_public' :  True, # Assumed to default to public 
    }
    ], 

}

def channel_invite_v1(auth_user_id, channel_id, u_id):
    # global channelData
    
    # Get the channels that auth_user_id is part of
    valid_channel = False
    valid_uid = False
    ismember = False
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel = True
            for member in channel["all_members"]:
                if member["auth_user_id"] == auth_user_id:
                    ismember = True
                    break
            break
    if valid_channel == False:
        raise InputError("channel_id is not a valid channel")
    if ismember == False:
        raise AccessError("authorised user not a member of channel")

    for user in data["users"]:
        if user["auth_user_id"] == u_id:
            valid_uid = True
            break
    if valid_uid == False:
        raise InputError("u_id is not valid user")


    # add_flag = False
    # belong_channel = [{"ch_id": 1, "name": "channel1"}, {"ch_id": 33, "name": "channel2"}]
    name = ""
    last = ""
    new_member = {}
    # for channel in belong_channel:
    #     if channel_id == channel["ch_id"]:
    #         add_flag = True

    for user in data["users"]:
        if user["auth_user_id"] == u_id:
            new_member = user

    
    for channel in data["channels"]:
        if channel_id == channel["channel_id"]:
            channel["all_members"].append(new_member)
        

    # print(data)
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

# channel_invite_v1(1, 1, 2)
print("HELLO")