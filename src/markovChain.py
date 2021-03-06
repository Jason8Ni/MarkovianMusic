#!/usr/bin/python3
# This class is the implementation of the Markov chain
# with all it's associated helper functions
# It is built from a nested dictionary of dictionaries. 

from collections import Counter, defaultdict, namedtuple

import random

import numpy as np

import json

#Define what a note is
# consists of a note as well as the duration it is to be played
Note = namedtuple('Note', ['note', 'duration'])

class MarkovChain: 

    def __init__(self):
        """
        Constructor 
        """
        self.chain = defaultdict(Counter)
        self.sums = defaultdict(int)

    @staticmethod
    def createFromDict(dict):
        """
        Build chain from a dictionary 
        """
        m = MarkovChain()

        for fromNote, toNotes in dict.items():
            for k, v in toNotes.items():
                m.add(fromNote, k, v)
        return m
    
    def _serialize(self, note, duration):
        """
        Serialize the note with it's attributes
        """
        return Note(note, duration)

    def __str__(self):
        return str(self.getChain())

    def getChain(self):
        return {k: dict(v) for k, v in self.chain.items()}

    def add(self, fromNote, toNotes, duration):
        self.chain[fromNote][self._serialize(toNotes, duration)] += 1
        self.sums[fromNote] += 1

    def merge(self, other):
        """
        Merge two Markov Chains together
        """
        assert isinstance(other, MarkovChain)
        self.sums = defaultdict(int)
        for fromNote, toNotes in other.chain.items():
            self.chain[fromNote].update(toNotes)
        for fromNote, toNotes in self.chain.items():
            self.sums[fromNote] = sum(self.chain[fromNote].values())
    
    def getNext(self, seedNote):
        """
        get the next note, based on the probabilities 
        """
        if seedNote is None or seedNote not in self.chain:
            randomChain = self.chain[random.choice(list(self.chain.keys()))]
            return random.choice(list(randomChain.keys()))
        note =  np.random.choice(self.chain[seedNote].items(),self.sums[seedNote])
        return note

    def printAsMatrix(self, limit=8):
        """
        Print the Markov chain as a matrix for visualization purposes
        """
        columns = []
        for fromNote, toNotes in self.chain.items():
            for note in toNotes:
                if note not in columns:
                    columns.append(note)
        _col = lambda string: '{:<12}'.format(string)
        _note = lambda note: '{}:{}'.format(note.note, note.duration)
        out = _col('')
        out += ''.join([_col(_note(note)) for note in columns[:limit]]) + '\n'
        for fromNote, toNotes in self.chain.items():
            out += _col(fromNote)
            for note in columns[:limit]:
                out += _col(toNotes[note])
            out += '\n'
        print(out)
    