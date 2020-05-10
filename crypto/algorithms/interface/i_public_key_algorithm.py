from abc import ABC, abstractmethod

from crypto.algorithms.interface.i_key_pair import IKeyPair
from crypto.algorithms.interface.i_private_key import IPrivateKey
from crypto.algorithms.interface.i_public_key import IPublicKey


class IPublicKeyAlgorithm(ABC):

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def generate_random_key_pair() -> IKeyPair:
        pass

    @staticmethod
    @abstractmethod
    def encrypt_bytes(plaintext: bytes, public_key: IPublicKey) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def decrypt_bytes(ciphertext: bytes, private_key: IPrivateKey) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def sign(message: bytes, private_key: IPrivateKey) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def verify_signature(message: bytes, signature: bytes, public_key: IPublicKey) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def signature_length() -> int:
        pass

    @staticmethod
    @abstractmethod
    def symmetric_key_encryption_length() -> int:
        pass

    @staticmethod
    @abstractmethod
    def get_public_key_class() -> IPublicKey:
        pass

    @staticmethod
    @abstractmethod
    def get_private_key_class() -> IPrivateKey:
        pass


