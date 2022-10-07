from brownie import accounts, config, network

LOCAL_FORKED_ENVIRONMENTS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-gui"]
LOCAL_ENVIRONMENTS = LOCAL_FORKED_ENVIRONMENTS + LOCAL_BLOCKCHAIN_ENVIRONMENTS


def get_account():
    if network.show_active() in LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        network.priority_fee("auto")
        return accounts.add(config["wallets"]["from_key"])
