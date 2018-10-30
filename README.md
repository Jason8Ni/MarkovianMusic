# MarkovianMusic

 The idea behind this project was to take an implementation of a Markov chain and use it 
 to generate music. 

 ## Markov Chains

 Basically, a Markov chain is a system that experiences trainsitions from one state to another based on a set of probabilistic rules. 

 The defining characteristic of a Markov chain is that the probability of transitioning to any other state is dependent only on the current state and time elapsed. 

## Why Music? 

I play a few instruments, and love music but theory lessons just didn't take off. Maybe this is the start of my musical career

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

> For more information about the structure and meaning behind the different types of notes visit the following [webpage](http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html)


### Preprocessing

The first step was to extract the note on messages as well as the duration these notes were on for and group them into a graph of note progressions over time. This was done by looping through each message in the MIDI file and filtering out those that were 'note_on' messages. Since multiple messages can be played at the same time, those messages that play at the same time form a chord. Each chord is then taken and all the permutations are generated and the transitions from the note before to the note after are added to the markov chain. 

### Markov Chain Representation

The Markov Chain is represended as a dictionary of dictionary. A subset of the Markov chain generated for `Unravel.mid` is seen below:

![`Unravel.mid` markov chain](https://github.com/Jason8Ni/MarkovianMusic/blob/master/exampleMatrix.PNG)

The first column are the original notes. You can see that the note is represented as a number. The top row contains a list of the Notes that the note in the first column will transition to. Each Note consists of the pitch as well as the duration of that note. 

The actual matrix contains the number of times that each note has been transitioned to. As the MIDI file is read into the parser, probabilities will begin to develop. 

Once the Markov Chain is generated, it is time to use it to generate our own music!

### Music generation

Music generation is done by picking a random note to transition to based on the probabilities from the Markov Chain. The first note as chosen at random, and after that the chosen note becomes the base note for the subsequent notes and so on. This is done for a predetermined number of notes until a new track has been built!

You can find two sample tracks, called `unravelGenerate.mid` and `StarWarsGenerate.mid`

### Analysis 

The generated tracks sound weird to say the least. There little musical structure and progression in the melody. Whether there even is a melody is up for debate. 

The tracks seem to jump around a lot, which does not seem to resemble their original scores. This can be attributed to the fact that the left and right hands were not separated during the parsing of the MIDI file. Perhaps a further take on this project would be to find a MIDI file with both left and right hands and build tracks for each hand separately. They perhaps, as the files are layered onto each other, the generated track will be more complete with a main melody with a harmonizing accompaniment. 

In addition, the defining the states as one note may have been too sparse. When broken down into singular notes, all of the structure is removed so it is hard to develop a meaningful Markov Chain model. A better idea may to represent each state as a sequence of a few notes. This way, some of the melody is captured as a part of each state, and can perhaps be used to build a meaningful model that represents the state transitions of parts of a melody rather than singular notes. 

If this path were to be taken there are a few parameters that would need to be chosen: 
    * The size of the sequence: There is no set size for a melody so choosing a fixed size can limit the results. 
    * Accuracy of each sub-melody. Where do I round off so that each melody is deemed exact, and a probability distribution can   start to be built up: If 1000 sub-melodies are analyzed and 1000 states are generated all with the same probability, than   the generated Markov chain is not meaningful in any way. Therefore a suitable rounding for timings must be chosen. 
    * Any other attributes of a melody: I've taken some musical theory classes (Rudiments and Harmony) and there are many different factors and elements in building a melody. If these can be captured and built into the generation algorithm, the resultant track will be much nicer to the ears! 

### TODO
* Separate hands MIDI file for analysis
* Incorporate pitch (loudness)
* Incorporate sequencing as states    

## Update 1

Separate hand files have been explored. The midi file analyzed was the song `Moonlight Sonata`. The MIDI was first separated into treble and bass clefs using [musescore](https://musescore.org/en). After this the separate files were saved and processed to generate their respective Markov Chain. 

After this was done, new MIDI tracks were generated and merged using `mergeTracks.py`. 

### Funky bits: 

* It was difficult to find a method to merge the two MIDI files. `Mido` has a built in function called merge_tracks that merges multiple tracks with their timings intact, but it seemed to speed up all of the notes. 
* To fix this, the notes were scaled out after the merge. 

### Results:

The resultant track, `moonlight_sonataMergeGen.mid` sounds much better than those generated without separating the parts. There sections which resemble the original song and the overlap between clefs line up pretty well. In addition, the number of large jumps and skips between octaves have dropped dramatically. It almost sounds like a piano novice's first play through! :) I call that a partial success. 

