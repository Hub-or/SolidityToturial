// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract FundMe {
    using SafeMath for uint256;

    mapping(address => uint256) public addressToAmountFunded;

    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function fund() public payable {
        // $10
        uint256 minimumUSD = 10 * 10**18;
        // 1finney = 0.001eth < $10 -> revert
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "More ETH spending needed."
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10**10); // Format consideration with wei (18 digits)
        // 129389474073 -> 1,293.89474073
    }

    // 1000000000 (1 gwei turning into wei
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 10**18;
        // both have 1e18 on its base unit (USD & ETH)
        // solidty have overflow (based on binary)
        return ethAmountInUsd;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        require(msg.sender == owner);
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
