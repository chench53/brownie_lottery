from brownie import MockAggregatorV3, VRFCoordinatorMock, LinkToken, network, config, accounts, Contract

# from scripts.deploy_lottery import deploy

FORKED_LOCAL_BLOCKCHAIN = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN = ['development', 'ganache-local']

DECIMALS = 8
STARTING_PRICE = 400000000000

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
    # elif contract_name == "vrf_coordinator":
    #     VRFCoordinatorMock.deploy({"from": account})
    # elif contract_name == "link_token":
    #     LinkToken.deploy({"from": account})
    else:
        link_token = LinkToken.deploy({"from": account})
        VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print('mock depolyed {}'.format(contract_name))

