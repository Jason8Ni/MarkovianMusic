# MarkovianMusic

 The idea behind this project was to take an implementation of a Markov chain and use it 
 to generate music. 

 ## Markov Chains

 Basically, a Markov chain is a system that experiences trainsitions from one state to another based on a set of probabilistic rules. 

 The defining characteristic of a Markov chain is that the probability of transitioning to any other state is dependent only on the current state and time elapsed. 

## Why Music? 

## File Type

MIDI files were chose because they are not truly audio files. Instead they just contain instructions on how the play the tracks. Due to this, MIDI files can be intrepreted and played by a multitude of software programs. This way, no "real" audio analysis would have to be done. 

The drawback to this is that MIDI files are limited in the ranges of notes they can store and the types of audio. No complex audio like vocals can be stored. This is fine, as the main point of the project is to generate music from some piano songs. 

> An interesting futher take on this project, would be to use audio files like MP3 to analysis. 

## Processing 

The first step in the process was to find a good Python library to analyze the MIDI files. After doing a bit of research, [Mido](https://mido.readthedocs.io/en/latest/) was chosen for its simplicity and good documentation on how to use it. 

## MIDI Format

### Start

The beginning of a MIDI file also know as Track 0 consists of meta data like the track name, author, any copyright data, and general information about the track like the tempo and time. 

The following is the meta information for `Unravel.mid`:

```
Track 0: Unravel
<meta message time_signature numerator=4 denominator=4 clocks_per_click=24 notated_32nd_notes_per_beat=8 time=0>
<meta message key_signature key='Gm' time=0>
<meta message track_name name='Unravel' time=0>
<meta message text text='Arranged by Animenz' time=0>
<meta message copyright text='Copyright � ' time=0>
<meta message set_tempo tempo=447761 time=3360>
<meta message time_signature numerator=6 denominator=4 clocks_per_click=72 notated_32nd_notes_per_beat=8 time=503520>
<meta message end_of_track time=1>
Track 1: Klavier
```

### Middle

Track one contains the data on how to play the song. 

`control_change` is used to convery performance or patch data for parameters other than those that have their own dedicated message types. 

`time` represents the time after the previuos message that the current message should be played. 

`velocity` represents the volumne of each note

`note` represents the type of note to be played. This ranges from 0 to 127 which maps to the notes C to B from octage -1 to 9. 

A small excerpt of this section is seen below: 

```
Track 1: Klavier
control_change channel=0 control=0 value=0 time=3360
control_change channel=0 control=32 value=0 time=0
program_change channel=0 program=0 time=0
control_change channel=0 control=121 value=0 time=0
control_change channel=0 control=64 value=0 time=0
control_change channel=0 control=91 value=48 time=0
control_change channel=0 control=10 value=51 time=0
control_change channel=0 control=7 value=100 time=0
note_on channel=0 note=94 velocity=63 time=0
control_change channel=0 control=121 value=0 time=0
control_change channel=0 control=64 value=0 time=0
control_change channel=0 control=91 value=48 time=0
control_change channel=0 control=10 value=51 time=0
control_change channel=0 control=7 value=100 time=0
<meta message track_name name='Klavier' time=0>
note_off channel=0 note=94 velocity=0 time=480
note_on channel=0 note=96 velocity=78 time=0
note_on channel=0 note=79 velocity=63 time=0
note_off channel=0 note=96 velocity=0 time=960
note_on channel=0 note=94 velocity=70 time=0
note_off channel=0 note=94 velocity=0 time=960
note_on channel=0 note=93 velocity=75 time=0
note_off channel=0 note=93 velocity=0 time=480
note_on channel=0 note=91 velocity=69 time=0
note_off channel=0 note=79 velocity=0 time=480
note_on channel=0 note=82 velocity=80 time=0
note_off channel=0 note=91 velocity=0 time=480
note_on channel=0 note=96 velocity=89 time=0
note_off channel=0 note=82 velocity=0 time=480
note_on channel=0 note=75 velocity=63 time=0
note_off channel=0 note=96 velocity=0 time=480
note_on channel=0 note=94 velocity=75 time=0
note_off channel=0 note=94 velocity=0 time=960
note_on channel=0 note=93 velocity=69 time=0
note_off channel=0 note=93 velocity=0 time=960
note_on channel=0 note=91 velocity=72 time=0
note_off channel=0 note=75 velocity=0 time=480
note_on channel=0 note=79 velocity=80 time=0
note_off channel=0 note=91 velocity=0 time=480
note_on channel=0 note=91 velocity=75 time=0
note_off channel=0 note=91 velocity=0 time=480
note_on channel=0 note=89 velocity=69 time=0
note_off channel=0 note=79 velocity=0 time=0
note_on channel=0 note=77 velocity=67 time=0
note_off channel=0 note=89 velocity=0 time=1440
```

