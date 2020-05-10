from nacl.signing import SigningKey
from crypto.algorithms.interface.i_private_key import IPrivateKey


class Curve25519PrivateKey(IPrivateKey):

    def __init__(self, signing_key: SigningKey):
        self.__signing_key = signing_key

    @property
    def decryption_key(self):
        return self.__signing_key.to_curve25519_private_key()

    @property
    def signing_key(self):
        return self.__signing_key

    def to_bytes(self) -> bytes:
        return self.__signing_key.encode()

    @staticmethod
    def parse(key_as_bytes: bytes) -> 'Curve25519PrivateKey':
        return Curve25519PrivateKey(SigningKey(key_as_bytes))

