#!/usr/bin/env python3
import sys
import socket

import random
from string import ascii_lowercase  # string containing all lower-case alphabets letters


def decode(ciphertext, frequencies):
    # ciphertext is a string, frequencies is a dictionary with entries {letter:  float}

    clear = ''

    # write code here
    cipherfrequency = {}
    for a in ascii_lowercase:
        cipherfrequency[a] = 0

    for c in ciphertext:
        # normalize frequency as we count them. should be close enough
        if c in ascii_lowercase:
            cipherfrequency[c] = cipherfrequency[c]+1/len(ciphertext)
        else:
            continue

    # sort each dict and create key between them
    sorted_cipherfrequency = dict(sorted(cipherfrequency.items(), key=lambda x:x[1]))
    print(sorted_cipherfrequency)

    sorted_frequency = dict(sorted(frequencies.items(), key=lambda x: x[1]))
    print(sorted_frequency)

    cipherkeys = list(sorted_cipherfrequency.keys())
    clearkeys = list(sorted_frequency.keys())
    print(clearkeys)
    print(cipherkeys)
    key = {}
    for k in range(len(cipherkeys)):
        key[cipherkeys[k]] = clearkeys[k]

    # finally decrypt using the key

    for c in ciphertext:
        if c in ascii_lowercase:
            clear += key[c]
        else:
            clear += c
    return clear


poem = \
"""
and death shall have no dominion.
dead men naked they shall be one
with the man in the wind and the west moon;
when their bones are picked clean and the clean bones gone,
they shall have stars at elbow and foot;
though they go mad they shall be sane,
though they sink through the sea they shall rise again;
though lovers be lost love shall not;
and death shall have no dominion.

and death shall have no dominion.
under the windings of the sea
they lying long shall not die windily;
twisting on racks when sinews give way,
strapped to a wheel, yet they shall not break;
faith in their hands shall snap in two,
and the unicorn evils run them through;
split all ends up they shan't crack;
and death shall have no dominion.

and death shall have no dominion.
no more may gulls cry at their ears
or waves break loud on the seashores;
where blew a flower may a flower no more
lift its head to the blows of the rain;
though they be mad and dead as nails,
heads of the characters hammer through daisies;
break in the sun till the sun breaks down,
and death shall have no dominion.
"""


frequencies = {'a': 0.09097387173396673, 'b': 0.014014251781472685, 'c': 0.010807600950118764, 'd': 0.047149643705463186, 'e': 0.10380047505938242, 'f': 0.008669833729216151, 'g': 0.0172209026128266, 'h': 0.08776722090261281, 'i': 0.04928741092636579, 'j': 0.00011876484560570071, 'k': 0.009738717339667458, 'l': 0.056769596199524944, 'm': 0.019358669833729216, 'n': 0.08135391923990498, 'o': 0.06638954869358671, 'p': 0.006532066508313539, 'q': 0.00011876484560570071, 'r': 0.035391923990498814, 's': 0.05890736342042756, 't': 0.06959619952494062, 'u': 0.016152019002375298, 'v': 0.012945368171021378, 'w': 0.02149643705463183, 'x': 0.00011876484560570071, 'y': 0.01828978622327791, 'z': 0.00011876484560570071}


decode(poem, frequencies)
