from crypto.algorithms.impl.rsa.rsa_private_key import RSAPrivateKey
from crypto.algorithms.impl.rsa.rsa_public_key import RSAPublicKey
from crypto.algorithms.interface.i_key_pair import IKeyPair


class RSAKeyPair(IKeyPair):
    def __init__(self, public_key: RSAPublicKey, private_key: RSAPrivateKey):
        super().__init__(public_key, private_key)
