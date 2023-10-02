import random
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware
from config import CONFIG, ERC20ABI, private_keys, token_addresses, recipient_addresses
from utils import logger, write_to_file


def send_assets(
    w3,
    private_key,
    recipient_address,
    token_address,
    token_abi,
    amount=0,
    value=0,
    gas_price=0,
    gas_limit=0,
    gas_limit_k=1.05,
    max_amount=False,
    max_value=False
):
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    sender_address = Web3.to_checksum_address(w3.eth.account.from_key(private_key=private_key).address)
    recipient_address = Web3.to_checksum_address(recipient_address)
    token_address = Web3.to_checksum_address(token_address)
    balance = w3.eth.get_balance(sender_address)
    can_send = False

    if balance == 0:
        return

    transaction = {
        "from":  sender_address,
        "to": recipient_address,
        "value": value,
        "nonce": w3.eth.get_transaction_count(sender_address)
    }

    if max_amount:
        amount = w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=token_abi
        ).functions.balanceOf(sender_address).call()

    if amount > 0:
        token_contract = w3.eth.contract(token_address, abi=token_abi)
        transaction = token_contract.functions.transfer(
            recipient_address, amount
        ).build_transaction({
            "from":  sender_address,
            "nonce": w3.eth.get_transaction_count(sender_address)
        })

    if gas_limit == 0:
        gas_limit = int(w3.eth.estimate_gas(transaction) * gas_limit_k)

    if gas_price == 0:
        gas_price = w3.eth.gas_price

    transaction["gas"] = gas_limit
    transaction["gasPrice"] = gas_price
    estimated_transaction_fee = gas_price * gas_limit

    if max_value:
        value = balance - estimated_transaction_fee
        transaction["value"] = value

    if value - estimated_transaction_fee > 0:
        can_send = True

    if can_send:
        try:
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
            txn = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.success(f"sender: {sender_address} | token: {token_address} | amount: {w3.from_wei(amount, 'ether')} | {txn.hex()}")

            return txn
        except Exception as ex:
            logger.error(f"{sender_address} | Error: {ex}")
    
def main():
    logger.success("Начало работы скрипта")
    w3 = Web3(Web3.HTTPProvider(endpoint_uri=CONFIG["rpc_url"]))

    for recipient_address in recipient_addresses:
        for private_key in private_keys:
            sender_address = Web3.to_checksum_address(w3.eth.account.from_key(private_key=private_key).address)
            
            for token_address in token_addresses:
                amount = round(random.uniform(CONFIG["token_amount"]["min"], CONFIG["token_amount"]["max"]), CONFIG["decimal_point"])
                amount_in_wei = w3.to_wei(amount, CONFIG["unit"])
                value = round(random.uniform(CONFIG["value"]["min"], CONFIG["value"]["max"]), CONFIG["decimal_point"])
                value_in_wei = w3.to_wei(value, CONFIG["unit"])
                delay = round(random.uniform(CONFIG["delay"]["min"], CONFIG["delay"]["max"]), 2)

                send_assets(
                    w3,
                    private_key,
                    recipient_address,
                    token_address,
                    ERC20ABI,
                    amount_in_wei,
                    value_in_wei,
                    CONFIG["gas_price"],
                    CONFIG["gas_limit"],
                    CONFIG["gas_limit_k"],
                    CONFIG["max_amount"],
                    CONFIG["max_value"]
                )
                time.sleep(delay)

            write_to_file("data/used-wallets.txt", f"{sender_address}:{private_key}")


if __name__ == "__main__":
    main()