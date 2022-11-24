import brownie

def test_eth_received_from_buyer(accounts, TokenSale):
    initial_eth_balance = TokenSale.balance()
    TokenSale.buyTokens(1, {'from':accounts[2], 'value':'1 ether'})

    assert TokenSale.balance() == initial_eth_balance + '1 ether'


def test_contract_balance_reduced(accounts, Token, TokenSale):
    initial_token_balance = Token.balanceOf(TokenSale.address)
    TokenSale.buyTokens(1, {'from':accounts[2], 'value':'1 ether'})

    assert Token.balanceOf(TokenSale.address) == initial_token_balance - 1


def test_buyer_received_token(accounts, Token, TokenSale):
    initial_buyer_balance = Token.balanceOf(accounts[2])
    TokenSale.buyTokens(1, {'from':accounts[2], 'value':'1 ether'})

    assert Token.balanceOf(accounts[2]) == initial_buyer_balance + 1


def test_sale_event_emitted(accounts, TokenSale):
    tx = TokenSale.buyTokens(1, {'from':accounts[2], 'value':'1 ether'})
    
    assert len(tx.events) == 2
    assert tx.events['Transfer'].values() == [TokenSale.address, accounts[2], 1]


def test_buy_with_low_funds(accounts, TokenSale):
    with brownie.reverts():
        TokenSale.buyTokens(1, {'from':accounts[2], 'value':'0.001 ether'})


def test_buy_with_high_funds(accounts, TokenSale):
    with brownie.reverts():
        TokenSale.buyTokens(1, {'from':accounts[2], 'value':'10 ether'})


def test_token_balance_not_enough(accounts, TokenSale):
    with brownie.reverts():
        TokenSale.buyTokens(999, {'from':accounts[2], 'value':'999 ether'})