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
            Rnext = bytes([a^b for a,b in zip(Lprevious,FR)])
            print(Lprevious,FR,Rnext)

           # for x in range(len(FR)):
           #     Rnext += bytes(Lprevious[x] ^ FR[x])
           #     print(Lprevious[x],FR[x],Rnext[x])

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

            Lnext = bytes([a^b for a,b in zip(Rprevious,FL)])
#            for x in range(len(Rprevious)):
#                Lnext[x] = Rprevious[x] ^ FL[x]

            Lprevious = Lnext
            Rprevious = Rnext
        plain = Lprevious + Rprevious
        return plain


def main(argv):
    sbox = [[random.getrandbits(32) for r in range(256)] for i in range(4)]
    hasher = Hasher(sbox) 

    keys = [random.getrandbits(32).to_bytes(4, 'little') for i in range(int(argv[2]))]
    f = Feistel(keys, hasher.transform)

    msg = argv[1]
    print('Message:', msg)

    cipher = f.encode(msg.encode())
    print('After encoding:', cipher)

    plain = f.decode(cipher)
    print('After decoding:', plain)


if __name__ == "__main__":
    if len(sys.argv) != 3 or len(sys.argv[1]) != 8:
        print('usage: python %s message rounds' % sys.argv[0])
        print('message should be 8 characters')
    else:
        main(sys.argv)
