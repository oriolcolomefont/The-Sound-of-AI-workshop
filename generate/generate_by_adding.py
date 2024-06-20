from music21 import converter, note, stream
import random

# Step 1: Parse the XML score
xml_file = 'modifiedmarkov.mxl'
score = converter.parse(xml_file)

# Step 2: Iterate through measures
for part in score.parts:
    for measure in part.getElementsByClass(stream.Measure):
        
        # Step 3: Identify all rests in the measure
        rests = [element for element in measure.notesAndRests if isinstance(element, note.Rest)]
        
        if rests:
            # Step 4: Select a random rest
            random_rest = random.choice(rests)
            
            # Step 5: Get the duration of the random rest
            rest_duration = random_rest.quarterLength
            
            # Step 6: Create a random note with the same duration and a random pitch
            random_pitch_name = random.choice(['C', 'D', 'E', 'F', 'G', 'A', 'B', 'B-', 'E-', 'A-', 'D-', 'G-', 'C-', 'F-', 'F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#'])
            random_octave = random.randint(4, 5)  # Octave range as needed
            random_pitch = note.Note(random_pitch_name + str(random_octave))
            random_pitch.quarterLength = rest_duration
            
            # Step 7: Replace the rest with the random note
            measure.replace(random_rest, random_pitch)

# Step 8: Output the modified score (optional)
output_file = 'path_to_output_xml_score.xml'
score.write('xml', fp=output_file)
score.show()
