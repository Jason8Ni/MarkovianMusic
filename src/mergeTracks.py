#!/usr/bin/python3
import mido
import math

def mergeTrack(bassTrack, trebleTrack):
    trebleTracks = mido.MidiFile(trebleTrack)
    bassTracks = mido.MidiFile(bassTrack)
    mergeTracks = mido.merge_tracks([trebleTracks, bassTracks])
    return mergeTracks


if __name__ == "__main__":
    print("HI")
    with mido.midifiles.MidiFile() as midi:
        mergeTracks = mergeTrack('moonlight_sonataBassGen.mid', 'moonlight_sonataTREBLEGen.mid')
        midi.tracks.append(mergeTracks)
        for i, track in enumerate(midi.tracks):
            print('Track {}: {}'.format(i, track.name))
        for message in track:
            print(message)
            message.time = math.ceil(message.time*100)
            print(message)
        midi.save('moonlight_sonataMergeGen.mid')