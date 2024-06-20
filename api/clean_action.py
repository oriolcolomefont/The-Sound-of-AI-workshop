import re
import sys

from music21 import converter, metadata, note, stream
from render import render_audio_and_score


def clean_action(melody, assets_path):
    melody = remove_chords(melody)
    uuid = render_audio_and_score(melody, assets_path)
    return [melody, uuid]


def remove_chords(abc_text):
    # Regular expression to match chords in ABC notation
    chord_pattern = re.compile(r'"[^"]*"|\[[^\]]*\]')
    # Remove all chords from the text
    filtered_text = re.sub(chord_pattern, '', abc_text)
    # Remove any extra spaces introduced by the removal
    #filtered_text = re.sub(r'\s+', ' ', filtered_text).strip()
    return filtered_text

def filter_abc_notes_and_rests_with_headers(abc_text):
    # Split the text into lines
    lines = abc_text.split('\n')
    
    # Separate headers and music lines
    header_lines = []
    music_lines = []
    header_detected = False
    
    for line in lines:
        if re.match(r'^[A-Z]:', line):
            header_detected = True
            header_lines.append(line)
        elif header_detected and not re.match(r'^[A-Z]:', line):
            music_lines.append(line)
    
    # Regular expression to match ABC notes and rests
    note_pattern = re.compile(r'[\^_=]?[A-Ga-gz](?:\d+|\/\d+|\/)?')
    note_pattern = re.compile(r'[\^_=]?[A-Ga-gz](?:\d+|\/\d+|\/)?|[\^_=]?[A-Ga-g][,\'\/\d]*|[\^_=]?z[,\'\/\d]*|\(\d?')

    
    # Filter notes and rests from the music lines
    filtered_music_lines = []
    for line in music_lines:
        notes_and_rests = note_pattern.findall(line)
        filtered_line = ' '.join(notes_and_rests)
        filtered_music_lines.append(filtered_line)
    
    # Combine header lines and filtered music lines
    filtered_text = '\n'.join(header_lines + filtered_music_lines)
    
    return filtered_text


def filter_abc_notes_and_rests(abc_text):
    # Regular expression to match ABC notes and rests
    # Notes: A-G, a-g, and their corresponding accidentals (^, _, =)
    # Rests: z (rest), x (space)
    # Optionally followed by digits or slashes for length
    note_pattern = re.compile(r'[\^_=]?[A-Ga-gz](?:\d+|\/\d+|\/)?')
    
    # Find all matches in the text
    notes_and_rests = note_pattern.findall(abc_text)
    
    # Join the matches into a single string
    filtered_text = ' '.join(notes_and_rests)
    
    return filtered_text


def score_to_notes_and_rests(score):
    notes_and_rests = [elem for elem in score if isinstance(elem, (note.Note, note.Rest))]
    return notes_and_rests


def convert_notes_and_rests_to_events(notes_and_rests):
    notes_and_durations = []

    for elem in notes_and_rests:
        duration = round(float(elem.duration.quarterLength), 3)

        if isinstance(elem, note.Note):
            notes_and_durations.append((elem.pitch.nameWithOctave, duration))
        elif isinstance(elem, note.Rest):
            notes_and_durations.append(("R", duration))

    return notes_and_durations



def convert_melody_to_abc(iter_num, notes_and_durations):
    abc_header = (
        f"X:{iter_num + 1}\n"  # Index for each generation
        f"M:4/4\n"  # Time signature
        f"L:1/4\n"  # Note length
        f"K:C\n"  # Key signature
    )    

    abc_notes = []
    for note, duration in notes_and_durations:
        if note == "R":
            abc_notes.append(f"z{duration}")
        else:
            note_without_octave = note[:-1]
            letter = note[0] 
            accidental = note_without_octave[1] if len(note_without_octave) > 1 else ""
            accidental = accidental.replace("#", "^")
            abc_note = f"{accidental}{letter}{duration}"
            abc_notes.append(abc_note)

    abc_score = abc_header + " ".join(abc_notes)
    return abc_score

