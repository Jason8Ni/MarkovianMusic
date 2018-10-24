# This class is the implementation of the Markov chain
# It will handle the generalr storage and interaction of the markov chain
# It is built from a nested dictionary of dictionaries. 

from collections import Counter, defaultdict, namedtuple

import random

#Define what a note is
# consists of a note as well as the duration it is to be played
Node = namedtuple('Node', ['note', duration])