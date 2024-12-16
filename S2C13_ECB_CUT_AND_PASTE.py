import secrets
from S2C10_Impl_CBC_Mode import aes_ecb_encrypt,aes_ecb_decrypt
from S2C12_ECB_decryption import discover_the_block_size_of_the_cipher,guess_next_word
def query_string_to_dict(query_string):
    # 初始化一个空字典来存储结果
    result = {}

    # 使用 split('&') 方法将查询字符串分割成键值对字符串的列表
    pairs = query_string.split('&')

    # 遍历每个键值对字符串
    for pair in pairs:
        # 使用 split('=') 方法将键值对字符串分割成键和值
        key, value = pair.split('=')

        # 将解码后的键和值添加到结果字典中
        # 这里假设查询字符串是有效的，即每个键值对都只有一个 '=' 并且格式正确
        result[key] = value

    return result


def profile_for(email):
    # 定义一个字典，包含电子邮件地址、固定的用户ID和角色
    profile = {
        'email': email,  # 吞噬 & 和 = 元字符（尽管它们通常不会出现在电子邮件中）
        'uid': 10,
        'role': 'role'
    }

    # 将字典编码为查询字符串
    pairs = [f"{key}={value}" for key, value in profile.items()]
    query_string = '&'.join(pairs)

    # 返回编码后的查询字符串
    return query_string




random_key=secrets.token_bytes(16)
# random_key="secrets.token_by"
def encrypt_profile(email):
   return aes_ecb_encrypt(profile_for(email).encode('ascii'),random_key)

def encrypt_profile_with_bytes_input(email_bytes):
   return encrypt_profile(str(email_bytes, 'ascii'))

email_address = "foo@bar.com"
profile = encrypt_profile(email_address)
print(profile)

print(aes_ecb_decrypt(profile,random_key))

guess_block_size,offset=discover_the_block_size_of_the_cipher(encrypt_profile_with_bytes_input)
print("猜测block size:" + str(guess_block_size))
print("猜测 offset:" + str(offset))
result=guess_next_word(guess_block_size,encrypt_profile_with_bytes_input,offset)
print("猜测结果:"+str(result))