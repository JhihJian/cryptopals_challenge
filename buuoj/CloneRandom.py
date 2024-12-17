import random
from os import urandom as _urandom
from S3C23_Clone_MT19937_RNG import untemper
from mersenne_twister import mersenne_rng
from reverse_mersenne_twister import MT19937

flag = "flag{" + ''.join(str(random.getrandbits(32)) for _ in range(4)) + "}"

random_list=[]
with open('output.txt', 'r') as f:
    random_list=[int(i) for i in f.readlines()]
# print(flag)
#atack ----------------------------
index =0
def mock_rng(random_list):
    mt = []
    # Recreate the state mt of original_rng
    for i in range(624):
        mt.append(untemper(random_list[i]))
    cloned_rng = mersenne_rng(0)
    cloned_rng.state=mt
    return cloned_rng

cloned_rng=mock_rng(random_list)
# for r in random_list[624:]:
#     assert cloned_rng.get_random_number()==r


mt = MT19937()
mt.clone_state_from_output_and_rewind(random_list[0:624])
mt.rewind(4)

print(mt.try_recover_seed())

flag = "flag{" + ','.join(str(mt.get_next_random()) for _ in range(4)) + "}"
print(flag)
flag = "flag{" + ','.join(str(mt.get_next_random()) for _ in range(4)) + "}"
print(flag)
mt=MT19937()
mt.seed(1121806820)
print(mt.get_next_random())