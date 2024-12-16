import base64
from S3C18_AES_CTR import aes_ctr_process,xor_bytes
import secrets
from S1.Challenge_6_Break_repeating_key_XOR import get_english_score
if __name__ == '__main__':
    nonce=0
    block_size=16
    aes_key=secrets.token_bytes(block_size)
    base64bytes_list=[base64.b64decode(line.strip()) for line in open("resources/S3C19_input.txt", 'r', encoding='utf-8')]
    encrypt_result_list=[aes_ctr_process(line_b,aes_key,nonce)[0] for line_b in base64bytes_list]
    print("encrypt_result_list:"+str(encrypt_result_list))
    # attack begin--------------------------------
    guess_keystream=[]

    # 初始化总长度和元素数量
    total_length = 0
    num_elements = len(encrypt_result_list)

    # 遍历数组，累加每个字符串的长度
    for item in encrypt_result_list:
        total_length += len(item)

    # 计算平均长度
    average_length = total_length / num_elements

    # 输出平均长度
    print("数组元素的平均长度是:", average_length)

    # 初始化最长项和它的长度
    longest_item = b''
    max_length = 0

    # 遍历数组，找出最长的字符串
    for item in encrypt_result_list:
        if len(item) > max_length:
            longest_item = item
            max_length = len(item)
    attack_line=longest_item

    for i in range(len(longest_item)):
        candidates=[]
        for b in range(32,127):
            guess_keystream_i = b ^ attack_line[i]
            flag=True
            guess_result=[]

            for bytes_line in encrypt_result_list:
                if len(bytes_line) <=i:
                    break
                # 32，127为常用数组
                r=bytes_line[i]
                guess_plain_text_i=guess_keystream_i^r
                guess_result.append(guess_plain_text_i)

            score=get_english_score(bytes(guess_result))
            result = {
                'key': guess_keystream_i,
                'score': score,
                'plaintext': str(bytes(guess_result))
            }
            candidates.append(result)
        sort_result=sorted(candidates, key=lambda c: c['score'], reverse=True)[0]
        guess_keystream.append(sort_result['key'])


    attack_result_keystream=bytes(guess_keystream)
    print(len(attack_result_keystream))

    # print attack result
    for encrypt_line in encrypt_result_list:
        print(xor_bytes(encrypt_line,attack_result_keystream))