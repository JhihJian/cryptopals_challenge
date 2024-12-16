import nltk_demo
s1='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

all_byte_values = [b for b in range(256)]

def one_byte_xor_all_result(s1):
    result_s=[]
    for key_b in all_byte_values:
        xor_result_list = []
        for b in bytes.fromhex(s1):
            r=b^key_b
            xor_result_list.append(r)

        xor_result_bytes = bytes(xor_result_list)

        try:
            sentens=str(xor_result_bytes, 'ascii')
            if(nltk_demo.is_likely_a_sentence(sentens)):
                result_s.append(sentens)
        except UnicodeDecodeError as e:
            continue
    return result_s


# for s in one_byte_xor_all_result(s1):
#     print(s)