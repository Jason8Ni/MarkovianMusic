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

| An interesting futher take on this project, would be to use audio files like MP3 to analysis. 

## Processing 