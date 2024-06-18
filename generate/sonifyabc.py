import argparse
import os
import subprocess

from music21 import converter, midi

"""
This script sonifies all files in the input folder using ABC notation.
The output is saved in the output folder as WAV files.
The MIDI files are saved in the midi folder.

Requirements:
- music21 library
- FluidSynth software (brew install fluidsynth on macOS)
- SoundFont file (e.g., SGM-V2.01.sf2)

To run the script, use the following command:
python sonifyabc.py {input_folder} {output_folder} {midi_folder} {soundfont_file}

You can also import the functions and call them from another script.
"""

# Function to sonify all files in a folder
def sonify_all_files(input_folder, midi_folder, output_folder, soundfont_file):
    for file in os.listdir(input_folder):
        if file.endswith('.abc'):
            with open(f'{input_folder}/{file}') as f:
                abc_string = f.read()
            midi_file = f'{midi_folder}/{file.replace(".abc", ".mid")}'
            output_wav_file = f'{output_folder}/{file.replace(".abc", ".wav")}'
            sonify_abc(abc_string, midi_file, soundfont_file, output_wav_file)

# Function to sonify the ABC notation
def sonify_abc(abc_string, midi_file, soundfont_file, output_wav_file):
    # Parse the ABC notation
    print(f"Sonifying {abc_string}")
    score = converter.parse(abc_string, format='abc')
    mf = midi.translate.music21ObjectToMidiFile(score)
    mf.open(midi_file, 'wb')
    mf.write()
    mf.close()

    # Command to run FluidSynth
    command = [
        'fluidsynth',
        '-ni',            # Non-interactive mode
        soundfont_file,   # Path to the SoundFont file
        midi_file,        # Path to the MIDI file
        '-F', output_wav_file,  # Output WAV file
        '-r', '44100'     # Sample rate (optional, 44100 Hz in this case)
    ]

    # Run the command
    subprocess.run(command)

    print(f"Saved WAV file as {output_wav_file}")

# Function to parse arguments from command line and call the main function
def parse_arguments():
    parser = argparse.ArgumentParser(description='Sonify ABC notation files')
    parser.add_argument('--single-file', '-f', help='Input folder containing ABC files')
    parser.add_argument('--input_folder', '-i', help='Input folder containing ABC files', default='output')
    parser.add_argument('--output_folder', '-o', help='Output folder to save WAV files', default='output-wav')
    parser.add_argument('--midi_folder', '-m', help='MIDI folder to save MIDI files', default='output-midi')
    parser.add_argument('--soundfont_file', '-so', help='Path to the SoundFont file', default='SGM-v2.01-NicePianosGuitarsBass-V1.2.sf2')
    return parser.parse_args()

# Main function
def main():
    args = parse_arguments()
    print(args)
    # create midi_folder if it does not exist
    os.makedirs(args.midi_folder, exist_ok=True)
    os.makedirs(args.output_folder, exist_ok=True)

    if args.single_file is not None:
        with open(args.single_file) as f:
            abc_string = f.read()
        base_file = os.path.basename(args.single_file)
        midi_file = f'{args.midi_folder}/{base_file.replace(".abc", ".mid")}'
        output_wav_file = f'{args.output_folder}/{base_file.replace(".abc", ".wav")}'
        sonify_abc(abc_string, midi_file, args.soundfont_file, output_wav_file)
    else:
        sonify_all_files(args.input_folder, args.midi_folder, args.output_folder, args.soundfont_file)

if __name__ == '__main__':
    main()