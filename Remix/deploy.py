import json
from web3 import Web3
from solcx import compile_standard

# from dotenv import load_dotenv
# load_dotenv()

with open("./1_SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)


print("Compiling & constructing contract...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            },
        },
    },
    solc_version="0.8.0",
)

with open("./compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(
    Web3.HTTPProvider("https://goerli.infura.io/v3/99bf48c800e34825b48c8c248518d606")
)
chain_id = 5
my_address = "0x1Dae6E95bc485aE1d571e77db0454BB16655B926"
private_key = "0xbfdac0757e8daf9e5ff8d5acfebec7bb58d448646288378ca7692002872f2799"  # Add 0x at front (hexadecimal)
# os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

# Transaction: Build -> Sign -> Send
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
nonce += 1  # nonce can only used once for each transaction()
print("Compile & construct success!")


print("Deploying contract...")
# Optional (for private key safeness): Add private key to environment variable.
# Or using .env (python-dotenv)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")


# Contract interaction
# Two basic info to intereact with
# Contract address & Contract ABI
simple_storage = w3.eth.contract(
    address=tx_receipt.contractAddress, abi=abi
)  # Optional: load abi from external .json or .py

# Ways of interact
# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change
print(
    simple_storage.functions.retrieve().call()
)  # return defined return written in .sol

store_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
nonce += 1
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
tx_hash_store = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt_store = w3.eth.wait_for_transaction_receipt(tx_hash_store)

print(simple_storage.functions.retrieve().call())
