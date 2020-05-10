from nacl.public import PublicKey
from nacl.signing import VerifyKey

from crypto.algorithms.interface.i_public_key import IPublicKey


class Curve25519PublicKey(IPublicKey):

    KEY_LENGTH = 32

    def __init__(self, verify_key: VerifyKey):
        self.__verify_key = verify_key

    @property
    def encryption_key(self):
        return self.__verify_key.to_curve25519_public_key()

    @property
    def verify_key(self):
        return self.__verify_key

    def to_bytes(self) -> bytes:
        return self.verify_key.encode()

    @staticmethod
    def parse(key_as_bytes: bytes) -> 'Curve25519PublicKey':
        return Curve25519PublicKey(VerifyKey(key_as_bytes))

    @staticmethod
    def key_length() -> int:
        return Curve25519PublicKey.KEY_LENGTH




