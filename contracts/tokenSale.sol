// SPDX-License-Identifier: MIT
// This contract is just a way for the buyer to interact with our token contract
// takes tokens from token contract and sells it to buyer (middleman)

pragma solidity >=0.7.0 <0.9.0;

import "./token.sol";
import "./safeMath.sol";

contract tokenSale {

    using SafeMath for uint;

    token public tokenContract;

    address admin;

    uint public tokenPrice;
    uint public tokensSold = 0;

    event Sale(address indexed _to, uint _numberOfTokens);

    constructor(token _tokenContract, uint _tokenPrice) {
        tokenContract = _tokenContract;
        admin = msg.sender;
        tokenPrice = _tokenPrice;
    }

    function buyTokens(uint _numberOfTokens) public payable {
        require(msg.value == _numberOfTokens.mul(tokenPrice), "Please add exactt amount of ether");
        require(tokenContract.balanceOf(address(this)) >= _numberOfTokens, "Insufficient Funds");
        require(tokenContract.transfer(msg.sender, _numberOfTokens));

        tokensSold = tokensSold.add(1);
        emit Sale(msg.sender, _numberOfTokens);
    }

    function endSale() public{
        require(msg.sender == admin);
        tokenContract.transfer(admin, tokenContract.balanceOf(address(this)));
        selfdestruct(payable(msg.sender));
    }
}