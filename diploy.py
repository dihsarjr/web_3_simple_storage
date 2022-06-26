from dis import Bytecode
from itertools import chain
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
import dotenv


dotenv.load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

# Compile our solidity code
install_solc("0.6.0")
compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
with open("compile_code.json", "w") as file:
    json.dump(compile_sol, file)

# get bytecode
get_bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

print(get_bytecode)

# get API
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
print(abi)

# connecting ganache
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/86b115e6f6504545ae5f280ba39298f7"))
chain_id = 4
my_address = "0x5B2e409171Df217f73B6D4A454B8B5cF15Da9A3d"
private_key = os.getenv("PRIVATE_KEY")
print(private_key)
print("privet key")

# create contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=get_bytecode)
print(SimpleStorage)

nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
print(transaction)
# sign transaction
signed_transaction = w3.eth.account.signTransaction(
    transaction, private_key=private_key
)

# send signed transaction
tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
transaction_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(transaction_receipt)


# working with contract
# get contract address
# contract abi
simple_storage = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
store_transaction = simple_storage.functions.store(42).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_transaction_store = w3.eth.account.signTransaction(store_transaction, private_key=private_key)
transaction_hash_store = w3.eth.sendRawTransaction(signed_transaction_store.rawTransaction)
transaction_receipt_store = w3.eth.waitForTransactionReceipt(transaction_hash_store)
print(simple_storage.functions.retrieve().call())

