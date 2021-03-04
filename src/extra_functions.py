from src.error import InputError, AccessError
#from src.auth import auth_register_v1
#import data

def check_valid_user(auth_user_id, authorised_users):
    valid_user_id = False
    #authorised_users = data.data['users']
    for user in authorised_users:
        if user['auth_user_id'] == auth_user_id :
            valid_user_id = True
            break
    if valid_user_id == False:
        raise AccessError("The auth_user_id input is not a valid id.")

