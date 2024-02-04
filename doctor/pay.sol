// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.0;

contract Payment {
    address payable public seller;
    uint256 public price;
    event PaymentReceived(address payer, uint256 amount);
    constructor(address payable _seller, uint256 _price) {
        seller = _seller;
        price = _price;
    }
    function buy() public payable {
        require(msg.value == price, "Incorrect amount sent");
        seller.transfer(price);
        emit PaymentReceived(msg.sender, price);
    }
}