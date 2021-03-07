import pytest

from src.channels import channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1, auth_login_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# Test to ensure that an InputError is raised after calling the function 
# auth_login_v1 after clearing 
def test_clear_user():
    # Register a user using valid information and add it to the storage file 
    # under data['users']
    auth_register_v1('john.smith@yahoo.com', 'smithjohn', 'john', 'smith')
    
    # Call the clear function to remove the information from above data['users']
    clear_v1()  
    # An InputError is expected to be raised when the auth_login_v1 function is 
    # called as the email and password are no longer valid. 
    with pytest.raises(InputError):
        auth_login_v1('john.smith@yahoo.com', 'smithjohn')

# Test to ensure that an AccessError is raised when channels_create_v1 is called
# after clearing        
def test_clear_channels():
    # Register a valid user and extract their auth_user_id from the dictionary 
    authorised_dict = auth_register_v1('jane.doe@gmail.com', 'janedoe2021', 
                       'jane', 'doe')
    authorised_token = authorised_dict['auth_user_id']
    # Create a channel and store it into channels['users']
    channels_create_v1(authorised_token, "Channel0", True) 
    
    # Clear the function to remove this information from the data['users']
    clear_v1()
    
    # Raise an AccessError if channels_create is called with an unauthorised 
    # user
    with pytest.raises(AccessError):
        channels_create_v1(authorised_token, 'Channel1', True)
       
    

        
