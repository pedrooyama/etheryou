from Crypto.PublicKey import RSA

from crypto.algorithms.interface.i_private_key import IPrivateKey


class RSAPrivateKey(IPrivateKey):

    def __init__(self, key):
        self.__key = key

    @property
    def decryption_key(self):
        return self.__key

    @property
    def signing_key(self):
        return self.__key

    def to_bytes(self) -> bytes:
        return self.__key.exportKey(format='DER')

    @staticmethod
    def parse(key_as_bytes: bytes) -> 'IPrivateKey':
        return RSAPrivateKey(RSA.import_key(key_as_bytes))

