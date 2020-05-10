import json
from typing import List
from web3 import Web3
from exception.gas_limit_exceeded import GasLimitExceeded
from model.blockchain_message_block import BlockchainMessageBlock
from model.message_block import MessageBlock
from model.user import User
from parameters.config import Config


class BlockchainApi:

    def __init__(self):
        self.rpc_server = Config.rpc_server
        self.truffleFile = json.load(open(Config.truffle_file_path))
        self.abi = self.truffleFile['abi']
        self.contract_address = Config.contract_address
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_server, request_kwargs={'timeout': 6000}))
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def is_connected(self) -> bool:
        return self.web3.isConnected()

    def send_message(self, sender: User, message_block: MessageBlock) -> (int, int, int):
        try:
            nonce = self.web3.eth.getTransactionCount(sender.eth_key_pair.public_key)
            txn = self.contract.functions.sendMessage(message_block.to_bytes()).buildTransaction(
                {'nonce': nonce, 'from': sender.eth_key_pair.public_key})
            signed = self.web3.eth.account.signTransaction(txn, private_key=sender.eth_key_pair.private_key)
            txn_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
            receipt = self.web3.eth.waitForTransactionReceipt(txn_hash)
            cumulative_gas_used = receipt.cumulativeGasUsed
            return self.web3.eth.getBlock(receipt.blockNumber).timestamp, cumulative_gas_used, len(message_block.to_bytes())
        except ValueError as e:
            if e.args[0]['message'] == GasLimitExceeded.MESSAGE:
                raise GasLimitExceeded
            raise e

    def get_message_by_index(self, index: int) -> BlockchainMessageBlock:
        timestamp, data = self.contract.functions.getMessage(index).call()
        return BlockchainMessageBlock(timestamp=timestamp, data=data)

    def get_message_by_hash(self, block_hash: bytes) -> BlockchainMessageBlock:
        timestamp, data = self.contract.functions.getMessageByHash(block_hash).call()
        return BlockchainMessageBlock(timestamp=timestamp, data=data)

    def fetch_messages_from_timestamp(self, timestamp: int) -> List[BlockchainMessageBlock]:
        timestamps, hashes, datas = self.contract.functions.getMessagesFromTimestamp(timestamp).call()
        message_blocks = []
        for i in range(len(timestamps)):
            message_blocks.append(BlockchainMessageBlock(timestamp=timestamps[i], block_hash=hashes[i], data=datas[i]))
        return message_blocks

    def get_latest_block_timestamp(self) -> int:
        return self.web3.eth.getBlock('latest').timestamp



