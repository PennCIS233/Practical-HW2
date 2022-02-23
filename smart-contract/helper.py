"""
Helper functions useful to compile, create, read state of, ... apps
"""

import base64

from algosdk.v2client import algod


def compile_program(client: algod, source_code: str) -> bytes:
    """
    Compile the program source code and return the resulting bytecode
    """
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])


def wait_for_confirmation(client: algod, tx_id: str):
    """
    Wait for confirmation of a given transaction ID
    """
    last_round = client.status().get("last-round")
    tx_info = client.pending_transaction_info(tx_id)
    while not (tx_info.get("confirmed-round") and tx_info.get("confirmed-round") > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        tx_info = client.pending_transaction_info(tx_id)
    print(
        "Transaction {} confirmed in round {}.".format(
            tx_id, tx_info.get("confirmed-round")
        )
    )
    return tx_info


def wait_for_round(client: algod, round: int):
    last_round = client.status().get("last-round")
    print(f"Waiting for round {round}")
    while last_round < round:
        last_round += 1
        client.status_after_block(last_round)
        print(f"Round {last_round}")


def int_to_bytes(i: int):
    """
    Convert a 64-bit integer i to byte string
    """
    return i.to_bytes(8, "big")


def format_state(state):
    """
    Format state assuming all keys and values are string
    """
    formatted = {}
    for item in state:
        key = item["key"]
        value = item["value"]
        formatted_key = base64.b64decode(key).decode("utf-8")
        if value["type"] == 1:
            # byte string
            formatted_value = base64.b64decode(value["bytes"]).decode("utf-8")
            formatted[formatted_key] = formatted_value
        else:
            # integer
            formatted[formatted_key] = value["uint"]
    return formatted


def read_local_state(client, addr, app_id):
    """
    Read user local state assuming all keys and values are string
    """
    results = client.account_info(addr)
    for local_state in results["apps-local-state"]:
        if local_state["id"] == app_id:
            if "key-value" not in local_state:
                return {}
            return format_state(local_state["key-value"])
    return {}


def read_global_state(client, app_id):
    """
    Read global state assuming all keys and values are string
    """
    app = client.application_info(app_id)
    if "global-state" in app["params"]:
        return format_state(app["params"]["global-state"])
    return {}
