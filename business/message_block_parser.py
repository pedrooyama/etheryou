import struct

from crypto.algorithms.interface.i_private_key import IPrivateKey
from crypto.algorithms.interface.i_public_key import IPublicKey
from crypto.crypto_utils import CryptoUtils
from exception.InvalidSignature import InvalidSignature
from exception.not_intended_receiver import NotIntendedReceiver
from exception.unable_to_decrypt import UnableToDecrypt
from model.blockchain_message_block import BlockchainMessageBlock
from model.compression_algorithm import CompressionAlgorithm
from model.encoding import Encoding
from model.message import Message
from model.message_type import MessageType
from parameters.constants import Constants
from utils.compressor import Compressor
from utils.general_utils import GeneralUtils


class MessageBlockParser:

    @staticmethod
    def parse_message_block(blockchain_message_block: BlockchainMessageBlock, private_key: IPrivateKey = None) -> Message:
        compression_algorithm = MessageBlockParser.__get_compression_algorithm(blockchain_message_block.data)
        encoding = MessageBlockParser.__get_encoding(blockchain_message_block.data)

        if MessageBlockParser.__is_encrypted(blockchain_message_block.data):
            return MessageBlockParser.__parse_encrypted_message_block(blockchain_message_block=blockchain_message_block,
                                                                      private_key=private_key,
                                                                      compression_algorithm=compression_algorithm,
                                                                      encoding=encoding)
        else:
            return MessageBlockParser.__parse_plain_message_block(blockchain_message_block=blockchain_message_block,
                                                                  timestamp=blockchain_message_block.timestamp,
                                                                  compression_algorithm=compression_algorithm,
                                                                  encoding=encoding)

    @staticmethod
    def __get_flag(flag_bytes: bytes, bit_number: int) -> bool:
        byte_number = bit_number // 8
        bit_number = bit_number % 8
        flag_value = flag_bytes[byte_number] >> (7 - bit_number) & 1
        return bool(flag_value)

    @staticmethod
    def __is_encrypted(message_block_data: bytes) -> bool:
        flags = message_block_data[:Constants.FLAGS_LENGTH]
        return MessageBlockParser.__get_flag(flags, Constants.ENCRYPTED_FLAG)

    @staticmethod
    def __get_compression_algorithm(message_block_data: bytes) -> CompressionAlgorithm:
        flags = message_block_data[:Constants.FLAGS_LENGTH]
        bits_list = []
        bits_list.append(MessageBlockParser.__get_flag(flag_bytes=flags, bit_number=Constants.COMPRESSION_ALGORITHM_BIT_0))
        bits_list.append(MessageBlockParser.__get_flag(flag_bytes=flags, bit_number=Constants.COMPRESSION_ALGORITHM_BIT_1))
        bits_list.append(MessageBlockParser.__get_flag(flag_bytes=flags, bit_number=Constants.COMPRESSION_ALGORITHM_BIT_2))
        return CompressionAlgorithm(GeneralUtils.bit_list_to_int(bits_list))

    @staticmethod
    def __get_encoding(message_block_data: bytes) -> Encoding:
        flags = message_block_data[:Constants.FLAGS_LENGTH]
        bits_list = []
        bits_list.append(
            MessageBlockParser.__get_flag(flag_bytes=flags, bit_number=Constants.ENCODING_BIT_0))
        bits_list.append(
            MessageBlockParser.__get_flag(flag_bytes=flags, bit_number=Constants.ENCODING_BIT_1))
        bits_list.append(
            MessageBlockParser.__get_flag(flag_bytes=flags, bit_number=Constants.ENCODING_BIT_2))
        return Encoding(GeneralUtils.bit_list_to_int(bits_list))

    @staticmethod
    def __get_key(message_block_as_bytes: bytes, private_key: IPrivateKey) -> bytes:
        assert MessageBlockParser.__is_encrypted(message_block_as_bytes)

        public_key_algorithm = Constants.PUBLIC_KEY_ALGORITHM()
        symmetric_key_encryption_length = public_key_algorithm.symmetric_key_encryption_length()

        byte_index = 0
        candidate_encrypted_key = message_block_as_bytes[-symmetric_key_encryption_length:]
        while len(candidate_encrypted_key) == symmetric_key_encryption_length:
            try:
                return public_key_algorithm.decrypt_bytes(candidate_encrypted_key, private_key)
            except UnableToDecrypt:
                byte_index -= symmetric_key_encryption_length
                candidate_encrypted_key = message_block_as_bytes[
                                          -symmetric_key_encryption_length + byte_index:byte_index]

        raise NotIntendedReceiver  # Message block is not addressed to the private key

    @staticmethod
    def __parse_plain_message_block(blockchain_message_block: BlockchainMessageBlock, timestamp: int,
                                    compression_algorithm: CompressionAlgorithm, encoding: Encoding) -> Message:

        public_key_algorithm = Constants.PUBLIC_KEY_ALGORITHM()
        message_block_as_bytes = blockchain_message_block.data

        byte_index = Constants.FLAGS_LENGTH

        signature_length = public_key_algorithm.signature_length()
        signature = message_block_as_bytes[byte_index:byte_index + signature_length]
        byte_index += signature_length

        message_content = message_block_as_bytes[:Constants.FLAGS_LENGTH]  # flags
        message_content += message_block_as_bytes[byte_index:]

        compressed_data = message_block_as_bytes[byte_index:]
        decompressed_data = Compressor.decompress(algorithm=compression_algorithm, data=compressed_data)
        byte_index = 0

        message_type_bytes = decompressed_data[byte_index:byte_index+Constants.MESSAGE_TYPE_LENGTH]
        byte_index += Constants.MESSAGE_TYPE_LENGTH
        message_type_value = struct.unpack('!B', message_type_bytes)[0]
        message_type = MessageType(message_type_value)

        public_key_length = public_key_algorithm.get_public_key_class().key_length()
        sender_bytes = decompressed_data[byte_index:byte_index + public_key_length]
        byte_index += public_key_length
        sender = public_key_algorithm.get_public_key_class().parse(sender_bytes)

        nonce_timestamp = GeneralUtils.decode_unix_timestamp(decompressed_data[byte_index:byte_index + Constants.TIMESTAMP_LENGTH])
        byte_index += Constants.TIMESTAMP_LENGTH

        message_bytes = decompressed_data[byte_index:]

        encoding_str = Encoding.get_str(encoding)
        message = message_bytes.decode(encoding_str)

        MessageBlockParser.__check_signature(message=message_content, public_key=sender, signature=signature)

        return Message(block_hash=blockchain_message_block.block_hash, sender=sender, message_type=message_type, message=message, timestamp=timestamp, nonce_timestamp=nonce_timestamp)

    @staticmethod
    def __parse_encrypted_message_block(blockchain_message_block: BlockchainMessageBlock, private_key: IPrivateKey,
                                        compression_algorithm: CompressionAlgorithm, encoding: Encoding) -> Message:

        public_key_algorithm = Constants.PUBLIC_KEY_ALGORITHM()
        message_block_as_bytes = blockchain_message_block.data

        byte_index = Constants.FLAGS_LENGTH

        signature = message_block_as_bytes[byte_index:byte_index + public_key_algorithm.signature_length()]
        byte_index += public_key_algorithm.signature_length()

        message_content = message_block_as_bytes[:Constants.FLAGS_LENGTH] #flags
        message_content += message_block_as_bytes[byte_index:]
        iv = message_block_as_bytes[byte_index:byte_index + Constants.AES_BLOCK_SIZE]
        byte_index += Constants.AES_BLOCK_SIZE

        encrypted_content_and_keys = message_block_as_bytes[byte_index:]
        symmetric_key = MessageBlockParser.__get_key(message_block_as_bytes, private_key)

        byte_index = 0
        first_block = encrypted_content_and_keys[byte_index:byte_index+Constants.AES_BLOCK_SIZE]
        decrypted_first_block = CryptoUtils.decrypt_bytes(symmetric_key=symmetric_key, ciphertext=first_block, iv=iv, unpad_bytes=False)

        compressed_content_length = struct.unpack('!H', decrypted_first_block[:Constants.MESSAGE_LENGTH_LENGTH])[0]

        encrypted_content_length = Constants.MESSAGE_LENGTH_LENGTH + compressed_content_length

        # Adjust length for padding
        if encrypted_content_length % Constants.AES_BLOCK_SIZE != 0:
            encrypted_content_length += Constants.AES_BLOCK_SIZE - encrypted_content_length % Constants.AES_BLOCK_SIZE

        encrypted_content = encrypted_content_and_keys[:encrypted_content_length]
        decrypted_content = CryptoUtils.decrypt_bytes(symmetric_key=symmetric_key, ciphertext=encrypted_content, iv=iv)
        compressed_content = decrypted_content[Constants.MESSAGE_LENGTH_LENGTH:]

        decompressed_content = Compressor.decompress(algorithm=compression_algorithm, data=compressed_content)

        message_type_value = struct.unpack('!B', decompressed_content[:Constants.MESSAGE_TYPE_LENGTH])[0]
        message_type = MessageType(message_type_value)

        byte_index = Constants.MESSAGE_TYPE_LENGTH

        public_key_length = public_key_algorithm.get_public_key_class().key_length()
        sender = public_key_algorithm.get_public_key_class().parse(decompressed_content[byte_index:byte_index+public_key_length])
        byte_index += public_key_length

        nonce_timestamp = GeneralUtils.decode_unix_timestamp(decompressed_content[byte_index:byte_index + Constants.TIMESTAMP_LENGTH])
        byte_index += Constants.TIMESTAMP_LENGTH

        encoding_str = Encoding.get_str(encoding)
        message = decompressed_content[byte_index:].decode(encoding_str)

        MessageBlockParser.__check_signature(message=message_content, public_key=sender, signature=signature)

        return Message(block_hash=blockchain_message_block.block_hash, sender=sender, message_type=message_type, message=message, timestamp=blockchain_message_block.timestamp, nonce_timestamp=nonce_timestamp)

    @staticmethod
    def __check_signature(message: bytes, public_key: IPublicKey, signature: bytes):
        if not Constants.PUBLIC_KEY_ALGORITHM().verify_signature(message=message, signature=signature,public_key=public_key):
            raise InvalidSignature
















