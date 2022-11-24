import pytest

@pytest.mark.parametrize('idx', range(5))
def test_initial_approve_is_zero(accounts, Token, idx):
    assert Token.allowance(accounts[0], accounts[idx]) == 0


def test_approve(accounts, Token):
    Token.approve(accounts[1], 100, {'from':accounts[0]})

    assert Token.allowance(accounts[0], accounts[1]) == 100


def test_modify_approve(accounts, Token):
    Token.approve(accounts[1], 100, {'from':accounts[0]})
    Token.approve(accounts[1], 200, {'from':accounts[0]})

    assert Token.allowance(accounts[0], accounts[1]) == 200

def test_revoke_approve(accounts, Token):
    Token.approve(accounts[1], 100, {'from':accounts[0]})
    Token.approve(accounts[1], 0, {'from':accounts[0]})

    assert Token.allowance(accounts[0], accounts[1]) == 0

def test_approve_self(accounts, Token):
    Token.approve(accounts[0], 100, {'from':accounts[0]})

    assert Token.allowance(accounts[0], accounts[0]) == 100

def test_only_affects_target(accounts, Token):
    Token.approve(accounts[1], 100, {'from':accounts[0]})

    assert Token.allowance(accounts[1], accounts[0]) == 0

def test_returns_true(accounts, Token):
    tx = Token.approve(accounts[1], 100, {'from':accounts[0]})

    assert tx.return_value is True

def test_approval_event_fires(accounts, Token):
    tx = Token.approve(accounts[1], 100, {'from':accounts[0]})

    assert len(tx.events) == 1
    assert tx.events['Approval'].values() == [accounts[0], accounts[1], 100]