import random
import secrets
from S2C10_Impl_CBC_Mode import aes_ecb_encrypt,aes_ecb_decrypt
from S2C12_ECB_decryption import discover_the_block_size_of_the_cipher,guess_next_word

random_key=secrets.token_bytes(16)
random_prefix = secrets.token_bytes(random.randint(2, 100))
flag_text_bytes=b'Think "STIMULUS" and "RESPONSE".'
def random_prefix_encrypt(input_bytes):
   return aes_ecb_encrypt(random_prefix+input_bytes+flag_text_bytes,random_key)


print('random key:'+str(random_key))
print('random prefix offset:'+str(random_prefix))
print('random prefix offset:'+str(len(random_prefix)))
guess_block_size,offset=discover_the_block_size_of_the_cipher(random_prefix_encrypt)
print("猜测block size:" + str(guess_block_size))
print("猜测 offset:" + str(offset))
result=guess_next_word(guess_block_size,random_prefix_encrypt,offset)
print("猜测结果:"+str(result))
assert result==flag_text_bytes