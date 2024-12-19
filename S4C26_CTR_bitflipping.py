from urllib.parse import quote_plus
import  secrets
import random
# from S2C10_Impl_CBC_Mode import aes_cbc_encrypt,aes_cbc_decrypt
from S3C18_AES_CTR import  aes_ctr_decrypt,aes_ctr_encrypt
random_key=secrets.token_bytes(16)
IV=secrets.token_bytes(16)

def process_user_input(input_string):
    # 定义要添加的前缀和后缀
    prefix = "comment1=cooking%20MCs;userdata="
    suffix = ";comment2=%20like%20a%20pound%20of%20bacon"
    # 对输入字符串、";" 和 "=" 进行URL编码
    encoded_input = quote_plus(input_string)

    # 构建完整的字符串，注意这里的encoded_semicolon和encoded_equals实际上不需要用到，
    # 因为prefix和suffix已经包含了编码后的特殊字符
    result = prefix + encoded_input + suffix
    # 因为在这个特定情况下，prefix和suffix已经是预编码的，所以我们不需要额外处理";"和"="
    # 如果输入字符串需要单独处理这些字符，我们已经在quote_plus(input_string)中完成了
    return aes_ctr_encrypt(result.encode('ascii'),random_key,0)

def check_user_auth(user_encrypt_data):
    try:
        user_data,nonce=aes_ctr_decrypt(user_encrypt_data,random_key,0)
        user_data=str(user_data,'ascii',errors='ignore')
        print("process user data:"+user_data)
        return ";admin=true;" in user_data
    except UnicodeDecodeError as e:
        print("process user data error.",e)
        return False
    except ValueError as e:
        print("process user data error.",e)
        return False

def shuffle_bytes(input_bytes):
    # 将bytes转换为bytearray，因为bytearray是可变的
    byte_array = bytearray(input_bytes)
    # 使用random.shuffle打乱bytearray的顺序
    random.shuffle(byte_array)
    # 将打乱后的bytearray转换回bytes
    shuffled_bytes = bytes(byte_array)
    return shuffled_bytes


def xor_bytes(bs1,bs2):
    return bytes([b1 ^ b2 for b1, b2 in zip(bs1, bs2)])

def attack_user_encrypt_data(attack_key,user_encrypt_data):
    all_result=[]
    for index in range(len(user_encrypt_data)-len(attack_key)):
        all_result.append(user_encrypt_data[0:index]+xor_bytes(attack_key,user_encrypt_data[index:]))
    return all_result


user_input=b"aaaaaaaaaaaa"
print(("user input:"+str(user_input)))


user_encrypt_data,nonce=process_user_input(user_input)
print(("user_encrypt_data:"+str(user_encrypt_data)))

print("check_user_auth:"+str(check_user_auth(user_encrypt_data)))
print("进行攻击")
attack_key_bytes=xor_bytes(user_input,b";admin=true;")
user_encrypt_data=user_encrypt_data[0:32]+xor_bytes(user_encrypt_data[32:44],attack_key_bytes)+user_encrypt_data[44:]

print("攻击结果 check_user_auth:"+str(check_user_auth(user_encrypt_data)))




