import sys
import random


class Hasher:
    def __init__(self, sbox):
        self.sbox = sbox

    def transform(self, key, data):
        # data is an array of size 4
        t = bytearray([key[i] ^ data[i] for i in range(4)])
        h = self.sbox[0][t[0]] + self.sbox[1][t[1]]
        h ^= self.sbox[2][t[2]]
        h += self.sbox[3][t[3]]
        h &= 0xFFFFFFFF # take care of overflow
        return h.to_bytes(4, 'little')


# Use Cbc from the CBC exercise
# Use class from Feistel exercise
class Feistel:
    def __init__(self, keys, roundf):
        self.keys = keys
        self.roundf = roundf

    def encode(self, plain):
        # plain is an array of length 8
        cipher = bytearray(plain)

        # write code here
        m = 4
        Lprevious = bytearray(plain[:m])
        Rprevious = bytearray(plain[m:])

        Rnext = bytearray(Rprevious)

        for i in range(len(self.keys)):
            Lnext = Rprevious
            FR = bytearray(self.roundf(Rprevious, self.keys[i]))

            Rnext = bytearray()
            Rnext = xor(Lprevious, FR)

            Lprevious = Lnext
            Rprevious = Rnext
            print(Lnext, Rnext)
        cipher = Lprevious + Rprevious
        return cipher

    def decode(self, cipher):
        # cipher is a byte array of length 8
        plain = bytearray(cipher)

        # write code here
        m = 4
        Lprevious = bytearray(plain[:m])
        Rprevious = bytearray(plain[m:])

        Lnext = bytearray(Lprevious)
        for i in range(len(self.keys)):
            Rnext = Lprevious
            j = i+1
            FL = bytearray(self.roundf(Lprevious, self.keys[-j]))

            Lnext = xor(Rprevious, FL)

            Lprevious = Lnext
            Rprevious = Rnext
        plain = Lprevious + Rprevious
        return plain


# XORs two bytearrays of same legth
def xor(a, b):
    return bytearray([x ^ y for x, y in zip(a, b)])


class Cbc:
    def __init__(self, block):
        self.block = block

    def encode(self, plain, iv):
        # plain is a byte array
        # iv is an initilization vector for cbc (byte array of length 8)
        # use self.block.encode() the blocks are length 8
        padding_len = 8 - len(plain) % len(iv)
        if padding_len == 0:
            padding_len = 8

        paddedplain = bytearray(plain)
        for i in range(padding_len):
            paddedplain.append(padding_len)

        print(paddedplain)
        print(len(paddedplain))

        Ci = bytearray(iv)
        cipher = bytearray()

        # i is the number of steps, and we use it to slice the bytearray
        # into 8byte chunks
        for i in range(int(len(paddedplain)/8)):
            Pi = paddedplain[8*i:8*i+8]
            initialized = xor(Pi, Ci)
            Ci = self.block.encode(initialized)
            cipher.extend(bytes(Ci))

        return cipher

    def decode(self, cipher, iv):
        # cipher is a byte array
        # iv is an initilization vector for cbc (byte array of length 8)
        # use self.block.encode() the blocks are length 8

        Cj = bytearray(iv)
        paddedplain = bytearray()
        for i in range(int(len(cipher)/8)):
            Ci = cipher[8*i:8*i+8]
            initialized = self.block.decode(Ci)
            Pi = xor(initialized, Cj)
            Cj = Ci
            paddedplain.extend(Pi)

        padding_len = int(paddedplain[-1])
        plain = paddedplain[:-padding_len]

        return plain

# add function decode_padded that is the same as decode but doesn't remove padding 

    def decode_padded(self, cipher, iv):
        # cipher is a byte array
        # iv is an initilization vector for cbc (byte array of length 8)
        # use self.block.decode() the blocks are length 8

        Cj = bytearray(iv)
        paddedplain = bytearray()
        for i in range(int(len(cipher)/8)):
            Ci = cipher[8*i:8*i+8]
            initialized = self.block.decode(Ci)
            Pi = xor(initialized, Cj)
            Cj = Ci
            paddedplain.extend(Pi)

        return paddedplain


class PaddingOracle:
    def __init__(self, cbc):
        self.cbc = cbc

    # tells if the cipher ends with the correct padding
    def isvalid(self, b1, b2):
        plain = self.cbc.decode_padded(b2, b1)  # b1 acts as iv
        padlen = plain[-1]
        if padlen > 8:
            return False
        return plain[-padlen:] == bytearray([padlen for i in range(padlen)])


# finds a valid padding in b2 by manipulating b1[index]
# b1 and b2 are bytearrays of length 8
# you have to deal with the special case when len(valid_values) == 2
# b1 should be given as iv to oracle (note the parameter order)
def test_value(b1, b2, index, oracle):
    valid_values = []
    m = b1[:]  # create a copy that we can modify without changing b1

    for i in range(256):
        m[index] = i
        if oracle.isvalid(m, b2):
            valid_values.append(i)
    if len(valid_values) == 2:
        m1 = b1[:]
        m2 = b1[:]
        m1[index] = valid_values[0]
        m2[index] = valid_values[1]
        for j in range(256):
            m1[index-1] = j
            m2[index-1] = j
            if oracle.isvalid(m1, b2):
                valid_values[0] = valid_values[0]
            elif oracle.isvalid(m2, b2):
                valid_values[0] = valid_values[1]
    return valid_values[0]


# decodes b2 by manipulating b1
# b1 and b2 are bytearrays of length 8
def decode_block(b1, b2, oracle):
    # output of the decoder _before_ xor with the previous cipher block
    d = bytearray(8)
    print(b1, b2)
    print("asd")
    # decoded block
    plain = bytearray(8)

    a = bytearray(8)
    q = bytearray(8)
    m = bytearray(8)

    for i in range(len(m)):
        index = -1-i
        m[index] = test_value(m, b2, index, oracle)
        for j in range(256):
            a[index] = j
            q[index] = m[index] ^ a[index]
            if q[index] == i+1:
                d[index] = a[index]
                break
        for x in range(index, 0):
            m[x] = a[x] ^ (i+2)
        d = m
    plain = xor(b1,a)
    return plain


def padding_attack(cipher, iv, oracle):
    plain = bytearray(len(cipher))

    # decode all blocks except the first block
    for i in range(8, len(cipher), 8):
        plain[i:(i + 8)] = decode_block(cipher[(i - 8):i], cipher[i:(i + 8)], oracle)
    plain[0:8] = decode_block(iv, cipher[0:8], oracle)

    return plain


def main(argv):
    sbox = [[random.getrandbits(32) for r in range(256)] for i in range(4)]
    hasher = Hasher(sbox)

    keys = [random.getrandbits(32).to_bytes(4, 'little') for i in range(int(argv[2]))]
    f = Feistel(keys, hasher.transform)

    cbc = Cbc(f)

    iv = bytearray(8)
    msg = argv[1]
    print('Message:', msg)

    cipher = cbc.encode(msg.encode(), iv)
    print('After encoding:', cipher)

    oracle = PaddingOracle(cbc)

    plain = padding_attack(cipher, iv, oracle)
    print('Padding attack:', plain)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('usage: python %s message rounds' % sys.argv[0])
    else:
        main(sys.argv)
