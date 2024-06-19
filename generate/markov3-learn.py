import random

import numpy as np
from music21 import converter, metadata, note, stream

GENERATIONS = 100
MELODY_LENGTH = 100
VALID_DURATIONS = [4.0, 2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]

def convert_notes_and_rests_to_events(notes_and_rests):
    """
    Converts a list of music notes and rests into a list of tuples representing
    events with their durations.

    Args:
    - notes_and_rests (list): A list of music21 note and rest objects.

    Returns:
    - list: A list of tuples, where each tuple contains:
        - For notes: (note name with octave, duration)
        - For rests: ("R", duration)
    """
    notes_and_durations = []

    for elem in notes_and_rests:
        duration = float(elem.duration.quarterLength)
        
        # Matching duration to closest valid duration from VALID_DURATIONS
        if duration not in VALID_DURATIONS:
            duration = min(VALID_DURATIONS, key=lambda x: abs(x - duration))

        # Adding note or rest to the list with its adjusted duration
        if isinstance(elem, note.Note):
            notes_and_durations.append((elem.pitch.nameWithOctave, duration))
        elif isinstance(elem, note.Rest):
            notes_and_durations.append(("R", duration))

    return notes_and_durations


def score_to_notes_and_rests(score):
    """
    Extracts notes and rests from a music21 Score object and returns them as a list.

    Args:
    - score (music21.stream.Score): A music21 Score object containing musical elements.

    Returns:
    - list: A list of music21 note and rest objects extracted from the Score.
    """
    notes_and_rests = [elem for elem in score if isinstance(elem, (note.Note, note.Rest))]
    return notes_and_rests


def convert_melody_to_abc(iter_num, notes_and_durations):
    """
    Converts a list of notes and their durations into an ABC notation string.

    Args:
    - iter_num (int): Index for each generation, used in the ABC notation header.
    - notes_and_durations (list): A list of tuples, where each tuple contains:
        - For notes: (note name with octave, duration)
        - For rests: ("R", duration)

    Returns:
    - str: A string representing the melody in ABC notation format.
    """
    abc_header = (
        f"X:{iter_num + 1}\n"  # Index for each generation
        f"T:Markov-{iter_num + 1}\n"  # Title
        f"M:4/4\n"  # Time signature
        f"L:1/4\n"  # Note length
        f"K:C\n"  # Key signature
    )    

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

    abc_notes = []
    for note, abs_duration in notes_and_durations:
        duration = VALID_DURATIONS_TO_ABC[abs_duration]
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


class MarkovChain:
    def __init__(self, unique_events, initial_probability):
        number_of_events = len(unique_events)
        self.unique_events = unique_events
        self.matrix = np.full((number_of_events, number_of_events), initial_probability)
        self.event_to_index = {event: i for (i, event) in enumerate(unique_events)} 
        
    def normalize_matrix(self):
        row_sums = self.matrix.sum(axis=1)
        normalized_matrix = np.where(
            row_sums[:, None],  # Condition: Check each row's sum.
            # True case: Normalize if sum is not zero.
            self.matrix / row_sums[:, None],
            0,  # False case: Keep as zero if sum is zero.
        ) 
        self.matrix = normalized_matrix

    def generate_melody(self, events, number_of_events):
        first_element = random.choice(events)
        available_indexes = list(self.event_to_index.values())
        melody = [first_element]
        for _ in range(1, number_of_events):
            last_event = melody[-1]
            last_event_index = self.event_to_index[last_event]
            current_row = self.matrix[last_event_index]
            next_index = np.random.choice(
                available_indexes,
                p=current_row,
            )
            next_element = events[next_index]

            melody.append(next_element)

        return melody

    def train(self, events):
        for i in range(0, len(events) - 1):
            current_event = events[i]
            next_event = events[i + 1]
            current_index = self.event_to_index[current_event]
            next_index = self.event_to_index[next_event]
            self.matrix[current_index, next_index] += 1



def main(input_file):
    score = converter.parse(input_file)
    notes_and_rests = score_to_notes_and_rests(score.flatten())
    events = convert_notes_and_rests_to_events(notes_and_rests)
    unique_events = list(set(events))
    markov = MarkovChain(unique_events, 0.0)

    markov.train(events)
    markov.normalize_matrix()

    number_of_events = MELODY_LENGTH

    for i in range(GENERATIONS):
        iter_num = i + 1
        melody = markov.generate_melody(unique_events, number_of_events)
        abc = convert_melody_to_abc(iter_num, melody)
        with open(f"output/markov-learn-{iter_num}.abc", "w") as file:
            file.write(abc)

if __name__ == "__main__":
    file_name = "markov.mxl"
    main(file_name)