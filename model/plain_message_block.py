import struct

from crypto.algorithms.interface.i_key_pair import IKeyPair
from model.encoding import Encoding
from model.message_block import MessageBlock
from model.message_type import MessageType
from utils.compressor import Compressor
from utils.general_utils import GeneralUtils


class PlainMessageBlock(MessageBlock):

    def __init__(self, encryption_key_pair: IKeyPair, message_type: MessageType, message: str, encoding: Encoding):
        self.sender_public_key = encryption_key_pair.public_key
        self.message_type = message_type
        self.message = message

        message_type_value = struct.pack('!B', message_type.value)
        exported_encryption_key_pair = self.sender_public_key.to_bytes()
        encoding_str = Encoding.get_str(encoding)
        encoded_message = message.encode(encoding=encoding_str)
        nonce_timestamp = GeneralUtils.get_current_unix_timestamp()
        content = message_type_value + exported_encryption_key_pair + nonce_timestamp + encoded_message
        compression_algorithm, content = Compressor.compress_with_best_algorithm(content)

        super().__init__(encrypted_flag=False, compression_algorithm=compression_algorithm, content=content, encoding=encoding, encryption_key_pair=encryption_key_pair)
