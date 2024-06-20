import random

import numpy as np


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

    def generate_melody(self, number_of_events):
        first_element = random.choice(self.unique_events)
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
            next_element = self.unique_events[next_index]

            melody.append(next_element)

        return melody

    def generate_single_note(self, last_event):
        last_event_index = self.event_to_index[last_event]
        current_row = self.matrix[last_event_index]
        next_index = np.random.choice(
            list(self.event_to_index.values()),
            p=current_row,
        )
        return self.unique_events[next_index]
    

    def train(self, events):
        for i in range(0, len(events) - 1):
            current_event = events[i]
            next_event = events[i + 1]
            current_index = self.event_to_index[current_event]
            next_index = self.event_to_index[next_event]
            self.matrix[current_index, next_index] += 1

