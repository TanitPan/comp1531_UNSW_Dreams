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
