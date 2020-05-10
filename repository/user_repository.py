from typing import List
from model.eth_key_pair import EthKeyPair
from model.user import User
from parameters.constants import Constants


class UserRepository:

    @staticmethod
    def get_test_users() -> List[User]:

        public_key_algorithm = Constants.PUBLIC_KEY_ALGORITHM()

        encryption_key_pair_A = public_key_algorithm.generate_random_key_pair()
        # TODO: define user A Ethereum key pair (from Ganache)
        eth_public_key_A = '__PUBLIC_KEY_A__'
        eth_private_key_A = '__PRIVATE_KEY_A__'
        eth_key_pair_A = EthKeyPair(public_key=eth_public_key_A, private_key=eth_private_key_A)
        user_A = User(eth_key_pair=eth_key_pair_A, encryption_key_pair=encryption_key_pair_A)

        encryption_key_pair_B = public_key_algorithm.generate_random_key_pair()
        # TODO: define user B Ethereum key pair (from Ganache)
        eth_public_key_B = '__PUBLIC_KEY_B__'
        eth_private_key_B = '__PRIVATE_KEY_B__'
        eth_key_pair_B = EthKeyPair(public_key=eth_public_key_B, private_key=eth_private_key_B)
        user_B = User(eth_key_pair=eth_key_pair_B, encryption_key_pair=encryption_key_pair_B)

        return [user_A, user_B]
