from typing import List

from crypto.algorithms.interface.i_key_pair import IKeyPair
from model.compression_algorithm import CompressionAlgorithm
from model.encoding import Encoding
from model.message_block import MessageBlock


class EncryptedMessageBlock(MessageBlock):

    def __init__(self, iv: bytes, encrypted_content: bytes, key_encryptions: List[bytes], compression_algorithm:CompressionAlgorithm, encoding: Encoding, encryption_key_pair: IKeyPair):
        content = iv + encrypted_content
        for key_encryption in key_encryptions:
            content += key_encryption
        super().__init__(encrypted_flag=True, compression_algorithm=compression_algorithm, content=content, encoding=encoding,
                         encryption_key_pair=encryption_key_pair)

