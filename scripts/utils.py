from brownie import (
    MockAggregatorV3, 
    VRFCoordinatorMock, 
    LinkToken, 
    network, 
    config, 
    accounts, 
    Contract,
    interface
)

# from scripts.deploy_lottery import deploy

FORKED_LOCAL_BLOCKCHAIN = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN = ['development', 'ganache-local']

DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN or network.show_active() in FORKED_LOCAL_BLOCKCHAIN:
        return accounts[0]

    return accounts.add(config['wallets']['from_key'])


contract_to_mock = {
    "price_feed": MockAggregatorV3,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}

def get_contract(contract_name):
    """
    Args:
        contract_name (string)

    Returns:
        brownie.network.contract.ProjectContract: 
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN:
        if len(contract_type) <= 0:
            deploy_mock(contract_name)
        contract = contract_type[-1]

    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)

    return contract

def deploy_mock(contract_name):
    account = get_account()
    # if len(MockAggregatorV3) == 0:
    print('depolying mocks...{}'.format(contract_name))
    # contract_type = contract_to_mock[contract_name]
    if contract_name == "price_feed":
        MockAggregatorV3.deploy(DECIMALS, STARTING_PRICE, {"from": account})
    else:
        link_token = LinkToken.deploy({"from": account})
        VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    # print('mock depolyed {}'.format(contract_name))

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000): # 0.1lnk
    account = account if account else  get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address) # ?
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("fund contract!")
    return tx