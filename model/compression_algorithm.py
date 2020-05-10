from enum import Enum


class CompressionAlgorithm(Enum):
    NONE = 0
    LZMA = 1
    ZLIB = 2
    BZ2 = 3
