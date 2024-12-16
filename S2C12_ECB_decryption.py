import math

from S2C10_Impl_CBC_Mode import aes_ecb_encrypt,pkcs7_unpad
import base64
import secrets

random_key=secrets.token_bytes(16)

def encrypt_with_unknown_str(str_bytes):
    unknown_str = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
    aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
    dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
    YnkK"""
    unknown_str_bytes = base64.b64decode(unknown_str)
    encrypt_bytes = aes_ecb_encrypt(b'\xf2o\x81\xa4e\x9f\xb8\xa0\xa9|\xc7|\xa7\xad\xeb\xd4Ty\xfe\xfe\x01\xc2\x08\xe3,\xab\xf9\x1f\x90F\xb4\xf5:\xaf!\xcf\xe2a\x10\x18\xb6\x1a\x1d\xa1#\xe2\x1cy\xc2\x9f\xf8\xea~\x9e%\xe5\xa8\xd3\\X\x17E~\x8f\xc3\x10l\x8b\x13\x81\xaa\x12\x96\x8as\x7f\xe1\xe9\xe1@b\xa6\x8c\x0c?\xd1\r\xedz\xa9\xf17\x03N\xb1\xba\xfc\xc1'+str_bytes + unknown_str_bytes, random_key)
    return encrypt_bytes

def discover_the_block_size_of_the_cipher(func):
    block_size=0
    offset=0
    for padding_len in range(8,256,2):
        text_data=b''.join([b'A']*padding_len)
        cipher_data=func(text_data)
        # 这里的+1是为了闭合区间
        for block_size in range(2,padding_len//2+1):
            # for offset in range(0,len(cipher_data)-2*block_size):
            for time in range(0,len(cipher_data)//block_size-1):
                if cipher_data[time*block_size:(time+1)*block_size] == cipher_data[(time+1)*block_size:(time+2)*block_size]:
                    return (block_size,(time+2)*block_size-padding_len)
    return block_size,offset

def guess_next_word(block_size,func,input_offset):
    result_guess_word_bytes=b''
    # print("all:"+str(func(b'')))

    for time in range(len(func(b''))//block_size):
        already_guess_block_word_bytes = b''
        for i in range(block_size):
            left=time*block_size+math.ceil(input_offset/block_size)*block_size
            right=left+block_size
            guess_word_block=b''.join([b'B']*(block_size-input_offset%block_size))+b''.join([b'A']*(block_size-i-1))
            cipher_text = func(guess_word_block)
            for word_int in range(128):
                try_word=guess_word_block+result_guess_word_bytes+already_guess_block_word_bytes+word_int.to_bytes(1,'big')
                try_cipher_text = func(try_word)
                origin=cipher_text[left:right]
                guess=try_cipher_text[left:right]
                if origin==guess:
                    already_guess_block_word_bytes+=word_int.to_bytes(1,'big')
                    break
        result_guess_word_bytes+=already_guess_block_word_bytes
    print("猜测密文的结果是:"+str(pkcs7_unpad(result_guess_word_bytes)))
    return  pkcs7_unpad(result_guess_word_bytes)

if __name__ == '__main__':
    guess_block_size,offset=discover_the_block_size_of_the_cipher(encrypt_with_unknown_str)
    print("猜测block size:"+str(guess_block_size))
    print("猜测 offset:"+str(offset))
    print(aes_ecb_encrypt(b'AAAAAAAA', b"random_key123456"))
    print(aes_ecb_encrypt(b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', b"random_key123456"))
    unknown_str = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
       aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
       dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
       YnkK"""

    result=guess_next_word(16,encrypt_with_unknown_str,offset)
    print("猜测结果:"+str(result))
    # assert base64.b64decode(unknown_str)==result