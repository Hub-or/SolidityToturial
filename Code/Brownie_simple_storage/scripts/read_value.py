from brownie import accounts, config, SimpleStorage, network

network.priority_fee("auto")


def get_account():
    # account = accounts[0]
    # account = accounts.load("Develop")
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def read_contract():
    account = get_account()
    print(SimpleStorage[0])


def main():
    read_contract()
