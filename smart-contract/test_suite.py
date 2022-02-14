# based off https://github.com/algorand/docs/blob/cdf11d48a4b1168752e6ccaf77c8b9e8e599713a/examples/smart_contracts/v2/python/stateful_smart_contracts.py

# this file is meant to test smart contract implementations

import base64
import datetime
import unittest
import time

import algosdk
from algosdk.encoding import decode_address, encode_address
from algosdk.future import transaction
from algosdk import account, mnemonic
from algosdk.v2client import algod
from pyteal import compileTeal, Mode
from election_smart_contract import approval_program, clear_state_program

from secrets import account_mnemonics, algod_token

account_private_keys = [mnemonic.to_private_key(mn) for mn in account_mnemonics]
account_addresses = [account.address_from_private_key(sk) for sk in account_private_keys]

# user declared account mnemonics
# creator_mnemonic = ENV.accountMnemonics[0]
# user_mnemonic = "enjoy face require vibrant fun detect solid divert police gasp clown entire vital mandate soccer ready oven proud breeze key mountain civil number absent whale"
# creator_mnemonic = "jelly move shuffle prevent vocal garden escape leave obvious shop ostrich lecture filter cake lamp strategy swim keen marble abstract inspire wife fossil about lamp"
# user_address = "ZY2RCEOGP5YTCTY2SW4UZ272VBZB2B3DYIG22JLBXSTFS3RTT67IZCZZV4"
# decoded_user_address = decode_address('ZY2RCEOGP5YTCTY2SW4UZ272VBZB2B3DYIG22JLBXSTFS3RTT67IZCZZV4')
# print("decoded")

# user declared algod connection parameters. Node must have EnableDeveloperAPI set to true in its config
algod_address = "https://testnet-algorand.api.purestake.io/ps2"


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


# create new application
def create_app(
        client,
        private_key,
        approval_program,
        clear_program,
        global_schema,
        local_schema,
        app_args,
):
    # define sender as creator
    sender = account.address_from_private_key(private_key)

    # declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationCreateTxn(
        sender,
        params,
        on_complete,
        approval_program,
        clear_program,
        global_schema,
        local_schema,
        app_args,
    )

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response["application-index"]
    print("Created new app-id:", app_id)

    return app_id


# opt-in to application
def opt_in_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)
    print("OptIn from account: ", sender)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationOptInTxn(sender, params, index)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("OptIn to app-id:", transaction_response["txn"]["txn"]["apid"])


def call_app_approve_voter(client, index, creator_private_key, user_address, yes_or_no_bytes):
    # user_address = app_args[1]
    app_args = [b"update_user_status", decode_address(user_address), yes_or_no_bytes]
    # declare sender
    sender = account.address_from_private_key(creator_private_key)

    print("Call from account:", sender)

    # get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(sender, params, index, app_args, accounts=[sender, user_address])

    # sign transaction
    signed_txn = txn.sign(creator_private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)
    transaction_response = client.pending_transaction_info(tx_id)
    print("Approved user ", user_address, "for apid ", transaction_response, ": ", yes_or_no_bytes)


# call application
def call_app(client, private_key, index, app_args):
    # declare sender
    sender = account.address_from_private_key(private_key)
    print("Call from account:", sender)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(sender, params, index, app_args)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)


def format_state(state):
    formatted = {}
    for item in state:
        key = item["key"]
        value = item["value"]
        formatted_key = base64.b64decode(key).decode("utf-8")
        if value["type"] == 1:
            # byte string
            if formatted_key in ["VoteOptions", "can_vote"]:
                formatted_value = base64.b64decode(value["bytes"]).decode("utf-8")
            elif formatted_key == "Creator":
                formatted_value = encode_address(base64.b64decode(value["bytes"]))
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


# delete application
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


# close out from application
def close_out_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationCloseOutTxn(sender, params, index)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Closed out from app-id: ", transaction_response["txn"]["txn"]["apid"])

