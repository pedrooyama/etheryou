import unittest

from crypto.algorithms.impl.curve25519.curve25519_algorithm import Curve25519Algorithm
from crypto.algorithms.impl.rsa.rsa_algorithm import RSAAlgorithm
from exception.unable_to_decrypt import UnableToDecrypt


class TestEncryptionAlgorithms(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.algorithms = [Curve25519Algorithm, RSAAlgorithm]

    def setUp(self):
        formated_test_name = str.upper(self._testMethodName.replace('test_', 'testing_')).replace('_', ' ')
        print('__________________________________________')
        print(formated_test_name)
        print('')

    def test_encryption_and_decryption(self):
        plaintext = 'A message'.encode()

        for algorithm in self.algorithms:
            print ('Testing %s ...' % algorithm.name(), end="", flush=True)

            key_pair = algorithm.generate_random_key_pair()
            public_key = key_pair.public_key
            private_key = key_pair.private_key

            ciphertext = algorithm.encrypt_bytes(plaintext, public_key)
            decrypted_message = algorithm.decrypt_bytes(ciphertext, private_key)

            self.assertEqual(plaintext, decrypted_message)
            print('[OK]')

    def test_decrypting_with_wrong_private_key(self):
        plaintext = 'A message'.encode()

        for algorithm in self.algorithms:
            print('Testing %s ...' % algorithm.name(), end="", flush=True)

            key_pair = algorithm.generate_random_key_pair()
            public_key = key_pair.public_key
            right_private_key = key_pair.private_key
            wrong_private_key = algorithm.generate_random_key_pair().private_key

            # Decrypting with
            ciphertext = algorithm.encrypt_bytes(plaintext, public_key)
            decrypted_message = algorithm.decrypt_bytes(ciphertext, right_private_key)
            self.assertEqual(plaintext, decrypted_message)

            with self.assertRaises(UnableToDecrypt):
                algorithm.decrypt_bytes(ciphertext, wrong_private_key)
            print('[OK]')

    def test_sign_and_verify(self):
        message = 'A message'.encode()

        for algorithm in self.algorithms:
            print('Testing %s ...' % algorithm.name(), end="", flush=True)

            key_pair = algorithm.generate_random_key_pair()
            public_key = key_pair.public_key
            private_key = key_pair.private_key

            signature = algorithm.sign(message, private_key)

            self.assertTrue(algorithm.verify_signature(message, signature, public_key))
            print('[OK]')

    def test_exporting_and_importing_public_key(self):
        plaintext = 'A message'.encode()

        for algorithm in self.algorithms:
            print('Testing %s ...' % algorithm.name(), end="", flush=True)

            key_pair = algorithm.generate_random_key_pair()
            public_key = key_pair.public_key
            private_key = key_pair.private_key

            exported_public_key = public_key.to_bytes()
            imported_public_key = algorithm.get_public_key_class().parse(exported_public_key)

            ciphertext = algorithm.encrypt_bytes(plaintext, imported_public_key)
            decrypted_message = algorithm.decrypt_bytes(ciphertext, private_key)

            self.assertEqual(plaintext, decrypted_message)
            print('[OK]')

    def test_exporting_and_importing_private_key(self):
        plaintext = 'A message'.encode()

        for algorithm in self.algorithms:
            print('Testing %s ...' % algorithm.name(), end="", flush=True)

            key_pair = algorithm.generate_random_key_pair()
            public_key = key_pair.public_key
            private_key = key_pair.private_key

            exported_private_key = private_key.to_bytes()
            imported_private_key = algorithm.get_private_key_class().parse(exported_private_key)

            ciphertext = algorithm.encrypt_bytes(plaintext, public_key)
            decrypted_message = algorithm.decrypt_bytes(ciphertext, imported_private_key)

            self.assertEqual(plaintext, decrypted_message)
            print('[OK]')

    def test_eq_is_overloaded_in_public_key(self):
        for algorithm in self.algorithms:
            print('Testing %s ...' % algorithm.name(), end="", flush=True)

            public_key = algorithm.generate_random_key_pair().public_key

            exported_public_key = public_key.to_bytes()
            imported_public_key = algorithm.get_public_key_class().parse(exported_public_key)

            self.assertEqual(public_key, imported_public_key)
            print('[OK]')


if __name__ == '__main__':
    unittest.main()
