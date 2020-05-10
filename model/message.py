from crypto.algorithms.interface.i_public_key import IPublicKey
from model.message_type import MessageType


class Message:

    def __init__(self, block_hash: bytes, sender: IPublicKey, message_type: MessageType, message: str, timestamp: int, nonce_timestamp: int):
        self.block_hash = block_hash
        self.sender = sender
        self.message_type = message_type
        self.message = message
        self.timestamp = timestamp
        self.nonce_timestamp = nonce_timestamp
