Assumptions: 

- When creating new user_ID or channel_ID, the ID will be generated through an 
    iterative process (the new ID will be one greater than the last created ID) 
    to avoid repetitions). 
- A user can be a member of multiple channels simultaneously. 
- Assume that there is only one owner in this iteration + the Dreams owner as we
    do not have a function to add owners.
- Assume that a channel is public by default. 
- Assume that if the authorised user is inviting a user already in channel (including himself),
    AccessError will be raised.
- Assume that if the authorised user is joining a channel he is already a member of, AccessError
    will be raised.
    
Iteration Two
- Assume that the message_id will be iterative and begin at 1
- Assume that a message being sent to a channel is a DM by default (-1)
- Assume that "value permission" means that the permission id is merely an 
  integer rather than the specific (1 or 2) required
- Assume that the last member/owner can leave a channel in channel_leave as
  in channel_removeowner this was explicitly specified as forbidden and in this
  scenario, no mention of it has been added
- Assume channel_addowner allows you to add an owner who is not already a member
