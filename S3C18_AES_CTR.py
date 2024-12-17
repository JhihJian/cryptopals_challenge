from S2C10_Impl_CBC_Mode import aes_ecb_encrypt,aes_cbc_decrypt
import secrets
import struct
def xor_bytes(plaintext_binary,keystream_binary):
    assert len(plaintext_binary)<=len(keystream_binary)
    result=[]
    for i in range(len(plaintext_binary)):
        result.append(plaintext_binary[i]^keystream_binary[i])
    return b''.join([i.to_bytes(1,'big') for i in result])

def aes_ctr_encrypt(binary_data, key_bytes, nonce=None):
    block_size=16
    encrypt_result=b''
    if nonce is None:
        nonce=secrets.randbelow(2**64)
    for start in range(0, len(binary_data), block_size):
        end = min(start + block_size, len(binary_data))
        count=start//block_size
        # count_bytes = count.to_bytes(8, 'little')
        # nonce_count_bytes = nonce_bytes + count_bytes
        nonce_count_bytes = struct.pack('<QQ', nonce, count)
        keystream=aes_ecb_encrypt(key_bytes,nonce_count_bytes)
        encrypt_result+=xor_bytes(binary_data[start:end],keystream)
    return encrypt_result,nonce

def aes_ctr_decrypt(binary_data,key_bytes,nonce):
   return aes_ctr_encrypt(binary_data,key_bytes,nonce)


if __name__ == '__main__':

    print(xor_bytes(b'111',b'1111'))
    encrypt_result,nonce_bytes=aes_ctr_encrypt(b'aaaabbbbbcccaaaacdddd', b'"YELLOW SUBMARINE"')
    print('encrypt_result:'+str(encrypt_result))
    print('nonce_bytes:'+str(nonce_bytes))
    decrypt_result,nonce_bytes=aes_ctr_encrypt(encrypt_result, b'"YELLOW SUBMARINE"', nonce_bytes)
    print('decrypt_result:'+str(decrypt_result))
