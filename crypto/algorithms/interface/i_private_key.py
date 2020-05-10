from abc import ABC, abstractmethod


class IPrivateKey(ABC):

    @property
    @abstractmethod
    def decryption_key(self):
        pass

    @property
    @abstractmethod
    def signing_key(self):
        pass

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def parse(key_as_bytes: bytes) -> 'IPrivateKey':
        pass

