import brownie

def test_sender_balance_decreases(accounts, Token):
    sender_balance = Token.balanceOf(accounts[0])
    amount = sender_balance // 4

    Token.approve(accounts[1], amount, {'from':accounts[0]})
    Token.transferFrom(accounts[0], accounts[2], amount, {'from':accounts[1]})

    assert Token.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(accounts, Token):
    receiver_balance = Token.balanceOf(accounts[2])
    amount = Token.balanceOf(accounts[0]) // 4

    Token.approve(accounts[1], amount, {'from':accounts[0]})
    Token.transferFrom(accounts[0], accounts[2], amount, {'from':accounts[1]})

    assert Token.balanceOf(accounts[2]) == receiver_balance + amount


def test_caller_balance_not_affected(accounts, Token):
    caller_balance = Token.balanceOf(accounts[1])
    amount = Token.balanceOf(accounts[0]) // 4

    Token.approve(accounts[1], amount, {'from':accounts[0]})
    Token.transferFrom(accounts[0], accounts[2], amount, {'from':accounts[1]})

    assert Token.balanceOf(accounts[1]) == caller_balance


def test_caller_approval_affected(accounts, Token):
    approval_amount = Token.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    Token.approve(accounts[1], approval_amount, {'from':accounts[0]})
    Token.transferFrom(accounts[0], accounts[2], transfer_amount, {'from':accounts[1]})
    
    assert Token.allowance(accounts[0], accounts[1]) == approval_amount - transfer_amount


def test_receiver_approval_not_affected(accounts, Token):
    approval_amount = Token.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    Token.approve(accounts[1], approval_amount, {'from': accounts[0]})
    Token.approve(accounts[2], approval_amount, {'from': accounts[0]})
    Token.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert Token.allowance(accounts[0], accounts[2]) == approval_amount


def test_total_supply_not_affected(accounts, Token):
    total_supply = Token.totalSupply()
    amount = Token.balanceOf(accounts[0])

    Token.approve(accounts[1], amount, {'from': accounts[0]})
    Token.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert Token.totalSupply() == total_supply


def test_returns_true(accounts, Token):
    amount = Token.balanceOf(accounts[0]) // 4

    Token.approve(accounts[1], amount, {'from':accounts[0]})
    tx = Token.transferFrom(accounts[0], accounts[2], amount, {'from':accounts[1]})

    assert tx.return_value is True


def test_transfer_full_balance(accounts, Token):
    amount = Token.balanceOf(accounts[0])
    receiver_balance = Token.balanceOf(accounts[2])

    Token.approve(accounts[1], amount, {'from': accounts[0]})
    Token.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert Token.balanceOf(accounts[0]) == 0
    assert Token.balanceOf(accounts[2]) == receiver_balance + amount


def test_transfer_zero_tokens(accounts, Token):
    sender_balance = Token.balanceOf(accounts[0])
    receiver_balance = Token.balanceOf(accounts[2])

    Token.approve(accounts[1], sender_balance, {'from': accounts[0]})
    Token.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert Token.balanceOf(accounts[0]) == sender_balance
    assert Token.balanceOf(accounts[2]) == receiver_balance


def test_transfer_zero_tokens_without_approval(accounts, Token):
    sender_balance = Token.balanceOf(accounts[0])
    receiver_balance = Token.balanceOf(accounts[2])

    Token.transferFrom(accounts[0], accounts[2], 0, {'from':accounts[1]})

    assert Token.balanceOf(accounts[0]) == sender_balance
    assert Token.balanceOf(accounts[2]) == receiver_balance


def test_insufficient_balance(accounts, Token):
    amount = Token.balanceOf(accounts[0])

    with brownie.reverts():
        Token.approve(accounts[1], amount + 1, {'from':accounts[0]})
        Token.transferFrom(accounts[0], accounts[2], amount + 1, {'from':accounts[1]})


def test_insufficiest_approval(accounts, Token):
    amount = Token.balanceOf(accounts[0])

    Token.approve(accounts[1], amount - 1, {'from':accounts[0]})
    with brownie.reverts():
        Token.transferFrom(accounts[0], accounts[2], amount, {'from':accounts[1]})


def test_no_approval(accounts, Token):
    balance = Token.balanceOf(accounts[0])

    with brownie.reverts():
        Token.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_revoked_approval(accounts, Token):
    balance = Token.balanceOf(accounts[0])

    Token.approve(accounts[1], balance, {'from': accounts[0]})
    Token.approve(accounts[1], 0, {'from': accounts[0]})

    with brownie.reverts():
        Token.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_transfer_to_self(accounts, Token):
    sender_balance = Token.balanceOf(accounts[0])
    amount = sender_balance // 4

    Token.approve(accounts[0], sender_balance, {'from': accounts[0]})
    Token.transferFrom(accounts[0], accounts[0], amount, {'from': accounts[0]})

    assert Token.balanceOf(accounts[0]) == sender_balance
    assert Token.allowance(accounts[0], accounts[0]) == sender_balance - amount