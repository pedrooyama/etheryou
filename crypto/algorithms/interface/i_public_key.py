from abc import ABC, abstractmethod


class IPublicKey(ABC):

    @property
    @abstractmethod
    def encryption_key(self):
        pass

    @property
    @abstractmethod
    def verify_key(self):
        pass

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def parse(key_as_bytes: bytes) -> 'IPublicKey':
        pass

    @staticmethod
    @abstractmethod
    def key_length() -> int:
        pass

    def __eq__(self, other):
        return self.to_bytes() == other.to_bytes()




