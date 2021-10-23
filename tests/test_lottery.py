from brownie import Lottery, accounts, config
from brownie.network import contract
from web3 import Web3

def test_get_entrance_fee():
    account = accounts[0]
    price_feed_address = config['networks']['mainnet-fork']['price_feed_address']
    lottery = Lottery.deploy(price_feed_address, {"from": account})
    entrance_fee = lottery.getEntanceFee()
    print(entrance_fee)
    assert entrance_fee > Web3.toWei(0.012, "ether")
    assert entrance_fee < Web3.toWei(0.013, "ether")