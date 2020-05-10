from abc import ABC

from crypto.algorithms.interface.i_private_key import IPrivateKey
from crypto.algorithms.interface.i_public_key import IPublicKey


class IKeyPair(ABC):

    def __init__(self, public_key: IPublicKey, private_key: IPrivateKey):
        self.public_key = public_key
        self.private_key = private_key
