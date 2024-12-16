import base64
from itertools import combinations
def bytes_to_bit_list(byte_data):
    # 初始化一个空列表来存储位
    bit_list = []

    # 遍历bytes对象的每个字节
    for byte in byte_data:
        # 将字节转换为8位的二进制字符串，并去掉开头的'0b'
        binary_str = format(byte, '08b')

        # 将二进制字符串的每个字符（即每位）添加到列表中
        for bit in binary_str:
            bit_list.append(bit)

    return bit_list

def calculate_hamming_distance(byte_data1, byte_data2):
    bit_list1 = bytes_to_bit_list((byte_data1))
    bit_list2 = bytes_to_bit_list((byte_data2))
    if len(bit_list1)!=len(bit_list2):
        return 0
    count=0
    for i in range(0,len(bit_list1)):
        if bit_list1[i]!=bit_list2[i]:
            count+=1
    return count

# http://www.data-compression.com/english.html
CHARACTER_FREQ = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
}
def singlechar_xor(input_bytes, key_value):
    """XORs every byte of the input with the given key_value and returns the result."""
    output = b''

    for char in input_bytes:
        output += bytes([char ^ key_value])

    return output

# 输入加密列，返回最可能的密钥前三
def decrypt_binary_data_by_guess_byte_key(binary_data):
    result = {}
    candidates=[]
    for key_candidate in range(0, 256):
        # plaintext = []
        # for b in binary_data:
        #     plaintext.append(b ^ key_candidate)
        plaintext=singlechar_xor(binary_data,key_candidate)
        score = get_english_score(plaintext)
        result = {
            'key': key_candidate,
            'score': score,
            'plaintext': str(bytes(plaintext))
        }
        candidates.append(result)
    # Return the candidate with the highest English score
    return sorted(candidates, key=lambda c: c['score'], reverse=True)[0]

def singlechar_xor(input_bytes, key_value):
    """XORs every byte of the input with the given key_value and returns the result."""
    output = b''

    for char in input_bytes:
        output += bytes([char ^ key_value])

    return output

def singlechar_xor_brute_force(ciphertext):
    """Tries every possible byte for the single-char key, decrypts the ciphertext with that byte
    and computes the english score for each plaintext. The plaintext with the highest score
    is likely to be the one decrypted with the correct value of key.
    """
    candidates = []

    for key_candidate in range(256):
        plaintext_candidate = singlechar_xor(ciphertext, key_candidate)
        candidate_score = get_english_score(plaintext_candidate)

        result = {
            'key': key_candidate,
            'score': candidate_score,
            'plaintext': plaintext_candidate
        }

        candidates.append(result)

    # Return the candidate with the highest English score
    return sorted(candidates, key=lambda c: c['score'], reverse=True)[0]

def get_english_score(input_bytes):
    """Returns a score which is the sum of the probabilities in how each letter of the input data
    appears in the English language. Uses the above probabilities.
    """
    score = 0
    for byte in input_bytes:
        score += CHARACTER_FREQ.get(chr(byte).lower(), 0)
    return score


def repeating_key_xor(binary_data,key):
    plaintext=[]
    index=0
    for c in binary_data:
        plaintext.append(c^key[index])
        index=(index+1)%len(key)
    return bytes(plaintext)

def break_repeating_key_xor(binary_data):
    keysize_hamming_distance_avg_list= {}
    for keysize in range(2,41):
        chunks=[binary_data[i:i+keysize] for i in range(0,len(binary_data),keysize)][:4]
        distance = 0
        pairs = combinations(chunks, 2)
        for (x,y) in pairs:
            distance+=calculate_hamming_distance(x, y)
        distance/=6
        normalized_distance = distance / keysize
        keysize_hamming_distance_avg_list[keysize]=normalized_distance


    #找到最小值
    print(keysize_hamming_distance_avg_list)
    possible_key_sizes = sorted(keysize_hamming_distance_avg_list, key=keysize_hamming_distance_avg_list.get)[:3]
    print(possible_key_sizes)
    possible_plaintexts=[]
    # for guess_keysize in possible_key_sizes:
    for guess_keysize in possible_key_sizes:
        print("guess key size:"+str(guess_keysize))
        key = b''
        for i in range(guess_keysize):
            block = b''
            # Transpose the blocks: make a block that is the i-th byte of every block
            for j in range(i, len(binary_data), guess_keysize):
                block += bytes([binary_data[j]])
            key+=bytes([singlechar_xor_brute_force(block)['key']])
        possible_plaintexts.append((repeating_key_xor(binary_data, key), key))
        # Return the candidate with the highest English score
    return max(possible_plaintexts, key=lambda k: get_english_score(k[0]))

