from algosdk.future import transaction
from algosdk import account, mnemonic
from secrets import account_mnemonics
from election_params import local_ints, local_bytes, global_ints, \
    global_bytes

# Define keys, addresses, and token
account_private_keys = [mnemonic.to_private_key(mn) for mn in account_mnemonics]
account_addresses = [account.address_from_private_key(sk) for sk in account_private_keys]

# Declare application state storage for local and global schema
global_schema = transaction.StateSchema(global_ints, global_bytes)
local_schema = transaction.StateSchema(local_ints, local_bytes)



def create_app(client, private_key, approval_program, clear_program, global_schema, local_schema, app_args):
    """
    Create a new application
    """
    # TODO: define sender as creator
    # TODO: declare the on_complete transaction as a NoOp transaction
    # TODO: get node suggested parameters
    # TODO: create unsigned transaction
    # TODO: sign transaction
    # TODO: send transaction
    # TODO: await confirmation

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response["application-index"]
    print("Created new app-id:", app_id)

    return app_id


def deploy_create_app(client, creator_private_key, election_end, num_vote_options, vote_options):
    """
    Deploy the application that was created
    """
    # TODO:
    # Get PyTeal approval program
    # compile program to TEAL assembly
    # compile program to binary
    # Do the same for PyTeal clear state program
    # TODO: Create list of bytes for application arguments and create new application. 

    app_id = None

    return app_id


def main():
    # TODO: Initialize algod client and define absolute election end time fom the status of the last round.
    # TODO: Deploy the app and print the global state.

    pass


if __name__ == "__main__":
    main()
