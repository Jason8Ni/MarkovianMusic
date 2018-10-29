# This class will parse the MIDI file and build a basic Markov chain from it 

import hashlib
import mido
import argparse

from markovChain import MarkovChain

class ParseMIDI:

    def __init__(self, filename):
        """
        This is the constructor for a Serializer. This will serialize
        a MIDI file given the filename and also generate a markov chain of the notes
        in the track
        """
        self.filename = filename

        # Number of MS per beat (given in each line of the MIDI message)
        self.tempo = None
        self.ticksPerBeat = None
        # The difference in time between each MIDI message represents
        # the number of ticks, which can be converted to beats using
        # ticks per beat
        self.markovChain = MarkovChain()
        self._parse()
    
    def _getTempo(self):
        return self.tempo
    
    def _getTicksPerBeat(self):
        return self.ticksPerBeat

    def _parse(self):
        """
        This function handles the reading of the MIDI file and breaks the
        notes into sequenced "chords", which are then inserted into the
        markov chain.

        Treats all of the notes that are played simultaneously, 
        """
        midi = mido.MidiFile(self.filename)
        self.ticksPerBeat = midi.ticks_per_beat
        print("TIcks per beat")
        print(self.ticksPerBeat)
        previousChunk = []
        currentChunk = []
        for track in midi.tracks:
            for message in track:
                if message.type == "set_tempo":
                    self.tempo = message.tempo
                elif message.type == "note_on":
                    if message.time == 0:
                        currentChunk.append(message.note)
                    else:
                        self._sequence(previousChunk,
                                       currentChunk,
                                       message.time)
                        previousChunk = currentChunk
                        currentChunk = []

    def _sequence(self, previousChunk, currentChunk, duration):
        """
        With the previous chunk, the current chunk of notes and
        an averaged duration of the current notes, sequence cycles through
        every combination of the previous notes to the current
        notes and sticks them into the markov chain.
        """
        for note1 in previousChunk:
            for note2 in currentChunk:
                self.markovChain.add(
                    note1, note2, self._bucket_duration(duration))

    def _bucket_duration(self, ticks):
        """
        This method takes a tick count and converts it to a time in
        milliseconds, bucketing it to the nearest 250 milliseconds.
        """
        try:
            ms = ((ticks / self.ticksPerBeat) * self.tempo) / 1000
            return int(ms - (ms % 250) + 250)
        except TypeError:
            raise TypeError(
                "Could not read a tempo and ticks_per_beat from midi")


    def getChain(self):
        return self.markovChain

if __name__ == "__main__":
    #print(ParseMIDI('./MIDIFiles/Unravel.mid').getChain().printAsMatrix())
    #print('Finished parsing {}'.format('./MIDIFiles/Unravel.mid'))
    print(ParseMIDI('./MIDIFiles/moonlight_sonataTREBLE.mid').getChain().printAsMatrix())
    print('Finished parsing {}'.format('./MIDIFiles/moonlight_sonataTREBLE.mid'))