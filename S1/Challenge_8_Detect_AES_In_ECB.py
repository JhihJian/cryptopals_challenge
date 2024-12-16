from Crypto.Cipher.AES import block_size
from itertools import combinations
def count_duplicate_block_in_aes_ciphertext(ciphertext_bytes):
    chunk_list=[ciphertext_bytes[index:index+block_size] for index in range(0,len(ciphertext_bytes),block_size)]
    return len(chunk_list)-len(set(chunk_list))

def detect_aes_block(ciphertext_bytes_list):
    best_repetitions=0
    for ciphertext_bytes in ciphertext_bytes_list:
        repetitions=count_duplicate_block_in_aes_ciphertext(ciphertext_bytes)
        if repetitions>best_repetitions:
            best_repetitions=repetitions
            candidate_ciphertext=ciphertext_bytes
    return best_repetitions,candidate_ciphertext

if __name__ == '__main__':
    ciphertexts=[bytes.fromhex(line) for line in open("../resources/S1C08_input.txt")]
    result=detect_aes_block(ciphertexts)
    print(result)
    print(bytes(result[1]).hex())