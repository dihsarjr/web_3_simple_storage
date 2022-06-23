from dis import Bytecode
from itertools import chain
from solcx import compile_standard, install_solc
import json
from web3 import Web3

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
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xc5e1e09B097B4732c92226e81Cd54db3583522Bc"
privet_key = "0x8db7669992aafdee7c22bf6ea6f13c59ea8b36fddb984fb2d62c59793b717a5e"

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
