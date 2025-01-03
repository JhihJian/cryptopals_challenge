from Crypto.Cipher import AES
import base64
from S2C9_Impl_PKCS_Padding import pkcs7_unpad

def aes_ecb_decrypt(data, key):
    """Decrypts the given AES-ECB encrypted data with the given key.
    The un-padding part has been added to support the use that I will make of this
    method on future challenges (for the sake of this challenge it's not needed).
    """
    cipher = AES.new(key, AES.MODE_ECB)
    return pkcs7_unpad(cipher.decrypt(data))


if __name__ == '__main__':
    with open("../resources/S1C07_input.txt") as input_file:
        binary_data = base64.b64decode(input_file.read())
    # Compute and print the decrypted plaintext
    print(aes_ecb_decrypt(binary_data, b'YELLOW SUBMARINE').decode().rstrip())
