channelData = {
        "33":{'name': 'Hayden',
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
            ],}
        }

users = [{"u_id":2, "name_first": "Mark", "name_last": "Smith"}]

def channel_invite_v1(auth_user_id, channel_id, u_id):
    # global channelData
    # Get the channels that auth_user_id is part of
    add_flag = False
    data = [{"ch_id": 1, "name": "channel1"}, {"ch_id": 33, "name": "channel2"}]
    name = ""
    last = ""
    for channel in data:
        if channel_id == channel["ch_id"]:
            add_flag = True
    if add_flag:
        for user in users:
            if user["u_id"] == u_id:
                name = user["name_first"]
                last = user["name_last"]
        print("GGGGGGGGGGGGGGGGGGGGGGGGGG")
        new_member = {"u_id": u_id,"name_first": name, "name_last":last}
        temp_dict = channelData[str(channel_id)]
        temp_dict["all_members"].append(new_member) 
        print(channelData)
        print("In IF statement")
        # for elem in channel:
        #     if ()
    print("Outside of IF")
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

# channel_invite_v1(1, 33, 2)
# print("HELLO")