from .tools import *
from brownie import FundMe

# (depreciated) brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 port=8545 fork='https://mainnet.infura.io/v3/$WEB3_INFURA_PROJECT_ID' accounts=10 mnemonic=brownie
# brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 port=8545 fork=https://eth-mainnet.g.alchemy.com/v2/qQbgVHTy-z72WdCBIsoKBizfsL4b_6Ji accounts=10 mnemonic=brownie


def fund():
    account = get_account()
    fund_me = FundMe[-1]

    # print(fund_me.getPrice())
    entrance_fee = fund_me.getEntranceFee() + 1
    print("Entrance fee is", entrance_fee, "in wei.")
    fund_me.fund({"from": account, "value": entrance_fee})
    print("Fund successful.")


def withdraw():
    account = get_account()
    fund_me = FundMe[-1]
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