# close out from application
def clear_state_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationClearStateTxn(sender, params, index)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Clear state from app-id: ", transaction_response["txn"]["txn"]["apid"])


# clear application
def clear_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationClearStateTxn(sender, params, index)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Cleared app-id:", transaction_response["txn"]["txn"]["apid"])


# convert 64 bit integer i to byte string
def intToBytes(i):
    return i.to_bytes(8, "big")


def test_create_app(client, creator_private_key, election_end, num_vote_options, vote_options):
    # declare application state storage (immutable)
    local_ints = 1  # user's voted variable
    local_bytes = 1  # user's can_vote variable
    global_ints = (
        24  # 3 for setup + x for choices. Use a larger number for more choices.
    )
    global_bytes = 2  # Creator and VoteOptions variables
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    # get PyTeal approval program
    approval_program_ast = approval_program()
    # compile program to TEAL assembly
    approval_program_teal = compileTeal(
        approval_program_ast, mode=Mode.Application, version=5
    )
    # compile program to binary
    approval_program_compiled = compile_program(client, approval_program_teal)

    # get PyTeal clear state program
    clear_state_program_ast = clear_state_program()
    # compile program to TEAL assembly
    clear_state_program_teal = compileTeal(
        clear_state_program_ast, mode=Mode.Application, version=5
    )
    # compile program to binary
    clear_state_program_compiled = compile_program(
        client, clear_state_program_teal
    )

    # create list of bytes for app args
    app_args = [
        intToBytes(election_end),
        intToBytes(num_vote_options),
        vote_options
    ]

    # create new application
    app_id = create_app(
        client,
        creator_private_key,
        approval_program_compiled,
        clear_state_program_compiled,
        global_schema,
        local_schema,
        app_args,
    )

    # read global state of application
    # print(
    #     "Global state:",
    #     read_global_state(
    #         client, account.address_from_private_key(creator_private_key), app_id
    #     ),
    # )

    return app_id

def approveUser():
    return 0

def rejectUser():
    return 0


client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers={"X-API-Key": algod_token}
)

