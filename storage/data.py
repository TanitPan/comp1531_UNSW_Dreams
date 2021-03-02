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