from brownie import Lottery, accounts, config, network

from .utils import get_account, get_contract

def deploy():
    account = get_account(id="me")
    lottery = Lottery.deploy(get_contract("price_feed").address, {
        "from": account
    })

def main():
    deploy()
