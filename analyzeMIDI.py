from mido import MidiFile
mid = MidiFile('./MIDIFiles/Unravel.mid')
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for message in track:
        print(message)