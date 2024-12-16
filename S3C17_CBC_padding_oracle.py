from S2C10_Impl_CBC_Mode import aes_cbc_encrypt,aes_cbc_decrypt
from S2C9_Impl_PKCS_Padding import is_pkcs7_padded,pkcs7_pad,pkcs7_unpad
import secrets
import random
import  base64
import uuid
from S2C16_CBC_bitflipping_attacks import xor_bytes
# 给定的 Base64 编码字符串列表
base64_strings = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBVZWdhJ3MgYXJlIHp1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmlmYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGaIGhpaIGhhdCB3aXRoIGEgc291cGVkIHVwIHRlbXBvw==",
    "MDAwMDA3SSdmIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
]
def random_choice_from_list():
    # 从解码后的字符串列表中随机选择一个
    return base64.b64decode(random.choice(base64_strings))

# init ---------------------
IV=uuid.uuid4().bytes
encrypt_key=secrets.token_bytes(16)
# init ---------------------


def encrypt(binary_data):
    encrypt_data=aes_cbc_encrypt(binary_data,encrypt_key,IV)
    return encrypt_data,IV
def decrypt_and_check_padding(binary_data,iv):
    decrypt_data=aes_cbc_decrypt(binary_data,encrypt_key,iv,False)
    # print("decrypt user input is:"+str(decrypt_data))
    return is_pkcs7_padded(decrypt_data)

# 测试函数
user_input=random_choice_from_list()
print("user encrypt:"+str(user_input))
encrypt_data,iv=encrypt(user_input)

#----------------------attack_begin_------------

print("user encrypt result:"+str(encrypt_data)+",iv:"+str(iv))
decrypt_check_result=decrypt_and_check_padding(encrypt_data,iv)
print("decrypt check result:"+ str(decrypt_check_result))


#----------------------attack_begin_------------
block_size=len(iv)
total_result=b''
pre_iv=iv
for left in range(0,len(encrypt_data),block_size):
    right=left+block_size
    intermediary_block_value=[b'0']*block_size
    attack_block_value=[b'0']*block_size
    for index in range(1,len(pre_iv)-1):
        for i in range(0,256):
            attack_block_value[-index]=i.to_bytes(1,'big')
            if decrypt_and_check_padding(encrypt_data[left:right],b''.join(attack_block_value)):
                # print("发现目标:"+str(i))
                intermediary_block_value[-index] = (i ^ index).to_bytes(1, 'big')
                attack_block_value[-index] = (intermediary_block_value[-index][0] ^ index.to_bytes(1, 'big')[0]).to_bytes(1, 'big')
                for j in range(0,index+1):
                    attack_block_value[-j]= (attack_block_value[-j][0]^index^(index+1).to_bytes(1,'big')[0]).to_bytes(1,'big')
                break
    current_block_decrypt_result=xor_bytes(b''.join(intermediary_block_value), pre_iv)
    # print(str(current_block_decrypt_result))
    pre_iv=encrypt_data[left:right]
    total_result=total_result+current_block_decrypt_result
total_result=pkcs7_unpad(total_result)
print(str(total_result))
assert total_result==user_input




