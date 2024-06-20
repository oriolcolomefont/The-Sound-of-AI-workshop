import re

from markov import MarkovChain
from music21 import converter, metadata, note, stream
from render import render_audio_and_score


def variate_action(melody, assets_path):
    melody = variate_abc_melody(melody)
    uuid = render_audio_and_score(melody, assets_path)
    return [melody, uuid]

def variate_abc_melody(original_melody):
    score = converter.parse(original_melody, type='abc')
    notes_and_rests = score_to_notes_and_rests(score.flatten())
    events = convert_notes_and_rests_to_events(notes_and_rests)
    unique_events = list(set(events))
    markov = MarkovChain(unique_events, 0.1)

    markov.train(events)
    markov.normalize_matrix()
    number_of_events = len(events)
    markov_melody = markov.generate_melody(unique_events, number_of_events)
    markov_abc_melody = convert_events_to_abc_melody(markov_melody)
    header = extract_abc_header(original_melody)
    return header + "\n" + " ".join(markov_abc_melody)

def convert_events_to_abc_melody(events):
    abc_notes = []
    VALID_DURATIONS_TO_ABC = {
        4.0: "4",
        2.0: "2",
        1.0: "",
        0.5: "/2",
        0.25: "/4",
        0.125: "/8",
        0.0625: "/16",
        0.03125: "/32",
    }
    for note, abs_duration in events:
        if abs_duration in VALID_DURATIONS_TO_ABC:
            duration = VALID_DURATIONS_TO_ABC[abs_duration]
        else:
            duration = ""

        if note == "R":
            abc_notes.append(f"z{duration}")
        else:
            note_without_octave = note[:-1]
            letter = note[0] 
            accidental = note_without_octave[1] if len(note_without_octave) > 1 else ""
            accidental = accidental.replace("#", "^")
            abc_note = f"{accidental}{letter}{duration}"
            abc_notes.append(abc_note)
    return abc_notes

def extract_abc_header(abc_text):
    header_lines = []
    lines = abc_text.split('\n')
    
    for line in lines:
        # Check if the line matches the pattern of an ABC header line
        if re.match(r'^\s*$', line):
            continue
        if re.match(r'^[A-Z]:', line):
            header_lines.append(line)
        else:
            # Stop collecting headers as soon as the first non-header line is found
            break
    
    # Join the header lines into a single string
    header_text = '\n'.join(header_lines)
    
    return header_text

def score_to_notes_and_rests(score):
    notes_and_rests = [elem for elem in score if isinstance(elem, (note.Note, note.Rest))]
    return notes_and_rests

def convert_notes_and_rests_to_events(notes_and_rests):
    notes_and_durations = []

    for elem in notes_and_rests:
        duration = float(elem.duration.quarterLength)

        # Adding note or rest to the list with its adjusted duration
        if isinstance(elem, note.Note):
            notes_and_durations.append((elem.pitch.nameWithOctave, duration))
        elif isinstance(elem, note.Rest):
            notes_and_durations.append(("R", duration))

    return notes_and_durations