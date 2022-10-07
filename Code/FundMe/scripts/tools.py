# from web3 import Web3
from brownie import accounts, config, network, MockV3Aggregator

LOCAL_FORKED_ENVIRONMENTS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-gui"]
LOCAL_ENVIRONMENTS = LOCAL_FORKED_ENVIRONMENTS + LOCAL_BLOCKCHAIN_ENVIRONMENTS

DECIMALS = 8
STARTING_PRICE = 1300 * 10 ** 8


def get_account():
    if network.show_active() in LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        network.priority_fee("auto")
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    # Mock
    print(f"Current active network is {network.show_active()}.")
    if len(MockV3Aggregator) < 3:
        print("Deploying mocks...")
        MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}  # Web3.toWei
        )
        print("Mocks deployed!")
    return MockV3Aggregator[-1]
