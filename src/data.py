'''
This is the dataframe file used in the project, with dummy data for reference
on variable names and data structure. Data is a dictionary containing 'users',
which is a list of dictionaries, and 'channels', also a list of dictionaries.
'''



'''
data = { 

    'users' : [
    { 

	    'auth_user_id' : 0, 

	    'name_first' : 'john', 

	    'name_last' : 'smith', 

        'handle_str' : 'johnsmith??, 

	    'email': 'johnsmith@gmail.com', 

	    'password': 'pass123', 

        'permission_id'  = 1, #1 for owner, 2 for member 
    }
    ], 

    'channels' : [
    {      

		'channel_id' :  1, # If DM, channel_id = -1

		'name' :  'channel0', 

		'owner_members' : [], 

        'all_members' : [], 

        'is_public' :  True, # Assumed to default to public

        'dm_id' : -1, # If channel, dm_id = -1

        'messages' : [
            {
                'message_id' : 0, # Assume that > 0

                'message' : 'hello world',

                'timestamp' : 12345678, # Do we need this for it 2?

                'auth_user_id' : 0,
            }
        ], 
        'standups' : 
        {
            'length': length,
            
            'start_time': 0, #isoformat
            
            'finish_time': 0 #isoformat
        } 
    }
    ], 

}''' 

data = { 
	'users' : [], 
	'channels' : [],
    'channels_exist': [],
    'dms_exist': [],
    'messages_exist': [], 
} 
