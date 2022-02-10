import time
from brownie import Lottery, accounts, config, network
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


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN:
        pytest.skip()
    lottery = deploy()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntanceFee()})
    lottery.enter({"from": account, "value": lottery.getEntanceFee()})
    # lottery.enter({"from": get_account(2), "value": lottery.getEntanceFee()})
    tx = fund_with_link(lottery)
    tx.wait(1)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    time.sleep(60)
    print(f"winner: {lottery.winner()}")
    assert lottery.winner() == account
    assert lottery.balance() == 0