import random

from S3C21_MT19937_Mersenne_Twister_RNG import MT19937
from random import randint
from time import time
from mersenne_twister import mersenne_rng
current_time = int(time())
rng = MT19937(current_time)

def get_rng_result():
    """Performs the operations specified in the challenge and returns the first result of the
    newly created MT19937 rng.
    """
    return rng.extract_number()
def get_bit(number, position):
    """Returns the bit at the given position of the given number. The position
    is counted starting from the left in the binary representation (from the most
    significant to the least significant bit).
    """
    if position < 0 or position > 31:
        return 0
    return (number >> (31 - position)) & 1


def set_bit_to_one(number, position):
    """Sets the bit at the given position of the given number to 1.The position
    is counted starting from the left in the binary representation (from the most
    significant to the least significant bit).
    """
    return number | (1 << (31 - position))

def right_shift_xor(value, shift):
    result = value
    result ^= (result >> shift)
    return result

def undo_right_shift_xor(result, shift_len):
    original = 0
    for i in range(32):
        next_bit = get_bit(result, i) ^ get_bit(original, i - shift_len)
        if next_bit == 1:
            original = set_bit_to_one(original, i)

    return original

def undo_left_shift_xor_and(result, shift_len, andd):
    """When the left shift, then XOR and then the AND are done, we can reverse the process
    bit by bit by redoing the AND between the un-shifted resulting value and the and'd value
    and then by XORing with the corresponding bit of the given result.
    Sounds like magic, but try it on paper and you'll see that it works.
    This time the process is doing starting from the right and each bit is AND'd with the bit
    shift_len positions above.
    """
    original = 0
    for i in range(32):
        next_bit = get_bit(result, 31 - i) ^ \
                   (get_bit(original, 31 - (i - shift_len)) &
                    get_bit(andd, 31 - i))

        if next_bit == 1:
            original = set_bit_to_one(original, 31 - i)

    return original
def untemper(y):
    """Reverts the operations done in the "tampering" process when the function extract_number() of
    the MT19937 generator is called, and returns the initial value state of the generator corresponding
    to its current index.
    """
    y = undo_right_shift_xor(y, MT19937.L)
    y = undo_left_shift_xor_and(y, MT19937.T, MT19937.C)
    y = undo_left_shift_xor_and(y, MT19937.S, MT19937.B)
    y = undo_right_shift_xor(y, MT19937.U)
    return y

def get_cloned_rng(original_rng):
    """Taps the given rng for 624 outputs, untempers each of them to recreate the state of the generator,
    and splices that state into a new "cloned" instance of the MT19937 generator.
    """
    mt = []
    # Recreate the state mt of original_rng
    for i in range(MT19937.N):
        mt.append(untemper(original_rng.extract_number()))

    # Create a new generator and set it to have the same state
    cloned_rng = MT19937(0)
    cloned_rng.mt = mt

    return cloned_rng
def get_cloned_systemrandom(rng):
    """Taps the given rng for 624 outputs, untempers each of them to recreate the state of the generator,
    and splices that state into a new "cloned" instance of the MT19937 generator.
    """
    mt = []
    # Recreate the state mt of original_rng
    for i in range(MT19937.N):
        mt.append(untemper(random.getrandbits(32)))

    # Create a new generator and set it to have the same state
    cloned_rng = mersenne_rng(0)
    cloned_rng.state = mt

    return cloned_rng


def reverse_state_update(state_i, f, i, ):
    # 假设我们知道 state[i]、f 和 i
    # state_i: 已知的 state[i]
    # f: 常数因子（如 Mersenne Twister 中的 0x6c078965）
    # i: 当前的索引
    # int_32: 用来确保返回值是32位整数的函数
    temp=state_i-i
    temp=temp//f
    temp=undo_right_shift_xor(temp,30)
    return temp



if __name__ == '__main__':
    # seed = randint(0, 2**32 - 1)
    # rng = MT19937(seed)
    rng= random.seed(100)

    cloned_rng = get_cloned_systemrandom(rng)

    # Check that the two PRNGs produce the same output now
    for i in range(1000):
        assert random.getrandbits(32) == cloned_rng.get_random_number()
    rng=mersenne_rng(0)
    random.seed(100)
    print(','.join(str(random.getrandbits(32)) for _ in range(6)))
    print(','.join(str(rng.get_random_number()) for _ in range(6)))
    print("----------------------")
    next=3310491232
    print(reverse_state_update(3310491232,rng.f,5))
    # for i in range(5,1,-1):
    #
    #     next=undo_right_shift_xor((next - i) // rng.f, 30)
    #     print(next)

    print(int(0xFFFFFFFF & (2588848963^(2588848963>>30))*rng.f+6))