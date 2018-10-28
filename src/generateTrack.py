# This class handles the generation of a new song given a markov chain
# containing the note transitions and their frequencies.


import random
import mido
from markovChain import MarkovChain


class Generator:

    def __init__(self, markovChain):
        self.markovChain = markovChain

    @staticmethod
    def load(markovChain):
        assert isinstance(markovChain, MarkovChain)
        return Generator(markovChain)

    def _noteToMessages(self, note):
        return [
            mido.Message('note_on', note=note.note, velocity=127,
                         time=int(0)),
            mido.Message('note_off', note=note.note, velocity=0,
                         time=int(note.duration))
        ]

    def generate(self, filename):
        with mido.midifiles.MidiFile() as midi:
            track = mido.MidiTrack()
            lastNote = None
            for i in range(1000):
                newNote = self.markovChain.getNext(lastNote)
                track.extend(self._noteToMessages(newNote))
            midi.tracks.append(track)
            midi.save(filename)

if __name__ == "__main__":
    import sys
    from parseMIDI import ParseMIDI
    print("BYE")
    chain = ParseMIDI('./MIDIFiles/moonlight_sonataBass.mid').getChain()
    chain.printAsMatrix()

    print("HI")
    Generator.load(chain).generate('moonlight_sonataBassGen.mid')
    print("Generated markov chain")

    print("BYE")
    chain = ParseMIDI('./MIDIFiles/moonlight_sonataTREBLE.mid').getChain()
    chain.printAsMatrix()

    print("HI")
    Generator.load(chain).generate('moonlight_sonataTREBLEGen.mid')
    print("Generated markov chain")