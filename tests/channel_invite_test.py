import pytest
from src.channel import channel_invite_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from storage.data import data



def test_channel_invite():
    
    # data_users = data["users"].deepcopy()
    # data_channels = data["channels"].deepcopy()
   
    channel_invite_v1(1, 1, 2)
    # channel_invite_v1(1, 1, 21)

   
  
    # print(data_channels)
    print(data["channels"])
    assert data["channels"] == [
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

        'is_public' :  True, # Assumed to default to public 
    }
    ]
  
# Test error for invalid channel
def test_channel_invite_except_channel():
    data['users'].clear()
    data['channels'].clear()
    data['users'] =  [
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

    ]
    data['channels'] = [
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
    ]
    
    

    with pytest.raises(InputError):
        channel_invite_v1(1, 12, 2)
        # assert data["channels"] == [
        # {      

        #     'channel_id' :  1, 

        #     'name' :  'channel0', 

        #     'owner_members' : [
        #         { 

        #             'auth_user_id' : 1, 

        #             'name_first' : 'john', 

        #             'name_last' : 'smith', 

        #             'handle_str' : 'johnsmith??', 

        #             'email': 'johnsmith@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id' : 1, #1 for owner, 2 for member 
        #         }

        #     ], 

        #     'all_members' : [
        #         { 

        #             'auth_user_id' : 1, 

        #             'name_first' : 'john', 

        #             'name_last' : 'smith', 

        #             'handle_str' : 'johnsmith??', 

        #             'email': 'johnsmith@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id'  : 1, #1 for owner, 2 for member 
        #         },
        #         { 

        #             'auth_user_id' : 2, 

        #             'name_first' : 'Mike', 

        #             'name_last' : 'Potato', 

        #             'handle_str' : 'potatomike??', 

        #             'email': 'potatomike@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id'  : 2, #1 for owner, 2 for member 
        #         }
                
        #     ], 

        #     'is_public' :  True, # Assumed to default to public 
        # }
        # ]

# Test error for invalid u_id
def test_channel_invite_except_user():
    data['users'].clear()
    data['channels'].clear()
    data['users'] =  [
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

    ]
    data['channels'] = [
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
    ]
    
    

    with pytest.raises(InputError):
        channel_invite_v1(1, 1, 2222)
        # assert data["channels"] == [
        # {      

        #     'channel_id' :  1, 

        #     'name' :  'channel0', 

        #     'owner_members' : [
        #         { 

        #             'auth_user_id' : 1, 

        #             'name_first' : 'john', 

        #             'name_last' : 'smith', 

        #             'handle_str' : 'johnsmith??', 

        #             'email': 'johnsmith@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id' : 1, #1 for owner, 2 for member 
        #         }

        #     ], 

        #     'all_members' : [
        #         { 

        #             'auth_user_id' : 1, 

        #             'name_first' : 'john', 

        #             'name_last' : 'smith', 

        #             'handle_str' : 'johnsmith??', 

        #             'email': 'johnsmith@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id'  : 1, #1 for owner, 2 for member 
        #         },
        #         { 

        #             'auth_user_id' : 2, 

        #             'name_first' : 'Mike', 

        #             'name_last' : 'Potato', 

        #             'handle_str' : 'potatomike??', 

        #             'email': 'potatomike@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id'  : 2, #1 for owner, 2 for member 
        #         }
                
        #     ], 

        #     'is_public' :  True, # Assumed to default to public 
        # }
        # ]


# Auth_user_id not a member of channel
def test_channel_invite_except_noaccess():
    data['users'].clear()
    data['channels'].clear()
    data['users'] =  [
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

    ]
    data['channels'] = [
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
    ]
    
    

    with pytest.raises(AccessError):
        channel_invite_v1(2, 1, 2)
        # assert data["channels"] == [
        # {      

        #     'channel_id' :  1, 

        #     'name' :  'channel0', 

        #     'owner_members' : [
        #         { 

        #             'auth_user_id' : 1, 

        #             'name_first' : 'john', 

        #             'name_last' : 'smith', 

        #             'handle_str' : 'johnsmith??', 

        #             'email': 'johnsmith@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id' : 1, #1 for owner, 2 for member 
        #         }

        #     ], 

        #     'all_members' : [
        #         { 

        #             'auth_user_id' : 1, 

        #             'name_first' : 'john', 

        #             'name_last' : 'smith', 

        #             'handle_str' : 'johnsmith??', 

        #             'email': 'johnsmith@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id'  : 1, #1 for owner, 2 for member 
        #         },
        #         { 

        #             'auth_user_id' : 2, 

        #             'name_first' : 'Mike', 

        #             'name_last' : 'Potato', 

        #             'handle_str' : 'potatomike??', 

        #             'email': 'potatomike@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id'  : 2, #1 for owner, 2 for member 
        #         }
                
        #     ], 

        #     'is_public' :  True, # Assumed to default to public 
        # }
        # ]


# Test invalid auth_user_id case
def test_channel_invite_except_invalid_auth():
    data['users'].clear()
    data['channels'].clear()
    data['users'] =  [
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

    ]
    data['channels'] = [
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
    ]
    
    
    
    with pytest.raises(AccessError):
        channel_invite_v1(222, 1, 2)
        # assert data["channels"] == [
        # {      

        #     'channel_id' :  1, 

        #     'name' :  'channel0', 

        #     'owner_members' : [
        #         { 

        #             'auth_user_id' : 1, 

        #             'name_first' : 'john', 

        #             'name_last' : 'smith', 

        #             'handle_str' : 'johnsmith??', 

        #             'email': 'johnsmith@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id' : 1, #1 for owner, 2 for member 
        #         }

        #     ], 

        #     'all_members' : [
        #         { 

        #             'auth_user_id' : 1, 

        #             'name_first' : 'john', 

        #             'name_last' : 'smith', 

        #             'handle_str' : 'johnsmith??', 

        #             'email': 'johnsmith@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id'  : 1, #1 for owner, 2 for member 
        #         },
        #         { 

        #             'auth_user_id' : 2, 

        #             'name_first' : 'Mike', 

        #             'name_last' : 'Potato', 

        #             'handle_str' : 'potatomike??', 

        #             'email': 'potatomike@gmail.com', 

        #             'password': 'pass123', 

        #             'permission_id'  : 2, #1 for owner, 2 for member 
        #         }
                
        #     ], 

        #     'is_public' :  True, # Assumed to default to public 
        # }
        # ]

# test_channel_invite()