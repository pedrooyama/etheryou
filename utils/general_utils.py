from typing import List
from datetime import datetime
import time
import struct
import base64


class GeneralUtils:

    @staticmethod
    def bit_list_to_int(bit_list: List[bool]) -> int:
        reverse_bit_list = bit_list.copy()
        reverse_bit_list.reverse()

        power = 1
        value = 0
        for bit in reverse_bit_list:
            if bit:
                value += power
            power *= 2
        return value

    @staticmethod
    def get_current_unix_timestamp() -> bytes:
        return struct.pack('i', int(time.time()))

    @staticmethod
    def encode_base_64(data: bytes) -> str:
        return base64.b64encode(data)

    @staticmethod
    def decode_unix_timestamp(encoded_timestamp: bytes) -> int:
        return struct.unpack('i', encoded_timestamp)[0]

    @staticmethod
    def convert_unix_timestamp_to_human_string(timestamp: int) -> str:
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

