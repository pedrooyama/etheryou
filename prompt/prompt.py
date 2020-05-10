from cmd import Cmd
from business.user_manager import UserManager
from model.message import Message
from model.message_type import MessageType
from model.user import User
from datetime import datetime
from utils.general_utils import GeneralUtils


class Prompt(Cmd):

    def __init__(self):
        self.user_manager = UserManager()
        self.not_implemented_types = [MessageType.LIKE, MessageType.SHARE]
        super().__init__()

    def run(self):
        self.prompt = '>'
        self.cmdloop('Starting prompt...')

    def do_list_message_types(self, args):
        """Lists the supported message types"""

        for message_type in MessageType:
            if message_type not in self.not_implemented_types:
                print('[%d]: %s' % (message_type.value, message_type.name))

    def do_create_user(self, args):
        """Creates a new user ans saves its info to file"""
        user_index = self.user_manager.create_user_with_ether(10)
        user = self.user_manager.users[user_index]
        print('A new user has been created:')
        self.__print_user(user_index, user)
        self.__print_user_captions()

    def do_list_users(self, args):
        """List the users"""
        if len(self.user_manager.users) == 0:
            return

        selected_user_index = self.user_manager.selected_user_index
        for i, user in enumerate(self.user_manager.users):
            is_selected = selected_user_index == i
            self.__print_user(i, user, is_selected)
        self.__print_user_captions()
        print('')
        print('-->: Selected User')

    def do_get_balance(self, args):
        """Get selected user's eth balance. """
        balance = self.user_manager.get_balance()
        print('%f Ether' % (balance))

    def do_send_message(self, args):
        """Send message as selected user to a list of users (their public keys)"""
        self.do_list_message_types(None)
        message_type = MessageType(int(input('Enter Message Type From List Above:')))

        if message_type == MessageType.PUBLIC_POST:
            recipients = []
        else:
            raw_recipients = input('Enter Recipients Public Keys (separeted by \',\'):')
            recipients = raw_recipients.split(',')

        message = input('Enter the Message:')

        timestamp, gas_used, _ = self.user_manager.send_message(message_type=message_type, message=message, recipients=recipients)
        timestamp_str = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print('The message was sent at %s consuming %d gas.' % (timestamp_str, gas_used))

    def do_list_messages(self, args):
        """List selected user's messages"""
        self.user_manager.fetch_messages()
        messages = self.user_manager.get_messages()
        for message in messages:
            self.__print_message(message)

    def __print_message(self, message: Message):
        timestamp_str = datetime.utcfromtimestamp(message.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        nonce_timestamp_str = datetime.utcfromtimestamp(message.nonce_timestamp).strftime('%Y-%m-%d %H:%M:%S')

        if self.user_manager.selected_user.encryption_key_pair.public_key == message.sender:
            sender = 'MYSELF'
        else:
            sender = message.sender.to_bytes().hex()

        print('FROM: %s' % sender)
        print('MESSAGE HASH: %s' % GeneralUtils.encode_base_64(message.block_hash))
        print('BLOCKCHAIN TIMESTAMP: %s' % timestamp_str)
        print('NONCE TIMESTAMP: %s' % nonce_timestamp_str)
        print('MESSAGE TYPE: %s' % message.message_type.name)
        print('MESSAGE: %s' % message.message)
        print('--------------------------------------------------------------------------------')

    def __print_user(self, index: int, user: User, is_selected: bool = False):
        selected_mark = '   '
        if is_selected:
            selected_mark = '-->'
        key = user.encryption_key_pair.public_key.to_bytes().hex()
        print('%s[%d]: %s' % (selected_mark, index, key))

    def __print_user_captions(self):
        print('    ^       ^')
        print('    |       |------- Public Key')
        print('    |---- User index ')

    def do_select_user(self, args):
        """Select User"""
        user_index = int(args[0])
        self.user_manager.select_user(user_index)
        print('Selected User: %d' % user_index)

    def do_exit(self, args):
        """Exits the program."""
        raise SystemExit
