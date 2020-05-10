from typing import List

from crypto.algorithms.interface.i_key_pair import IKeyPair
from crypto.algorithms.interface.i_public_key import IPublicKey
from model.eth_key_pair import EthKeyPair


class User:

    def __init__(self, eth_key_pair: EthKeyPair, encryption_key_pair: IKeyPair):
        self.eth_key_pair: EthKeyPair = eth_key_pair
        self.encryption_key_pair: IKeyPair = encryption_key_pair
        self.followers: List[IPublicKey] = []
        self.following: List[IPublicKey] = []


