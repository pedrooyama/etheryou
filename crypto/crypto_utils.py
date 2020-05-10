from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from parameters.constants import Constants


class CryptoUtils:

    # Ref: https://nitratine.net/blog/post/python-encryption-and-decryption-with-pycryptodome/
    @staticmethod
    def encrypt_bytes(symmetric_key: bytes, message: bytes):
        aes = AES.new(key=symmetric_key, mode=AES.MODE_CBC)
        ciphertext = aes.encrypt(pad(data_to_pad=message, block_size=Constants.AES_BLOCK_SIZE))
        iv = aes.iv
        return ciphertext, iv

    @staticmethod
    def decrypt_bytes(symmetric_key: bytes, ciphertext, iv, unpad_bytes: bool = True):
        aes = AES.new(key=symmetric_key, mode=AES.MODE_CBC, iv=iv)
        unpadded_plaintext = aes.decrypt(ciphertext)
        if not unpad_bytes:
            return unpadded_plaintext
        plaintext = unpad(unpadded_plaintext, Constants.AES_BLOCK_SIZE)
        return plaintext

    @staticmethod
    def generate_random_symmetric_key() -> bytes:
        return get_random_bytes(Constants.SYMMETRIC_KEY_LENGTH)
