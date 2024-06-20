import random
from music21 import converter, stream, note

def substitute_note_with_rest(score_path, output_path=None):
    # Load the score from XML file
    score = converter.parse(score_path)

    # Iterate through each measure in the score
    for part in score.parts:  # Assuming parts are used
        for measure in part.getElementsByClass(stream.Measure):
            # Get all notes and chords in the measure
            notes = list(measure.notesAndRests)
            
            if len(notes) > 0:
                # Select a random note or rest
                random_note_index = random.randint(0, len(notes) - 1)
                random_note = notes[random_note_index]
                
                if isinstance(random_note, note.Note):
                    # Substitute the random note with a rest of the same duration
                    rest_duration = random_note.quarterLength
                    measure.remove(random_note)
                    measure.insert(random_note_index, note.Rest(quarterLength=rest_duration))
                elif isinstance(random_note, note.Rest):
                    # Already a rest, do nothing or handle as needed
                    pass

    # Optionally save the modified score to a new XML file or print it
    if output_path:
        score.write('xml', fp=output_path)
        score.show()

# Example usage
input_xml = 'modifiedmarkov.mxl'
output_xml = f'modified_{input_xml}.xml'
substitute_note_with_rest(input_xml, output_xml)