if __name__ == '__main__':
    assert calculate_hamming_distance(b'this is a test', b'wokka wokka!!!') == 37
    with open('../resources/S1C06_input.txt', 'r', encoding='utf-8') as f:
        binary_data = base64.b64decode(f.read())
    # Compute and print the result of the attack
    result = break_repeating_key_xor(binary_data)
    print(result)
    print("Key =", result[1].decode())
    print("---------------------------------------")
    print(result[0].decode().rstrip())

#
# import string
#
# # 初始化一个空列表来存储ASCII码
# ascii_codes = []
#
# # 添加ASCII字母的码值
# for char in string.ascii_letters:
#     ascii_codes.append(ord(char))
#
# # 添加ASCII数字的码值
# # for char in string.digits:
# #     ascii_codes.append(ord(char))
#
#
# # 添加ASCII标点符号的码值
# # for char in string.punctuation:
# #     ascii_codes.append(ord(char))
# ascii_codes.append(ord("'"))
# ascii_codes.append(ord(","))
# ascii_codes.append(ord("."))
# ascii_codes.append(ord("!"))
# ascii_codes.append(ord("?"))
#
# # 如果你还需要空格，也可以加上
# ascii_codes.append(ord(' '))
#
#
#
# word_ascii_codes=[]
#
# # 添加ASCII字母的码值
# for char in string.ascii_letters:
#     word_ascii_codes.append(ord(char))
# ######################################################
# guess_keysize=8
# all_byte_values = [b for b in range(256)]
# guess_key=[]
# for i in range(0,guess_keysize):
#     guess_key.append([])
# for key_index in range(0,guess_keysize):
#     # for guess_key_i in word_ascii_codes:
#     for guess_key_i in b"Vigenere":
#         not_in_common_code_count = 0
#         all_code_count = 0
#         for file_content_bytes in file_lines:
#             # if guess_key_i not in word_ascii_codes:
#             #     continue
#             is_right_guess=True
#             plain_word_list=[]
#             time = 0
#
#             while time*guess_keysize+guess_keysize<len(file_content_bytes):
#                 block=file_content_bytes[time*guess_keysize:time*guess_keysize+guess_keysize]
#                 plain_word=block[key_index]^guess_key_i
#                 # plain_word_list.append(plain_word)
#                 all_code_count+=1
#                 if plain_word not in ascii_codes:
#                     not_in_common_code_count+=1
#                 # if plain_word > 127:
#                 #     is_right_guess=False
#                 #     break
#                 time+=1
#
#         # if is_right_guess==True:
#         if (not_in_common_code_count/all_code_count) <0.1:
#             print(not_in_common_code_count / all_code_count)
#             print("密钥"+str(key_index)+"猜测为"+chr(guess_key_i))
#             guess_key[key_index].append(guess_key_i)
#
# print(guess_key)
#
# all_guess_key_list=[""]
# for i in range(0,len(guess_key)):
#     new_list = []
#     for c in guess_key[i]:
#         for sub in all_guess_key_list:
#             new_list.append(sub+chr(c))
#     all_guess_key_list=new_list
# all_guess_key_list=set(all_guess_key_list)
# print(all_guess_key_list)
# #
#
#
#
# all_guess_key_list=["Vigenere"]
# for key in all_guess_key_list:
#     for file_content_bytes in file_lines:
#         result_bytes = []
#         index = 0
#         for b in file_content_bytes:
#             c=b ^b"Vigenere"[index]
#             result_bytes.append(c)
#             index = (index + 1) % len(key)
#         print(bytes( result_bytes))