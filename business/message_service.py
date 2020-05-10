from typing import List
from blockchain.blockchain_api import BlockchainApi
from business.message_block_builder import MessageBlockBuilder
from business.message_block_parser import MessageBlockParser
from crypto.algorithms.interface.i_public_key import IPublicKey
from exception.not_intended_receiver import NotIntendedReceiver
from model.blockchain_message_block import BlockchainMessageBlock
from model.message import Message
from model.message_type import MessageType
from model.user import User


class MessageService:

    @staticmethod
    def filter_messages_for_user(message_blocks: List[BlockchainMessageBlock], user: User) -> List[Message]:
        messages = []
        for message_block in message_blocks:
            try:
                messages.append(MessageBlockParser.parse_message_block(blockchain_message_block=message_block,
                                                                       private_key=user.encryption_key_pair.private_key))
            except NotIntendedReceiver:
                pass
        return messages

    @staticmethod
    def fetch_messages_for_user(timestamp: int, user: User) -> List[Message]:
        blockchain_messages = BlockchainApi().fetch_messages_from_timestamp(timestamp=timestamp)
        return MessageService.filter_messages_for_user(message_blocks=blockchain_messages, user=user)

    @staticmethod
    def send_message(sender: User, message_type: MessageType, message: str, recipients_public_keys: List[IPublicKey] = None) -> (int, int, int):
        if not recipients_public_keys:
            recipients_public_keys = []

        if message_type == MessageType.PRIVATE_POST:
            recipients_public_keys = []
            for user_public_key in sender.followers:
                recipients_public_keys.append(user_public_key)
        recipients_public_keys.append(sender.encryption_key_pair.public_key)

        message_block = MessageBlockBuilder.build_message_block(message=message, message_type=message_type, sender=sender,
                                                                recipients_public_keys=recipients_public_keys)

        return BlockchainApi().send_message(sender=sender, message_block=message_block)

    @staticmethod
    def follow(follower: User, followed: User):
        followed.followers.append(follower.encryption_key_pair.public_key)
        follower.following.append(followed.encryption_key_pair.public_key)

