import base64
import datetime

import algosdk
from algosdk.encoding import decode_address, encode_address
from algosdk.future import transaction
from algosdk import account, mnemonic
from algosdk.v2client import algod
from pyteal import compileTeal, Mode
from election_smart_contract import approval_program, clear_state_program
from secrets import account_mnemonics, algod_headers, algod_address
import election_params
from election_params import relative_election_end, num_vote_options, vote_options, local_ints, local_bytes, global_ints, global_bytes

''' Each Algorand account can only create 10 apps unless apps are deleted. To create more voting smart contracts or test smart contract create app functionalities more than 10 times, 
use this script to delete previously created apps. Uncomment the last few lines of this script to either delete a specific app or all apps from a user's account.'''

'''------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

# Define keys, addresses, and token
account_private_keys = [mnemonic.to_private_key(mn) for mn in account_mnemonics]
account_addresses = [account.address_from_private_key(sk) for sk in account_private_keys]


algod_client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers=algod_headers
)
''' TODO: Fill in to define account to delete apps from and app_id of app to delete''' 

creator_mnemonic = "your mnemonic"
app_id = 0 # app id for the app you want to delete

creator_private_key = mnemonic.to_private_key(creator_mnemonic)
creator_address = account.address_from_private_key(creator_private_key)



# DELETE SPECIFIC APPLICATION
def delete_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationDeleteTxn(sender, params, index)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Deleted app-id:", transaction_response["txn"]["txn"]["apid"])


# DELETE ALL APPS 
def delete_all_apps(client, creator_address, private_key):
    results = client.account_info(creator_address)
    apps_created = results["created-apps"]
    for app in apps_created:
        delete_app(client, private_key, app["id"])



'''------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

# UNCOMMENT BELOW TO DELETE APP 
# this following line deletes the specified app_id, 
# delete_app(algod_client, creator_private_key, app_id)

# this following code deletes all the apps the creator has created, use with caution!! Uncomment if you want to do this
# delete_all_apps(algod_client, creator_address, creator_private_key)

