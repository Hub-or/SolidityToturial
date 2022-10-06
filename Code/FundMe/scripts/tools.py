from web3 import Web3
from brownie import accounts, config, network, MockV3Aggregator

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-gui"]

DECIMALS = 18
STARTING_PRICE = 1300


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        network.priority_fee("auto")
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    # Mock
    print(f"Current active network is {network.show_active()}.")
    if len(MockV3Aggregator) <= 0:
        print("Deploying mocks...")
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
        )
        print("Mocks deployed!")
    return MockV3Aggregator[-1]
