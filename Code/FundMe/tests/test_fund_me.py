import pytest
from brownie import exceptions

from scripts.tools import *
from scripts.deploy import deploy

def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy()

    entrance_fee = fund_me.getEntranceFee() + 10
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account) == entrance_fee

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_ENVIRONMENTS:
        pytest.skip("For local tests only.")
    fund_me = deploy()

    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})