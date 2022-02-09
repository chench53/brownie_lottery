How do we want to test this?

1. `mainnet-fork`
2. `development` with mocks
3. `testnet`


### cmd
compile
`brownie compile`
run
`brownie run scripts/deploy_lottery.py`
test
`brownie test -k test_get_entrance_fee`