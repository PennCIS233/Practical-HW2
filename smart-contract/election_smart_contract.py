from pyteal import *
from pyteal_helper import itoa

# APPROVAL PROGRAM handles the main logic of the application

def approval_program():
    i = ScratchVar(TealType.uint64) # i-variable for for-loop
    
    
    on_creation = Seq(
        [

            # Check number of required arguments are present
            # Store relevant parameters of the election. When storing the options to vote for, consider storing all of them as a string separated by commas e.g: "A,B,C,D". Note that index-wise, A=0, B=1, C=2, D=3
            # Set all initial vote tallies to 0 for all vote options, keys are the vote options
            For(
                
            ).Do(
                
            ),
            

            Return(Int(1)),
        ]
    )

    # call to determine whether the current transaction sender is the creator
    is_creator = Txn.sender() == App.globalGet(Bytes("Creator"))
    # value of whether or not the sender can vote ("yes", "no", or "maybe")
    get_sender_can_vote = App.localGetEx(Int(0), App.id(), Bytes("can_vote"))

    # get_vote_sender is a value that the sender voted for, a number indicating index in the VoteOptions string faux-array.
    # Remember that since we stored the election's voting options as a string separated by commas (such as "A,B,C,D"),
    # if a user wants to vote for C, then the choice that the user wants to vote for is equivalent to "3".
    get_vote_of_sender = App.localGetEx(Int(0), App.id(), Bytes("voted"))
    

    # CLOSE OUT: 
    # Removes the user's vote from the correct vote tally if the user closes out of program before the end of the election. 
    # Check that the voter is still in the election period and has actually voted. If so, update vote tally by subtracting one vote for whom the user voted for.
    on_closeout = Seq(
        [
            

            Return(Int(1))
        ]
    )

    # REGISTRATION:
    # Check users are registering before the end of the election period and set user's voting status to "maybe"
    on_register = Seq(

        Return(Int(1))
    )

    # UPDATE USER LOGIC: 
    # Fetch the creator's decision to approve or reject a user acccount and update user's voting status accordingly. 
    # Only the creator can approve or disapprove users and users can only be approved before the election ends. 
    # Think about how the given user's address and creator's decision are stored 
    on_update_user_status = Seq(

        Return(Int(1))
    )

    # USER VOTING LOGIC: 
    # This logic is responsible for casting an account's vote. 

    # STEP 1: check that the election isn't over and that user is allowed to vote using get_sender_can_vote. 

    # STEP 2: check using get_vote_of_sender to check if the user has already voted. If so, return a 0. 
    # Otherwise, get the choice that the user wants to vote for from the application arguments.

    # STEP 3: Update the vote tally for the user's choice under the corresponding global variables.
    # STEP 4: Record the user has successfully voted by writing the choice they voted for to the user's "voted" key to reflect their choice. 
    # Make sure that the vote choice is within index bounds of the vote options. 
    choice = Btoi(Txn.application_args[1])
    on_vote = Seq(
        [
            

            Return(Int(1))
        ]
    )

    # PART 1: Main Conditional
    # This logic allows the contract to choose which operation to run based on how the contract is called. 
    # For example, if Txn.application_id() is 0, then the on_creation sequence will run. 
    # If Txn.on_completion() is OnComplete.OptIn, the on_register sequence will run. We've completed the first few cases. 
    
    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        [Txn.on_completion() == OnComplete.OptIn, on_register],
        # TODO: Complete the cases that will trigger the update_user_status and on_vote sequences. 
    )

    return program

# CLEAR STATE PROGRAM 
# This handles the logic of when an account clears its participation in a smart contract. 
def clear_state_program():
    get_vote_of_sender = App.localGetEx(Int(0), App.id(), Bytes("voted"))

    # Just like the close_out sequence, ensure the user clears state of program before the end of voting period
    # remove their vote from the correct vote tally
    program = Seq(
        [
        

            Return(Int(1))
        ]
    )

    return program


if __name__ == "__main__":
    with open("vote_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled)

    with open("vote_clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled)
