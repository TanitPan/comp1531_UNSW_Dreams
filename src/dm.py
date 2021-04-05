""" 
This file implement dm(direct message) functionality of DREAM
"""
from data import data
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.helper import valid_token, save_data, check_valid_user

def dm_create_v1(token, u_ids):
    auth_id = valid_token(token)
    for u_id in u_ids:
        check_valid_user(u_id)
    
    # Assume the dm id start at 1 and increment it by one for
    # any newdm created
    curr_id = 0
    for channel in data["channels"]:
        if channel["dm_id"] > curr_id:
            curr_id = channel["dm_id"]
    dm_id = curr_id + 1

    curr_message_id = 0
    for channel in data["channels"]:
        for message in channel["messages"]:
            if message["message_id"] > curr_message_id:
                curr_message_id = message["message_id"]
    new_message_id = curr_message_id + 1

    id_list = u_ids.copy()
    id_list.append(auth_id)
    name_list = []
    for item in id_list:
        for user in data["users"]:
            if item == user["auth_user_id"]:
                name_list.append(user["handle_str"])
                break

    name_list.sort()
    dm_name = ",".join(name_list)
    owner_list = [{"auth_user_id": auth_id}]
    all_member_list = []
    owner = {"auth_user_id": auth_id}
    all_member_list.append(owner)
    for member in u_ids:
       all_member_list.append({"auth_user_id": member})

    new_dm = {
        "channel_id": -1, # default value
        "name": dm_name,
        "owner_members": owner_list,
        "all_members": all_member_list,
        "is_public": False, # Assume false since its a dm
        "dm_id": dm_id,
        "messages": [
            {
                "message_id" : new_message_id, # Assume it is greater than 0
                "message" : "",
                "timestamp" : 0,
                "auth_user_id" : auth_id
            }

        ]

    }

    # Append the newly create dm channel to channels
    data["channels"].append(new_dm)
    
    # Writes data to file for persistence
    save_data(data)

    return {"dm_id": dm_id, "dm_name": dm_name}

def dm_list_v1(token):

    auth_id = valid_token(token)
    dm_list = []
    for channel in data["channels"]:
        for member in channel["all_members"]:
            if channel["channel_id"] == -1 and auth_id == member["auth_user_id"]:
                new_dict = {"dm_id": channel["dm_id"], "name": channel["name"]}
                dm_list.append(new_dict)
                break

    return {"dms": dm_list}