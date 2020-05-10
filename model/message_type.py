from enum import Enum


class MessageType(Enum):
    PUBLIC_POST = 0
    PRIVATE_POST = 1
    DIRECT_MESSAGE = 2
    SHARE = 3
    LIKE = 4
