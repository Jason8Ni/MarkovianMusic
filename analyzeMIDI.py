

def printMIDI(filename):
    from mido import MidiFile
    mid = MidiFile(filename)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for message in track:
            print(message)


printMIDI('./moonlight_sonataTREBLEGen.mid')