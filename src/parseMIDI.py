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

        # The difference in time between each MIDI message represents
        # the number of ticks, which can be converted to beats using
        # ticks per beat
        self.ticksPerBeat = None
        self.markovChain = MarkovChain()
        self._parse()

    def _parse(self):
        """
        This function handles the reading of the MIDI file and breaks the
        notes into sequenced "chords", which are inserted into the
        markov chain.
        """
        midi = mido.MidiFile(self.filename)
        self.ticksPerBeat = midi.ticks_per_beat
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
                    note1, note2, self._bucketDuration(duration))

    def _bucketDuration(self, ticks):
        """
        This method takes a tick count and converts it to a time in
        milliseconds and rounds it to the nearest millisecond.
        """
        try:
            ms = ((ticks / self.ticksPerBeat) * self.tempo) / 1000
            return int(round(ms))
        except TypeError:
            raise TypeError(
                "Could not read a tempo from MIDI File")

    def getChain(self):
        return self.markovChain

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The midi file input")
    args = parser.parse_args()
    print(ParseMIDI(args.input_file).getChain())
    print('No issues parsing {}'.format(args.input_file))