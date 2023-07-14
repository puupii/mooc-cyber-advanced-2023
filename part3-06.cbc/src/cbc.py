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

        print(paddedplain)
        padding_len = int(paddedplain[-1])
        plain = paddedplain[:-padding_len]
        print(plain)

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

    plain = cbc.decode(cipher, iv)
    print('After decoding:', plain)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('usage: python %s message rounds' % sys.argv[0])
    else:
        main(sys.argv)
