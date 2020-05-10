from crypto.algorithms.impl.curve25519.curve25519_private_key import Curve25519PrivateKey
from crypto.algorithms.impl.curve25519.curve25519_public_key import Curve25519PublicKey
from crypto.algorithms.interface.i_key_pair import IKeyPair


class Curve25519KeyPair(IKeyPair):

    def __init__(self, public_key: Curve25519PublicKey, private_key: Curve25519PrivateKey):
        super().__init__(public_key, private_key)
