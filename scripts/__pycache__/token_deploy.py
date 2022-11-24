from brownie import token, accounts

def main():
    return token.deploy("Test Token", "TST", 1000, {'from': accounts[0]})