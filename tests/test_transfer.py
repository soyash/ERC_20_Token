import brownie

def test_sender_balance_decreases(accounts, Token):
    sender_balance = Token.balanceOf(accounts[0])
    amount = sender_balance // 4

    Token.transfer(accounts[1], amount, {'from': accounts[0]})

    assert Token.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(accounts, Token):
    receiver_balance = Token.balanceOf(accounts[1])
    amount = Token.balanceOf(accounts[0]) // 4

    Token.transfer(accounts[1], amount, {'fomr':accounts[0]})

    assert Token.balanceOf(accounts[1]) == receiver_balance + amount


def test_total_supply_not_affected(accounts, Token):
    total_supply = Token.totalSupply()
    amount = Token.balanceOf(accounts[0])

    Token.transfer(accounts[1], amount, {'from':accounts[0]})

    assert total_supply == Token.totalSupply()


def test_returns_true(accounts, Token):
    amount = Token.balanceOf(accounts[0])
    result = Token.transfer(accounts[1], amount, {'from':accounts[0]})

    assert result.return_value is True


def test_transfer_full_balance(accounts, Token):
    amount = Token.balanceOf(accounts[0])
    receiver_balance = Token.balanceOf(accounts[1])

    Token.transfer(accounts[1], amount, {'from':accounts[0]})

    assert Token.balanceOf(accounts[0]) == 0
    assert Token.balanceOf(accounts[1]) == receiver_balance + amount


def test_transfer_zero_tokens(accounts, Token):
    sender_balance = Token.balanceOf(accounts[0])
    receiver_balance = Token.balanceOf(accounts[1])

    Token.transfer(accounts[1], 0, {'from':accounts[0]})

    assert Token.balanceOf(accounts[0]) == sender_balance
    assert Token.balanceOf(accounts[1]) == receiver_balance


def test_transfer_to_self(accounts, Token):
    sender_balance = Token.balanceOf(accounts[0])
    amount = Token.balanceOf(accounts[0]) // 3

    Token.transfer(accounts[0], amount, {'from':accounts[0]})

    assert Token.balanceOf(accounts[0]) == sender_balance


def test_insufficient_balance(accounts, Token):
    balance = Token.balanceOf(accounts[0])
    
    with brownie.reverts():
        Token.transfer(accounts[0], balance + 1, {'from':accounts[0]})


def test_transfer_event_fires(accounts, Token):
    amount = Token.balanceOf(accounts[0])
    tx = Token.transfer(accounts[1], amount, {'from':accounts[0]})

    assert len(tx.events) == 1
    assert tx.events['Transfer'].values() == [accounts[0], accounts[1], amount]