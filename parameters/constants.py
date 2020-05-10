from crypto.algorithms.interface.i_public_key_algorithm import IPublicKeyAlgorithm
from model.encoding import Encoding


class Constants:
    FLAGS_LENGTH = 1  # in bytes
    ENCRYPTED_FLAG = 0
    COMPRESSION_ALGORITHM_BIT_0 = 1
    COMPRESSION_ALGORITHM_BIT_1 = 2
    COMPRESSION_ALGORITHM_BIT_2 = 3
    ENCODING_BIT_0 = 4
    ENCODING_BIT_1 = 5
    ENCODING_BIT_2 = 6

    MESSAGE_TYPE_LENGTH = 1   # in bytes
    MESSAGE_LENGTH_LENGTH = 2  # in bytes
    SYMMETRIC_KEY_LENGTH = 32  # in bytes
    AES_BLOCK_SIZE = 16
    BLOCK_HASH_LENGTH = 32
    TIMESTAMP_LENGTH = 4
    DEFAULT_ENCODING = Encoding.UTF_8
    CREATE_ACCOUNT_RANDOMNESS = 9999
    DEFAULT_GAS = 2000000
    DEFAULT_GAS_PRICE_IN_GWEI = 50

    @staticmethod
    def PUBLIC_KEY_ALGORITHM() -> IPublicKeyAlgorithm:
        from crypto.algorithms.impl.rsa.rsa_algorithm import RSAAlgorithm
        from crypto.algorithms.impl.curve25519.curve25519_algorithm import Curve25519Algorithm

        available_algorithms = [RSAAlgorithm, Curve25519Algorithm]
        return available_algorithms[1]


