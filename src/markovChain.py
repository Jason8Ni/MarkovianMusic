# This class is the implementation of the Markov chain
# It will handle the generalr storage and interaction of the markov chain
# It is built from a nested dictionary of dictionaries. 

from collections import Counter, defaultdict, namedtuple

import random

import numpy as np

#Define what a note is
# consists of a note as well as the duration it is to be played
Note = namedtuple('Node', ['note', 'duration'])

class MarkovChain: 

    def __init__(self):
        self.chain = defaultdict(Counter)
        self.sums = defaultdict(int)
    
    def _serialize(self, note, duration):
        return Note(note, duration)

    def __str__(self):
        return str(self.getChain())

    def getChain(self):
        return {k: dict(v) for k, v in self.chain.items()}

    def add(self, fromNote, toNote, duration):
        self.chain[fromNote][self._serialize(toNote, duration)] += 1
        self.sums[fromNote] += 1