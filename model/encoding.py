from enum import Enum


class Encoding(Enum):
    UTF_8 = 0
    UTF_16 = 1
    ASCII = 2

    @staticmethod
    def get_str(encoding: 'Encoding') -> str:
        if encoding is Encoding.UTF_8:
            return 'utf-8'
        elif encoding is Encoding.UTF_16:
            return 'utf-16'
        elif encoding is Encoding.ASCII:
            return 'ascii'
        else:
            raise ValueError
