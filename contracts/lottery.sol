// SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    address payable public winner;
    uint256 public randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal priceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    // 0, 1, 2
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyhash;

    constructor(
        address _priceFeed, 
        address _vrfCoordinator, 
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18);
        priceFeed = AggregatorV3Interface(_priceFeed);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        // 50 min
        require(lottery_state == LOTTERY_STATE.OPEN, "lottery is not open!");
        require(msg.value >= getEntanceFee(), "you need pay more!");
        players.push(payable(msg.sender));
    }

    function getEntanceFee() public  view returns (uint256){
        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10 ** 10; // 18 decimals

        uint256 costToEnter = (usdEntryFee * 10 ** 18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, "cant start a new lottery");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        // uint256(keccak256(abi.encodePacked(nonce, msg.sender, block.difficulty, block.timestamp))) % players.length;

        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "not there yet!");
        require(_randomness > 0, "random nt found");
        uint256 indexWinner = _randomness % players.length;
        winner = players[indexWinner];
        winner.transfer(address(this).balance);
        // reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}