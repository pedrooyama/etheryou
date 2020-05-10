from typing import List
from blockchain.account_service import AccountService
from blockchain.blockchain_api import BlockchainApi
from business.message_service import MessageService
from model.message import Message
from model.message_type import MessageType
from model.user import User
from parameters.constants import Constants


class UserManager:

    @property
    def selected_user(self) -> User:
        if self.selected_user_index < 0:
            return None
        if self.selected_user_index >= len(self.users):
            return None
        return self.users[self.selected_user_index]

    def __init__(self):
        self.users: List[User] = []
        self.users_messages = {}
        self.users_lastest_fetch_time = {}
        self.selected_user_index: int = -1

    def create_user_with_ether(self, amount_of_ether: int) -> int:
        if amount_of_ether > 0:
            eth_keys = AccountService().create_account_with_ether(amount_of_ether)
        else:
            eth_keys = AccountService().create_account()
        encryption_key_pair = Constants.PUBLIC_KEY_ALGORITHM().generate_random_key_pair()
        user = User(eth_key_pair=eth_keys, encryption_key_pair=encryption_key_pair)
        self.users.append(user)
        user_index = len(self.users)-1
        if user_index == 0:
            self.selected_user_index = user_index

        self.users_messages[user.eth_key_pair.public_key] = []
        self.users_lastest_fetch_time[user.eth_key_pair.public_key] = 0

        return user_index

    def select_user(self, user_index):
        if user_index < 0 or user_index >= len(self.users):
            raise ValueError
        self.selected_user_index = user_index

    def get_balance(self) -> float:
        return AccountService().get_balance(self.selected_user.eth_key_pair.public_key)

    def send_message(self, message_type: MessageType, message: str, recipients: List[str]) -> (int, int, int):
        recipients_public_keys = []
        for recipient in recipients:
            public_key = Constants.PUBLIC_KEY_ALGORITHM().get_public_key_class().parse(bytes.fromhex(recipient))
            recipients_public_keys.append(public_key)

        sender = self.selected_user
        return MessageService.send_message(sender=sender, message_type=message_type, message=message, recipients_public_keys=recipients_public_keys)

    def fetch_messages(self):
        timestamp = self.users_lastest_fetch_time[self.selected_user.eth_key_pair.public_key]
        self.users_lastest_fetch_time[self.selected_user.eth_key_pair.public_key] = BlockchainApi().get_latest_block_timestamp()
        messages = MessageService.fetch_messages_for_user(timestamp=timestamp, user=self.selected_user)
        for message in messages:
            self.add_message(message)

    def get_messages(self) -> List[Message]:
        return self.users_messages[self.selected_user.eth_key_pair.public_key]

    def get_message_from_hash(self, message_hash: str) -> Message:
        for message in self.users_messages[self.selected_user.eth_key_pair.public_key]:
            if message.block_hash == message_hash:
                return message
        return None

    def add_message(self, message: Message):
        if self.get_message_from_hash(message.block_hash):
            return
        self.users_messages[self.selected_user.eth_key_pair.public_key].append(message)



