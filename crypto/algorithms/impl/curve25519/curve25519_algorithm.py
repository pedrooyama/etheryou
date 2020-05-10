import nacl.utils
from nacl.exceptions import CryptoError
from nacl.public import PrivateKey, SealedBox
from nacl.signing import SigningKey, VerifyKey

from crypto.algorithms.impl.curve25519.curve25519_key_pair import Curve25519KeyPair
from crypto.algorithms.impl.curve25519.curve25519_private_key import Curve25519PrivateKey
from crypto.algorithms.impl.curve25519.curve25519_public_key import Curve25519PublicKey
from crypto.algorithms.interface.i_private_key import IPrivateKey
from crypto.algorithms.interface.i_public_key import IPublicKey
from crypto.algorithms.interface.i_public_key_algorithm import IPublicKeyAlgorithm
from exception.unable_to_decrypt import UnableToDecrypt


class Curve25519Algorithm(IPublicKeyAlgorithm):

    SIGNATURE_LENGTH = 64
    SYMMETRIC_KEY_ENCRYPTION_LENGTH = 80
    NAME = 'Curve 25519'

    @staticmethod
    def name() -> str:
        return Curve25519Algorithm.NAME

    @staticmethod
    def generate_random_key_pair() -> (IPrivateKey, IPublicKey):
        signing_key = nacl.signing.SigningKey.generate()
        verify_key = signing_key.verify_key

        public_key = Curve25519PublicKey(verify_key=verify_key)
        private_key = Curve25519PrivateKey(signing_key=signing_key)

        return Curve25519KeyPair(public_key, private_key)

    @staticmethod
    def encrypt_bytes(plaintext: bytes, public_key: IPublicKey) -> bytes:
        sealed_box = SealedBox(public_key.encryption_key)
        return sealed_box.encrypt(plaintext)

    @staticmethod
    def decrypt_bytes(ciphertext: bytes, private_key: IPrivateKey) -> bytes:
        unseal_box = SealedBox(private_key.decryption_key)
        try:
            return unseal_box.decrypt(ciphertext)
        except CryptoError:
            raise UnableToDecrypt

    @staticmethod
    def sign(message: bytes, private_key: IPrivateKey) -> bytes:
        return private_key.signing_key.sign(message).signature

    @staticmethod
    def verify_signature(message: bytes, signature: bytes, public_key: IPublicKey) -> bool:
        try:
            public_key.verify_key.verify(message, signature)
            return True
        except nacl.exceptions.BadSignatureError:
            return False

    @staticmethod
    def signature_length() -> int:
        return Curve25519Algorithm.SIGNATURE_LENGTH

    @staticmethod
    def symmetric_key_encryption_length() -> int:
        return Curve25519Algorithm.SYMMETRIC_KEY_ENCRYPTION_LENGTH

    @staticmethod
    def get_public_key_class() -> IPublicKey:
        return Curve25519PublicKey

    @staticmethod
    def get_private_key_class() -> IPrivateKey:
        return Curve25519PrivateKey


