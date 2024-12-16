def get_lowest_bits(n, number_of_bits): #n=False ....
    """Returns the lowest "number_of_bits" bits of n."""
    mask = (1 << number_of_bits) - 1  #=4294967295 32位的1
    return n & mask


class MT19937:
    """This implementation resembles the one of the Wikipedia pseudo-code."""
    W, N, M, R = 32, 624, 397, 31
    A = 0x9908B0DF
    U, D = 11, 0xFFFFFFFF
    S, B = 7, 0x9D2C5680
    T, C = 15, 0xEFC60000
    L = 18
    F = 1812433253
    LOWER_MASK = (1 << R) - 1 #011111111111111111111111111 共31位1  =2147483647
    UPPER_MASK = get_lowest_bits(not LOWER_MASK, W) #011111111 共31位1 & 10000000 共31位0 =32位的1 =0

    def __init__(self, seed):
        self.mt = []

        self.index = self.N
        self.mt.append(seed)
        for i in range(1, self.index):
            self.mt.append(get_lowest_bits(self.F * (self.mt[i - 1] ^ (self.mt[i - 1] >> (self.W - 2))) + i, self.W))

    def extract_number(self):
        # 右乘可逆矩阵
        if self.index >= self.N:
            self.twist()
        y = self.mt[self.index]
        y ^= (y >> self.U) & self.D
        y ^= (y << self.S) & self.B
        y ^= (y << self.T) & self.C
        y ^= (y >> self.L)

        self.index += 1
        return get_lowest_bits(y, self.W)

    def twist(self):
        for i in range(self.N):
            x = (self.mt[i] & self.UPPER_MASK) + (self.mt[(i + 1) % self.N] & self.LOWER_MASK)
            x_a = x >> 1
            if x % 2 != 0:
                x_a ^= self.A

            self.mt[i] = self.mt[(i + self.M) % self.N] ^ x_a

        self.index = 0

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

def main():
    # Check if the numbers look random
    for i in range(10):
        print(MT19937(i).extract_number())


if __name__ == '__main__':
    main()