class TestElection1(unittest.TestCase):

    def test_01_create_election(self):
        print(f"Running test 1")
        relative_election_end = 5000
        # app args
        status = client.status()
        election_end = status["last-round"] + relative_election_end
        num_vote_options = 4
        vote_options = "BTC,ETH,USDT,ALGO"
        points = 0  # points for grading purposes

        # test smart contract creation with large election end time
        try:
            TestElection1.app_id = test_create_app(client, account_private_keys[0], election_end, num_vote_options, vote_options)
        except:
            print('App creation failed')
            raise 'App creation failed'
        time.sleep(1)
        # check global variables setup
        global_state = read_global_state(client, account_addresses[0], TestElection1.app_id)
        self.assertEqual(global_state["Creator"], account_addresses[0], "Creator variable is NOT correct")
        self.assertEqual(global_state["VoteOptions"], vote_options, "VoteOptions variable is NOT correct")
        self.assertEqual(global_state["ElectionEnd"], election_end, "ElectionEnd variable is NOT correct")
        for i in range(0, 4):
            self.assertEqual(global_state[f"VotesFor{i}"], 0, f"VotesFor{i} not initialized to 0")


    def test_02_opt_in(self):
        # test user opt-in (5 users, creator + 4 others)
        for i in range(0, 6):
            opt_in_app(client, account_private_keys[i], TestElection1.app_id)
            local_state = read_local_state(client, account_addresses[i], TestElection1.app_id)
            self.assertEqual(local_state["can_vote"], "maybe", f"User {i}'s can_vote not set to 'maybe'")
            time.sleep(0.5)

    def test_03_maybe_users_cant_vote(self):
        for i in range(0, 2):
            app_args = [b"vote", i.to_bytes(8, 'big')]
            self.assertRaises(
                Exception,
                call_app,
                client,
                account_private_keys[i],
                TestElection1.app_id,
                app_args
            )
            time.sleep(0.5)

    def test_04_deny_users(self):
        for i in range(4, 6):
            call_app_approve_voter(
                client=client,
                index=TestElection1.app_id,
                creator_private_key=account_private_keys[0],
                user_address=account_addresses[i],
                yes_or_no_bytes=b"no"
            )
            time.sleep(0.5)
            local_state = read_local_state(client, account_addresses[i], TestElection1.app_id)
            self.assertEqual("no", local_state["can_vote"], f"Denied user's can_vote should be 'no'!")
            time.sleep(0.5)

    def test_05_denied_users_cant_vote(self):
        for i in range(4, 6):
            app_args = [b"vote", (i-3).to_bytes(8, 'big')]
            self.assertRaises(
                Exception,
                call_app,
                client,
                account_private_keys[i],
                TestElection1.app_id,
                app_args
            )
            time.sleep(0.5)

    def test_06_approve_users(self):
        for i in range(0, 4):
            call_app_approve_voter(
                client=client,
                index=TestElection1.app_id,
                creator_private_key=account_private_keys[0],
                user_address=account_addresses[i],
                yes_or_no_bytes=b"yes"
            )
            time.sleep(1)
            local_state = read_local_state(client, account_addresses[i], TestElection1.app_id)
            self.assertEqual("yes", local_state["can_vote"], f"Approved user's can_vote should be 'yes'!")
            time.sleep(1)

    def test_07_creator_cant_double_approve(self):
        for i in range(0, 6):
            yes_no_bytes = b"no" if i < 4 else b"yes"
            self.assertRaises(
                Exception,
                call_app_approve_voter,
                client,
                TestElection1.app_id,
                account_private_keys[0],
                account_addresses[i],
                yes_no_bytes
            )
            time.sleep(1)

    def test_08_approved_users_can_vote(self):
        for i in range(0, 3):
            app_args = [b"vote", i.to_bytes(8, 'big')]
            call_app(client, account_private_keys[i], TestElection1.app_id, app_args)
            time.sleep(1)

            local_state = read_local_state(client, account_addresses[i], TestElection1.app_id)
            print(f"User {i}")
            print(local_state)
            self.assertEqual(i, local_state["voted"], f"Wrong vote in user's voted variable")
            time.sleep(1)

            global_state = read_global_state(client, account_addresses[0], TestElection1.app_id)
            for j in range(0, 4):
                self.assertEqual(1 if i >= j and j != 3 else 0, global_state[f"VotesFor{j}"])

        # have user 3 vote for choice 1 (testing 2 votes for same option)
        app_args = [b"vote", (1).to_bytes(8, 'big')]
        call_app(client, account_private_keys[3], TestElection1.app_id, app_args)
        time.sleep(1)
        local_state = read_local_state(client, account_addresses[3], TestElection1.app_id)
        print(f"User {3}")
        print(local_state)
        self.assertEqual(1, local_state["voted"], f"Wrong vote in user's voted variable")
        time.sleep(1)

        global_state = read_global_state(client, account_addresses[0], TestElection1.app_id)
        print(global_state)
        self.assertEqual(1, global_state[f"VotesFor{0}"])
        self.assertEqual(2, global_state[f"VotesFor{1}"])
        self.assertEqual(1, global_state[f"VotesFor{2}"])
        self.assertEqual(0, global_state[f"VotesFor{3}"])

    # this tests that users that already voted cannot vote again
    def test_09_approved_users_cant_vote_twice(self):
        # ensure that transactions that would be voting twice don't go through
        for i in range(0, 4):
            app_args = [b"vote", i.to_bytes(8, 'big')]
            self.assertRaises(
                Exception,
                call_app,
                client,
                account_private_keys[i],
                TestElection1.app_id,
                app_args
            )
            time.sleep(1)

        # ensure user's local variables have stayed the same
        local_state = read_local_state(client, account_addresses[0], TestElection1.app_id)
        self.assertEqual(0, local_state["voted"], f"Wrong vote in user's voted variable")
        time.sleep(0.5)
        local_state = read_local_state(client, account_addresses[1], TestElection1.app_id)
        self.assertEqual(1, local_state["voted"], f"Wrong vote in user's voted variable")
        time.sleep(0.5)
        local_state = read_local_state(client, account_addresses[2], TestElection1.app_id)
        self.assertEqual(2, local_state["voted"], f"Wrong vote in user's voted variable")
        time.sleep(0.5)
        local_state = read_local_state(client, account_addresses[3], TestElection1.app_id)
        self.assertEqual(1, local_state["voted"], f"Wrong vote in user's voted variable")
        time.sleep(0.5)

        # ensure the votes have stayed the same as they were in test_08
        global_state = read_global_state(client, account_addresses[0], TestElection1.app_id)
        self.assertEqual(1, global_state[f"VotesFor{0}"])
        self.assertEqual(2, global_state[f"VotesFor{1}"])
        self.assertEqual(1, global_state[f"VotesFor{2}"])
        self.assertEqual(0, global_state[f"VotesFor{3}"])

    # test closeout functionality on approved user 1, note: this happens before the election end
    def test_10_approved_user_closeout(self):
        close_out_app(client, account_private_keys[1], TestElection1.app_id)
        time.sleep(1)

        global_state = read_global_state(client, account_addresses[0], TestElection1.app_id)
        print(global_state)
        self.assertEqual(1, global_state[f"VotesFor{0}"])
        self.assertEqual(1, global_state[f"VotesFor{1}"]) # used to be 2, now is 1
        self.assertEqual(1, global_state[f"VotesFor{2}"])
        self.assertEqual(0, global_state[f"VotesFor{3}"])
        time.sleep(1)

    # test clear_state functionality on approved user 2, note: this happens before the election end
    def test_11_approved_user_clearstate(self):
        clear_state_app(client, account_private_keys[2], TestElection1.app_id)
        time.sleep(1)

        global_state = read_global_state(client, account_addresses[0], TestElection1.app_id)
        print(global_state)
        self.assertEqual(1, global_state[f"VotesFor{0}"])
        self.assertEqual(1, global_state[f"VotesFor{1}"])  # (happens in test 10) used to be 2, now is 1
        self.assertEqual(0, global_state[f"VotesFor{2}"])  # used to be 1, now is 0
        self.assertEqual(0, global_state[f"VotesFor{3}"])
        time.sleep(1)

    # test closeout functionality on rejected user 4, note: this happens before the election end
    # closeout of rejected user 4 should not change the global state
    def test_12_denied_user_closeout(self):
        close_out_app(client, account_private_keys[4], TestElection1.app_id)
        time.sleep(1)

        global_state = read_global_state(client, account_addresses[0], TestElection1.app_id)
        print(global_state)
        self.assertEqual(1, global_state[f"VotesFor{0}"])
        self.assertEqual(1, global_state[f"VotesFor{1}"])
        self.assertEqual(0, global_state[f"VotesFor{2}"])
        self.assertEqual(0, global_state[f"VotesFor{3}"])
        time.sleep(1)

    # test clear_state functionality on rejected user 5, note: this happens before the election end
    # clearstate of rejected user 5 should not change the global state
    def test_13_denied_user_clearstate(self):
        clear_state_app(client, account_private_keys[5], TestElection1.app_id)
        time.sleep(1)

        global_state = read_global_state(client, account_addresses[0], TestElection1.app_id)
        print(global_state)
        self.assertEqual(1, global_state[f"VotesFor{0}"])
        self.assertEqual(1, global_state[f"VotesFor{1}"])
        self.assertEqual(0, global_state[f"VotesFor{2}"])
        self.assertEqual(0, global_state[f"VotesFor{3}"])
        time.sleep(1)

    # delete the app as cleanup
    def test_99_delete_app(self):
        # delete app
        print(f"Deleting app {TestElection1.app_id}")
        delete_app(client, account_private_keys[0], TestElection1.app_id)
        print(f"App {TestElection1.app_id} Deleted")

if __name__ == '__main__':
    unittest.main()