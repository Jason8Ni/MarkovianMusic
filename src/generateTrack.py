#!/usr/bin/python3
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
                         time=note.duration)
        ]

    def generate(self, filename, tempo):
        
        midi = mido.midifiles.MidiFile()
        track = mido.MidiTrack()
        track.append(mido.MetaMessage('set_tempo', tempo = tempo, time = 0))
        lastNote = None
        #number is arbituary...
        for i in range(98):
            newNote = self.markovChain.getNext(lastNote)
            track.extend(self._noteToMessages(newNote))
        midi.tracks.append(track)
        midi.save(filename)

if __name__ == "__main__":
    import sys
    from parseMIDI import ParseMIDI
    parsedFile = ParseMIDI('./MIDIFiles/moonlight_sonataBass.mid')
    chain1 = parsedFile.getChain()
    tempo1 = parsedFile._getTempo()
    chain1.printAsMatrix()

    Generator.load(chain1).generate('moonlight_sonataBassGen.mid', tempo1)
    print("Generated markov chain")

    parsedFile1 = ParseMIDI('./MIDIFiles/moonlight_sonataTREBLE.mid')
    chain2 = parsedFile1.getChain()

    tempo2 = parsedFile1._getTempo()
    chain2.printAsMatrix()

    Generator.load(chain2).generate('moonlight_sonataTREBLEGen.mid', tempo2)
    print("Generated markov chain")