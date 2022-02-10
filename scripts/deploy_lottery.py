import time

from brownie import Lottery, accounts, config, network

from .utils import get_account, get_contract, fund_with_link

def deploy():
    # account = get_account(id="me")
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("price_feed").address, 
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {
            "from": account
        },
        publish_source = config["networks"][network.show_active()].get("verify", False)
    )
    print("deployed lottery {}".format(lottery.address))
    return lottery

def start_lottery():
    # account = get_account(id="me")
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("lottery started!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntanceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("you enter lottery!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund contract link
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    time.sleep(60)
    print(f"winner: {lottery.winner()}")
    print("lottery end!")

def main():
    deploy()
    start_lottery()
    enter_lottery()
    end_lottery()
