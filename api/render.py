import os
import subprocess
import sys

from music21 import converter, midi
from utils import create_uuid, get_absolute_path_from_relative_to_source


def render_audio_and_score(abc_text, assets_path):
    uuid = create_uuid(abc_text)
    assets_abs_path = get_absolute_path_from_relative_to_source(assets_path)
    wav_output = f"{assets_abs_path}/{uuid}.wav"
    if not os.path.exists(wav_output):
        render_audio_from_abc(abc_text, wav_output)
    png_output = f"{assets_abs_path}/{uuid}"
    #if not os.path.exists(png_output):
        # render_png_from_abc(abc_text, png_output)
    return uuid


def soundfont_file_path():
    soundfont_path = "../generate/SGM-v2.01-NicePianosGuitarsBass-V1.2.sf2"
    return get_absolute_path_from_relative_to_source(soundfont_path)

def render_png_from_abc(abc_text, output_path):
    score = converter.parse(abc_text, format='abc')
    score.write("lily", fp=output_path)
    score.write("lily.png", fp=output_path)


def render_audio_from_abc(abc_text, output_file):
    score = converter.parse(abc_text, format='abc')
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


