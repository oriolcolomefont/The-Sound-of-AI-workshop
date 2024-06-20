from music21 import converter, note

def flag_score(score):
    flag_array = []  # Initialize an empty list to store boolean values
    
    for part in score.parts:
        for measure in part.getElementsByClass('Measure'):
            for note_or_rest in measure.notesAndRests:
                if isinstance(note_or_rest, note.Note):
                    if note_or_rest.beat % 1.0 == 0 or note_or_rest.tie is not None:
                        flag_array.append(True)  # Flag as True if note meets condition
                    else:
                        flag_array.append(False)  # Flag as False if note does not meet condition
                elif isinstance(note_or_rest, note.Rest):
                    flag_array.append(True)  # Flag rests as True (they are kept)
    
    return flag_array


file_path = 'Africa.mxl'
    
# Load the MusicXML file into a Score object
score = converter.parse(file_path)

# Apply filtering or manipulation rules
flag_array = flag_score(score)

print(flag_array)