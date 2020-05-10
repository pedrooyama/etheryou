from Crypto.Hash import SHA256

from crypto.algorithms.interface.i_key_pair import IKeyPair
from crypto.algorithms.interface.i_private_key import IPrivateKey
from model.compression_algorithm import CompressionAlgorithm
from model.encoding import Encoding
from parameters.constants import Constants


class MessageBlock:

    def __init__(self, encrypted_flag: bool, compression_algorithm: CompressionAlgorithm, content: bytes, encoding: Encoding, encryption_key_pair: IKeyPair):
        self.content = content
        self.is_encrypted = encrypted_flag
        self.compression_algorithm = compression_algorithm
        self.encoding: Encoding = encoding
        self.flags = self.__build_flags()
        self.signature = self.__sign(encryption_key_pair.private_key)
        self.block_hash = self.__calculate_block_hash()

    def __calculate_block_hash(self) -> bytes:
        data_to_be_hashed = self.flags + self.content + self.signature
        hash_object = SHA256.new(data=data_to_be_hashed)
        return hash_object.digest()

    def __sign(self, private_key: IPrivateKey) -> bytes:
        public_key_algorithm = Constants.PUBLIC_KEY_ALGORITHM()
        return public_key_algorithm.sign(self.flags + self.content, private_key)

    def __build_flags(self) -> bytes:
        number_of_bits = Constants.FLAGS_LENGTH * 8
        flags = int(self.is_encrypted) << (number_of_bits - Constants.ENCRYPTED_FLAG - 1)

        # Compression Algorithm
        compression_algorithm_bit_str = "{:03b}".format(self.compression_algorithm.value)
        flags += int(compression_algorithm_bit_str[0]) << (number_of_bits - Constants.COMPRESSION_ALGORITHM_BIT_0 - 1)
        flags += int(compression_algorithm_bit_str[1]) << (number_of_bits - Constants.COMPRESSION_ALGORITHM_BIT_1 - 1)
        flags += int(compression_algorithm_bit_str[2]) << (number_of_bits - Constants.COMPRESSION_ALGORITHM_BIT_2 - 1)

        # Encoding
        encoding_bit_str = "{:03b}".format(self.encoding.value)
        flags += int(encoding_bit_str[0]) << (number_of_bits - Constants.ENCODING_BIT_0 - 1)
        flags += int(encoding_bit_str[1]) << (number_of_bits - Constants.ENCODING_BIT_1 - 1)
        flags += int(encoding_bit_str[2]) << (number_of_bits - Constants.ENCODING_BIT_2 - 1)

        return flags.to_bytes(Constants.FLAGS_LENGTH, 'little', signed=False)

    def to_bytes(self) -> bytes:
        # return self.flags + self.block_hash + self.signature + self.content
        return self.flags + self.signature + self.content
