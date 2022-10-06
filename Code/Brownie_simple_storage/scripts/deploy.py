# import os
from brownie import accounts, config, SimpleStorage, network

network.priority_fee("auto")


# cmd
# brownie accounts new (name)
# brownie networks list
# brownie run (script) --network [network]


# account = accounts[0]
# account = accounts.load("Develop")
# account = accounts.add(os.getenv("PRIVATE_KEY"))
# account = accounts.add(config["wallets"]["from_key"])
# print(account)
def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_simple_storage():

    account = get_account()

    simple_storage = SimpleStorage.deploy({"from": account})

    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    stored_value = simple_storage.retrieve()
    print(stored_value)


def main():
    deploy_simple_storage()
