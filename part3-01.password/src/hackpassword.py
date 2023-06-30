import sys
import hashlib
import base64


def test_password(passhash, candidates):
    #print(passhash)
    protocol, encoded64salt, encoded64passwordhash = passhash.split('$')
    salt = base64.b64decode(encoded64salt)
    #print(salt)
    #print(encoded64passwordhash)
    passwordhash = base64.b64decode(encoded64passwordhash.encode('UTF-8'))
    #print(passwordhash)
    salthash = hashlib.new('sha384')
    salthash.update(salt)
    for guess in candidates:
        guesshash = salthash.copy()
        #print(guess.encode('utf-8'))
        guesshash.update(guess.encode('utf-8'))
        hashedguess = guesshash.digest()
        #print(hashedguess)
        #print(passwordhash)
        if hashedguess == passwordhash:
            return guess
    return None



def main(argv):
    passhash = argv[1]
    testhash = '42$cHl0aG9u$JQrvRSZk/xPIm6pfSfjoG8Jgb9JT5c1nnUtg6vs6QCHn+AR9lhH27PkmB3oeuN9u'
    print('Given hash:', passhash)
    fname = argv[2]
    candidates = [p.strip() for p in open(fname)]
    #print(test_password(testhash, candidates))
    print(test_password(passhash, candidates))


# This makes sure the main function is not called immediatedly
# when TMC imports this module
if __name__ == "__main__": 
    if len(sys.argv) != 3:
        print('usage: python %s hash filename' % sys.argv[0])
    else:
        main(sys.argv)
