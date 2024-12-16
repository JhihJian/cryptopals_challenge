import random
import secrets
from S2C10_Impl_CBC_Mode import aes_cbc_encrypt,aes_ecb_encrypt
from S1.Challenge_8_Detect_AES_In_ECB import count_duplicate_block_in_aes_ciphertext
def generate_random_bytes(n=16):
    """
    生成 n 个随机字节。

    参数:
    n (int): 要生成的随机字节的数量，默认为 16。

    返回:
    bytes: 包含 n 个随机字节的字节串。
    """
    return secrets.token_bytes(n)

def random_padding(binary_data):
    return generate_random_bytes(random.randint(5,10))+binary_data+generate_random_bytes(random.randint(5,10))

def random_encrypt(binary_data):
    mode=''
    if random.randint(0,1):
        cipher_data=aes_cbc_encrypt(binary_data,generate_random_bytes(16),generate_random_bytes(16))
        mode='cbc'
    else:
        cipher_data=aes_ecb_encrypt(binary_data,generate_random_bytes(16))
        mode = 'ecb'
    return cipher_data,mode

def detect_data_aes_encrypts_mode(binary_data):
    detect_result=count_duplicate_block_in_aes_ciphertext(binary_data)
    if detect_result >0:
        return "ecb"
    else:
        return "cbc"

if __name__ == '__main__':
    total=100
    count_guess_right_time=0
    for i in range(total):
        origin_data=b'We choose a repeating input data so that we will be able to detect'
        cipher_data,cipher_mode=random_encrypt(origin_data)
        guess_cipher_mode=detect_data_aes_encrypts_mode(cipher_data)
        if guess_cipher_mode==cipher_mode:
            count_guess_right_time+=1
    print("总重复次数:"+str(total)+"猜测正确次数:"+str(count_guess_right_time))