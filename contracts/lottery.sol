// SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal priceFeed;

    constructor(address _priceFeed) public {
        usdEntryFee = 50 * (10**18);
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function enter() public payable {
        // 50 min
        require(true);
        players.push(payable(msg.sender));
    }

    function getEntanceFee() public  view returns (uint256){

    }

    function start() public {

    }

    function end() public {

    }
}