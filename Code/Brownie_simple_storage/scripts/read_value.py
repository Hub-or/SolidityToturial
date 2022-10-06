from brownie import accounts, config, SimpleStorage, network

network.priority_fee("auto")

# cmd
# brownie console
# everything import in script will automatically import into command line
# (Python shell with all smartcontract features)


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
    sp = SimpleStorage[-1]  # latest deployment
    # ABI & Address
    print(sp.retrieve())


def main():
    read_contract()
