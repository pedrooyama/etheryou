import struct
from typing import List
from crypto.algorithms.interface.i_public_key import IPublicKey
from crypto.crypto_utils import CryptoUtils
from model.encoding import Encoding
from model.encrypted_message_block import EncryptedMessageBlock
from model.message_block import MessageBlock
from model.message_type import MessageType
from model.plain_message_block import PlainMessageBlock
from model.user import User
from parameters.constants import Constants
from utils.compressor import Compressor
from utils.general_utils import GeneralUtils


class MessageBlockBuilder:

    @staticmethod
    def build_message_block(message: str, message_type: MessageType, sender: User, recipients_public_keys: List[IPublicKey]=None, encoding: Encoding=Constants.DEFAULT_ENCODING) -> MessageBlock:
        if message_type in [MessageType.PRIVATE_POST, MessageType.DIRECT_MESSAGE]:
            return MessageBlockBuilder.__build_encrypted_message_block(message=message, message_type=message_type, sender=sender, recipients_public_keys=recipients_public_keys)

        if message_type in [MessageType.PUBLIC_POST]:
            return MessageBlockBuilder.__build_plain_message_block(message=message, message_type=message_type, sender=sender, encoding=encoding)

    @staticmethod
    def __build_plain_message_block(message: str, message_type: MessageType, sender: User, encoding: Encoding=Constants.DEFAULT_ENCODING) -> MessageBlock:
        return PlainMessageBlock(encryption_key_pair=sender.encryption_key_pair, message_type=message_type, message=message, encoding=encoding)

    @staticmethod
    def __build_encrypted_message_block(message: str, message_type: MessageType, sender: User, recipients_public_keys: List[IPublicKey], encoding: Encoding=Constants.DEFAULT_ENCODING) -> MessageBlock:
        public_key_algorithm = Constants.PUBLIC_KEY_ALGORITHM()

        content_to_be_compressed = b''

        encoding_str = Encoding.get_str(encoding)
        encoded_message = message.encode(encoding=encoding_str)

        message_type_value = struct.pack('!B', message_type.value)
        assert len(message_type_value) == Constants.MESSAGE_TYPE_LENGTH
        content_to_be_compressed += message_type_value

        sender_public_key = sender.encryption_key_pair.public_key.to_bytes()
        assert len(sender_public_key) == public_key_algorithm.get_public_key_class().key_length()
        content_to_be_compressed += sender_public_key
        content_to_be_compressed += GeneralUtils.get_current_unix_timestamp()  # nonce timestamp

        content_to_be_compressed += encoded_message

        compression_algorithm, compressed_content = Compressor.compress_with_best_algorithm(content_to_be_compressed)

        compressed_content_length = struct.pack('!H', len(compressed_content))
        assert len(compressed_content_length) == Constants.MESSAGE_LENGTH_LENGTH
        content_to_be_encrypted = compressed_content_length + compressed_content

        symmetric_key = CryptoUtils.generate_random_symmetric_key()
        assert len(symmetric_key) == Constants.SYMMETRIC_KEY_LENGTH
        key_encryptions = MessageBlockBuilder.__encrypt_symmetric_key(symmetric_key=symmetric_key,
                                                                      public_keys=recipients_public_keys)
        for key_encryption in key_encryptions:
            assert len(key_encryption) == public_key_algorithm.symmetric_key_encryption_length()

        encrypted_data, iv = CryptoUtils.encrypt_bytes(symmetric_key=symmetric_key, message=content_to_be_encrypted)
        assert len(iv) == Constants.AES_BLOCK_SIZE

        return EncryptedMessageBlock(iv=iv, encrypted_content=encrypted_data, compression_algorithm=compression_algorithm, key_encryptions=key_encryptions, encoding=encoding, encryption_key_pair=sender.encryption_key_pair)

    @staticmethod
    def __encrypt_symmetric_key(symmetric_key: bytes, public_keys: List[IPublicKey]) -> List[bytes]:
        key_encryptions = []
        for public_key in public_keys:
            encryption = Constants.PUBLIC_KEY_ALGORITHM().encrypt_bytes(symmetric_key, public_key)
            key_encryptions.append(encryption)
        return key_encryptions
