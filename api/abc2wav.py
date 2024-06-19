import os
import subprocess
import sys

from abc_clean import remove_chords
from music21 import converter, midi
from utils import get_absolute_path_from_relative_to_source


def soundfont_file_path():
    soundfont_path = "../generate/SGM-v2.01-NicePianosGuitarsBass-V1.2.sf2"
    return get_absolute_path_from_relative_to_source(soundfont_path)

def render_audio(input_file, output_file):
    with open(input_file, "r") as file:
        text = file.read()
    render_abc(text, output_file)

def render_abc(abc_text, output_file):
    abc = remove_chords(abc_text)
    score = converter.parse(abc, format='abc')
    mf = midi.translate.music21ObjectToMidiFile(score)


    midi_file = "output.mid"
    mf.open(midi_file, 'wb')
    mf.write()
    mf.close()

    # Command to run FluidSynth
    command = [
        'fluidsynth',
        '-ni',            # Non-interactive mode
        soundfont_file_path(),   # Path to the SoundFont file
        midi_file,        # Path to the MIDI file
        '-F', output_file,  # Output WAV file
        '-r', '44100'     # Sample rate (optional, 44100 Hz in this case)
    ]
    subprocess.run(command)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = "input.abc"

    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = "output.wav"
    render_audio(file_name, output_file)