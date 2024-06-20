from music21 import converter, stream, note, chord
from melodic_scheleton_flag import flag_score

# Paths to the anchor and query scores
anchor_path = '../wikifonia-dataset/original-abc/32Kombine.abc'
query_path = '../wikifonia-dataset/original-abc/A.abc'

# Parse the scores
anchor_score = converter.parse(anchor_path)
query_score = converter.parse(query_path)

# Generate the boolean array
boolean_array_from_anchor = flag_score(anchor_score)

# Flatten the anchor score to get all notes in a flat structure
anchor_notes = anchor_score.flatten().notesAndRests

# Ensure the boolean_array matches the length of anchor_notes
if len(boolean_array_from_anchor) != len(anchor_notes):
    raise ValueError(f"Boolean array length ({len(boolean_array_from_anchor)}) does not match the number of notes in the anchor score ({len(anchor_notes)}).")

# Ensure the query_score has enough notes to replace in the anchor_score
query_notes = query_score.flatten().notesAndRests
query_note_index = 0

# Create a new stream for the modified anchor score
modified_anchor = stream.Score()

# Iterate over the notes in the anchor score
for idx, item in enumerate(anchor_notes):
    if boolean_array[idx]:
        # If the flag is True, keep the original note
        modified_anchor.append(item)
    else:
        # If the flag is False, replace the note with one from the query score
        if query_note_index < len(query_notes):
            modified_anchor.append(query_notes[query_note_index])
            query_note_index += 1
        else:
            # If the query score runs out of notes, raise an error or handle it as needed
            raise ValueError("Not enough notes in the query score to replace all required notes in the anchor score.")

# Save or show the modified anchor score
modified_anchor.show()
