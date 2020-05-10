import unittest

from business.message_block_builder import MessageBlockBuilder
from business.message_block_parser import MessageBlockParser
from model.blockchain_message_block import BlockchainMessageBlock
from model.message_type import MessageType
from repository.user_repository import UserRepository


class TestMessageBlock(unittest.TestCase):
    def test_building_and_parsing_encrypted_message(self):
        test_users = UserRepository.get_test_users()
        sender = test_users[0]
        recipients_public_keys = [test_users[1].encryption_key_pair.public_key]
        recipients_private_key = test_users[1].encryption_key_pair.private_key
        message = 'Random Message'
        message_type = MessageType.PRIVATE_POST

        message_block = MessageBlockBuilder.build_message_block(message=message, message_type=message_type, sender=sender, recipients_public_keys=recipients_public_keys)
        blockchain_message_block = BlockchainMessageBlock(timestamp=0, block_hash=None, data=message_block.to_bytes())
        parsed_block = MessageBlockParser.parse_message_block(blockchain_message_block=blockchain_message_block, private_key=recipients_private_key)

        self.assertEqual(message, parsed_block.message)
        self.assertEqual(message_type, parsed_block.message_type)
        self.assertEqual(sender.encryption_key_pair.public_key, parsed_block.sender)

    def test_building_and_parsing_plain_message(self):
        test_users = UserRepository.get_test_users()
        sender = test_users[0]
        message = 'Message'
        message_type = MessageType.PUBLIC_POST

        message_block = MessageBlockBuilder.build_message_block(message=message, message_type=message_type, sender=sender)
        blockchain_message_block = BlockchainMessageBlock(timestamp=0, block_hash=None, data=message_block.to_bytes())
        parsed_block = MessageBlockParser.parse_message_block(blockchain_message_block=blockchain_message_block)

        self.assertEqual(message, parsed_block.message)
        self.assertEqual(message_type, parsed_block.message_type)
        self.assertEqual(sender.encryption_key_pair.public_key, parsed_block.sender)


if __name__ == '__main__':
    unittest.main()
