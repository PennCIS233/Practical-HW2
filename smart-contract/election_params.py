#define parameters for your voting election here

 # You need to declare both local and global ints and bytes for the local and global state schema. 
local_ints = 1  # user's voted variable
local_bytes = 1  # user's can_vote variable
global_ints = (
    24  # 3 for setup + x for choices. Use a larger number for more choices.
)
global_bytes = 2  # Creator and VoteOptions variables

#define an election end period relative to current client status
relative_election_end = 5000
num_vote_options = 4

#define vote options in a string separated by commas without spaces e.g., "BTC,ETH,USDT,ALGO"
vote_options = ""
