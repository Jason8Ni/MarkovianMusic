# This class handles the generation of a new song given a markov chain
# containing the note transitions and their frequencies.


import random
import mido
from markovChain import MarkovChain


class Generator:

    def __init__(self, markov_chain):
        self.markov_chain = markov_chain

    @staticmethod
    def load(markovChain):
        assert isinstance(markovChain, MarkovChain)
        return Generator(markovChain)

    def _noteToMessages(self, note):
        return [
            mido.Message('note_on', note=note.note, velocity=127,
                         time=0),
            mido.Message('note_off', note=note.note, velocity=0,
                         time=note.duration)
        ]

    def generate(self, filename):
        with mido.midifiles.MidiFile() as midi:
            track = mido.MidiTrack()
            lastNote = None
            for i in range(1000):
                newNote = self.markov_chain.getNext(lastNote)
                track.extend(self._noteToMessages(newNote))
            midi.tracks.append(track)
            midi.save(filename)

if __name__ == "__main__":
    import sys
    from parseMIDI import ParseMIDI
    print("BYE")
    chain = ParseMIDI('./MIDIFiles/Unravel.mid').getChain()
    
    print("HI")
    Generator.load(chain).generate('unravelGenerate.mid')
    print("Generated markov chain")