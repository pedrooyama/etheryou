from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP

from crypto.algorithms.impl.rsa.rsa_key_pair import RSAKeyPair
from crypto.algorithms.impl.rsa.rsa_private_key import RSAPrivateKey
from crypto.algorithms.impl.rsa.rsa_public_key import RSAPublicKey
from crypto.algorithms.interface.i_private_key import IPrivateKey
from crypto.algorithms.interface.i_public_key import IPublicKey
from crypto.algorithms.interface.i_public_key_algorithm import IPublicKeyAlgorithm
from exception.unable_to_decrypt import UnableToDecrypt
from parameters.constants import Constants


class RSAAlgorithm(IPublicKeyAlgorithm):

    SIGNATURE_LENGTH = 256
    SYMMETRIC_KEY_ENCRYPTION_LENGTH = 256
    NAME = 'RSA'
    KEY_BITS = 2048

    @staticmethod
    def name() -> str:
        return RSAAlgorithm.NAME

    @staticmethod
    def generate_random_key_pair() -> (IPrivateKey, IPublicKey):
        rsa_key = RSA.generate(RSAAlgorithm.KEY_BITS)
        public_key = RSAPublicKey(rsa_key.publickey())
        private_key = RSAPrivateKey(rsa_key)

        return RSAKeyPair(public_key, private_key)

    @staticmethod
    def encrypt_bytes(plaintext: bytes, public_key: IPublicKey) -> bytes:
        rsa_public_key = public_key.encryption_key
        return PKCS1_OAEP.new(rsa_public_key).encrypt(plaintext)

    @staticmethod
    def decrypt_bytes(ciphertext: bytes, private_key: IPrivateKey) -> bytes:
        cipher_rsa = PKCS1_OAEP.new(private_key.decryption_key)
        try:
            return cipher_rsa.decrypt(ciphertext)
        except ValueError:
            raise UnableToDecrypt

    @staticmethod
    def sign(message: bytes, private_key: IPrivateKey) -> bytes:
        h = SHA256.new(data=message)
        return pkcs1_15.new(private_key.signing_key).sign(h)

    @staticmethod
    def verify_signature(message: bytes, signature: bytes, public_key: IPublicKey) -> bool:
        h = SHA256.new(message)
        try:
            pkcs1_15.new(public_key.verify_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def signature_length() -> int:
        return RSAAlgorithm.SIGNATURE_LENGTH

    @staticmethod
    def symmetric_key_encryption_length() -> int:
        return RSAAlgorithm.SYMMETRIC_KEY_ENCRYPTION_LENGTH

    @staticmethod
    def get_public_key_class() -> IPublicKey:
        return RSAPublicKey

    @staticmethod
    def get_private_key_class() -> IPrivateKey:
        return RSAPrivateKey



