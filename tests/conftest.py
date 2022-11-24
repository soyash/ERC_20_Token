#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def Token(token, accounts):
    return token.deploy("Test Token", "TST", 1000, {'from': accounts[0]})

@pytest.fixture(scope="module")
def TokenSale(tokenSale, accounts, Token):
    ts = tokenSale.deploy(Token.address, '1 ether', {'from':accounts[0]})
    Token.transfer(ts.address, 100, {'from':accounts[0]})
    return ts