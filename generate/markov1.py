import sys

import numpy as np
from music21 import converter, metadata, note, stream

GENERATIONS = 10
VALID_DURATIONS = [4.0, 2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]



class MarkovChainMelodyGenerator:
    """
    Represents a Markov Chain model for melody generation.
    """

    def __init__(self, states):
        """
        Initialize the MarkovChain with a list of states.

        Parameters:
            states (list of tuples): A list of possible (pitch, duration)
                pairs.
        """
        self.states = states
        self.initial_probabilities = np.zeros(len(states))
        self.transition_matrix = np.zeros((len(states), len(states)))
        self._state_indexes = {state: i for (i, state) in enumerate(states)}
        print(self.states)

    def train(self, notes_and_durations):
        """
        Train the model based on a list of notes.

        Parameters:
            notes (list): A list of music21.note.Note objects.
        """
        self._calculate_initial_probabilities(notes_and_durations)
        self._calculate_transition_matrix(notes_and_durations)

    def generate(self, length):
        """
        Generate a melody of a given length.

        Parameters:
            length (int): The length of the sequence to generate.

        Returns:
            melody (list of tuples): A list of generated states.
        """
        melody = [self._generate_starting_state()]
        for _ in range(1, length):
            melody.append(self._generate_next_state(melody[-1]))
        return melody

    def _calculate_initial_probabilities(self, notes_and_durations):
        """
        Calculate the initial probabilities from the provided notes.

        Parameters:
            notes (list): A list of music21.note.Note objects.
        """
        for note_and_duration in notes_and_durations:
            self._increment_initial_probability_count(note_and_duration)
        self._normalize_initial_probabilities()

    def _increment_initial_probability_count(self, note_and_duration):
        """
        Increment the probability count for a given note.

        Parameters:
            note (music21.note.Note): A note object.
        """
        state = note_and_duration
        self.initial_probabilities[self._state_indexes[state]] += 1

    def _normalize_initial_probabilities(self):
        """
        Normalize the initial probabilities array such that the sum of all
        probabilities equals 1.
        """
        total = np.sum(self.initial_probabilities)
        if total:
            self.initial_probabilities /= total
        self.initial_probabilities = np.nan_to_num(self.initial_probabilities)

    def _calculate_transition_matrix(self, notes_and_durations):
        """
        Calculate the transition matrix from the provided notes.

        Parameters:
            notes (list): A list of music21.note.Note objects.
        """
        for i in range(len(notes_and_durations) - 1):
            self._increment_transition_count(notes_and_durations[i], notes_and_durations[i + 1])
        self._normalize_transition_matrix()

    def _increment_transition_count(self, current_note_and_duration, next_note_and_duration):
        """
        Increment the transition count from current_note to next_note.

        Parameters:
            current_note (music21.note.Note): The current note object.
            next_note (music21.note.Note): The next note object.
        """
        state = current_note_and_duration
        next_state = next_note_and_duration
        self.transition_matrix[
            self._state_indexes[state], self._state_indexes[next_state]
        ] += 1

    def _normalize_transition_matrix(self):
        """
        This method normalizes each row of the transition matrix so that the
        sum of probabilities in each row equals 1. This is essential for the rows
        of the matrix to represent probability distributions of
        transitioning from one state to the next.
        """

        # Calculate the sum of each row in the transition matrix.
        # These sums represent the total count of transitions from each state
        # to any other state.
        row_sums = self.transition_matrix.sum(axis=1)

        # Use np.errstate to ignore any warnings that arise during division.
        # This is necessary because we might encounter rows with a sum of 0,
        # which would lead to division by zero.
        with np.errstate(divide="ignore", invalid="ignore"):
            # Normalize each row by its sum. np.where is used here to handle
            # rows where the sum is zero.
            # If the sum is zero (no transitions from that state), np.where
            # ensures that the row remains a row of zeros instead of turning
            # into NaNs due to division by zero.
            self.transition_matrix = np.where(
                row_sums[:, None],  # Condition: Check each row's sum.
                # True case: Normalize if sum is not zero.
                self.transition_matrix / row_sums[:, None],
                0,  # False case: Keep as zero if sum is zero.
            )

    def _generate_starting_state(self):
        """
        Generate a starting state based on the initial probabilities.

        Returns:
            A state from the list of states.
        """
        initial_index = np.random.choice(
            list(self._state_indexes.values()), p=self.initial_probabilities
        )
        return self.states[initial_index]

    def _generate_next_state(self, current_state):
        """
        Generate the next state based on the transition matrix and the current
        state.

        Parameters:
            current_state: The current state in the Markov Chain.

        Returns:
            The next state in the Markov Chain.
        """
        if self._does_state_have_subsequent(current_state):
            index = np.random.choice(
                list(self._state_indexes.values()),
                p=self.transition_matrix[self._state_indexes[current_state]],
            )
            return self.states[index]
        return self._generate_starting_state()

    def _does_state_have_subsequent(self, state):
        """
        Check if a given state has a subsequent state in the transition matrix.

        Parameters:
            state: The state to check.

        Returns:
            True if the state has a subsequent state, False otherwise.
        """
        return self.transition_matrix[self._state_indexes[state]].sum() > 0



def visualize_melody(melody):
    """
    Visualize a sequence of (pitch, duration) pairs using music21.

    Parameters:
        - melody (list): A list of (pitch, duration) pairs.
    """
    print(melody)
    score = stream.Score()
    score.metadata = metadata.Metadata(title="Markov Chain Melody")
    part = stream.Part()
    for n, d in melody:
        part.append(note.Note(n, quarterLength=d))
    score.append(part)
    score.show()

def convert_stream_to_notes_and_durations(score):
    notes_and_durations = []

    for elem in score:
        duration = float(elem.duration.quarterLength)
        if duration not in VALID_DURATIONS:
            duration = min(VALID_DURATIONS, key=lambda x: abs(x - duration))

        if isinstance(elem, note.Note):
            notes_and_durations.append((elem.pitch.nameWithOctave, duration))
        elif isinstance(elem, note.Rest):
            notes_and_durations.append(("R", duration))

    return notes_and_durations





def convert_to_abc(iter, notes_and_durations):
    abc_header = (
        f"X:{iter + 1}\n"  # Index for each generation
        f"T:Markov-{iter + 1}\n"  # Title
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

def main(file_name):
    """Main function for training the chain, generating a melody, and
    visualizing the result."""

    # read a file
    score = converter.parse(file_name).flatten()

    notes_and_rests = [elem for elem in score if isinstance(elem, (note.Note, note.Rest))]


    # Convert notes and rest into a list of tuples (pitch, duration) with rest represeted with an R
    notes_rest_and_durations = convert_stream_to_notes_and_durations(notes_and_rests)

    # We need to find unique occurrences inside notes_rest_and_durations
    unique_notes_and_durations = list(set(notes_rest_and_durations))

    # Sort by the first element of the tuple
    unique_notes_and_durations.sort(key=lambda x: x[0])

 
    model = MarkovChainMelodyGenerator(unique_notes_and_durations)
    model.train(notes_rest_and_durations)

    generated_melody = model.generate(40)

    for i in range(GENERATIONS):
        iter = i + 1
        abc_melody = convert_to_abc(iter, generated_melody)
        with open(f"output/markov-{iter}.abc", "w") as file:
            file.write(abc_melody)


if __name__ == "__main__":
    #file_name = sys.argv[1]
    file_name = "markov.mxl"
    main(file_name)