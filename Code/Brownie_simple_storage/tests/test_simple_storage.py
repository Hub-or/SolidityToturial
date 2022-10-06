from brownie import accounts, config, SimpleStorage

# -k test_func_name
# --pdb debug while assertion failed  (quit)
# -s more details


def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    stored = simple_storage.retrieve()
    expected = 0
    # Assert
    assert stored == expected


def test_update_storage():
    account = accounts[0]
    sp = SimpleStorage.deploy({"from": account})

    expected = 15
    sp.store(expected, {"from": account})

    assert expected == sp.retrieve()
