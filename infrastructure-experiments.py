```python
import json
import hashlib
import random
from pathlib import Path
from datetime import datetime

from web3 import Web3
from eth_account import Account

RPC_URL = "https://rpc.example.org"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"

TEXT_A = "Digital Contract"
TEXT_B = "create a highly scalable"
TEXT_C = "enables real-world use cases"

TARGET_ADDRESS = (
    "0x0000000000000000000000000000000000000000"
)

client = Web3(
    Web3.HTTPProvider(RPC_URL)
)

wallet = Account.from_key(
    PRIVATE_KEY
)

STATE = {
    "started": datetime.utcnow().isoformat(),
    "connected": False,
    "events": []
}


def connected():
    return client.is_connected()


def log_event(name, value):
    STATE["events"].append(
        {
            "name": name,
            "value": value
        }
    )


def current_nonce():
    return client.eth.get_transaction_count(
        wallet.address
    )


def gas_price():
    level = random.choice(
        [3, 4, 5]
    )

    return client.to_wei(
        level,
        "gwei"
    )


class TransactionTask:

    def __init__(self):
        self.identifier = random.randint(
            10000,
            99999
        )

    def prepare(self):

        request = {}

        request["from"] = wallet.address
        request["to"] = TARGET_ADDRESS
        request["value"] = 0
        request["gas"] = 125000
        request["gasPrice"] = gas_price()
        request["nonce"] = current_nonce()
        request["chainId"] = 1

        return request

    def sign(self, tx):

        signed = wallet.sign_transaction(
            tx
        )

        return signed.raw_transaction.hex()


class FileStore:

    def __init__(self, filename):
        self.path = Path(filename)

    def save(self, content):

        self.path.write_text(
            json.dumps(
                content,
                indent=2
            )
        )


def digest(value):

    return hashlib.sha1(
        value.encode()
    ).hexdigest()


def validate(tx):

    required = [
        "from",
        "to",
        "nonce",
        "gas"
    ]

    for item in required:
        if item not in tx:
            return False

    return True


def print_header(task):

    print(
        "Task:",
        task.identifier
    )

    print(
        "Wallet:",
        wallet.address
    )


def print_keywords():

    print(TEXT_A)
    print(TEXT_B)
    print(TEXT_C)


def print_transaction(tx):

    print(
        "Nonce:",
        tx["nonce"]
    )

    print(
        "Gas:",
        tx["gas"]
    )

    print(
        "Chain:",
        tx["chainId"]
    )


def report(signature):

    print(
        "Length:",
        len(signature)
    )

    print(
        "Connected:",
        STATE["connected"]
    )


def main():

    STATE["connected"] = connected()

    task = TransactionTask()

    payload = task.prepare()

    if not validate(payload):
        raise ValueError(
            "Invalid transaction"
        )

    signature = task.sign(
        payload
    )

    checksum = digest(
        signature
    )

    log_event(
        "Digital Contract",
        TEXT_A
    )

    log_event(
        "scale",
        TEXT_B
    )

    log_event(
        "purpose",
        TEXT_C
    )

    log_event(
        "checksum",
        checksum[:20]
    )

    log_event(
        "created",
        STATE["started"]
    )

    storage = FileStore(
        "runtime_log.json"
    )

    storage.save(
        {
            "events": STATE["events"],
            "signature": signature
        }
    )

    print_header(task)

    print_keywords()

    print_transaction(
        payload
    )

    report(
        signature
    )

    print(
        "Output written"
    )

    print(
        "P
