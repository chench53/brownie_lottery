from brownie import Lottery, accounts, config, network

from .utils import get_account, get_contract

def deploy():
    account = get_account(id="me")
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

def main():
    deploy()
