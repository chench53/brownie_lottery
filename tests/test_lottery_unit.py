from brownie import Lottery, accounts, config, network, exceptions
from brownie.network import contract
import pytest
from web3 import Web3

from scripts.deploy_lottery import deploy
from scripts.utils import (
    fund_with_link, 
    get_account, 
    get_contract, 
    LOCAL_BLOCKCHAIN
)

def test_get_entrance_fee():
    """
    account = accounts[0]
    price_feed_address = config['networks']['mainnet-fork']['price_feed_address']
    lottery = Lottery.deploy(price_feed_address, {"from": account})
    entrance_fee = lottery.getEntanceFee()
    print(entrance_fee)
    # assert entrance_fee > Web3.toWei(0.012, "ether")
    # assert entrance_fee < Web3.toWei(0.013, "ether")
    """
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    lottery = deploy()
    # 2000 usd/eth
    # EntanceFee is 50usd, 0.025eth
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntanceFee()

    assert expected_entrance_fee == entrance_fee

def test_cant_enter_unless_starter():
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    lottery = deploy()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntanceFee()})

def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    lottery = deploy()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": get_account(), "value": lottery.getEntanceFee()})
    assert lottery.players(0) == account

def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    lottery = deploy()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": get_account(), "value": lottery.getEntanceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2

def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip()
    lottery = deploy()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": get_account(), "value": lottery.getEntanceFee()})
    lottery.enter({"from": get_account(1), "value": lottery.getEntanceFee()})
    lottery.enter({"from": get_account(2), "value": lottery.getEntanceFee()})
    fund_with_link(lottery)
    tx = lottery.endLottery({"from": account})

    request_id = tx.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 666
    start_balance_account = account.balance() # 8:10 may have bugs
    start_balance_lottery = lottery.balance()
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )
    assert lottery.winner() == account
    assert lottery.balance() == 0
    assert account.balance() == start_balance_account + start_balance_lottery
    

