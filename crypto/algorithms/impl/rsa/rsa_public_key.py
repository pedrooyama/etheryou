from Crypto.PublicKey import RSA

from crypto.algorithms.interface.i_public_key import IPublicKey


class RSAPublicKey(IPublicKey):

    KEY_LENGTH = 294

    def __init__(self, key):
        self.__key = key

    @property
    def encryption_key(self):
        return self.__key

    @property
    def verify_key(self):
        return self.__key

    def to_bytes(self) -> bytes:
        return self.__key.exportKey(format='DER')

    @staticmethod
    def parse(key_as_bytes: bytes) -> 'IPublicKey':
        return RSAPublicKey(RSA.import_key(key_as_bytes))

    @staticmethod
    def key_length() -> int:
        return RSAPublicKey.KEY_LENGTH

