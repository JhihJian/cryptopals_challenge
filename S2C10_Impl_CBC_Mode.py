from Crypto.Cipher import AES
import base64
from Crypto.Cipher.AES import block_size
from S2C9_Impl_PKCS_Padding import pkcs7_pad, pkcs7_unpad
from S1.Challenge_7_AES_Decrypy import aes_ecb_decrypt
def aes_ecb_encrypt(data, key):
    """Encrypts the given data with AES-ECB, using the given key.
    The data is always PKCS 7 padded before being encrypted.
    """
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pkcs7_pad(data, AES.block_size))

def aes_cbc_encrypt(data, key, iv):
    """Encrypts the given data with AES-CBC, using the given key and iv."""
    ciphertext = b''
    prev = iv
    # Process the encryption block by block
    for i in range(0, len(data), AES.block_size):
        # Always PKCS 7 pad the current plaintext block before proceeding
        curr_plaintext_block = pkcs7_pad(data[i:i + AES.block_size], AES.block_size)
        block_cipher_input = xor_data(curr_plaintext_block, prev)
        encrypted_block = aes_ecb_encrypt(block_cipher_input, key)
        ciphertext += encrypted_block
        prev = encrypted_block

    return ciphertext

def aes_cbc_decrypt(data, key, iv, unpad=True):
    """Decrypts the given AES-CBC encrypted data with the given key and iv.
    Returns the unpadded decrypted message when unpad is true, or keeps the plaintext
    padded when unpad is false.
    """
    plaintext = b''
    prev = iv

    # Process the decryption block by block
    for i in range(0, len(data), AES.block_size):
        curr_ciphertext_block = data[i:i + AES.block_size]
        decrypted_block = aes_ecb_decrypt(curr_ciphertext_block, key)
        plaintext += xor_data(prev, decrypted_block)
        prev = curr_ciphertext_block

    # Return the plaintext either unpadded or left with the padding depending on the unpad flag
    return pkcs7_unpad(plaintext) if unpad else plaintext

def xor_data(binary_data_1, binary_data_2):
    """Returns the xor of the two binary arrays given."""
    return bytes([b1 ^ b2 for b1, b2 in zip(binary_data_1, binary_data_2)])

if __name__ == '__main__':
    with open("resources/S2C10_input.txt","r") as f:
        binary_content=base64.b64decode(f.read())

    chunks=[binary_content[index:index+block_size] for index in range(0,len(binary_content),block_size)]
    init_vector=b"\x00\x00\x00 &c"
    key=b"YELLOW SUBMARINE"
    origin_data=aes_cbc_decrypt(binary_content,key,init_vector,True)
    print(origin_data.decode('ascii') )

