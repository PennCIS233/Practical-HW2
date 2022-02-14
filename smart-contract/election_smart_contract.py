from pyteal import *
from pyteal_helper import itoa

'''APPROVAL PROGRAM handles the main logic of the application'''

def approval_program():
    i = ScratchVar(TealType.uint64) # i-variable for for-loop
    
    
    on_creation = Seq(
        [   
            # TODO:
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
    

    # TODO: CLOSE OUT: 
    on_closeout = Seq(
        [
            

            Return(Int(1))
        ]
    )

    # TODO: REGISTRATION:
    on_register = Seq(

        Return(Int(1))
    )

    # TODO: UPDATE USER LOGIC: 
    on_update_user_status = Seq(

        Return(Int(1))
    )

    # TODO: USER VOTING LOGIC: 
    choice = Btoi(Txn.application_args[1])
    on_vote = Seq(
        [
            

            Return(Int(1))
        ]
    )

    ''' TODO: MAIN CONDITIONAL '''
    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        [Txn.on_completion() == OnComplete.OptIn, on_register],
        # TODO: Complete the cases that will trigger the update_user_status and on_vote sequences. 
    )

    return program

''' TODO: CLEAR STATE PROGRAM '''
# This handles the logic of when an account clears its participation in a smart contract. 
def clear_state_program():
    get_vote_of_sender = App.localGetEx(Int(0), App.id(), Bytes("voted"))

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
