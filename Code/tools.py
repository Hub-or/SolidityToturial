from brownie import accounts, config, network


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        network.priority_fee("auto")
        return accounts.add(config["wallets"]["from_key"])
