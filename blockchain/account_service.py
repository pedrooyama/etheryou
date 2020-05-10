import json

from Crypto.Random import get_random_bytes
from eth_account import Account
from web3 import Web3
import random

from exception.gas_limit_exceeded import GasLimitExceeded
from model.eth_key_pair import EthKeyPair
from parameters.config import Config
from parameters.constants import Constants
from repository.user_repository import UserRepository


class AccountService:

    def __init__(self):
        self.rpc_server = Config.rpc_server
        self.truffleFile = json.load(open(Config.truffle_file_path))
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_server))

    def create_account(self) -> EthKeyPair:
        randomness = random.randint(0, Constants.CREATE_ACCOUNT_RANDOMNESS)
        eth_keys = Account.create(extra_entropy=get_random_bytes(randomness))
        return EthKeyPair(public_key=eth_keys.address, private_key=eth_keys.privateKey)

    def create_account_with_ether(self, amount_of_ether: int) -> EthKeyPair:
        account = self.create_account()
        provider = UserRepository.get_test_users()[0]
        self.send_ether(source=provider.eth_key_pair, destination_public_key=account.public_key, amount_in_ether=amount_of_ether, gas=Constants.DEFAULT_GAS, gas_price_in_gwei=Constants.DEFAULT_GAS_PRICE_IN_GWEI)
        return account

    def send_ether(self, source: EthKeyPair, destination_public_key: str, amount_in_ether: int, gas: int, gas_price_in_gwei: int):
        try:
            nonce = self.web3.eth.getTransactionCount(source.public_key)
            tx = {
                'nonce': nonce,
                'from': source.public_key,
                'to': destination_public_key,
                'value': self.web3.toWei(amount_in_ether, 'ether'),
                'gas': gas,
                'gasPrice': self.web3.toWei(gas_price_in_gwei, 'gwei')
            }
            signed_tx = self.web3.eth.account.signTransaction(tx, private_key=source.private_key)
            txn_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            self.web3.eth.waitForTransactionReceipt(txn_hash)
        except ValueError as e:
            if e.args[0]['message'] == GasLimitExceeded.MESSAGE:
                raise GasLimitExceeded
            raise e


    def get_balance(self, public_key: str) -> float:
        balance = self.web3.eth.getBalance(public_key)
        return self.web3.fromWei(balance, 'ether')
