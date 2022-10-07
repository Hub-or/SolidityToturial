from .tools import *
from brownie import FundMe

# brownie networks add Ethereum ganache-gui host=http://127.0.0.1:7545 chainid=1337


def deploy():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        price_feed_address = deploy_mocks()

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )  # publish_source=True  .get to know errors for unset values
    # print(fund_me)
    return fund_me


def main():
    fund_me = deploy()
    print(fund_me.getPrice())
