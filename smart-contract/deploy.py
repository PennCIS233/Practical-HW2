import base64
import datetime

import algosdk
from algosdk.encoding import decode_address, encode_address
from algosdk.future import transaction
from algosdk import account, mnemonic
from algosdk.v2client import algod
from pyteal import compileTeal, Mode
from election_smart_contract import approval_program, clear_state_program
from secrets import account_mnemonics, algod_token, algod_address
import election_params
from election_params import relative_election_end, num_vote_options, vote_options, local_ints, local_bytes, global_ints, global_bytes

''' Define keys, addresses, and token ''' 
#import ENV # import your own file that has your private keys, mnemonics, etc
account_private_keys = [mnemonic.to_private_key(mn) for mn in account_mnemonics]
account_addresses = [account.address_from_private_key(sk) for sk in account_private_keys]
# user declared algod connection parameters. Node must have EnableDeveloperAPI set to true in its config
algod_address = algod_address
algod_token = algod_token

''' Declare application state storage for local and global schema ''' 
local_ints = local_ints  # user's voted variable
local_bytes = local_bytes  # user's can_vote variable
global_ints = (
    global_ints  # 3 for setup + x for choices. Use a larger number for more choices.
)
global_bytes = global_bytes  # Creator and VoteOptions variables
global_schema = transaction.StateSchema(global_ints, global_bytes)
local_schema = transaction.StateSchema(local_ints, local_bytes)


''' Define election parameters ''' 
relative_election_end = relative_election_end
num_vote_options = num_vote_options
vote_options = vote_options

'''HELPER FUNCTIONS ''' 
# helper function to compile program source
def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])


# helper function that converts a mnemonic passphrase into a private signing key
def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    return private_key


# helper function that waits for a given txid to be confirmed by the network
def wait_for_confirmation(client, txid):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print(
        "Transaction {} confirmed in round {}.".format(
            txid, txinfo.get("confirmed-round")
        )
    )
    return txinfo


def wait_for_round(client, round):
    last_round = client.status().get("last-round")
    print(f"Waiting for round {round}")
    while last_round < round:
        last_round += 1
        client.status_after_block(last_round)
        print(f"Round {last_round}")

# convert 64 bit integer i to byte string
def intToBytes(i):
    return i.to_bytes(8, "big")

'''----------------------------------------TODO-----------------------------------------------'''

''' Implement the functions below that create the logic for every interaction with the smart contract: creation, opt-in, approval, vote '''

# CREATE NEW APPLICATION
def create_app(client, private_key, approval_program, clear_program, global_schema, local_schema, app_args,
):
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


# OPT-IN 
def opt_in_app(client, private_key, index):
    # TODO: declare sender from the private key of the user who opts in
    print("OptIn from account: ", sender)
    # TODO: get node suggested parameters
    # TODO: create unsigned transaction
    # TODO: sign transaction
    # TODO: send transaction
    # TODO: await confirmation

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("OptIn to app-id:", transaction_response["txn"]["txn"]["apid"])

# APPROVE VOTER WHO OPTS IN
def call_app_approve_voter(client, private_key, index, app_args):
    # TODO: Create a transaction that will be called when a creator has to approve a user account to vote. 
    transaction_response = client.pending_transaction_info(tx_id)
    print("Approved user ", user_address, "for apid ", transaction_response, ": ", response)


# CALL VOTING APPLICATION 
def call_app(client, private_key, index, app_args):
    # TODO: Create a transaction that will be called when a user casts their vote.



def format_state(state):
    formatted = {}
    for item in state:
        key = item["key"]
        value = item["value"]
        formatted_key = base64.b64decode(key).decode("utf-8")
        if value["type"] == 1:
            # byte string
            if formatted_key == "VoteOptions":
                formatted_value = base64.b64decode(value["bytes"]).decode("utf-8")
            else:
                formatted_value = value["bytes"]
            formatted[formatted_key] = formatted_value
        else:
            # integer
            formatted[formatted_key] = value["uint"]
    return formatted


# read user local state
def read_local_state(client, addr, app_id):
    results = client.account_info(addr)
    for local_state in results["apps-local-state"]:
        if local_state["id"] == app_id:
            if "key-value" not in local_state:
                return {}
            return format_state(local_state["key-value"])
    return {}


# read app global state
def read_global_state(client, addr, app_id):
    results = client.account_info(addr)
    apps_created = results["created-apps"]
    for app in apps_created:
        if app["id"] == app_id:
            return format_state(app["params"]["global-state"])
    return {}

'''----------------------------------------TODO-----------------------------------------------'''
# DELETE APPLICATION
def delete_app(client, private_key, index):
    # TODO: Create transaction that gets called when the application is deleted.

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Deleted app-id:", transaction_response["txn"]["txn"]["apid"])


# CLOSE OUT OF APPLICATION
def close_out_app(client, private_key, index):
    # TODO: Create transaction that gets called when the application is closed out of. 

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Closed out from app-id: ", transaction_response["txn"]["txn"]["apid"])


# CLEAR APPLICATION
def clear_app(client, private_key, index):
    # TODO: Create transaction that gets called when the application gets cleared.

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Cleared app-id:", transaction_response["txn"]["txn"]["apid"])


# DEPLOY APPLICATION THAT WAS CREATED
def deploy_create_app(client, creator_private_key, election_end, num_vote_options, vote_options):
    
    # TODO:
    # Get PyTeal approval program
    # compile program to TEAL assembly
    # compile program to binary
    # Do the same for PyTeal clear state program
    # TODO: Create list of bytes for application arguments and create new application. 
    

    return app_id


def main():
    # TODO: Initialize algod client and define absolute election end time fom the status of the last round. 
    # TODO: Deploy the app and print the global state. 
    


if __name__ == "__main__":
    main()